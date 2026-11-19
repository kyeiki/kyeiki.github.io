#!/usr/bin/env python3
## -*- coding: utf-8 -*-
"""
================================================================================
MODUL KOMPUTER GRAFIK (V2) - ASCII FLOOR PLAN TO 3D BLENDER 4.3 GENERATOR
File: ascii_to_blender_3d.py

Arsitektur SOLID:
  1. AsciiDenahParser : Mengubah teks denah ASCII (+, -, |, dan label ruang)
                        menjadi dictionary/JSON berformat config_denah.json.
                        Mendukung denah Gedung Kantor maupun Rumah Tinggal (ETS).
  2. SceneManager     : Lifecycle scene, koleksi, join, dan origin ke tengah alas
                        secara world-accurate (matrix_world + view_layer.update).
  3. MaterialFactory  : Pembuatan material Principled BSDF (kompatibel Blender 4.3).
  4. AssetBuilder     : Registry pembangun primitif 3D (OCP + fail-fast ValueError).
                        Berisi 21 tipe aset primitif (kantor & rumah tinggal).
  5. DenahBuilder     : Menerjemahkan config_denah.json menjadi dinding 3D
                        (_potong_dengan_celah), kusen otomatis (_pasang_kusen),
                        zona lantai berwarna, furnitur primitif, dan teks 3D.

Cara Pakai di Blender 4.3 (GUI):
  1. Buka Blender 4.3 -> Pindah ke tab "Scripting" -> Klik "New" atau "Open".
  2. Pilih/tempel file ascii_to_blender_3d.py ini, lalu tekan Run Script (Alt + P).
  3. Denah 3D langsung terbangun di koleksi "RumahIndoor", sekaligus membuat
     blok teks internal "denah_ascii.txt", "config_denah.json", dan
     "config_assets.json" di dalam file .blend.
================================================================================
"""

import json
import math
import os
import re
from collections import deque

## ==============================================================================
## BAGIAN 1: KONFIGURASI DENAH ASCII & PARAMETER SKALA
## Mahasiswa cukup mengganti isi string DENAH_ASCII di bawah ini dengan denah
## ETS 2D miliknya sendiri (menggunakan karakter '+', '-', '|', dan nama ruang).
## ==============================================================================
SKALA_X_METER_PER_KARAKTER = 0.5   # 1 kolom karakter ASCII = 0.5 meter (sumbu X)
SKALA_Y_METER_PER_KARAKTER = 0.5   # 1 baris karakter ASCII = 0.5 meter (sumbu Y)
TINGGI_DINDING_DEFAULT     = 3.0   # Tinggi dinding lantai 1 dalam meter (sumbu Z)
TEBAL_DINDING_DEFAULT      = 0.15  # Ketebalan dinding dalam meter

DENAH_ASCII = r"""
+---+---------------------------------------------------------+---+
|   | [R] | [R] | [R] |     |     |     | [R] | [R] | [R] | [R] |   |
|   +-----+-----+-----+     |     |     +-----+-----+-----+-----+   |
|   |                 |                                   |     |   |
| R |                                                           | R |
| . |                    WORK STATION (UTARA)                   | . |
| A |                                                           | A |
| R |                                                           | R |
| S |                                                           | S |
| I |                                                           | I |
| P |                                                           | P |
+---+-------+-------------------+-----+-------------------+-----+---+
|   |       |    TOILET PRIA    |     |  LIFT  |  PANTRY  |     |   |
|   |       +-------------------+     +--------+----------+     |   |
|   |       | R.AHU | [LIFT-1]  |  C  |  LIFT  |  TANGGA  |     |   |
|   |       |       | [LIFT-2]  |  O  +--------+ DARURAT  |     |   |
|   |       +-------+-----------+  R  | [LIFT] |          |     |   |
|   |       |                   |  I  +--------+----------+     |   |
|   |       |   TOILET WANITA   |  D  |    TANGGA DARURAT |     |   |
|   |       |                   |  O  +-------------------+     |   |
|   |       |                   |  R  |      R. PANEL     |     |   |
+---+-------+-------------------+-----+-------------------+-----+---+
|   |                                                           |   |
| R |                                                           | R |
| . |                    WORK STATION (SELATAN)                 | . |
| A |                                                           | A |
| R |                                                           | R |
| S |                                                           | S |
| I |                                                           | I |
| P |                 |                                   |     | P |
|   +---+---+---+-----+---+---+---+---+---+---+---+---+---+-----+   |
|   | R | R | R |  R  | R | R | R | R | R | R | R | R | R |  R  |   |
+---+---+---+---+-----+---+---+---+---+---+---+---+---+---+-----+---+
"""

## Contoh alternatif Denah Rumah Tinggal ETS (bisa di-copy ke DENAH_ASCII):
CONTOH_DENAH_RUMAH_ETS = r"""
+---------------+---------------+---------------+
|               |               |               |
|  KAMAR TIDUR  |  KAMAR MANDI  |     DAPUR     |
|       1       |               |               |
+---------------+---------------+---------------+
|                               |               |
|          RUANG TAMU           |  KAMAR TIDUR  |
|                               |       2       |
|                               +---------------+
|                               |     TERAS     |
+-------------------------------+---------------+
"""

## ==============================================================================
## BAGIAN 2: PALET MATERIAL (config_assets.json)
## Format RGBA: [Red, Green, Blue, Alpha] bernilai 0.0 s.d. 1.0
## ==============================================================================
DEFAULT_CONFIG_ASSETS = {
    "palet": {
        "dinding_eksterior": {"rgba": [0.92, 0.91, 0.88, 1.0], "roughness": 0.85},
        "dinding_interior":  {"rgba": [0.85, 0.86, 0.88, 1.0], "roughness": 0.80},
        "dinding_core":      {"rgba": [0.76, 0.79, 0.83, 1.0], "roughness": 0.75},
        "kusen_kayu":        {"rgba": [0.35, 0.22, 0.12, 1.0], "roughness": 0.65},
        "kusen_aluminium":   {"rgba": [0.22, 0.25, 0.28, 1.0], "roughness": 0.35},
        "kaca_jendela":      {"rgba": [0.65, 0.85, 0.95, 1.0], "roughness": 0.15, "emission": [0.4, 0.6, 0.7, 1.0], "emission_strength": 0.15},
        "lantai_workstation":{"rgba": [0.82, 0.80, 0.76, 1.0], "roughness": 0.70},
        "lantai_koridor":    {"rgba": [0.72, 0.74, 0.77, 1.0], "roughness": 0.50},
        "lantai_ruang_r":    {"rgba": [0.66, 0.52, 0.38, 1.0], "roughness": 0.60},
        "lantai_arsip":      {"rgba": [0.58, 0.60, 0.62, 1.0], "roughness": 0.85},
        "lantai_toilet":     {"rgba": [0.75, 0.88, 0.90, 1.0], "roughness": 0.35},
        "lantai_pantry":     {"rgba": [0.88, 0.82, 0.72, 1.0], "roughness": 0.45},
        "lantai_teknis":     {"rgba": [0.42, 0.45, 0.48, 1.0], "roughness": 0.90},
        "lantai_tangga":     {"rgba": [0.52, 0.50, 0.48, 1.0], "roughness": 0.85},
        "lantai_lift":       {"rgba": [0.30, 0.32, 0.35, 1.0], "roughness": 0.40},
        "kayu_meja":         {"rgba": [0.72, 0.53, 0.34, 1.0], "roughness": 0.55},
        "kayu_gelap":        {"rgba": [0.28, 0.18, 0.10, 1.0], "roughness": 0.65},
        "partisi_kubikel":   {"rgba": [0.46, 0.56, 0.68, 1.0], "roughness": 0.80},
        "kursi_kantor":      {"rgba": [0.18, 0.20, 0.24, 1.0], "roughness": 0.70},
        "kain_sofa":         {"rgba": [0.26, 0.42, 0.58, 1.0], "roughness": 0.85},
        "kain_kasur":        {"rgba": [0.92, 0.90, 0.86, 1.0], "roughness": 0.80},
        "selimut_biru":      {"rgba": [0.30, 0.50, 0.72, 1.0], "roughness": 0.85},
        "logam_abu":         {"rgba": [0.60, 0.63, 0.66, 1.0], "roughness": 0.35},
        "logam_lift":        {"rgba": [0.78, 0.80, 0.83, 1.0], "roughness": 0.25},
        "keramik_putih":     {"rgba": [0.96, 0.97, 0.98, 1.0], "roughness": 0.20},
        "layar_monitor":     {"rgba": [0.08, 0.12, 0.18, 1.0], "roughness": 0.20, "emission": [0.15, 0.45, 0.85, 1.0], "emission_strength": 0.6},
        "hijau_daun":        {"rgba": [0.22, 0.55, 0.26, 1.0], "roughness": 0.75},
        "pot_terakota":      {"rgba": [0.68, 0.36, 0.22, 1.0], "roughness": 0.80},
        "panel_listrik":     {"rgba": [0.25, 0.32, 0.38, 1.0], "roughness": 0.50},
        "lampu_indikator":   {"rgba": [0.10, 0.90, 0.30, 1.0], "roughness": 0.20, "emission": [0.10, 0.95, 0.30, 1.0], "emission_strength": 2.5},
        "mesin_hvac":        {"rgba": [0.35, 0.52, 0.65, 1.0], "roughness": 0.45},
        "kardus_arsip":      {"rgba": [0.78, 0.64, 0.44, 1.0], "roughness": 0.85},
        "rail_tangga":       {"rgba": [0.85, 0.22, 0.18, 1.0], "roughness": 0.40},
        "teks_label":        {"rgba": [0.12, 0.14, 0.18, 1.0], "roughness": 0.50}
    }
}

