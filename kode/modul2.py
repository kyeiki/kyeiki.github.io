#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODUL 2 KOMPUTER GRAFIK (V3) - 3D TRANSFORMATION, HIERARCHY, TEXTURE & LEGO APP
File: modul2_transform_texture_lego.py (Kompatibel Blender 4.3)

Fokus Materi 2:
  1. Transform3DEngine  : Implementasi eksplisit Matriks Transformasi Homogen 4x4
                          (Translasi T, Rotasi Euler Rx/Ry/Rz, Skala S, Shear)
                          serta Hierarki Scene Graph (Parent-Child Matrix).
  2. TextureFactory     : Pembuatan Shader Node Tree (UV Mapping + Procedural
                          Brick, Checker, Wood Wave, Noise Bump, & Image Texture).
  3. LegoBrickBuilder   : Perakitan objek modular bergaya LEGO (Studs + Bricks)
                          menggunakan komposisi transformasi lokal-ke-dunia.
  4. LegoAppPanel (UI)  : Mini-App di Sidebar 3D Viewport Blender (Tekan 'N' ->
                          tab 'LegoApp M2') untuk manipulasi Transformasi 3D,
                          susun balok LEGO interaktif, dan ganti tekstur real-time.
================================================================================
"""

import json
import math
import os
import re
from collections import deque

# ==============================================================================
# BAGIAN 1: KONFIGURASI DENAH ASCII & PARAMETER SKALA
# ==============================================================================
SKALA_X_METER_PER_KARAKTER = 0.5
SKALA_Y_METER_PER_KARAKTER = 0.5
TINGGI_DINDING_DEFAULT     = 3.0
TEBAL_DINDING_DEFAULT      = 0.15

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

# ==============================================================================
# BAGIAN 2: PALET MATERIAL & KONFIGURASI TEKSTUR PROSEDURAL (MATERI 2)
# Mendukung tipe tekstur: "NONE", "BRICK", "CHECKER", "WOOD", "NOISE", "LEGO_PLASTIC"
# ==============================================================================
DEFAULT_CONFIG_ASSETS = {
    "palet": {
        "dinding_eksterior": {
            "rgba": [0.88, 0.84, 0.78, 1.0], "roughness": 0.85,
            "tex_type": "BRICK", "color2": [0.65, 0.58, 0.50, 1.0],
            "uv_scale": [4.0, 4.0, 4.0], "bump_strength": 0.25
        },
        "dinding_interior": {
            "rgba": [0.90, 0.91, 0.93, 1.0], "roughness": 0.75,
            "tex_type": "NOISE", "uv_scale": [8.0, 8.0, 8.0], "bump_strength": 0.08
        },
        "dinding_core": {
            "rgba": [0.72, 0.76, 0.80, 1.0], "roughness": 0.65,
            "tex_type": "BRICK", "color2": [0.55, 0.58, 0.62, 1.0],
            "uv_scale": [3.0, 3.0, 3.0], "bump_strength": 0.20
        },
        "kusen_kayu": {
            "rgba": [0.42, 0.25, 0.12, 1.0], "roughness": 0.55,
            "tex_type": "WOOD", "color2": [0.25, 0.14, 0.06, 1.0],
            "uv_scale": [6.0, 6.0, 6.0], "bump_strength": 0.12
        },
        "kusen_aluminium": {"rgba": [0.22, 0.25, 0.28, 1.0], "roughness": 0.25, "metallic": 0.8},
        "kaca_jendela": {
            "rgba": [0.65, 0.85, 0.95, 1.0], "roughness": 0.10,
            "emission": [0.4, 0.6, 0.7, 1.0], "emission_strength": 0.20
        },
        "lantai_workstation": {
            "rgba": [0.85, 0.82, 0.75, 1.0], "roughness": 0.45,
            "tex_type": "CHECKER", "color2": [0.72, 0.68, 0.60, 1.0],
            "uv_scale": [12.0, 12.0, 1.0], "bump_strength": 0.05
        },
        "lantai_koridor": {
            "rgba": [0.78, 0.80, 0.83, 1.0], "roughness": 0.35,
            "tex_type": "CHECKER", "color2": [0.60, 0.63, 0.68, 1.0],
            "uv_scale": [8.0, 8.0, 1.0], "bump_strength": 0.05
        },
        "lantai_ruang_r": {
            "rgba": [0.68, 0.48, 0.30, 1.0], "roughness": 0.50,
            "tex_type": "WOOD", "color2": [0.48, 0.32, 0.18, 1.0],
            "uv_scale": [5.0, 5.0, 5.0], "bump_strength": 0.10
        },
        "lantai_arsip": {
            "rgba": [0.58, 0.60, 0.62, 1.0], "roughness": 0.80,
            "tex_type": "NOISE", "uv_scale": [10.0, 10.0, 1.0], "bump_strength": 0.15
        },
        "lantai_toilet": {
            "rgba": [0.82, 0.94, 0.96, 1.0], "roughness": 0.25,
            "tex_type": "CHECKER", "color2": [0.62, 0.82, 0.86, 1.0],
            "uv_scale": [16.0, 16.0, 1.0], "bump_strength": 0.08
        },
        "lantai_pantry": {
            "rgba": [0.90, 0.84, 0.72, 1.0], "roughness": 0.40,
            "tex_type": "CHECKER", "color2": [0.76, 0.66, 0.52, 1.0],
            "uv_scale": [10.0, 10.0, 1.0], "bump_strength": 0.06
        },
        "lantai_teknis": {"rgba": [0.42, 0.45, 0.48, 1.0], "roughness": 0.85, "tex_type": "NOISE"},
        "lantai_tangga": {"rgba": [0.52, 0.50, 0.48, 1.0], "roughness": 0.80},
        "lantai_lift":   {"rgba": [0.30, 0.32, 0.35, 1.0], "roughness": 0.35, "metallic": 0.6},
        "kayu_meja": {
            "rgba": [0.76, 0.55, 0.34, 1.0], "roughness": 0.45,
            "tex_type": "WOOD", "color2": [0.55, 0.38, 0.20, 1.0],
            "uv_scale": [4.0, 4.0, 4.0], "bump_strength": 0.08
        },
        "kayu_gelap": {
            "rgba": [0.32, 0.20, 0.11, 1.0], "roughness": 0.50,
            "tex_type": "WOOD", "color2": [0.18, 0.10, 0.05, 1.0],
            "uv_scale": [5.0, 5.0, 5.0], "bump_strength": 0.10
        },
        "partisi_kubikel": {"rgba": [0.46, 0.56, 0.68, 1.0], "roughness": 0.80, "tex_type": "NOISE"},
        "kursi_kantor":    {"rgba": [0.18, 0.20, 0.24, 1.0], "roughness": 0.65},
        "kain_sofa":       {"rgba": [0.26, 0.42, 0.58, 1.0], "roughness": 0.85, "tex_type": "NOISE"},
        "kain_kasur":      {"rgba": [0.92, 0.90, 0.86, 1.0], "roughness": 0.80},
        "selimut_biru":    {"rgba": [0.30, 0.50, 0.72, 1.0], "roughness": 0.85},
        "logam_abu":       {"rgba": [0.65, 0.68, 0.72, 1.0], "roughness": 0.30, "metallic": 0.75},
        "logam_lift":      {"rgba": [0.80, 0.82, 0.85, 1.0], "roughness": 0.20, "metallic": 0.85},
        "keramik_putih":   {"rgba": [0.96, 0.97, 0.98, 1.0], "roughness": 0.15},
        "layar_monitor": {
            "rgba": [0.08, 0.12, 0.18, 1.0], "roughness": 0.15,
            "emission": [0.15, 0.50, 0.95, 1.0], "emission_strength": 0.8
        },
        "hijau_daun":      {"rgba": [0.22, 0.58, 0.26, 1.0], "roughness": 0.65},
        "pot_terakota":    {"rgba": [0.72, 0.38, 0.22, 1.0], "roughness": 0.75, "tex_type": "NOISE"},
        "panel_listrik":   {"rgba": [0.25, 0.32, 0.38, 1.0], "roughness": 0.45, "metallic": 0.5},
        "lampu_indikator": {
            "rgba": [0.10, 0.90, 0.30, 1.0], "roughness": 0.20,
            "emission": [0.10, 0.95, 0.30, 1.0], "emission_strength": 2.5
        },
        "mesin_hvac":      {"rgba": [0.35, 0.52, 0.65, 1.0], "roughness": 0.40, "metallic": 0.5},
        "kardus_arsip":    {"rgba": [0.78, 0.64, 0.44, 1.0], "roughness": 0.85},
        "rail_tangga":     {"rgba": [0.85, 0.22, 0.18, 1.0], "roughness": 0.35},
        "teks_label":      {"rgba": [0.12, 0.14, 0.18, 1.0], "roughness": 0.50},
        # Material Khusus Balok LEGO (Materi 2)
        "lego_merah":      {"rgba": [0.85, 0.12, 0.12, 1.0], "roughness": 0.20, "tex_type": "LEGO_PLASTIC"},
        "lego_kuning":     {"rgba": [0.95, 0.78, 0.08, 1.0], "roughness": 0.20, "tex_type": "LEGO_PLASTIC"},
        "lego_biru":       {"rgba": [0.10, 0.38, 0.82, 1.0], "roughness": 0.20, "tex_type": "LEGO_PLASTIC"},
        "lego_hijau":      {"rgba": [0.12, 0.68, 0.28, 1.0], "roughness": 0.20, "tex_type": "LEGO_PLASTIC"}
    }
}

# ==============================================================================
# BAGIAN 3: KELAS AsciiDenahParser (Tetap kompatibel dengan Modul 1)
# ==============================================================================
class AsciiDenahParser:
    def __init__(self, scale_x=0.5, scale_y=0.5, tinggi_dinding=3.0, tebal_dinding=0.15):
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.tinggi_dinding = float(tinggi_dinding)
        self.tebal_dinding = float(tebal_dinding)

    @staticmethod
    def _normalisasi_baris(ascii_text):
        raw_lines = [l.rstrip("\r\n") for l in ascii_text.strip().splitlines() if l.strip()]
        if not raw_lines:
            raise ValueError("Teks ASCII kosong!")
        max_len = max(len(l) for l in raw_lines)
        grid = []
        for l in raw_lines:
            if len(l) < max_len and "---" in l:
                diff = max_len - len(l)
                runs = [(m.end() - m.start(), m.start(), m.end()) for m in re.finditer(r"-+", l)]
                runs.sort(reverse=True)
                _, start_idx, _ = runs[0]
                l = l[:start_idx] + ("-" * diff) + l[start_idx:]
            grid.append(l.ljust(max_len))
        return grid

    @staticmethod
    def _is_horizontal_wall_char(grid, r, c):
        W = len(grid[0])
        ch = grid[r][c]
        if ch == "+":
            return True
        if ch == "-":
            left = grid[r][c - 1] if c > 0 else " "
            right = grid[r][c + 1] if c + 1 < W else " "
            return (left in ("+", "-")) or (right in ("+", "-"))
        return False

    @staticmethod
    def _is_vertical_wall_char(grid, r, c):
        return grid[r][c] in ("+", "|")

    def _is_any_wall(self, grid, r, c):
        ch = grid[r][c]
        if ch in ("+", "|"):
            return True
        if ch == "-":
            return self._is_horizontal_wall_char(grid, r, c)
        return False

    def _rc_to_xy(self, r, c, max_r):
        x = round(c * self.scale_x, 3)
        y = round((max_r - r) * self.scale_y, 3)
        return x, y

    def _ekstrak_ruangan(self, grid):
        H, W = len(grid), len(grid[0])
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
                            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc] and not self._is_any_wall(grid, nr, nc):
                                visited[nr][nc] = True
                                q.append((nr, nc))

                    min_r, max_r_cell = min(p[0] for p in cells), max(p[0] for p in cells)
                    min_c, max_c_cell = min(p[1] for p in cells), max(p[1] for p in cells)
                    r1, r2 = max(0, min_r - 1), min(max_r, max_r_cell + 1)
                    c1, c2 = max(0, min_c - 1), min(W - 1, max_c_cell + 1)

                    cell_set = set(cells)
                    row_texts = []
                    for rr in range(min_r, max_r_cell + 1):
                        s = "".join(grid[rr][cc] for cc in range(min_c, max_c_cell + 1) if (rr, cc) in cell_set)
                        s_clean = " ".join(s.split())
                        if s_clean:
                            row_texts.append(s_clean)
                    raw_label = " ".join(row_texts)
                    norm_label = raw_label
                    if raw_label.replace(" ", "") == "R.ARSIP":
                        norm_label = "R. ARSIP"
                    elif raw_label.replace(" ", "") == "CORIDOR":
                        norm_label = "CORIDOR"

                    x1, y2 = self._rc_to_xy(r1, c1, max_r)
                    x2, y1 = self._rc_to_xy(r2, c2, max_r)
                    rooms.append({
                        "id": len(rooms), "r1": r1, "r2": r2, "c1": c1, "c2": c2,
                        "x1": min(x1, x2), "x2": max(x1, x2), "y1": min(y1, y2), "y2": max(y1, y2),
                        "area_cells": len(cells), "raw_label": raw_label, "label": norm_label,
                    })
        return rooms

    def _ekstrak_segmen_dinding(self, grid):
        H, W = len(grid), len(grid[0])
        max_r = H - 1
        horiz_segments, vert_segments = [], []

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
                        mat = "dinding_eksterior" if r in (0, max_r) else ("dinding_core" if 11 <= r <= 21 else "dinding_interior")
                        horiz_segments.append({
                            "nama": f"Dinding_H_R{r:02d}_C{start_c:02d}_{end_c:02d}",
                            "orientasi": "H", "r": r, "c1": start_c, "c2": end_c,
                            "dari": [x1, y], "ke": [x2, y], "material": mat, "celah": [],
                        })
                else:
                    c += 1

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
                        if start_r > 0 and self._is_horizontal_wall_char(grid, start_r - 1, c):
                            start_r -= 1
                        if end_r + 1 < H and self._is_horizontal_wall_char(grid, end_r + 1, c):
                            end_r += 1
                        if end_r == start_r:
                            end_r = min(max_r, start_r + 1)
                        x, y2 = self._rc_to_xy(start_r, c, max_r)
                        _, y1 = self._rc_to_xy(end_r, c, max_r)
                        mat = "dinding_eksterior" if c in (0, W - 1) else ("dinding_core" if (12 <= c <= 58 and start_r >= 11 and end_r <= 21) else "dinding_interior")
                        vert_segments.append({
                            "nama": f"Dinding_V_C{c:02d}_R{start_r:02d}_{end_r:02d}",
                            "orientasi": "V", "c": c, "r1": start_r, "r2": end_r,
                            "dari": [x, min(y1, y2)], "ke": [x, max(y1, y2)], "material": mat, "celah": [],
                        })
                else:
                    r += 1
        return horiz_segments, vert_segments

    @staticmethod
    def _tambah_celah_ke_segmen(seg_list, orientasi, garis_idx, pos_tengah, lebar_celah, tinggi_bukaan=2.1, ambang_bawah=0.0):
        half = round(lebar_celah / 2.0, 3)
        c_dari, c_ke = round(pos_tengah - half, 3), round(pos_tengah + half, 3)
        for seg in seg_list:
            if orientasi == "H" and seg["r"] == garis_idx:
                s_min, s_max = min(seg["dari"][0], seg["ke"][0]), max(seg["dari"][0], seg["ke"][0])
            elif orientasi == "V" and seg["c"] == garis_idx:
                s_min, s_max = min(seg["dari"][1], seg["ke"][1]), max(seg["dari"][1], seg["ke"][1])
            else:
                continue
            if c_dari >= s_min + 0.05 and c_ke <= s_max - 0.05:
                if not any(not (c_ke <= ex["dari"] or c_dari >= ex["ke"]) for ex in seg["celah"]):
                    seg["celah"].append({"dari": c_dari, "ke": c_ke, "tinggi_bukaan": round(tinggi_bukaan, 2), "ambang_bawah": round(ambang_bawah, 2)})
                return True
        return False

    def _injeksi_pintu_dan_jendela_otomatis(self, rooms, horiz_segments, vert_segments, max_r, max_c):
        for rm in rooms:
            lbl = rm["label"].upper()
            r1, r2, c1, c2 = rm["r1"], rm["r2"], rm["c1"], rm["c2"]
            cx, cy = round((rm["x1"] + rm["x2"]) / 2.0, 2), round((rm["y1"] + rm["y2"]) / 2.0, 2)
            width_x, height_y = rm["x2"] - rm["x1"], rm["y2"] - rm["y1"]
            lebar_pintu = max(0.7, min(0.9, round(min(width_x, height_y) * 0.45, 2)))

            if lbl == "[R]" and r1 == 0:
                self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, lebar_pintu, 2.1, 0.0)
                self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, min(1.2, width_x * 0.5), 1.0, 1.0)
            elif lbl == "R" and r2 == max_r:
                self._tambah_celah_ke_segmen(horiz_segments, "H", r1, cx, lebar_pintu, 2.1, 0.0)
                self._tambah_celah_ke_segmen(horiz_segments, "H", r2, cx, min(1.0, width_x * 0.5), 1.0, 1.0)
            elif "ARSIP" in lbl:
                self._tambah_celah_ke_segmen(vert_segments, "V", c2 if c1 == 0 else c1, cy, 1.0, 2.1, 0.0)
                self._tambah_celah_ke_segmen(vert_segments, "V", c1 if c1 == 0 else c2, cy, 1.6, 1.0, 1.1)
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
                self._tambah_celah_ke_segmen(vert_segments, "V", c1 if c1 == 38 else c2, cy, 0.85, 2.1, 0.0)
            elif "PANEL" in lbl:
                self._tambah_celah_ke_segmen(vert_segments, "V", c1, cy, 0.8, 2.1, 0.0)

    def _tentukan_material_lantai(self, label):
        lbl = label.upper()
        if "WORK STATION" in lbl or "TAMU" in lbl: return "lantai_workstation"
        if "CORIDOR" in lbl or lbl == "": return "lantai_koridor"
        if lbl in ("[R]", "R") or "KAMAR" in lbl: return "lantai_ruang_r"
        if "ARSIP" in lbl: return "lantai_arsip"
        if "TOILET" in lbl or "MANDI" in lbl: return "lantai_toilet"
        if "PANTRY" in lbl or "DAPUR" in lbl: return "lantai_pantry"
        if "TANGGA" in lbl: return "lantai_tangga"
        if "LIFT" in lbl: return "lantai_lift"
        return "lantai_teknis"

    def _bangun_furnitur_dan_label_otomatis(self, rooms):
        furnitur, label_ruang = [], []
        for rm in rooms:
            lbl = rm["label"].upper()
            x1, x2, y1, y2 = rm["x1"], rm["x2"], rm["y1"], rm["y2"]
            cx, cy = round((x1 + x2) / 2.0, 2), round((y1 + y2) / 2.0, 2)
            wx, wy = round(x2 - x1, 2), round(y2 - y1, 2)

            if rm["label"]:
                label_ruang.append({
                    "teks": rm["label"], "di": [cx, cy],
                    "ukuran": 0.45 if wx >= 6.0 else (0.28 if wx >= 2.5 else 0.22),
                })

            if "WORK STATION" in lbl:
                is_utara = "UTARA" in lbl
                y_base = round(y1 + 1.8, 2) if is_utara else round(y2 - 1.8, 2)
                y_row2 = round(y1 + 3.4, 2) if is_utara else round(y2 - 3.4, 2)
                for idx, x_pos in enumerate([5.5, 9.0, 12.5, 21.5, 25.0, 28.5]):
                    if x1 + 1.0 < x_pos < x2 - 1.0:
                        # Menambahkan atribut transformasi 3D eksplisit (scale & rotasi)
                        furnitur.append({
                            "nama": f"Kubikel_{'U' if is_utara else 'S'}_R1_{idx+1}",
                            "type": "meja_kerja", "di": [x_pos, y_base],
                            "rot": [0.0, 0.0, 0.0 if is_utara else round(math.pi, 4)],
                            "scale": [1.0, 1.0, 1.0],
                        })
                        furnitur.append({
                            "nama": f"Kubikel_{'U' if is_utara else 'S'}_R2_{idx+1}",
                            "type": "meja_kerja", "di": [x_pos, y_row2],
                            "rot": [0.0, 0.0, round(math.pi, 4) if is_utara else 0.0],
                            "scale": [1.0, 1.0, 1.0],
                        })
                # Tambahkan Monumen LEGO Modular di tengah Workstation (Materi 2)
                furnitur.append({
                    "nama": f"MenaraLego_{'Utara' if is_utara else 'Selatan'}",
                    "type": "menara_lego",
                    "di": [cx, round((y_base + y_row2) / 2.0, 2)],
                    "rot": [0.0, 0.0, round(math.pi / 4.0, 4)],
                    "scale": [1.1, 1.1, 1.1],
                })

            elif lbl in ("[R]", "R"):
                furnitur.append({
                    "nama": f"SetRuangR_{rm['id']}", "type": "set_ruang_r",
                    "di": [cx, cy], "rot": [0.0, 0.0, round(math.pi, 4) if lbl == "[R]" else 0.0],
                })
            elif "ARSIP" in lbl:
                for idx, ry in enumerate([round(y1 + 1.4, 2), round(cy, 2), round(y2 - 1.4, 2)]):
                    furnitur.append({
                        "nama": f"RakArsip_{rm['id']}_{idx+1}", "type": "rak_arsip",
                        "di": [cx, ry], "rot": [0.0, 0.0, round(math.pi / 2.0, 4)],
                    })
            elif "TOILET" in lbl:
                furnitur.append({"nama": f"Wastafel_{rm['id']}", "type": "wastafel", "di": [cx, round(y1 + 0.4, 2)]})
            elif "PANTRY" in lbl:
                furnitur.append({"nama": f"MejaPantry_{rm['id']}", "type": "meja_pantry", "di": [cx, round(y1 + 0.45, 2)]})
            elif "TANGGA" in lbl:
                furnitur.append({
                    "nama": f"TanggaDarurat_{rm['id']}", "type": "tangga_darurat",
                    "di": [cx, cy], "panjang": round(max(2.5, wx - 1.2), 2), "lebar": round(max(0.8, wy - 0.3), 2),
                })
        return furnitur, label_ruang

    def parse_to_dict(self, ascii_text):
        grid = self._normalisasi_baris(ascii_text)
        H, W = len(grid), len(grid[0])
        max_r, max_c = H - 1, W - 1
        rooms = self._ekstrak_ruangan(grid)
        horiz_segments, vert_segments = self._ekstrak_segmen_dinding(grid)
        self._injeksi_pintu_dan_jendela_otomatis(rooms, horiz_segments, vert_segments, max_r, max_c)

        segmen_dinding = [
            {
                "nama": s["nama"], "dari": s["dari"], "ke": s["ke"],
                "material": s["material"], "celah": sorted(s["celah"], key=lambda item: item["dari"]),
            }
            for s in horiz_segments + vert_segments
        ]
        zona_lantai = [
            {
                "nama": f"Lantai_{rm['id']:02d}_{re.sub(r'[^A-Za-z0-9]+', '_', rm['label'] or 'Koridor').strip('_')}",
                "min_xy": [rm["x1"], rm["y1"]], "max_xy": [rm["x2"], rm["y2"]],
                "material": self._tentukan_material_lantai(rm["label"]),
            }
            for rm in rooms
        ]
        furnitur, label_ruang = self._bangun_furnitur_dan_label_otomatis(rooms)
        return {
            "meta": {"modul": "Modul 2 - Transformasi 3D, Hierarki LEGO & Texture Shader"},
            "rumah": {
                "grid": [round(max_c * self.scale_x, 2), round(max_r * self.scale_y, 2)],
                "tinggi_dinding": self.tinggi_dinding,
                "tebal_dinding": self.tebal_dinding,
                "segmen_dinding": segmen_dinding,
                "zona_lantai": zona_lantai,
                "furnitur": furnitur,
                "label_ruang": label_ruang,
            },
        }

# ==============================================================================
# BAGIAN 4: INTI MATERI 2 - ENGINE TRANSFORMASI 3D, SHADER TEXTURE, & LEGO APP
# ==============================================================================
try:
    import bpy
    import bmesh
    from mathutils import Matrix, Vector, Euler
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

if BLENDER_AVAILABLE:

    # --------------------------------------------------------------------------
    # 1. Transform3DEngine: Matriks Homogen 4x4 Eksplisit & Hierarki Parent-Child
    # --------------------------------------------------------------------------
    class Transform3DEngine:
        """
        MATERI 2 - TRANSFORMASI 3D:
        Mengimplementasikan rumus aljabar linear matriks transformasi homogen 4x4:
          M = T(tx, ty, tz) @ Rz(gamma) @ Ry(beta) @ Rx(alpha) @ S(sx, sy, sz) @ Shear
        Semua transformasi objek dihitung dengan perkalian matriks 4x4 sebelum
        diterapkan ke obj.matrix_world atau obj.matrix_local.
        """

        @staticmethod
        def matriks_translasi(tx, ty, tz):
            return Matrix((
                (1.0, 0.0, 0.0, float(tx)),
                (0.0, 1.0, 0.0, float(ty)),
                (0.0, 0.0, 1.0, float(tz)),
                (0.0, 0.0, 0.0, 1.0),
            ))

        @staticmethod
        def matriks_skala(sx, sy, sz):
            return Matrix((
                (float(sx), 0.0,       0.0,       0.0),
                (0.0,       float(sy), 0.0,       0.0),
                (0.0,       0.0,       float(sz), 0.0),
                (0.0,       0.0,       0.0,       1.0),
            ))

        @staticmethod
        def matriks_rotasi_x(rad):
            c, s = math.cos(rad), math.sin(rad)
            return Matrix((
                (1.0, 0.0, 0.0, 0.0),
                (0.0, c,  -s,   0.0),
                (0.0, s,   c,   0.0),
                (0.0, 0.0, 0.0, 1.0),
            ))

        @staticmethod
        def matriks_rotasi_y(rad):
            c, s = math.cos(rad), math.sin(rad)
            return Matrix((
                ( c,  0.0, s,   0.0),
                (0.0, 1.0, 0.0, 0.0),
                (-s,  0.0, c,   0.0),
                (0.0, 0.0, 0.0, 1.0),
            ))

        @staticmethod
        def matriks_rotasi_z(rad):
            c, s = math.cos(rad), math.sin(rad)
            return Matrix((
                (c,  -s,   0.0, 0.0),
                (s,   c,   0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
            ))

        @staticmethod
        def matriks_shear_xy(sh_x=0.0, sh_y=0.0):
            """Matriks Geser (Shearing) pada sumbu X/Y terhadap Z."""
            return Matrix((
                (1.0, 0.0, float(sh_x), 0.0),
                (0.0, 1.0, float(sh_y), 0.0),
                (0.0, 0.0, 1.0,         0.0),
                (0.0, 0.0, 0.0,         1.0),
            ))

        @classmethod
        def komposisi_trs(cls, lokasi=(0.0, 0.0, 0.0), rotasi_euler=(0.0, 0.0, 0.0), skala=(1.0, 1.0, 1.0), shear=(0.0, 0.0)):
            """Menghasilkan matriks komposit M = T @ Rz @ Ry @ Rx @ Shear @ S."""
            T = cls.matriks_translasi(*lokasi)
            Rx = cls.matriks_rotasi_x(rotasi_euler[0])
            Ry = cls.matriks_rotasi_y(rotasi_euler[1])
            Rz = cls.matriks_rotasi_z(rotasi_euler[2])
            Sh = cls.matriks_shear_xy(shear[0], shear[1])
            S = cls.matriks_skala(*skala)
            return T @ Rz @ Ry @ Rx @ Sh @ S

        @classmethod
        def terapkan_matriks(cls, obj, lokasi=(0.0, 0.0, 0.0), rotasi_euler=(0.0, 0.0, 0.0), skala=(1.0, 1.0, 1.0), parent=None):
            """
            Menerapkan matriks transformasi 4x4 ke objek.
            Jika memiliki parent (Hierarki LEGO), maka transformasi dihitung
            relatif terhadap koordinat lokal parent-nya (M_world = M_parent @ M_local).
            """
            M_lokal = cls.komposisi_trs(lokasi, rotasi_euler, skala)
            if parent is not None:
                obj.parent = parent
                obj.matrix_parent_inverse = Matrix.Identity(4)
                obj.matrix_local = M_lokal
            else:
                obj.matrix_world = M_lokal

    # --------------------------------------------------------------------------
    # 2. SceneManager: Lifecycle Scene & UV Unwrapping Otomatis
    # --------------------------------------------------------------------------
    class SceneManager:
        @staticmethod
        def bersihkan_scene():
            if bpy.context.active_object and bpy.context.active_object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.object.delete()
            for block_list in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.textures, bpy.data.images):
                for item in list(block_list):
                    block_list.remove(item)

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
        def generate_box_uv(obj):
            """Memastikan mesh memiliki UV Map proporsional (Cube Projection) untuk tekstur."""
            if not obj or obj.type != "MESH":
                return
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()
            for face in bm.faces:
                n = face.normal
                for loop in face.loops:
                    co = loop.vert.co
                    if abs(n.z) > 0.5:
                        loop[uv_layer].uv = (co.x, co.y)
                    elif abs(n.x) > 0.5:
                        loop[uv_layer].uv = (co.y, co.z)
                    else:
                        loop[uv_layer].uv = (co.x, co.z)
            bm.to_mesh(obj.data)
            bm.free()

    # --------------------------------------------------------------------------
    # 3. TextureMaterialFactory: Procedural Shader Nodes & Image Texture (Materi 2)
    # --------------------------------------------------------------------------
    class TextureMaterialFactory:
        """
        MATERI 2 - TEXTURE MAPPING & SHADING:
        Membangun jaringan Node Shader di Blender 4.3:
          [TexCoord] -> [Mapping (UV Scale/Rot/Trans)] -> [Procedural/Image Texture]
                                                       -> [Bump Node] -> [Principled BSDF]
        """

        @staticmethod
        def buat_tekstur_citra_checker(nama_img="Tekstur_Lego_Checker", ukuran=256):
            """Membuat Image Texture piksel secara prosedural di memori Blender (tanpa file eksternal)."""
            if nama_img in bpy.data.images:
                return bpy.data.images[nama_img]
            img = bpy.data.images.new(nama_img, width=ukuran, height=ukuran)
            pixels = [0.0] * (ukuran * ukuran * 4)
            for y in range(ukuran):
                for x in range(ukuran):
                    idx = (y * ukuran + x) * 4
                    kotak = ((x // 32) + (y // 32)) % 2 == 0
                    border = (x % 32 < 2) or (y % 32 < 2)
                    if border:
                        r, g, b = 0.15, 0.18, 0.22
                    elif kotak:
                        r, g, b = 0.92, 0.78, 0.20
                    else:
                        r, g, b = 0.18, 0.48, 0.85
                    pixels[idx : idx + 4] = [r, g, b, 1.0]
            img.pixels = pixels
            img.pack()
            return img

        @classmethod
        def get_or_create(cls, nama_mat, spec):
            if nama_mat in bpy.data.materials:
                return bpy.data.materials[nama_mat]

            mat = bpy.data.materials.new(name=nama_mat)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            bsdf = nodes.get("Principled BSDF")

            rgba = tuple(spec.get("rgba", [0.8, 0.8, 0.8, 1.0]))
            roughness = float(spec.get("roughness", 0.5))
            metallic = float(spec.get("metallic", 0.0))
            tex_type = spec.get("tex_type", "NONE").upper()
            uv_scale = tuple(spec.get("uv_scale", [4.0, 4.0, 4.0]))
            bump_strength = float(spec.get("bump_strength", 0.1))

            if bsdf:
                bsdf.inputs["Base Color"].default_value = rgba
                bsdf.inputs["Roughness"].default_value = roughness
                if "Metallic" in bsdf.inputs:
                    bsdf.inputs["Metallic"].default_value = metallic

                if spec.get("emission") and spec.get("emission_strength", 0) > 0:
                    em_in = bsdf.inputs.get("Emission Color") or bsdf.inputs.get("Emission")
                    if em_in:
                        em_in.default_value = tuple(spec["emission"])
                    if "Emission Strength" in bsdf.inputs:
                        bsdf.inputs["Emission Strength"].default_value = float(spec["emission_strength"])

            if tex_type != "NONE" and bsdf:
                # Buat Node Texture Coordinate & Mapping (Transformasi UV 2D/3D)
                coord_node = nodes.new(type="ShaderNodeTexCoord")
                coord_node.location = (-850, 200)

                map_node = nodes.new(type="ShaderNodeMapping")
                map_node.name = "UV_Mapping"
                map_node.location = (-650, 200)
                map_node.inputs["Scale"].default_value = uv_scale
                links.new(coord_node.outputs["Generated"], map_node.inputs["Vector"])

                bump_node = nodes.new(type="ShaderNodeBump")
                bump_node.location = (-200, -120)
                bump_node.inputs["Strength"].default_value = bump_strength

                if tex_type == "BRICK":
                    tex_node = nodes.new(type="ShaderNodeTexBrick")
                    tex_node.location = (-420, 200)
                    tex_node.inputs["Color1"].default_value = rgba
                    tex_node.inputs["Color2"].default_value = tuple(spec.get("color2", [0.6, 0.5, 0.4, 1.0]))
                    tex_node.inputs["Mortar"].default_value = (0.35, 0.35, 0.35, 1.0)
                    tex_node.inputs["Mortar Size"].default_value = 0.025
                    links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
                    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
                    links.new(tex_node.outputs["Fac"], bump_node.inputs["Height"])
                    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type == "CHECKER":
                    tex_node = nodes.new(type="ShaderNodeTexChecker")
                    tex_node.location = (-420, 200)
                    tex_node.inputs["Color1"].default_value = rgba
                    tex_node.inputs["Color2"].default_value = tuple(spec.get("color2", [0.5, 0.5, 0.5, 1.0]))
                    tex_node.inputs["Scale"].default_value = 1.0
                    links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
                    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
                    links.new(tex_node.outputs["Fac"], bump_node.inputs["Height"])
                    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type == "WOOD":
                    tex_node = nodes.new(type="ShaderNodeTexWave")
                    tex_node.location = (-450, 200)
                    tex_node.wave_type = "BANDS"
                    tex_node.inputs["Scale"].default_value = 2.5
                    tex_node.inputs["Distortion"].default_value = 4.5
                    tex_node.inputs["Detail"].default_value = 3.0

                    mix_node = nodes.new(type="ShaderNodeMix")
                    mix_node.data_type = "RGBA"
                    mix_node.location = (-230, 220)
                    mix_node.inputs["A"].default_value = rgba
                    mix_node.inputs["B"].default_value = tuple(spec.get("color2", [0.35, 0.20, 0.10, 1.0]))

                    links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
                    links.new(tex_node.outputs["Fac"], mix_node.inputs["Factor"])
                    links.new(mix_node.outputs["Result"], bsdf.inputs["Base Color"])
                    links.new(tex_node.outputs["Fac"], bump_node.inputs["Height"])
                    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type in ("NOISE", "LEGO_PLASTIC"):
                    tex_node = nodes.new(type="ShaderNodeTexNoise")
                    tex_node.location = (-420, 100)
                    tex_node.inputs["Scale"].default_value = 25.0 if tex_type == "LEGO_PLASTIC" else 12.0
                    tex_node.inputs["Detail"].default_value = 4.0
                    bump_node.inputs["Strength"].default_value = 0.03 if tex_type == "LEGO_PLASTIC" else bump_strength
                    links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
                    links.new(tex_node.outputs["Fac"], bump_node.inputs["Height"])
                    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type == "IMAGE_CHECKER":
                    img = cls.buat_tekstur_citra_checker()
                    tex_node = nodes.new(type="ShaderNodeTexImage")
                    tex_node.location = (-420, 200)
                    tex_node.image = img
                    links.new(coord_node.outputs["UV"], map_node.inputs["Vector"])
                    links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
                    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

            mat.diffuse_color = rgba
            return mat

    # --------------------------------------------------------------------------
    # 4. AssetBuilder: Hierarki Modular LEGO (Parent-Child) & Transformasi 3D
    # --------------------------------------------------------------------------
    class AssetBuilder:
        """
        MATERI 2 - MODULAR LEGO BUILDER:
        Alih-alih menggabungkan mesh dengan bpy.ops.object.join() yang merusak
        koordinat lokal tiap sub-bagian, AssetBuilder merakit komponen sebagai
        HIERARKI PARENT-CHILD (Scene Graph) menggunakan Transform3DEngine.
        """

        def __init__(self, mat_factory, palet):
            self.mat_factory = mat_factory
            self.palet = palet
            self._registry = {
                "box": self._bangun_kotak,
                "silinder": self._bangun_silinder,
                "lego_brick": self._bangun_bata_lego,
                "menara_lego": self._bangun_menara_lego,
                "meja_kerja": self._bangun_meja_kerja,
                "set_ruang_r": self._bangun_set_ruang_r,
                "rak_arsip": self._bangun_rak_arsip,
                "wastafel": self._bangun_wastafel,
                "meja_pantry": self._bangun_meja_pantry,
                "tangga_darurat": self._bangun_tangga_darurat,
            }

        def _mat(self, nama_mat):
            if nama_mat not in self.palet:
                return self.mat_factory.get_or_create(nama_mat, {"rgba": [0.8, 0.8, 0.8, 1.0]})
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
            rot = spec.get("rot", [0.0, 0.0, 0.0])
            skala = spec.get("scale", [1.0, 1.0, 1.0])
            shear = spec.get("shear", [0.0, 0.0])
            parent = spec.get("parent", None)

            # Buat kubus satuan (size=1.0), lalu transformasikan menggunakan Matriks 4x4
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
            o = bpy.context.active_object
            o.name = spec.get("name", spec.get("nama", "Kotak"))

            skala_total = (dim[0] * skala[0], dim[1] * skala[1], dim[2] * skala[2])
            M = Transform3DEngine.komposisi_trs(
                lokasi=(di[0], di[1], z),
                rotasi_euler=rot,
                skala=skala_total,
                shear=shear,
            )
            if parent is not None:
                o.parent = parent
                o.matrix_parent_inverse = Matrix.Identity(4)
                o.matrix_local = M
            else:
                o.matrix_world = M

            SceneManager.generate_box_uv(o)
            o.data.materials.append(self._mat(spec["material"]))
            return o

        def _bangun_silinder(self, spec):
            r = spec.get("radius", 0.25)
            t = spec.get("depth", 1.0)
            di = spec.get("di", [0.0, 0.0])
            z = spec.get("z", t / 2.0)
            rot = spec.get("rot", [0.0, 0.0, 0.0])
            skala = spec.get("scale", [1.0, 1.0, 1.0])
            parent = spec.get("parent", None)

            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=(0.0, 0.0, 0.0))
            o = bpy.context.active_object
            o.name = spec.get("name", spec.get("nama", "Silinder"))

            Transform3DEngine.terapkan_matriks(
                o,
                lokasi=(di[0], di[1], z),
                rotasi_euler=rot,
                skala=(r * skala[0], r * skala[1], t * skala[2]),
                parent=parent,
            )
            o.data.materials.append(self._mat(spec["material"]))
            return o

        def _bangun_bata_lego(self, spec):
            """
            Membangun 1 Balok LEGO Modular (Studs X * Studs Y) dengan hierarki Parent-Child.
            Saat balok induk ditranslasikan/dirotasi/diskalakan, seluruh stud di atasnya
            ikut bertransformasi secara otomatis melalui perkalian matriks parent.
            """
            studs_x = int(spec.get("studs_x", 2))
            studs_y = int(spec.get("studs_y", 4))
            unit = float(spec.get("unit_size", 0.25))
            tinggi_bata = float(spec.get("height", 0.30))
            mat_name = spec.get("material", "lego_merah")

            wx, wy = studs_x * unit, studs_y * unit
            di = spec.get("di", [0.0, 0.0])
            z_alas = float(spec.get("z", 0.0))
            rot = spec.get("rot", [0.0, 0.0, 0.0])
            skala = spec.get("scale", [1.0, 1.0, 1.0])

            # Buat Empty sebagai Root Pivot di tengah alas balok LEGO
            root = bpy.data.objects.new(spec.get("nama", "LegoBrick"), None)
            root.empty_display_type = "PLAIN_AXES"
            root.empty_display_size = 0.2
            bpy.context.scene.collection.objects.link(root)

            Transform3DEngine.terapkan_matriks(
                root,
                lokasi=(di[0], di[1], z_alas),
                rotasi_euler=rot,
                skala=skala,
                parent=spec.get("parent", None),
            )

            # Badan utama balok LEGO (anak dari root)
            self._bangun_kotak({
                "name": f"{root.name}_Body",
                "dimensions": [wx * 0.98, wy * 0.98, tinggi_bata],
                "di": [0.0, 0.0],
                "z": tinggi_bata / 2.0,
                "material": mat_name,
                "parent": root,
            })

            # Stud silinder di atas balok LEGO (anak dari root)
            tinggi_stud = unit * 0.22
            radius_stud = unit * 0.30
            start_x = -wx / 2.0 + unit / 2.0
            start_y = -wy / 2.0 + unit / 2.0
            for ix in range(studs_x):
                for iy in range(studs_y):
                    sx = start_x + ix * unit
                    sy = start_y + iy * unit
                    self._bangun_silinder({
                        "name": f"{root.name}_Stud_{ix}_{iy}",
                        "radius": radius_stud,
                        "depth": tinggi_stud,
                        "di": [sx, sy],
                        "z": tinggi_bata + tinggi_stud / 2.0,
                        "material": mat_name,
                        "parent": root,
                    })
            return root

        def _bangun_menara_lego(self, spec):
            """Membangun struktur modular bertumpuk dari beberapa Lego Brick (Hierarchy Demo)."""
            di = spec.get("di", [0.0, 0.0])
            rot = spec.get("rot", [0.0, 0.0, 0.0])
            skala = spec.get("scale", [1.0, 1.0, 1.0])

            root = bpy.data.objects.new(spec.get("nama", "MenaraLego"), None)
            root.empty_display_type = "ARROWS"
            root.empty_display_size = 0.5
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(di[0], di[1], 0.0), rotasi_euler=rot, skala=skala)

            lapis = [
                ("lego_merah",  4, 4, 0.00, 0.0),
                ("lego_kuning", 3, 3, 0.30, math.radians(15)),
                ("lego_biru",   2, 4, 0.60, math.radians(30)),
                ("lego_hijau",  2, 2, 0.90, math.radians(45)),
            ]
            for idx, (warna, sx, sy, z_pos, r_z) in enumerate(lapis):
                self._bangun_bata_lego({
                    "nama": f"{root.name}_Lapis{idx+1}",
                    "studs_x": sx, "studs_y": sy,
                    "unit_size": 0.28, "height": 0.30,
                    "di": [0.0, 0.0], "z": z_pos,
                    "rot": [0.0, 0.0, r_z],
                    "material": warna,
                    "parent": root,
                })
            return root

        def _rakit_hierarki_lokal(self, spec, daftar_komponen):
            """
            Membangun grup furnitur menggunakan Root Empty (Hierarchy Transform)
            sehingga seluruh bagian anak tetap memiliki matriks lokal masing-masing.
            """
            di = spec.get("di", [0.0, 0.0])
            z_root = float(spec.get("z", 0.0))
            rot = spec.get("rot", [0.0, 0.0, 0.0])
            skala = spec.get("scale", [1.0, 1.0, 1.0])

            root = bpy.data.objects.new(spec.get("nama", "GrupLego"), None)
            root.empty_display_type = "PLAIN_AXES"
            root.empty_display_size = 0.35
            bpy.context.scene.collection.objects.link(root)

            Transform3DEngine.terapkan_matriks(
                root,
                lokasi=(di[0], di[1], z_root),
                rotasi_euler=rot,
                skala=skala,
            )

            for idx, komp in enumerate(daftar_komponen):
                k_spec = dict(komp)
                k_spec["name"] = f"{root.name}_part{idx+1}"
                k_spec["parent"] = root
                self.membangun(k_spec)
            return root

        def _bangun_meja_kerja(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.4, 0.7, 0.05], "di": [0.0, 0.0], "z": 0.73, "material": "kayu_meja"},
                {"type": "box", "dimensions": [0.06, 0.66, 0.71], "di": [-0.65, 0.0], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [0.06, 0.66, 0.71], "di": [0.65, 0.0], "z": 0.355, "material": "logam_abu"},
                {"type": "box", "dimensions": [1.42, 0.05, 1.15], "di": [0.0, 0.35], "z": 0.575, "material": "partisi_kubikel"},
                {"type": "box", "dimensions": [0.52, 0.04, 0.32], "di": [0.0, 0.15], "z": 0.98, "material": "layar_monitor"},
                {"type": "box", "dimensions": [0.48, 0.48, 0.07], "di": [0.0, -0.55], "z": 0.46, "material": "kursi_kantor"},
                {"type": "box", "dimensions": [0.46, 0.06, 0.48], "di": [0.0, -0.77], "z": 0.72, "material": "kursi_kantor"},
                {"type": "silinder", "radius": 0.06, "depth": 0.44, "di": [0.0, -0.55], "z": 0.22, "material": "logam_abu"},
            ]
            return self._rakit_hierarki_lokal(spec, komp)

        def _bangun_set_ruang_r(self, spec):
            komp = [
                {"type": "box", "dimensions": [0.95, 0.45, 0.05], "di": [0.0, 0.12], "z": 0.73, "material": "kayu_meja"},
                {"type": "box", "dimensions": [0.38, 0.04, 0.26], "di": [0.0, 0.22], "z": 0.90, "material": "layar_monitor"},
                {"type": "box", "dimensions": [0.40, 0.40, 0.45], "di": [0.0, -0.22], "z": 0.225, "material": "kursi_kantor"},
            ]
            return self._rakit_hierarki_lokal(spec, komp)

        def _bangun_rak_arsip(self, spec):
            komp = []
            for sz in [0.20, 0.75, 1.30, 1.85]:
                komp.append({"type": "box", "dimensions": [1.35, 0.48, 0.04], "di": [0.0, 0.0], "z": sz, "material": "logam_abu"})
                if sz < 1.80:
                    komp.append({"type": "box", "dimensions": [1.10, 0.38, 0.32], "di": [0.0, 0.0], "z": sz + 0.18, "material": "kardus_arsip"})
            return self._rakit_hierarki_lokal(spec, komp)

        def _bangun_wastafel(self, spec):
            komp = [
                {"type": "box", "dimensions": [1.60, 0.52, 0.82], "di": [0.0, 0.0], "z": 0.41, "material": "keramik_putih"},
                {"type": "box", "dimensions": [1.50, 0.04, 0.95], "di": [0.0, -0.24], "z": 1.35, "material": "kaca_jendela"},
            ]
            return self._rakit_hierarki_lokal(spec, komp)

        def _bangun_meja_pantry(self, spec):
            komp = [
                {"type": "box", "dimensions": [2.2, 0.60, 0.85], "di": [0.0, 0.0], "z": 0.425, "material": "kayu_meja"},
                {"type": "box", "dimensions": [2.24, 0.64, 0.05], "di": [0.0, 0.0], "z": 0.875, "material": "keramik_putih"},
            ]
            return self._rakit_hierarki_lokal(spec, komp)

        def _bangun_tangga_darurat(self, spec):
            panjang = spec.get("panjang", 4.0)
            lebar = spec.get("lebar", 1.2)
            jml_anak = 8
            dx, dz = panjang / float(jml_anak), 2.4 / float(jml_anak)
            komp = []
            for i in range(jml_anak):
                x_pos = -panjang / 2.0 + (i + 0.5) * dx
                t_blok = (i + 1) * dz
                komp.append({
                    "type": "box", "dimensions": [dx * 0.96, lebar, t_blok],
                    "di": [x_pos, 0.0], "z": t_blok / 2.0, "material": "lantai_tangga",
                })
            return self._rakit_hierarki_lokal(spec, komp)

    # --------------------------------------------------------------------------
    # 5. DenahBuilder: Membangun Lantai Bertekstur, Dinding Bata & Aset Modular
    # --------------------------------------------------------------------------
    class DenahBuilder:
        def __init__(self, builder, cfg_rumah):
            self.builder = builder
            self.cfg = cfg_rumah
            self.tinggi = float(cfg_rumah.get("tinggi_dinding", 3.0))
            self.tebal = float(cfg_rumah.get("tebal_dinding", 0.15))

        @staticmethod
        def _potong_dengan_celah(a1, a2, celah_list):
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

        def _bangun_dinding(self):
            for seg in self.cfg.get("segmen_dinding", []):
                x1, y1 = float(seg["dari"][0]), float(seg["dari"][1])
                x2, y2 = float(seg["ke"][0]), float(seg["ke"][1])
                horizontal = abs(y1 - y2) < 1e-4
                mat = seg.get("material", "dinding_interior")
                celah_list = seg.get("celah", [])

                a1, a2 = (min(x1, x2), max(x1, x2)) if horizontal else (min(y1, y2), max(y1, y2))
                for idx, (s, e) in enumerate(self._potong_dengan_celah(a1, a2, celah_list)):
                    panjang = e - s
                    tengah = (s + e) / 2.0
                    dim = [panjang, self.tebal, self.tinggi] if horizontal else [self.tebal, panjang, self.tinggi]
                    pos = [tengah, y1] if horizontal else [x1, tengah]
                    self.builder.membangun({
                        "type": "box", "name": f"{seg['nama']}_seg{idx}",
                        "dimensions": dim, "di": pos, "z": self.tinggi / 2.0, "material": mat,
                    })

        def _bangun_lantai(self):
            for z in self.cfg.get("zona_lantai", []):
                x1, y1 = float(z["min_xy"][0]), float(z["min_xy"][1])
                x2, y2 = float(z["max_xy"][0]), float(z["max_xy"][1])
                self.builder.membangun({
                    "type": "box", "name": z["nama"],
                    "dimensions": [abs(x2 - x1), abs(y2 - y1), 0.10],
                    "di": [(x1 + x2) / 2.0, (y1 + y2) / 2.0],
                    "z": -0.05, "material": z.get("material", "lantai_koridor"),
                })

        def _bangun_furnitur(self):
            for f in self.cfg.get("furnitur", []):
                self.builder.membangun(f)

        def bangun_semua(self):
            self._bangun_lantai()
            self._bangun_dinding()
            self._bangun_furnitur()

    # ==========================================================================
    # BAGIAN 5: LEGO BUILDER & 3D TRANSFORM INTERACTIVE APP (SIDEBAR N-PANEL)
    # Menjadikan script ini seperti Aplikasi di dalam Blender!
    # ==========================================================================
    class LegoTransformAppProps(bpy.types.PropertyGroup):
        brick_color: bpy.props.EnumProperty(
            name="Warna LEGO",
            items=[
                ("lego_merah",  "Merah LEGO",  ""),
                ("lego_kuning", "Kuning LEGO", ""),
                ("lego_biru",   "Biru LEGO",   ""),
                ("lego_hijau",  "Hijau LEGO",  ""),
            ],
            default="lego_merah",
        )
        studs_x: bpy.props.IntProperty(name="Stud X", default=2, min=1, max=8)
        studs_y: bpy.props.IntProperty(name="Stud Y", default=4, min=1, max=8)

        # Parameter Transformasi Matriks 3D
        trans_xyz: bpy.props.FloatVectorProperty(name="Translasi (T)", default=(18.0, 9.0, 0.0), subtype="TRANSLATION")
        rot_deg: bpy.props.FloatVectorProperty(name="Rotasi Euler (deg)", default=(0.0, 0.0, 0.0), subtype="XYZ")
        scale_xyz: bpy.props.FloatVectorProperty(name="Skala (S)", default=(1.0, 1.0, 1.0), min=0.1, max=10.0, subtype="XYZ")
        shear_xy: bpy.props.FloatVectorProperty(name="Shear XY", default=(0.0, 0.0), size=2, min=-1.5, max=1.5)

        # Parameter Texture & UV Mapping
        preset_tekstur: bpy.props.EnumProperty(
            name="Preset Tekstur",
            items=[
                ("BRICK",         "Bata Prosedural (Brick + Bump)", ""),
                ("CHECKER",       "Ubin Catur (Checker)",           ""),
                ("WOOD",          "Serat Kayu (Wave Wood)",         ""),
                ("IMAGE_CHECKER", "Image Texture (UV Pixel Map)",   ""),
                ("LEGO_PLASTIC",  "Plastik LEGO Glossy",            ""),
            ],
            default="BRICK",
        )
        uv_scale_val: bpy.props.FloatProperty(name="Skala UV", default=4.0, min=0.2, max=30.0)

    class LEGOAPP_OT_spawn_brick(bpy.types.Operator):
        bl_idname = "legoapp.spawn_brick"
        bl_label = "Tambah Balok LEGO (Matriks 4x4)"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            props = context.scene.lego_app_props
            builder = AssetBuilder(TextureMaterialFactory(), DEFAULT_CONFIG_ASSETS["palet"])
            rot_rad = [math.radians(a) for a in props.rot_deg]
            brick = builder.membangun({
                "type": "lego_brick",
                "nama": f"Lego_{props.studs_x}x{props.studs_y}",
                "studs_x": props.studs_x,
                "studs_y": props.studs_y,
                "unit_size": 0.35,
                "height": 0.40,
                "di": [props.trans_xyz[0], props.trans_xyz[1]],
                "z": props.trans_xyz[2],
                "rot": rot_rad,
                "scale": list(props.scale_xyz),
                "material": props.brick_color,
            })
            context.view_layer.objects.active = brick
            brick.select_set(True)
            self.report({"INFO"}, f"Balok LEGO {brick.name} berhasil dirakit!")
            return {"FINISHED"}

    class LEGOAPP_OT_apply_matrix(bpy.types.Operator):
        bl_idname = "legoapp.apply_matrix"
        bl_label = "Terapkan Matriks 4x4 ke Objek Aktif"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            obj = context.active_object
            if not obj:
                self.report({"WARNING"}, "Pilih objek terlebih dahulu di 3D Viewport!")
                return {"CANCELLED"}
            props = context.scene.lego_app_props
            rot_rad = [math.radians(a) for a in props.rot_deg]
            M = Transform3DEngine.komposisi_trs(
                lokasi=tuple(props.trans_xyz),
                rotasi_euler=rot_rad,
                skala=tuple(props.scale_xyz),
                shear=tuple(props.shear_xy),
            )
            obj.matrix_world = M
            self.report({"INFO"}, f"Matriks 4x4 (T*R*Shear*S) diterapkan ke {obj.name}")
            return {"FINISHED"}

    class LEGOAPP_OT_apply_texture(bpy.types.Operator):
        bl_idname = "legoapp.apply_texture"
        bl_label = "Terapkan Tekstur & Skala UV"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            obj = context.active_object
            if not obj or obj.type != "MESH":
                self.report({"WARNING"}, "Pilih objek MESH (Lantai/Dinding/Bata) terlebih dahulu!")
                return {"CANCELLED"}
            props = context.scene.lego_app_props
            s = props.uv_scale_val
            nama_mat = f"Mat_Custom_{props.preset_tekstur}_{int(s*10)}"
            spec = {
                "rgba": [0.85, 0.78, 0.68, 1.0],
                "color2": [0.35, 0.28, 0.22, 1.0],
                "roughness": 0.35,
                "tex_type": props.preset_tekstur,
                "uv_scale": [s, s, s],
                "bump_strength": 0.20,
            }
            if nama_mat in bpy.data.materials:
                bpy.data.materials.remove(bpy.data.materials[nama_mat])
            mat = TextureMaterialFactory.get_or_create(nama_mat, spec)
            SceneManager.generate_box_uv(obj)
            obj.data.materials.clear()
            obj.data.materials.append(mat)
            self.report({"INFO"}, f"Tekstur {props.preset_tekstur} (UV Scale={s:.1f}) diterapkan ke {obj.name}")
            return {"FINISHED"}

    class LEGOAPP_PT_main_panel(bpy.types.Panel):
        bl_label = "Modul 2: LEGO 3D Transform & Texture"
        bl_idname = "LEGOAPP_PT_main_panel"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "LegoApp M2"

        def draw(self, context):
            layout = self.layout
            props = context.scene.lego_app_props

            box1 = layout.box()
            box1.label(text="1. Generator Balok LEGO Modular", icon="MESH_CUBE")
            box1.prop(props, "brick_color")
            row = box1.row(align=True)
            row.prop(props, "studs_x")
            row.prop(props, "studs_y")
            box1.operator("legoapp.spawn_brick", icon="ADD")

            box2 = layout.box()
            box2.label(text="2. Matriks Transformasi 3D (4x4)", icon="ORIENTATION_GLOBAL")
            box2.prop(props, "trans_xyz")
            box2.prop(props, "rot_deg")
            box2.prop(props, "scale_xyz")
            box2.prop(props, "shear_xy")
            box2.operator("legoapp.apply_matrix", icon="CHECKMARK")

            box3 = layout.box()
            box3.label(text="3. Shader Texture & UV Mapping", icon="MATERIAL")
            box3.prop(props, "preset_tekstur")
            box3.prop(props, "uv_scale_val")
            box3.operator("legoapp.apply_texture", icon="TEXTURE")

    DAFTAR_KELAS_UI = (
        LegoTransformAppProps,
        LEGOAPP_OT_spawn_brick,
        LEGOAPP_OT_apply_matrix,
        LEGOAPP_OT_apply_texture,
        LEGOAPP_PT_main_panel,
    )

    def register_lego_ui():
        for cls in DAFTAR_KELAS_UI:
            try:
                bpy.utils.unregister_class(cls)
            except Exception:
                pass
            bpy.utils.register_class(cls)
        bpy.types.Scene.lego_app_props = bpy.props.PointerProperty(type=LegoTransformAppProps)

# ==============================================================================
# BAGIAN 6: ORKESTRASI UTAMA & PENCAHAYAAN PRATINJAU MATERIAL
# ==============================================================================
def atur_kamera_cahaya_dan_viewport(grid_xy):
    if not BLENDER_AVAILABLE:
        return
    gx, gy = float(grid_xy[0]), float(grid_xy[1])
    cx, cy = gx / 2.0, gy / 2.0

    bpy.ops.object.light_add(type="SUN", location=(cx + 10.0, cy - 12.0, 25.0))
    sun = bpy.context.active_object
    sun.name = "Matahari_Modul2"
    sun.data.energy = 4.0
    sun.rotation_euler = (math.radians(38), math.radians(18), math.radians(-25))

    bpy.ops.object.camera_add(location=(cx, -gy * 0.65, max(gx, gy) * 0.95))
    cam = bpy.context.active_object
    cam.name = "Kamera_Modul2"
    cam.rotation_euler = (math.radians(46), 0.0, 0.0)
    cam.data.lens = 32.0
    bpy.context.scene.camera = cam

    # Otomatis aktifkan mode shading 'MATERIAL' agar tekstur langsung terlihat
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"

def jalankan_modul_2(ascii_str=DENAH_ASCII):
    parser = AsciiDenahParser(
        scale_x=SKALA_X_METER_PER_KARAKTER,
        scale_y=SKALA_Y_METER_PER_KARAKTER,
        tinggi_dinding=TINGGI_DINDING_DEFAULT,
        tebal_dinding=TEBAL_DINDING_DEFAULT,
    )
    cfg_denah = parser.parse_to_dict(ascii_str)
    cfg_assets = DEFAULT_CONFIG_ASSETS

    if BLENDER_AVAILABLE:
        SceneManager.bersihkan_scene()
        koleksi = SceneManager.buat_koleksi("RumahLego_Modul2")
        builder = AssetBuilder(TextureMaterialFactory(), cfg_assets["palet"])
        DenahBuilder(builder, cfg_denah["rumah"]).bangun_semua()

        for obj in list(bpy.context.scene.objects):
            SceneManager.pindahkan_ke_koleksi(obj, koleksi)

        atur_kamera_cahaya_dan_viewport(cfg_denah["rumah"]["grid"])
        register_lego_ui()
        print("MATERI 2 OK: Transformasi Matriks 4x4, Tekstur Prosedural, & Panel UI 'LegoApp M2' aktif!")

    return cfg_denah

if __name__ == "__main__":
    jalankan_modul_2(DENAH_ASCII)