## ==============================================================================
## BAGIAN 3: KELAS AsciiDenahParser (SRP: Teks ASCII -> Dict config_denah.json)
## ==============================================================================
class AsciiDenahParser:
    """
    Single Responsibility: Menerjemahkan teks denah ASCII (karakter '+', '-', '|',
    dan nama ruangan di dalamnya) menjadi dictionary yang mematuhi kontrak
    config_denah.json:
      - rumah.grid           : [lebar_x, tinggi_y] dalam satuan meter
      - rumah.segmen_dinding : daftar segmen {nama, dari, ke, material, celah[]}
      - rumah.zona_lantai    : daftar area lantai per ruangan {nama, min_xy, max_xy, material}
      - rumah.furnitur       : daftar furnitur primitif otomatis sesuai label ruangan
      - rumah.label_ruang    : daftar label teks 3D nama ruangan
    """

    def __init__(self, scale_x=0.5, scale_y=0.5, tinggi_dinding=3.0, tebal_dinding=0.15):
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.tinggi_dinding = float(tinggi_dinding)
        self.tebal_dinding = float(tebal_dinding)

    @staticmethod
    def _normalisasi_baris(ascii_text):
        """Merapikan panjang baris ASCII agar membentuk matriks 2D persegi panjang."""
        raw_lines = [
            l.rstrip("\r\n")
            for l in ascii_text.strip().splitlines()
            if l.strip()
        ]
        if not raw_lines:
            raise ValueError("Teks ASCII kosong! Pastikan DENAH_ASCII berisi gambar denah.")
        max_len = max(len(l) for l in raw_lines)
        grid = []
        for l in raw_lines:
## Jika ada baris border '+---+' yang kurang karakter '-' (mis. baris paling atas),
## rentangkan segmen '---' terpanjang secara otomatis agar kolom '+' sejajar.
            if len(l) < max_len and "---" in l:
                diff = max_len - len(l)
                runs = [
                    (m.end() - m.start(), m.start(), m.end())
                    for m in re.finditer(r"-+", l)
                ]
                runs.sort(reverse=True)
                _, start_idx, _ = runs[0]
                l = l[:start_idx] + ("-" * diff) + l[start_idx:]
            grid.append(l.ljust(max_len))
        return grid

    @staticmethod
    def _is_horizontal_wall_char(grid, r, c):
        """Mengecek apakah karakter pada (r, c) merupakan bagian dari dinding horizontal."""
        W = len(grid[0])
        ch = grid[r][c]
        if ch == "+":
            return True
        if ch == "-":
## Membedakan '-' garis dinding vs tanda hubung teks seperti "[LIFT-1]"
            left = grid[r][c - 1] if c > 0 else " "
            right = grid[r][c + 1] if c + 1 < W else " "
            return (left in ("+", "-")) or (right in ("+", "-"))
        return False

    @staticmethod
    def _is_vertical_wall_char(grid, r, c):
        """Mengecek apakah karakter pada (r, c) merupakan bagian dari dinding vertikal."""
        return grid[r][c] in ("+", "|")

    def _is_any_wall(self, grid, r, c):
        ch = grid[r][c]
        if ch in ("+", "|"):
            return True
        if ch == "-":
            return self._is_horizontal_wall_char(grid, r, c)
        return False

    def _rc_to_xy(self, r, c, max_r):
        """
        Konversi indeks (baris, kolom) ASCII ke koordinat dunia Blender (x, y) meter.
        Penting: Di teks ASCII baris 0 berada di ATAS (Utara), sedangkan di Blender
        tampak atas (Numpad 7) sumbu +Y mengarah ke ATAS (Utara).
        Maka y = (max_r - r) * scale_y agar tampilan Numpad 7 sama persis dengan ASCII.
        """
        x = round(c * self.scale_x, 3)
        y = round((max_r - r) * self.scale_y, 3)
        return x, y

    def _ekstrak_ruangan(self, grid):
        """Algoritma Flood-Fill (BFS) untuk mengenali batas ruangan & membaca teks di dalamnya."""
        H = len(grid)
        W = len(grid[0])
        max_r = H - 1
        visited = [[False] * W for _ in range(H)]
        rooms = []

        for r in range(H):
            for c in range(W):
                if not visited[r][c] and not self._is_any_wall(grid, r, c):
                    q = deque([(r, c)])
                    visited[r][c] = True
                    cells = []
                    while q:
                        cr, cc = q.popleft()
                        cells.append((cr, cc))
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = cr + dr, cc + dc
                            if (
                                0 <= nr < H
                                and 0 <= nc < W
                                and not visited[nr][nc]
                                and not self._is_any_wall(grid, nr, nc)
                            ):
                                visited[nr][nc] = True
                                q.append((nr, nc))

                    min_r = min(p[0] for p in cells)
                    max_r_cell = max(p[0] for p in cells)
                    min_c = min(p[1] for p in cells)
                    max_c_cell = max(p[1] for p in cells)

## Indeks garis dinding pengapit ruangan
                    r1 = max(0, min_r - 1)
                    r2 = min(max_r, max_r_cell + 1)
                    c1 = max(0, min_c - 1)
                    c2 = min(W - 1, max_c_cell + 1)

                    cell_set = set(cells)
                    row_texts = []
                    for rr in range(min_r, max_r_cell + 1):
                        s = "".join(
                            grid[rr][cc]
                            for cc in range(min_c, max_c_cell + 1)
                            if (rr, cc) in cell_set
                        )
                        s_clean = " ".join(s.split())
                        if s_clean:
                            row_texts.append(s_clean)
                    raw_label = " ".join(row_texts)

## Normalisasi teks vertikal seperti "R . A R S I P" atau "C O R I D O R"
                    norm_label = raw_label
                    if raw_label.replace(" ", "") == "R.ARSIP":
                        norm_label = "R. ARSIP"
                    elif raw_label.replace(" ", "") == "CORIDOR":
                        norm_label = "CORIDOR"

                    x1, y2 = self._rc_to_xy(r1, c1, max_r)
                    x2, y1 = self._rc_to_xy(r2, c2, max_r)

                    rooms.append(
                        {
                            "id": len(rooms),
                            "r1": r1,
                            "r2": r2,
                            "c1": c1,
                            "c2": c2,
                            "x1": min(x1, x2),
                            "x2": max(x1, x2),
                            "y1": min(y1, y2),
                            "y2": max(y1, y2),
                            "area_cells": len(cells),
                            "raw_label": raw_label,
                            "label": norm_label,
                        }
                    )
        return rooms

    def _ekstrak_segmen_dinding(self, grid):
        """Mengekstrak segmen dinding horizontal dan vertikal (termasuk sambungan T-junction)."""
        H = len(grid)
        W = len(grid[0])
        max_r = H - 1
        horiz_segments = []
        vert_segments = []

## 1. Segmen Dinding Horizontal (sepanjang baris r)
        for r in range(H):
            c = 0
            while c < W:
                if self._is_horizontal_wall_char(grid, r, c):
                    start_c = c
                    has_dash = False
                    while c < W and self._is_horizontal_wall_char(grid, r, c):
                        if grid[r][c] == "-":
                            has_dash = True
                        c += 1
                    end_c = c - 1
                    if has_dash and end_c > start_c:
                        x1, y = self._rc_to_xy(r, start_c, max_r)
                        x2, _ = self._rc_to_xy(r, end_c, max_r)
                        is_ext = r in (0, max_r)
                        is_core = 11 <= r <= 21
                        mat = (
                            "dinding_eksterior"
                            if is_ext
                            else ("dinding_core" if is_core else "dinding_interior")
                        )
                        horiz_segments.append(
                            {
                                "nama": f"Dinding_H_R{r:02d}_C{start_c:02d}_{end_c:02d}",
                                "orientasi": "H",
                                "r": r,
                                "c1": start_c,
                                "c2": end_c,
                                "dari": [x1, y],
                                "ke": [x2, y],
                                "material": mat,
                                "celah": [],
                            }
                        )
                else:
                    c += 1

## 2. Segmen Dinding Vertikal (sepanjang kolom c)
        for c in range(W):
            r = 0
            while r < H:
                if self._is_vertical_wall_char(grid, r, c):
                    start_r = r
                    has_pipe = False
                    while r < H and self._is_vertical_wall_char(grid, r, c):
                        if grid[r][c] == "|":
                            has_pipe = True
                        r += 1
                    end_r = r - 1
                    if has_pipe:
## Resolusi T-Junction otomatis: jika ujung '|' bertemu '-' pada baris di atas/bawahnya,
## sambungkan segmen vertikal ke baris dinding horizontal tersebut.
                        if start_r > 0 and self._is_horizontal_wall_char(grid, start_r - 1, c):
                            start_r -= 1
                        if end_r + 1 < H and self._is_horizontal_wall_char(grid, end_r + 1, c):
                            end_r += 1
                        if end_r == start_r:
                            end_r = min(max_r, start_r + 1)

                        x, y2 = self._rc_to_xy(start_r, c, max_r)
                        _, y1 = self._rc_to_xy(end_r, c, max_r)
                        is_ext = c in (0, W - 1)
                        is_core = 12 <= c <= 58 and start_r >= 11 and end_r <= 21
                        mat = (
                            "dinding_eksterior"
                            if is_ext
                            else ("dinding_core" if is_core else "dinding_interior")
                        )
                        vert_segments.append(
                            {
                                "nama": f"Dinding_V_C{c:02d}_R{start_r:02d}_{end_r:02d}",
                                "orientasi": "V",
                                "c": c,
                                "r1": start_r,
                                "r2": end_r,
                                "dari": [x, min(y1, y2)],
                                "ke": [x, max(y1, y2)],
                                "material": mat,
                                "celah": [],
                            }
                        )
                else:
                    r += 1

        return horiz_segments, vert_segments

    @staticmethod
    def _tambah_celah_ke_segmen(seg_list, orientasi, garis_idx, pos_tengah, lebar_celah, tinggi_bukaan=2.1, ambang_bawah=0.0):
        """Menyisipkan spesifikasi celah {dari, ke, tinggi_bukaan, ambang_bawah} ke segmen dinding."""
        half = round(lebar_celah / 2.0, 3)
        c_dari = round(pos_tengah - half, 3)
        c_ke = round(pos_tengah + half, 3)

        for seg in seg_list:
            if orientasi == "H" and seg["r"] == garis_idx:
                s_min = min(seg["dari"][0], seg["ke"][0])
                s_max = max(seg["dari"][0], seg["ke"][0])
            elif orientasi == "V" and seg["c"] == garis_idx:
                s_min = min(seg["dari"][1], seg["ke"][1])
                s_max = max(seg["dari"][1], seg["ke"][1])
            else:
                continue

            if c_dari >= s_min + 0.05 and c_ke <= s_max - 0.05:
                overlap = any(
                    not (c_ke <= ex["dari"] or c_dari >= ex["ke"])
                    for ex in seg["celah"]
                )
                if not overlap:
                    seg["celah"].append(
                        {
                            "dari": c_dari,
                            "ke": c_ke,
                            "tinggi_bukaan": round(tinggi_bukaan, 2),
                            "ambang_bawah": round(ambang_bawah, 2),
                        }
                    )
                return True
        return False

    def _injeksi_pintu_dan_jendela_otomatis(self, rooms, horiz_segments, vert_segments, max_r, max_c):
        """
        Menambahkan bukaan pintu dan jendela secara otomatis berdasarkan posisi & tipe ruangan
        (mendukung baik denah Gedung Kantor maupun denah Rumah Tinggal ETS).
        """
        for rm in rooms:
            lbl = rm["label"].upper()
            r1, r2, c1, c2 = rm["r1"], rm["r2"], rm["c1"], rm["c2"]
            cx = round((rm["x1"] + rm["x2"]) / 2.0, 2)
            cy = round((rm["y1"] + rm["y2"]) / 2.0, 2)
            width_x = rm["x2"] - rm["x1"]
            height_y = rm["y2"] - rm["y1"]
            lebar_pintu = min(0.9, round(min(width_x, height_y) * 0.45, 2))
            lebar_pintu = max(0.7, lebar_pintu)

## A. Aturan Ruangan Gedung Kantor
            if lbl == "[R]" and r1 == 0:
                self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, lebar_pintu, 2.1, 0.0)
                self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, min(1.2, width_x * 0.5), 1.0, 1.0)
            elif lbl == "R" and r2 == max_r:
                self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, lebar_pintu, 2.1, 0.0)
                self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, min(1.0, width_x * 0.5), 1.0, 1.0)
            elif "ARSIP" in lbl:
                wall_c = c2 if c1 == 0 else c1
                self._tambah_celah_ke_segmen(vert_segments, "V", wall_c, cy, 1.0, 2.1, 0.0)
                ext_c = c1 if c1 == 0 else c2
                self._tambah_celah_ke_segmen(vert_segments, "V", ext_c, cy, 1.6, 1.0, 1.1)
            elif "CORIDOR" in lbl or "KORIDOR" in lbl:
                self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, min(2.0, width_x - 0.6), 2.5, 0.0)
                self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, min(2.0, width_x - 0.6), 2.5, 0.0)
            elif "TOILET" in lbl:
                self._tambah_celah_ke_segmen(vert_segments, "V", c2, cy, 0.9, 2.1, 0.0)
            elif "LIFT-1" in lbl or "LIFT-2" in lbl:
                self._tambah_celah_ke_segmen(vert_segments, "V", c2, cy, 1.1, 2.2, 0.0)
            elif lbl in ("LIFT", "[LIFT]"):
                self._tambah_celah_ke_segmen(vert_segments, "V", c1, cy, 0.8, 2.1, 0.0)
            elif "AHU" in lbl:
                self._tambah_celah_ke_segmen(vert_segments, "V", c1, cy, 0.9, 2.1, 0.0)
            elif "PANTRY" in lbl:
                self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, 0.9, 2.1, 0.0)
            elif "TANGGA" in lbl:
                if c1 == 38:
                    self._tambah_celah_ke_segmen(vert_segments, "V", c1, cy, 0.8, 2.1, 0.0)
                else:
                    self._tambah_celah_ke_segmen(vert_segments, "V", c2, cy, 0.9, 2.1, 0.0)
            elif "PANEL" in lbl:
                self._tambah_celah_ke_segmen(vert_segments, "V", c1, cy, 0.8, 2.1, 0.0)
            elif lbl == "" and r1 == 11 and r2 == 21:
                if width_x >= 2.5:
                    self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, 1.4, 2.3, 0.0)
                    self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, 1.4, 2.3, 0.0)
                else:
                    inner_c = c2 if c1 == 0 else c1
                    self._tambah_celah_ke_segmen(vert_segments, "V", inner_c, cy, 0.9, 2.1, 0.0)

## B. Aturan Generik Ruangan Rumah Tinggal ETS (Kamar, Ruang Tamu, Dapur, Kamar Mandi, Teras)
            elif any(k in lbl for k in ("KAMAR", "TAMU", "KELUARGA", "DAPUR", "MAKAN", "MANDI", "TERAS", "GARASI")):
## Pasang pintu pada sisi dinding dalam (yang bukan dinding batas luar gedung)
                if r2 < max_r:
                    self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, 0.9, 2.0, 0.0)
                elif r1 > 0:
                    self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, 0.9, 2.0, 0.0)
                if c1 > 0 and "TAMU" not in lbl:
                    self._tambah_celah_ke_segmen(vert_segments, "V", c1, cy, 0.9, 2.0, 0.0)
## Pasang jendela pada dinding luar (eksterior)
                if r1 == 0 and "MANDI" not in lbl:
                    self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, min(1.4, width_x * 0.4), 1.0, 1.0)
                if r2 == max_r:
                    if "TAMU" in lbl or "TERAS" in lbl:
                        self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, 1.0, 2.0, 0.0)
                    else:
                        self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, min(1.4, width_x * 0.4), 1.0, 1.0)

    def _tentukan_material_lantai(self, label):
        lbl = label.upper()
        if "WORK STATION" in lbl or "TAMU" in lbl or "KELUARGA" in lbl:
            return "lantai_workstation"
        if "CORIDOR" in lbl or "KORIDOR" in lbl or lbl == "":
            return "lantai_koridor"
        if lbl in ("[R]", "R") or "KAMAR TIDUR" in lbl:
            return "lantai_ruang_r"
        if "ARSIP" in lbl or "GARASI" in lbl:
            return "lantai_arsip"
        if "TOILET" in lbl or "MANDI" in lbl:
            return "lantai_toilet"
        if "PANTRY" in lbl or "DAPUR" in lbl or "MAKAN" in lbl:
            return "lantai_pantry"
        if "TANGGA" in lbl or "TERAS" in lbl:
            return "lantai_tangga"
        if "LIFT" in lbl:
            return "lantai_lift"
        if "AHU" in lbl or "PANEL" in lbl:
            return "lantai_teknis"
        return "lantai_koridor"

    def _bangun_furnitur_dan_label_otomatis(self, rooms):
        """Menghasilkan daftar furnitur primitif & label 3D berdasarkan nama tiap ruangan."""
        furnitur = []
        label_ruang = []

        for rm in rooms:
            lbl = rm["label"].upper()
            x1, x2, y1, y2 = rm["x1"], rm["x2"], rm["y1"], rm["y2"]
            cx = round((x1 + x2) / 2.0, 2)
            cy = round((y1 + y2) / 2.0, 2)
            wx = round(x2 - x1, 2)
            wy = round(y2 - y1, 2)

            if rm["label"]:
                label_ruang.append(
                    {
                        "teks": rm["label"],
                        "di": [cx, cy],
                        "ukuran": 0.45 if wx >= 6.0 else (0.28 if wx >= 2.5 else 0.22),
                    }
                )

## --- A. KATEGORI GEDUNG KANTOR ---
            if "WORK STATION" in lbl:
                is_utara = "UTARA" in lbl
                y_base = round(y1 + 1.8, 2) if is_utara else round(y2 - 1.8, 2)
                y_row2 = round(y1 + 3.4, 2) if is_utara else round(y2 - 3.4, 2)
                for idx, x_pos in enumerate([5.5, 9.0, 12.5, 21.5, 25.0, 28.5]):
                    if x1 + 1.0 < x_pos < x2 - 1.0:
                        furnitur.append({
                            "nama": f"Kubikel_{'U' if is_utara else 'S'}_R1_{idx+1}",
                            "type": "meja_kerja",
                            "di": [x_pos, y_base],
                            "rot": [0.0, 0.0, 0.0 if is_utara else round(math.pi, 4)],
                        })
                        furnitur.append({
                            "nama": f"Kubikel_{'U' if is_utara else 'S'}_R2_{idx+1}",
                            "type": "meja_kerja",
                            "di": [x_pos, y_row2],
                            "rot": [0.0, 0.0, round(math.pi, 4) if is_utara else 0.0],
                        })
                furnitur.append({
                    "nama": f"MejaRapat_{'Utara' if is_utara else 'Selatan'}",
                    "type": "meja_rapat",
                    "di": [cx, round((y_base + y_row2) / 2.0, 2)],
                    "rot": [0.0, 0.0, 0.0],
                })
                for p_idx, px in enumerate([round(x1 + 1.0, 2), round(cx - 2.0, 2), round(cx + 2.5, 2), round(x2 - 1.0, 2)]):
                    furnitur.append({
                        "nama": f"PotTanaman_{'U' if is_utara else 'S'}_{p_idx+1}",
                        "type": "pot_tanaman",
                        "di": [px, y_base],
                    })

            elif lbl in ("[R]", "R"):
                rot_z = round(math.pi, 4) if lbl == "[R]" else 0.0
                furnitur.append({
                    "nama": f"SetRuangR_{rm['id']}",
                    "type": "set_ruang_r",
                    "di": [cx, cy],
                    "rot": [0.0, 0.0, rot_z],
                })

            elif "ARSIP" in lbl:
                for idx, ry in enumerate([round(y1 + 1.4, 2), round(cy, 2), round(y2 - 1.4, 2)]):
                    furnitur.append({
                        "nama": f"RakArsip_{rm['id']}_{idx+1}",
                        "type": "rak_arsip",
                        "di": [cx, ry],
                        "rot": [0.0, 0.0, round(math.pi / 2.0, 4)],
                    })

            elif "TOILET" in lbl or "MANDI" in lbl:
                jml_kloset = 4 if wx >= 6.0 and wy >= 2.0 else (3 if wx >= 6.0 else 1)
                start_x = round(x1 + 1.2, 2) if jml_kloset > 1 else round(cx - 0.6, 2)
                for k_idx in range(jml_kloset):
                    furnitur.append({
                        "nama": f"Kloset_{rm['id']}_{k_idx+1}",
                        "type": "kloset",
                        "di": [round(start_x + k_idx * 1.4, 2), round(y2 - 0.45, 2)],
                        "rot": [0.0, 0.0, round(math.pi, 4)],
                    })
                furnitur.append({
                    "nama": f"Wastafel_{rm['id']}",
                    "type": "wastafel",
                    "di": [round(x2 - 1.2, 2) if wx >= 4.0 else round(cx + 0.6, 2), round(y1 + 0.4, 2)],
                    "rot": [0.0, 0.0, 0.0],
                })

            elif "LIFT" in lbl:
                if "LIFT-1" in lbl:
                    furnitur.append({
                        "nama": f"KabinLift1_{rm['id']}",
                        "type": "kabin_lift",
                        "di": [round(cx - 1.2, 2), cy],
                        "ukuran": [1.8, 1.2],
                    })
                    furnitur.append({
                        "nama": f"KabinLift2_{rm['id']}",
                        "type": "kabin_lift",
                        "di": [round(cx + 1.2, 2), cy],
                        "ukuran": [1.8, 1.2],
                    })
                else:
                    furnitur.append({
                        "nama": f"KabinLift_{rm['id']}",
                        "type": "kabin_lift",
                        "di": [cx, cy],
                        "ukuran": [round(max(1.2, wx - 0.6), 2), round(max(0.7, wy - 0.3), 2)],
                    })

            elif "PANTRY" in lbl or "DAPUR" in lbl:
                furnitur.append({
                    "nama": f"MejaPantry_{rm['id']}",
                    "type": "meja_pantry",
                    "di": [round(cx - 0.6, 2), round(y1 + 0.45, 2)],
                    "rot": [0.0, 0.0, 0.0],
                })
                furnitur.append({
                    "nama": f"Kulkas_{rm['id']}",
                    "type": "kulkas",
                    "di": [round(x2 - 0.6, 2), round(cy, 2)],
                    "rot": [0.0, 0.0, round(-math.pi / 2.0, 4)],
                })

            elif "TANGGA" in lbl:
                furnitur.append({
                    "nama": f"TanggaDarurat_{rm['id']}",
                    "type": "tangga_darurat",
                    "di": [cx, cy],
                    "panjang": round(max(2.5, wx - 1.2), 2),
                    "lebar": round(max(0.8, wy - 0.3), 2),
                })

            elif "AHU" in lbl:
                furnitur.append({
                    "nama": f"MesinAHU_{rm['id']}",
                    "type": "mesin_ahu",
                    "di": [cx, cy],
                })

            elif "PANEL" in lbl:
                for p_idx, px in enumerate([round(cx - 2.2, 2), cx, round(cx + 2.2, 2)]):
                    furnitur.append({
                        "nama": f"PanelListrik_{rm['id']}_{p_idx+1}",
                        "type": "panel_listrik",
                        "di": [px, round(y1 + 0.35, 2)],
                    })

## --- B. KATEGORI RUMAH TINGGAL ETS ---
            elif "TAMU" in lbl or "KELUARGA" in lbl:
                furnitur.append({
                    "nama": f"Sofa_{rm['id']}",
                    "type": "sofa",
                    "di": [round(cx - 0.8, 2), round(cy + 0.5, 2)],
                    "rot": [0.0, 0.0, round(math.pi, 4)],
                })
                furnitur.append({
                    "nama": f"RakTV_{rm['id']}",
                    "type": "rak_tv",
                    "di": [round(cx - 0.8, 2), round(cy - 1.2, 2)],
                    "rot": [0.0, 0.0, 0.0],
                })
                furnitur.append({
                    "nama": f"PotTanamanTamu_{rm['id']}",
                    "type": "pot_tanaman",
                    "di": [round(x1 + 0.6, 2), round(y2 - 0.6, 2)],
                })

            elif "KAMAR" in lbl and "MANDI" not in lbl:
                furnitur.append({
                    "nama": f"Kasur_{rm['id']}",
                    "type": "kasur",
                    "di": [cx, round(y2 - 1.1, 2)],
                    "rot": [0.0, 0.0, round(math.pi, 4)],
                })
                furnitur.append({
                    "nama": f"Lemari_{rm['id']}",
                    "type": "lemari",
                    "di": [round(x1 + 0.5, 2), round(y1 + 0.7, 2)],
                    "rot": [0.0, 0.0, round(math.pi / 2.0, 4)],
                })

            elif "MAKAN" in lbl:
                furnitur.append({
                    "nama": f"MejaMakan_{rm['id']}",
                    "type": "meja_makan",
                    "di": [cx, cy],
                    "rot": [0.0, 0.0, 0.0],
                })

        return furnitur, label_ruang

    def parse_to_dict(self, ascii_text):
        """Menghasilkan dictionary lengkap yang mengikuti skema config_denah.json."""
        grid = self._normalisasi_baris(ascii_text)
        H = len(grid)
        W = len(grid[0])
        max_r = H - 1
        max_c = W - 1

        grid_width_m = round(max_c * self.scale_x, 2)
        grid_height_m = round(max_r * self.scale_y, 2)

        rooms = self._ekstrak_ruangan(grid)
        horiz_segments, vert_segments = self._ekstrak_segmen_dinding(grid)
        self._injeksi_pintu_dan_jendela_otomatis(
            rooms, horiz_segments, vert_segments, max_r, max_c
        )

        segmen_dinding = []
        for s in horiz_segments + vert_segments:
            segmen_dinding.append(
                {
                    "nama": s["nama"],
                    "dari": s["dari"],
                    "ke": s["ke"],
                    "material": s["material"],
                    "celah": sorted(s["celah"], key=lambda item: item["dari"]),
                }
            )

        zona_lantai = []
        for rm in rooms:
            nama_zona = rm["label"] if rm["label"] else f"Area_Sirkulasi_{rm['id']}"
            zona_lantai.append(
                {
                    "nama": f"Lantai_{rm['id']:02d}_{re.sub(r'[^A-Za-z0-9]+', '_', nama_zona).strip('_')}",
                    "min_xy": [rm["x1"], rm["y1"]],
                    "max_xy": [rm["x2"], rm["y2"]],
                    "material": self._tentukan_material_lantai(rm["label"]),
                }
            )

        furnitur, label_ruang = self._bangun_furnitur_dan_label_otomatis(rooms)

        return {
            "meta": {
                "sumber": "AsciiDenahParser (SOLID Config-Driven)",
                "ascii_grid_chars": [W, H],
                "skala_meter_per_char": [self.scale_x, self.scale_y],
            },
            "rumah": {
                "grid": [grid_width_m, grid_height_m],
                "tinggi_dinding": self.tinggi_dinding,
                "tebal_dinding": self.tebal_dinding,
                "segmen_dinding": segmen_dinding,
                "zona_lantai": zona_lantai,
                "furnitur": furnitur,
                "label_ruang": label_ruang,
            },
        }

## ==============================================================================
## BAGIAN 4: LIBRARY BLENDER SOLID (Kompatibel Penuh dengan Blender 4.3)
## ==============================================================================
try:
    import bpy
    from mathutils import Vector
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

if BLENDER_AVAILABLE:

    class SceneManager:
        """SRP: Mengelola lifecycle scene, koleksi, join, dan origin alas (world-accurate)."""

        @staticmethod
        def bersihkan_scene():
            if bpy.context.active_object and bpy.context.active_object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.object.delete()
            for mesh in list(bpy.data.meshes):
                bpy.data.meshes.remove(mesh)
            for curve in list(bpy.data.curves):
                bpy.data.curves.remove(curve)
            for mat in list(bpy.data.materials):
                bpy.data.materials.remove(mat)

        @staticmethod
        def buat_koleksi(nama_koleksi):
            if nama_koleksi in bpy.data.collections:
                return bpy.data.collections[nama_koleksi]
            kol = bpy.data.collections.new(nama_koleksi)
            bpy.context.scene.collection.children.link(kol)
            return kol

        @staticmethod
        def pindahkan_ke_koleksi(obj, koleksi):
            for c in list(obj.users_collection):
                c.objects.unlink(obj)
            koleksi.objects.link(obj)

        @staticmethod
        def set_origin_ke_tengah_alas(obj):
            """Origin di tengah alas: bbox dihitung dalam koordinat DUNIA (matrix_world),
            kursor dipulihkan setelah dipakai."""
            if hasattr(bpy.context.view_layer, "update"):
                bpy.context.view_layer.update()
            bpy.context.view_layer.objects.active = obj
            world_bbox = [obj.matrix_world @ Vector(b) for b in obj.bound_box]
            min_z = min(v.z for v in world_bbox)
            cx = (min(v.x for v in world_bbox) + max(v.x for v in world_bbox)) / 2.0
            cy = (min(v.y for v in world_bbox) + max(v.y for v in world_bbox)) / 2.0
            cursor_lama = bpy.context.scene.cursor.location.copy()
            bpy.context.scene.cursor.location = Vector((cx, cy, min_z))
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            bpy.context.scene.cursor.location = cursor_lama
            obj.location = Vector((0.0, 0.0, 0.0))

        @staticmethod
        def gabung_objek(daftar_obj, nama_hasil="GrupFurnitur"):
            if not daftar_obj:
                return None
            bpy.ops.object.select_all(action="DESELECT")
            for o in daftar_obj:
                o.select_set(True)
            bpy.context.view_layer.objects.active = daftar_obj[0]
            if len(daftar_obj) > 1:
                bpy.ops.object.join()
            hasil = bpy.context.active_object
            hasil.name = nama_hasil
            return hasil

    class MaterialFactory:
        """SRP: Membuat atau mengambil material dari palet JSON (mendukung Blender 4.3)."""

        @staticmethod
        def get_or_create(nama_mat, spec):
            if nama_mat in bpy.data.materials:
                return bpy.data.materials[nama_mat]
            mat = bpy.data.materials.new(name=nama_mat)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = tuple(spec["rgba"])
                bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.85))
                if spec.get("emission") and spec.get("emission_strength", 0) > 0:
                    em_input = (
                        bsdf.inputs.get("Emission Color")
                        or bsdf.inputs.get("Emission")
                    )
                    if em_input:
                        em_input.default_value = tuple(spec["emission"])
                    if "Emission Strength" in bsdf.inputs:
                        bsdf.inputs["Emission Strength"].default_value = float(
                            spec["emission_strength"]
                        )
            mat.diffuse_color = tuple(spec["rgba"])
            return mat

    class AssetBuilder:
        """SRP & OCP: Registry pembangun primitif & furnitur 3D. Fail-fast bila tipe tak dikenal."""

        def __init__(self, mat_factory, palet):
            self.mat_factory = mat_factory
            self.palet = palet
            self._registry = {
                "box": self._bangun_kotak,
                "silinder": self._bangun_silinder,
                "grup": self._bangun_grup_furnitur,
                "pot_tanaman": self._bangun_pot_tanaman,
## Aset Gedung Kantor
                "meja_kerja": self._bangun_meja_kerja,
                "meja_rapat": self._bangun_meja_rapat,
                "set_ruang_r": self._bangun_set_ruang_r,
                "rak_arsip": self._bangun_rak_arsip,
                "kloset": self._bangun_kloset,
                "wastafel": self._bangun_wastafel,
                "kabin_lift": self._bangun_kabin_lift,
                "meja_pantry": self._bangun_meja_pantry,
                "kulkas": self._bangun_kulkas,
                "tangga_darurat": self._bangun_tangga_darurat,
                "mesin_ahu": self._bangun_mesin_ahu,
                "panel_listrik": self._bangun_panel_listrik,
## Aset Rumah Tinggal (ETS)
                "sofa": self._bangun_sofa,
                "rak_tv": self._bangun_rak_tv,
                "kasur": self._bangun_kasur,
                "lemari": self._bangun_lemari,
                "meja_makan": self._bangun_meja_makan,
            }

        def daftar_tipe(self, tipe, fungsi):
            """OCP: Daftarkan tipe aset baru dari luar tanpa mengubah kode inti."""
            self._registry[tipe] = fungsi

        def _mat(self, nama_mat):
            if nama_mat not in self.palet:
                raise ValueError(f"Material tak dikenal di palet: {nama_mat!r}")
            return self.mat_factory.get_or_create(nama_mat, self.palet[nama_mat])

        def membangun(self, spec):
            fn = self._registry.get(spec["type"])
            if fn is None:
                raise ValueError(f"Tipe aset tak dikenal: {spec['type']!r}")
            return fn(spec)

        def _bangun_kotak(self, spec):
            dim = spec["dimensions"]
            di = spec.get("di", [0.0, 0.0])
            z = spec.get("z", dim[2] / 2.0)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(di[0], di[1], z))
            o = bpy.context.active_object
            o.name = spec.get("name", spec.get("nama", "Kotak"))
            o.scale = Vector(dim)
            bpy.ops.object.transform_apply(scale=True)
            if spec.get("rot"):
                o.rotation_euler = tuple(spec["rot"])
            o.data.materials.append(self._mat(spec["material"]))
            return o

        def _bangun_silinder(self, spec):
            r = spec.get("radius", 0.25)
            t = spec.get("depth", 1.0)
            di = spec.get("di", [0.0, 0.0])
            z = spec.get("z", t / 2.0)
            bpy.ops.mesh.primitive_cylinder_add(
                radius=r, depth=t, location=(di[0], di[1], z)
            )
            o = bpy.context.active_object
            o.name = spec.get("name", spec.get("nama", "Silinder"))
            if spec.get("rot"):
                o.rotation_euler = tuple(spec["rot"])
            o.data.materials.append(self._mat(spec["material"]))
            return o

        def _rakit_komponen_lokal(self, spec, daftar_komponen):
            """Membangun furnitur komposit dari daftar primitif lokal lalu menerapkan posisi & rotasi."""
            bagian = []
            for idx, komp in enumerate(daftar_komponen):
                k_spec = dict(komp)
                k_spec["name"] = f"{spec.get('nama', 'Aset')}_part{idx}"
                bagian.append(self.membangun(k_spec))
            gabungan = SceneManager.gabung_objek(bagian, spec.get("nama", "Furnitur"))
            SceneManager.set_origin_ke_tengah_alas(gabungan)
            di = spec.get("di", [0.0, 0.0])
            gabungan.location = Vector((di[0], di[1], spec.get("z", 0.0)))
            if spec.get("rot"):
                gabungan.rotation_euler = tuple(spec["rot"])
            return gabungan

        def _bangun_grup_furnitur(self, spec):
            return self._rakit_komponen_lokal(spec, spec["komponen"])

        def _bangun_pot_tanaman(self, spec):
            komp = [
                {"type": "silinder", "radius": 0.22, "depth": 0.38, "di": [0.0, 0.0], "z": 0.19, "material": "pot_terakota"},
                {"type": "silinder", "radius": 0.05, "depth": 0.45, "di": [0.0, 0.0], "z": 0.55, "material": "kayu_gelap"},
                {"type": "box", "dimensions": [0.42, 0.42, 0.38], "di": [0.0, 0.0], "z": 0.85, "material": "hijau_daun"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_meja_kerja(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.4, 0.7, 0.05], "di": [0.0, 0.0], "z": 0.73, "material": "kayu_meja"},
                {"type": "box", "dimensions": [0.06, 0.66, 0.71], "di": [-0.65, 0.0], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.06, 0.66, 0.71], "di": [0.65, 0.0], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [1.42, 0.05, 1.15], "di": [0.0, 0.35], "z": 0.575, "material": "partisi_kubikel"},
                {"type": "box", "dimensions": [0.52, 0.04, 0.32], "di": [0.0, 0.15], "z": 0.98, "material": "layar_monitor"},
                {"type": "box", "dimensions": [0.08, 0.08, 0.12], "di": [0.0, 0.15], "z": 0.80, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.48, 0.48, 0.07], "di": [0.0, -0.55], "z": 0.46, "material": "kursi_kantor"},
                {"type": "box", "dimensions": [0.46, 0.06, 0.48], "di": [0.0, -0.77], "z": 0.72, "material": "kursi_kantor"},
                {"type": "silinder", "radius": 0.06, "depth": 0.44, "di": [0.0, -0.55], "z": 0.22, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_meja_rapat(self, spec):
            komp = [
                {"type": "box", "dimensions": [2.8, 1.1, 0.06], "di": [0.0, 0.0], "z": 0.74, "material": "kayu_gelap"},
                {"type": "box", "dimensions": [0.14, 0.75, 0.71], "di": [-0.95, 0.0], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.14, 0.75, 0.71], "di": [0.95, 0.0], "z": 0.355, "material": "logam_abu"},
            ]
            for kx in [-0.9, 0.0, 0.9]:
                komp.append({"type": "box", "dimensions": [0.44, 0.44, 0.46], "di": [kx, -0.78], "z": 0.23, "material": "kursi_kantor"})
                komp.append({"type": "box", "dimensions": [0.44, 0.44, 0.46], "di": [kx, 0.78], "z": 0.23, "material": "kursi_kantor"})
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_set_ruang_r(self, spec):
            komp = [
                {"type": "box", "dimensions": [0.95, 0.45, 0.05], "di": [0.0, 0.12], "z": 0.73, "material": "kayu_meja"},
                {"type": "box", "dimensions": [0.06, 0.42, 0.71], "di": [-0.42, 0.12], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.06, 0.42, 0.71], "di": [0.42, 0.12], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.38, 0.04, 0.26], "di": [0.0, 0.22], "z": 0.90, "material": "layar_monitor"},
                {"type": "box", "dimensions": [0.40, 0.40, 0.45], "di": [0.0, -0.22], "z": 0.225, "material": "kursi_kantor"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_rak_arsip(self, spec):
            komp = [
                {"type": "box", "dimensions": [0.05, 0.05, 2.0], "di": [-0.65, -0.22], "z": 1.0, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.05, 0.05, 2.0], "di": [0.65, -0.22], "z": 1.0, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.05, 0.05, 2.0], "di": [-0.65, 0.22], "z": 1.0, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.05, 0.05, 2.0], "di": [0.65, 0.22], "z": 1.0, "material": "logam_abu"},
            ]
            for sz in [0.20, 0.75, 1.30, 1.85]:
                komp.append({"type": "box", "dimensions": [1.35, 0.48, 0.04], "di": [0.0, 0.0], "z": sz, "material": "logam_abu"})
                if sz < 1.80:
                    komp.append({"type": "box", "dimensions": [1.10, 0.38, 0.32], "di": [0.0, 0.0], "z": sz + 0.18, "material": "kardus_arsip"})
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_kloset(self, spec):
            komp = [
                {"type": "box", "dimensions": [0.42, 0.55, 0.40], "di": [0.0, 0.0], "z": 0.20, "material": "keramik_putih"},
                {"type": "box", "dimensions": [0.44, 0.22, 0.42], "di": [0.0, -0.18], "z": 0.60, "material": "keramik_putih"},
                {"type": "box", "dimensions": [0.05, 1.10, 1.85], "di": [0.55, 0.15], "z": 0.925, "material": "partisi_kubikel"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_wastafel(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.60, 0.52, 0.82], "di": [0.0, 0.0], "z": 0.41, "material": "keramik_putih"},
                {"type": "box", "dimensions": [1.50, 0.04, 0.95], "di": [0.0, -0.24], "z": 1.35, "material": "kaca_jendela"},
                {"type": "silinder", "radius": 0.04, "depth": 0.18, "di": [-0.42, -0.12], "z": 0.91, "material": "logam_abu"},
                {"type": "silinder", "radius": 0.04, "depth": 0.18, "di": [0.42, -0.12], "z": 0.91, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_kabin_lift(self, spec):
            ux, uy = spec.get("ukuran", [1.8, 1.1])
            komp = [
                {"type": "box", "dimensions": [ux, uy, 0.10], "di": [0.0, 0.0], "z": 0.05, "material": "lantai_lift"},
                {"type": "box", "dimensions": [ux, 0.06, 2.30], "di": [0.0, uy / 2.0 - 0.03], "z": 1.15, "material": "logam_lift"},
                {"type": "box", "dimensions": [0.06, uy, 2.30], "di": [-ux / 2.0 + 0.03, 0.0], "z": 1.15, "material": "logam_lift"},
                {"type": "box", "dimensions": [0.06, uy, 2.30], "di": [ux / 2.0 - 0.03, 0.0], "z": 1.15, "material": "logam_lift"},
                {"type": "box", "dimensions": [0.35, 0.08, 0.12], "di": [0.0, -uy / 2.0 + 0.05], "z": 2.22, "material": "lampu_indikator"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_meja_pantry(self, spec):
            komp = [
                {"type": "box", "dimensions": [2.2, 0.60, 0.85], "di": [0.0, 0.0], "z": 0.425, "material": "kayu_meja"},
                {"type": "box", "dimensions": [2.24, 0.64, 0.05], "di": [0.0, 0.0], "z": 0.875, "material": "keramik_putih"},
                {"type": "box", "dimensions": [0.45, 0.38, 0.42], "di": [-0.55, 0.0], "z": 1.11, "material": "panel_listrik"},
                {"type": "silinder", "radius": 0.04, "depth": 0.24, "di": [0.55, -0.15], "z": 1.02, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_kulkas(self, spec):
            komp = [
                {"type": "box", "dimensions": [0.75, 0.70, 1.15], "di": [0.0, 0.0], "z": 0.575, "material": "logam_lift"},
                {"type": "box", "dimensions": [0.75, 0.70, 0.62], "di": [0.0, 0.0], "z": 1.48, "material": "logam_lift"},
                {"type": "box", "dimensions": [0.04, 0.06, 0.45], "di": [0.32, -0.36], "z": 0.85, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_tangga_darurat(self, spec):
            panjang = spec.get("panjang", 4.0)
            lebar = spec.get("lebar", 1.2)
            jml_anak = 9
            dx = panjang / float(jml_anak)
            dz = 2.4 / float(jml_anak)
            komp = []
            for i in range(jml_anak):
                x_pos = -panjang / 2.0 + (i + 0.5) * dx
                tinggi_blok = (i + 1) * dz
                komp.append({
                    "type": "box",
                    "dimensions": [dx * 0.96, lebar, tinggi_blok],
                    "di": [x_pos, 0.0],
                    "z": tinggi_blok / 2.0,
                    "material": "lantai_tangga",
                })
            komp.append({"type": "box", "dimensions": [panjang, 0.05, 0.06], "di": [0.0, lebar / 2.0 - 0.03], "z": 1.55, "material": "rail_tangga"})
            komp.append({"type": "box", "dimensions": [panjang, 0.05, 0.06], "di": [0.0, -lebar / 2.0 + 0.03], "z": 1.55, "material": "rail_tangga"})
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_mesin_ahu(self, spec):
            komp = [
                {"type": "box", "dimensions": [2.2, 0.95, 1.65], "di": [0.0, 0.0], "z": 0.825, "material": "mesin_hvac"},
                {"type": "silinder", "radius": 0.32, "depth": 0.45, "di": [-0.55, 0.0], "z": 1.85, "material": "logam_abu"},
                {"type": "silinder", "radius": 0.32, "depth": 0.45, "di": [0.55, 0.0], "z": 1.85, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_panel_listrik(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.10, 0.45, 2.00], "di": [0.0, 0.0], "z": 1.00, "material": "panel_listrik"},
                {"type": "box", "dimensions": [0.12, 0.06, 0.12], "di": [-0.25, -0.23], "z": 1.65, "material": "lampu_indikator"},
                {"type": "box", "dimensions": [0.12, 0.06, 0.12], "di": [0.0, -0.23], "z": 1.65, "material": "lampu_indikator"},
                {"type": "box", "dimensions": [0.12, 0.06, 0.12], "di": [0.25, -0.23], "z": 1.65, "material": "lampu_indikator"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

## --- Builder Aset Rumah Tinggal (ETS) ---
        def _bangun_sofa(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.80, 0.75, 0.40], "di": [0.0, 0.0], "z": 0.20, "material": "kain_sofa"},
                {"type": "box", "dimensions": [1.80, 0.18, 0.48], "di": [0.0, -0.28], "z": 0.64, "material": "kain_sofa"},
                {"type": "box", "dimensions": [0.18, 0.75, 0.30], "di": [-0.81, 0.0], "z": 0.55, "material": "kain_sofa"},
                {"type": "box", "dimensions": [0.18, 0.75, 0.30], "di": [0.81, 0.0], "z": 0.55, "material": "kain_sofa"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_rak_tv(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.50, 0.42, 0.48], "di": [0.0, 0.0], "z": 0.24, "material": "kayu_meja"},
                {"type": "box", "dimensions": [1.10, 0.06, 0.62], "di": [0.0, 0.0], "z": 0.85, "material": "layar_monitor"},
                {"type": "box", "dimensions": [0.25, 0.20, 0.08], "di": [0.0, 0.0], "z": 0.52, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_kasur(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.60, 2.00, 0.32], "di": [0.0, 0.0], "z": 0.16, "material": "kayu_gelap"},
                {"type": "box", "dimensions": [1.52, 1.92, 0.22], "di": [0.0, 0.0], "z": 0.43, "material": "kain_kasur"},
                {"type": "box", "dimensions": [1.50, 1.20, 0.05], "di": [0.0, 0.32], "z": 0.56, "material": "selimut_biru"},
                {"type": "box", "dimensions": [1.60, 0.10, 0.95], "di": [0.0, -0.95], "z": 0.475, "material": "kayu_gelap"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_lemari(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.20, 0.55, 2.00], "di": [0.0, 0.0], "z": 1.00, "material": "kayu_meja"},
                {"type": "box", "dimensions": [0.04, 0.04, 0.35], "di": [-0.08, -0.29], "z": 1.05, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.04, 0.04, 0.35], "di": [0.08, -0.29], "z": 1.05, "material": "logam_abu"},
            ]
            return self._rakit_komponen_lokal(spec, komp)

        def _bangun_meja_makan(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.50, 0.90, 0.06], "di": [0.0, 0.0], "z": 0.74, "material": "kayu_meja"},
                {"type": "box", "dimensions": [0.08, 0.08, 0.71], "di": [-0.65, -0.35], "z": 0.355, "material": "kayu_gelap"},
                {"type": "box", "dimensions": [0.08, 0.08, 0.71], "di": [0.65, -0.35], "z": 0.355, "material": "kayu_gelap"},
                {"type": "box", "dimensions": [0.08, 0.08, 0.71], "di": [-0.65, 0.35], "z": 0.355, "material": "kayu_gelap"},
                {"type": "box", "dimensions": [0.08, 0.08, 0.71], "di": [0.65, 0.35], "z": 0.355, "material": "kayu_gelap"},
            ]
            for kx in [-0.42, 0.42]:
                komp.append({"type": "box", "dimensions": [0.42, 0.42, 0.45], "di": [kx, -0.68], "z": 0.225, "material": "kursi_kantor"})
                komp.append({"type": "box", "dimensions": [0.42, 0.42, 0.45], "di": [kx, 0.68], "z": 0.225, "material": "kursi_kantor"})
            return self._rakit_komponen_lokal(spec, komp)

    class DenahBuilder:
        """
        SRP: Menerjemahkan data rumah (config_denah.json) menjadi geometri 3D:
          1. Zona lantai per ruangan
          2. Dinding terpotong celah (_potong_dengan_celah) + kusen otomatis (_pasang_kusen)
          3. Furnitur / peralatan gedung dari AssetBuilder
          4. Teks 3D nama ruangan di atas lantai
        """

        def __init__(self, builder, cfg_rumah):
            self.builder = builder
            self.cfg = cfg_rumah
            self.tinggi = float(cfg_rumah.get("tinggi_dinding", 3.0))
            self.tebal = float(cfg_rumah.get("tebal_dinding", 0.15))

        @staticmethod
        def _potong_dengan_celah(a1, a2, celah_list):
            """Interval subtraction: memotong segmen [a1, a2] dengan daftar celah {dari, ke}."""
            batas = [(min(a1, a2), max(a1, a2))]
            for c in celah_list:
                baru = []
                for (s, e) in batas:
                    if c["ke"] <= s or c["dari"] >= e:
                        baru.append((s, e))
                    else:
                        if c["dari"] > s:
                            baru.append((s, c["dari"]))
                        if c["ke"] < e:
                            baru.append((c["ke"], e))
                batas = baru
            return [(s, e) for (s, e) in batas if e - s > 0.01]

        def _pasang_kusen(self, seg, c, horizontal, t, z_offset=0.0):
            """Setiap celah otomatis mendapat kusen (2 tiang + lintel; jendela ditambah sill & kaca)."""
            fk = 0.06
            tp = t + 0.05
            bukaan = float(c.get("tinggi_bukaan", 2.1))
            ambang = float(c.get("ambang_bawah", 0.0))
            mat_kusen = "kusen_aluminium" if ambang > 0.01 else "kusen_kayu"

            c_dari, c_ke = float(c["dari"]), float(c["ke"])
            lebar_lubang = c_ke - c_dari
            tengah_c = (c_dari + c_ke) / 2.0
            z_tengah_tiang = z_offset + ambang + bukaan / 2.0

            if horizontal:
                y_pos = float(seg["dari"][1])
                self.builder.membangun({
                    "type": "box",
                    "name": f"KusenTiangL_{seg['nama']}",
                    "dimensions": [fk, tp, bukaan],
                    "di": [c_dari + fk / 2.0, y_pos],
                    "z": z_tengah_tiang,
                    "material": mat_kusen,
                })
                self.builder.membangun({
                    "type": "box",
                    "name": f"KusenTiangR_{seg['nama']}",
                    "dimensions": [fk, tp, bukaan],
                    "di": [c_ke - fk / 2.0, y_pos],
                    "z": z_tengah_tiang,
                    "material": mat_kusen,
                })
                self.builder.membangun({
                    "type": "box",
                    "name": f"KusenLintel_{seg['nama']}",
                    "dimensions": [lebar_lubang, tp, fk],
                    "di": [tengah_c, y_pos],
                    "z": z_offset + ambang + bukaan - fk / 2.0,
                    "material": mat_kusen,
                })
                if ambang > 0.01:
                    self.builder.membangun({
                        "type": "box",
                        "name": f"KusenSill_{seg['nama']}",
                        "dimensions": [lebar_lubang, tp, fk],
                        "di": [tengah_c, y_pos],
                        "z": z_offset + ambang + fk / 2.0,
                        "material": mat_kusen,
                    })
                    self.builder.membangun({
                        "type": "box",
                        "name": f"KacaJendela_{seg['nama']}",
                        "dimensions": [max(0.05, lebar_lubang - 2 * fk), 0.02, max(0.05, bukaan - 2 * fk)],
                        "di": [tengah_c, y_pos],
                        "z": z_tengah_tiang,
                        "material": "kaca_jendela",
                    })
            else:
                x_pos = float(seg["dari"][0])
                self.builder.membangun({
                    "type": "box",
                    "name": f"KusenTiangB_{seg['nama']}",
                    "dimensions": [tp, fk, bukaan],
                    "di": [x_pos, c_dari + fk / 2.0],
                    "z": z_tengah_tiang,
                    "material": mat_kusen,
                })
                self.builder.membangun({
                    "type": "box",
                    "name": f"KusenTiangT_{seg['nama']}",
                    "dimensions": [tp, fk, bukaan],
                    "di": [x_pos, c_ke - fk / 2.0],
                    "z": z_tengah_tiang,
                    "material": mat_kusen,
                })
                self.builder.membangun({
                    "type": "box",
                    "name": f"KusenLintel_{seg['nama']}",
                    "dimensions": [tp, lebar_lubang, fk],
                    "di": [x_pos, tengah_c],
                    "z": z_offset + ambang + bukaan - fk / 2.0,
                    "material": mat_kusen,
                })
                if ambang > 0.01:
                    self.builder.membangun({
                        "type": "box",
                        "name": f"KusenSill_{seg['nama']}",
                        "dimensions": [tp, lebar_lubang, fk],
                        "di": [x_pos, tengah_c],
                        "z": z_offset + ambang + fk / 2.0,
                        "material": mat_kusen,
                    })
                    self.builder.membangun({
                        "type": "box",
                        "name": f"KacaJendela_{seg['nama']}",
                        "dimensions": [0.02, max(0.05, lebar_lubang - 2 * fk), max(0.05, bukaan - 2 * fk)],
                        "di": [x_pos, tengah_c],
                        "z": z_tengah_tiang,
                        "material": "kaca_jendela",
                    })

        def _bangun_dinding(self):
            for seg in self.cfg.get("segmen_dinding", []):
                x1, y1 = float(seg["dari"][0]), float(seg["dari"][1])
                x2, y2 = float(seg["ke"][0]), float(seg["ke"][1])
                horizontal = abs(y1 - y2) < 1e-4
                mat = seg.get("material", "dinding_interior")
                celah_list = seg.get("celah", [])

                a1, a2 = (min(x1, x2), max(x1, x2)) if horizontal else (min(y1, y2), max(y1, y2))
                potongan = self._potong_dengan_celah(a1, a2, celah_list)

                for idx, (s, e) in enumerate(potongan):
                    panjang = e - s
                    tengah = (s + e) / 2.0
                    if horizontal:
                        dim = [panjang, self.tebal, self.tinggi]
                        pos = [tengah, y1]
                    else:
                        dim = [self.tebal, panjang, self.tinggi]
                        pos = [x1, tengah]
                    self.builder.membangun({
                        "type": "box",
                        "name": f"{seg.get('nama', 'Dinding')}_seg{idx}",
                        "dimensions": dim,
                        "di": pos,
                        "z": self.tinggi / 2.0,
                        "material": mat,
                    })

                for c_idx, c in enumerate(celah_list):
                    c_dari, c_ke = float(c["dari"]), float(c["ke"])
                    lebar_c = c_ke - c_dari
                    tengah_c = (c_dari + c_ke) / 2.0
                    bukaan = float(c.get("tinggi_bukaan", 2.1))
                    ambang = float(c.get("ambang_bawah", 0.0))
                    tinggi_atas = self.tinggi - (ambang + bukaan)

                    if tinggi_atas > 0.02:
                        if horizontal:
                            dim_atas = [lebar_c, self.tebal, tinggi_atas]
                            pos_atas = [tengah_c, y1]
                        else:
                            dim_atas = [self.tebal, lebar_c, tinggi_atas]
                            pos_atas = [x1, tengah_c]
                        self.builder.membangun({
                            "type": "box",
                            "name": f"{seg.get('nama', 'Dinding')}_lintel{c_idx}",
                            "dimensions": dim_atas,
                            "di": pos_atas,
                            "z": ambang + bukaan + tinggi_atas / 2.0,
                            "material": mat,
                        })

                    if ambang > 0.02:
                        if horizontal:
                            dim_bawah = [lebar_c, self.tebal, ambang]
                            pos_bawah = [tengah_c, y1]
                        else:
                            dim_bawah = [self.tebal, lebar_c, ambang]
                            pos_bawah = [x1, tengah_c]
                        self.builder.membangun({
                            "type": "box",
                            "name": f"{seg.get('nama', 'Dinding')}_ambang{c_idx}",
                            "dimensions": dim_bawah,
                            "di": pos_bawah,
                            "z": ambang / 2.0,
                            "material": mat,
                        })

                    self._pasang_kusen(seg, c, horizontal, self.tebal, z_offset=0.0)

        def _bangun_lantai(self):
            zona_list = self.cfg.get("zona_lantai", [])
            if zona_list:
                for z in zona_list:
                    x1, y1 = float(z["min_xy"][0]), float(z["min_xy"][1])
                    x2, y2 = float(z["max_xy"][0]), float(z["max_xy"][1])
                    wx, wy = abs(x2 - x1), abs(y2 - y1)
                    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
                    self.builder.membangun({
                        "type": "box",
                        "name": z.get("nama", "LantaiZona"),
                        "dimensions": [wx, wy, 0.10],
                        "di": [cx, cy],
                        "z": -0.05,
                        "material": z.get("material", "lantai_koridor"),
                    })
            else:
                gx, gy = int(self.cfg["grid"][0]), int(self.cfg["grid"][1])
                for ix in range(gx):
                    for iy in range(gy):
                        self.builder.membangun({
                            "type": "box",
                            "name": f"Ubin_{ix}_{iy}",
                            "dimensions": [0.98, 0.98, 0.08],
                            "di": [ix + 0.5, iy + 0.5],
                            "z": -0.04,
                            "material": "lantai_workstation",
                        })

        def _bangun_furnitur(self):
            for f in self.cfg.get("furnitur", []):
                self.builder.membangun(f)

        def _bangun_label_ruang(self):
            mat_teks = self.builder._mat("teks_label")
            for lbl in self.cfg.get("label_ruang", []):
                bpy.ops.object.text_add(
                    location=(float(lbl["di"][0]), float(lbl["di"][1]), 0.03)
                )
                txt_obj = bpy.context.active_object
                txt_obj.name = f"Label_{lbl['teks'][:16]}"
                txt_obj.data.body = lbl["teks"]
                txt_obj.data.size = float(lbl.get("ukuran", 0.35))
                txt_obj.data.extrude = 0.015
                txt_obj.data.align_x = "CENTER"
                txt_obj.data.align_y = "CENTER"
                txt_obj.data.materials.append(mat_teks)

        def bangun_semua(self):
            self._bangun_lantai()
            self._bangun_dinding()
            self._bangun_furnitur()
            self._bangun_label_ruang()

## ==============================================================================
## BAGIAN 5: ORKESTRASI UTAMA (Sinkronisasi Text Block Blender + Build 3D)
## ==============================================================================
def simpan_ke_blok_teks_blender(nama_blok, isi_str):
    if not BLENDER_AVAILABLE:
        return
    if nama_blok in bpy.data.texts:
        blok = bpy.data.texts[nama_blok]
        blok.clear()
    else:
        blok = bpy.data.texts.new(nama_blok)
    blok.write(isi_str)

def atur_kamera_dan_cahaya(grid_xy):
    if not BLENDER_AVAILABLE:
        return
    gx, gy = float(grid_xy[0]), float(grid_xy[1])
    cx, cy = gx / 2.0, gy / 2.0

    bpy.ops.object.light_add(type="SUN", location=(cx + 10.0, cy - 12.0, 25.0))
    sun = bpy.context.active_object
    sun.name = "Matahari_Indoor"
    sun.data.energy = 3.5
    sun.rotation_euler = (math.radians(38), math.radians(18), math.radians(-25))

    bpy.ops.object.camera_add(location=(cx, -gy * 0.65, max(gx, gy) * 0.95))
    cam = bpy.context.active_object
    cam.name = "Kamera_Pratinjau"
    cam.rotation_euler = (math.radians(46), 0.0, 0.0)
    cam.data.lens = 32.0
    bpy.context.scene.camera = cam

    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 720

def jalankan_konversi_ascii_ke_3d(ascii_str=DENAH_ASCII, output_json_path=None):
    parser = AsciiDenahParser(
        scale_x=SKALA_X_METER_PER_KARAKTER,
        scale_y=SKALA_Y_METER_PER_KARAKTER,
        tinggi_dinding=TINGGI_DINDING_DEFAULT,
        tebal_dinding=TEBAL_DINDING_DEFAULT,
    )
    cfg_denah = parser.parse_to_dict(ascii_str)
    cfg_assets = DEFAULT_CONFIG_ASSETS

    if output_json_path:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(cfg_denah, f, indent=2, ensure_ascii=False)
        print(f"[OK] File JSON denah berhasil ditulis ke: {output_json_path}")

    if BLENDER_AVAILABLE:
        simpan_ke_blok_teks_blender("denah_ascii.txt", ascii_str.strip() + "\n")
        simpan_ke_blok_teks_blender(
            "config_denah.json", json.dumps(cfg_denah, indent=2, ensure_ascii=False)
        )
        simpan_ke_blok_teks_blender(
            "config_assets.json", json.dumps(cfg_assets, indent=2, ensure_ascii=False)
        )

        SceneManager.bersihkan_scene()
        koleksi = SceneManager.buat_koleksi("RumahIndoor")
        builder = AssetBuilder(MaterialFactory(), cfg_assets["palet"])
        DenahBuilder(builder, cfg_denah["rumah"]).bangun_semua()

        for obj in list(bpy.context.scene.objects):
            SceneManager.pindahkan_ke_koleksi(obj, koleksi)

        atur_kamera_dan_cahaya(cfg_denah["rumah"]["grid"])
        print(
            f"MATERI 1 ASCII->3D OK: Denah {cfg_denah['rumah']['grid'][0]}x{cfg_denah['rumah']['grid'][1]}m "
            f"({len(cfg_denah['rumah']['segmen_dinding'])} segmen dinding, "
            f"{len(cfg_denah['rumah']['zona_lantai'])} ruangan, "
            f"{len(cfg_denah['rumah']['furnitur'])} furnitur) berhasil dibangun di koleksi 'RumahIndoor'."
        )

    return cfg_denah

if __name__ == "__main__":
    out_path = os.environ.get("OUTPUT_DENAH_JSON", "config_denah.json")
    jalankan_konversi_ascii_ke_3d(DENAH_ASCII, output_json_path=out_path if not BLENDER_AVAILABLE else None)
