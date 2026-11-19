#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODUL 3 KOMPUTER GRAFIK (V4) - LIGHTING, ATMOSPHERE & MACRO ENVIRONMENT (3 GEDUNG 2 LANTAI)
File: modul3_lighting_environment_makro.py (Kompatibel Penuh Blender 4.3)

Fokus Materi 3:
  1. LightingRigManager     : Mengelola 4 sumber cahaya utama Komputer Grafik:
                              - Directional Light (SUN) + sudut elevasi matahari
                              - Point Light (Lampu Interior Lantai 1 & Lantai 2)
                              - Spot Light (Lampu Jalan PJU dengan Sudut Cone)
                              - Area Light (Pencahayaan Plasa & Taman)
                              - World Environment Sky Shader (Langit Siang/Sore/Malam)
  2. MultiFloorBuilder      : Membangun 3 Gedung 2 Lantai dari blueprint ASCII,
                              lengkap dengan pelat lantai 2, fasad kaca, lampu
                              plafon tiap lantai, dan atap rooftop.
  3. MacroEnvironmentBuilder: Membangun kawasan jalan raya bermarka, trotoar,
                              taman kota, pepohonan, bangku taman, lampu PJU,
                              kolam air mancur, dan kendaraan LEGO di jalan.
  4. MacroLightApp (UI)     : Panel Aplikasi Interaktif di Sidebar 3D Viewport
                              (Tekan 'N' -> tab 'MacroLight M3') untuk simulasi
                              waktu (Day / Sunset / Night) & kontrol lampu.
================================================================================
"""

import json
import math
import re
from collections import deque

# ==============================================================================
# BAGIAN 1: KONFIGURASI KAWASAN MAKRO & DENAH GEDUNG 2 LANTAI
# ==============================================================================
SKALA_MAKRO_METER = 1.0          # 1 karakter di peta makro = 1.0 meter
TINGGI_PER_LANTAI = 3.2          # Tinggi per lantai = 3.2m (2 lantai = 6.4m)
TEBAL_DINDING     = 0.18
TEBAL_SLAB_LANTAI = 0.22

# Peta Kawasan Makro (Masterplan 3 Gedung + Jalan Utama + Taman & Plasa)
# Legenda Karakter:
#   '=' : Jalan Raya Aspal       '#' : Marka Putih Jalan
#   '.' : Trotoar Pejalan Kaki   '~' : Taman Rumput Hijau
#   'T' : Pohon Taman            'L' : Tiang Lampu Jalan (Spot Light)
#   'B' : Bangku Taman           'W' : Kolam Air Mancur Plasa
#   'C' : Mobil LEGO di Jalan
PETA_MAKRO_ASCII = r"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~  T       +-------------------+      T      +-----------------+ ~~
~~          |                   |             |                 | ~~
~~     T    |     GEDUNG A      |      W      |    GEDUNG B     | ~~
~~          |    (2 LANTAI)     |     WWW     |   (2 LANTAI)    | ~~
~~  B       |   KANTOR UTAMA    |      W      |   PUSAT RISET   | ~~
~~          |                   |             |                 | ~~
~~          +-------------------+      B      +-----------------+ ~~
....................................................................
..  L             L                   L                 L         ..
====================================================================
====  C  =============  #  =============  #  ========  C  ==========
====     =============     =============     =======================
====================================================================
..  L             L                   L                 L         ..
....................................................................
~~  T       +-----------------------------------------+     T     ~~
~~          |                                         |           ~~
~~  B       |                GEDUNG C                 |     B     ~~
~~          |         (2 LANTAI - CONVENTION)         |           ~~
~~     T    |                                         |  T     T  ~~
~~          +-----------------------------------------+           ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# Denah Interior Modular yang dipakai untuk mengekstrusi tiap lantai gedung
DENAH_GEDUNG_MODULAR_ASCII = r"""
+-----------+---------------+-----------+
|   RUANG   |    KORIDOR    |   RUANG   |
|  RAPAT 1  |     UTAMA     |  RAPAT 2  |
+-----------+-------+-------+-----------+
|                   |                   |
|    WORKSTATION    |    WORKSTATION    |
|       BARAT       |       TIMUR       |
+-------------------+-------------------+
"""

# ==============================================================================
# BAGIAN 2: PALET MATERIAL & SHADER (TERMASUK EMISSION & ENVIRONMENT)
# ==============================================================================
CONFIG_MATERIAL_MODUL3 = {
    # Material Gedung
    "dinding_eksterior_a": {
        "rgba": [0.88, 0.85, 0.78, 1.0], "roughness": 0.75,
        "tex_type": "BRICK", "color2": [0.72, 0.66, 0.58, 1.0], "uv_scale": [5.0, 5.0, 5.0], "bump": 0.20
    },
    "dinding_eksterior_b": {
        "rgba": [0.74, 0.80, 0.86, 1.0], "roughness": 0.55, "metallic": 0.25,
        "tex_type": "BRICK", "color2": [0.58, 0.65, 0.72, 1.0], "uv_scale": [4.0, 4.0, 4.0], "bump": 0.15
    },
    "dinding_eksterior_c": {
        "rgba": [0.86, 0.78, 0.72, 1.0], "roughness": 0.70,
        "tex_type": "BRICK", "color2": [0.68, 0.56, 0.48, 1.0], "uv_scale": [6.0, 6.0, 6.0], "bump": 0.22
    },
    "dinding_interior": {
        "rgba": [0.92, 0.92, 0.94, 1.0], "roughness": 0.70, "tex_type": "NOISE", "uv_scale": [8.0, 8.0, 8.0], "bump": 0.05
    },
    "slab_beton": {
        "rgba": [0.55, 0.57, 0.60, 1.0], "roughness": 0.80, "tex_type": "NOISE", "uv_scale": [6.0, 6.0, 6.0], "bump": 0.12
    },
    "lantai_interior": {
        "rgba": [0.84, 0.80, 0.72, 1.0], "roughness": 0.35,
        "tex_type": "CHECKER", "color2": [0.70, 0.65, 0.56, 1.0], "uv_scale": [10.0, 10.0, 1.0], "bump": 0.04
    },
    "kaca_fasad": {
        "rgba": [0.55, 0.80, 0.95, 1.0], "roughness": 0.08, "metallic": 0.15,
        "emission": [0.95, 0.85, 0.55, 1.0], "emission_strength": 0.35
    },
    "kusen_hitam": {"rgba": [0.15, 0.17, 0.20, 1.0], "roughness": 0.30, "metallic": 0.75},
    # Material Jalan, Taman & Lingkungan
    "aspal_jalan": {
        "rgba": [0.16, 0.17, 0.19, 1.0], "roughness": 0.88,
        "tex_type": "NOISE", "uv_scale": [25.0, 25.0, 1.0], "bump": 0.30
    },
    "marka_jalan": {
        "rgba": [0.96, 0.96, 0.92, 1.0], "roughness": 0.40,
        "emission": [0.95, 0.95, 0.85, 1.0], "emission_strength": 0.25
    },
    "trotoar_paving": {
        "rgba": [0.68, 0.66, 0.62, 1.0], "roughness": 0.75,
        "tex_type": "CHECKER", "color2": [0.56, 0.54, 0.50, 1.0], "uv_scale": [20.0, 20.0, 1.0], "bump": 0.15
    },
    "rumput_taman": {
        "rgba": [0.20, 0.52, 0.22, 1.0], "roughness": 0.90,
        "tex_type": "NOISE", "uv_scale": [18.0, 18.0, 1.0], "bump": 0.25
    },
    "batang_pohon": {
        "rgba": [0.38, 0.24, 0.12, 1.0], "roughness": 0.85,
        "tex_type": "WOOD", "color2": [0.24, 0.14, 0.06, 1.0], "uv_scale": [5.0, 5.0, 5.0], "bump": 0.20
    },
    "daun_pohon": {
        "rgba": [0.16, 0.58, 0.20, 1.0], "roughness": 0.75,
        "tex_type": "NOISE", "uv_scale": [8.0, 8.0, 8.0], "bump": 0.18
    },
    "air_kolam": {
        "rgba": [0.18, 0.62, 0.82, 1.0], "roughness": 0.05, "metallic": 0.10,
        "tex_type": "WOOD", "color2": [0.35, 0.80, 0.95, 1.0], "uv_scale": [8.0, 8.0, 1.0], "bump": 0.08
    },
    "tiang_lampu": {"rgba": [0.22, 0.25, 0.28, 1.0], "roughness": 0.35, "metallic": 0.80},
    "bohlam_lampu": {
        "rgba": [1.0, 0.92, 0.72, 1.0], "roughness": 0.10,
        "emission": [1.0, 0.88, 0.60, 1.0], "emission_strength": 6.0
    },
    "kayu_bangku": {
        "rgba": [0.62, 0.38, 0.18, 1.0], "roughness": 0.55,
        "tex_type": "WOOD", "color2": [0.42, 0.24, 0.10, 1.0], "uv_scale": [4.0, 4.0, 4.0], "bump": 0.10
    },
    "mobil_merah":  {"rgba": [0.85, 0.14, 0.14, 1.0], "roughness": 0.20, "metallic": 0.30},
    "mobil_biru":   {"rgba": [0.14, 0.42, 0.86, 1.0], "roughness": 0.20, "metallic": 0.30},
    "roda_hitam":   {"rgba": [0.12, 0.12, 0.14, 1.0], "roughness": 0.85},
}

# ==============================================================================
# BAGIAN 3: PARSER KAWASAN MAKRO ASCII (Mendukung 3 Gedung + Jalan + Taman)
# ==============================================================================
class AsciiMacroParser:
    """
    Mengekstrak:
      1. Footprint kotak gedung (GEDUNG A, GEDUNG B, GEDUNG C) via Flood-Fill
      2. Jalur jalan raya, marka jalan, trotoar, dan hamparan rumput
      3. Titik koordinat objek taman: Pohon ('T'), Lampu Jalan ('L'),
         Bangku ('B'), Air Mancur ('W'), dan Mobil LEGO ('C')
    """

    def __init__(self, scale=1.0):
        self.scale = float(scale)

    @staticmethod
    def _normalisasi_grid(ascii_text):
        lines = [l.rstrip("\r\n") for l in ascii_text.strip().splitlines() if l.strip()]
        max_w = max(len(l) for l in lines)
        return [l.ljust(max_w) for l in lines]

    def _rc_to_xy(self, r, c, max_r):
        return round(c * self.scale, 2), round((max_r - r) * self.scale, 2)

    def parse(self, ascii_text):
        grid = self._normalisasi_grid(ascii_text)
        H, W = len(grid), len(grid[0])
        max_r = H - 1

        # 1. Ekstrak kotak gedung yang dibatasi '+', '-', '|'
        visited = [[False] * W for _ in range(H)]
        buildings = []
        building_cells = set()

        for r in range(H):
            for c in range(W):
                if grid[r][c] == "+" and not visited[r][c]:
                    # Cari batas kanan dan bawah kotak gedung
                    c2 = c + 1
                    while c2 < W and grid[r][c2] == "-":
                        c2 += 1
                    if c2 < W and grid[r][c2] == "+":
                        r2 = r + 1
                        while r2 < H and grid[r2][c] == "|":
                            r2 += 1
                        if r2 < H and grid[r2][c] == "+":
                            # Tandai seluruh sel di dalam kotak gedung
                            teks_dalam = []
                            for rr in range(r, r2 + 1):
                                row_str = ""
                                for cc in range(c, c2 + 1):
                                    visited[rr][cc] = True
                                    building_cells.add((rr, cc))
                                    if r < rr < r2 and c < cc < c2:
                                        row_str += grid[rr][cc]
                                if row_str.strip():
                                    teks_dalam.append(" ".join(row_str.split()))

                            label_gabung = " ".join(teks_dalam)
                            nama_gedung = f"Gedung_{len(buildings)+1}"
                            if "GEDUNG A" in label_gabung.upper():
                                nama_gedung = "Gedung_A_KantorUtama"
                            elif "GEDUNG B" in label_gabung.upper():
                                nama_gedung = "Gedung_B_PusatRiset"
                            elif "GEDUNG C" in label_gabung.upper():
                                nama_gedung = "Gedung_C_Convention"

                            x1, y2 = self._rc_to_xy(r, c, max_r)
                            x2, y1 = self._rc_to_xy(r2, c2, max_r)
                            buildings.append({
                                "id": len(buildings),
                                "nama": nama_gedung,
                                "label": label_gabung,
                                "min_xy": [min(x1, x2), min(y1, y2)],
                                "max_xy": [max(x1, x2), max(y1, y2)],
                                "jumlah_lantai": 2,
                            })

        # 2. Ekstrak baris zona jalan & trotoar serta objek titik (T, L, B, W, C, #)
        pohon_list, lampu_jalan_list, bangku_list, kolam_cells, mobil_list, marka_list = [], [], [], [], [], []
        jalan_rows, trotoar_rows = set(), set()

        for r in range(H):
            for c in range(W):
                if (r, c) in building_cells:
                    continue
                ch = grid[r][c]
                x, y = self._rc_to_xy(r, c, max_r)
                if ch == "=":
                    jalan_rows.add(r)
                elif ch == "#":
                    jalan_rows.add(r)
                    marka_list.append([x, y])
                elif ch == ".":
                    trotoar_rows.add(r)
                elif ch == "T":
                    pohon_list.append([x, y])
                elif ch == "L":
                    trotoar_rows.add(r)
                    lampu_jalan_list.append([x, y])
                elif ch == "B":
                    bangku_list.append([x, y])
                elif ch == "W":
                    kolam_cells.append([x, y])
                elif ch == "C":
                    jalan_rows.add(r)
                    mobil_list.append([x, y])

        lebar_kawasan = round((W - 1) * self.scale, 2)
        tinggi_kawasan = round((H - 1) * self.scale, 2)

        # Rentang Y jalan raya & trotoar
        if jalan_rows:
            _, y_j_max = self._rc_to_xy(min(jalan_rows), 0, max_r)
            _, y_j_min = self._rc_to_xy(max(jalan_rows), 0, max_r)
            zona_jalan = [min(y_j_min, y_j_max) - 0.5, max(y_j_min, y_j_max) + 0.5]
        else:
            zona_jalan = [tinggi_kawasan * 0.4, tinggi_kawasan * 0.6]

        return {
            "ukuran_kawasan": [lebar_kawasan, tinggi_kawasan],
            "zona_jalan_y": zona_jalan,
            "gedung": buildings,
            "pohon": pohon_list,
            "lampu_jalan": lampu_jalan_list,
            "bangku": bangku_list,
            "kolam_cells": kolam_cells,
            "mobil": mobil_list,
            "marka": marka_list,
        }

# ==============================================================================
# BAGIAN 4: ENGINE BLENDER 4.3 (TRANSFORM 4x4, SHADER, LIGHTING, & BUILDER)
# ==============================================================================
try:
    import bpy
    import bmesh
    from mathutils import Matrix, Vector
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False

if BLENDER_AVAILABLE:

    # --------------------------------------------------------------------------
    # 1. Transform3DEngine (Matriks Homogen 4x4 & Hierarki Parent-Child)
    # --------------------------------------------------------------------------
    class Transform3DEngine:
        @staticmethod
        def komposisi_trs(lokasi=(0.0, 0.0, 0.0), rotasi_euler=(0.0, 0.0, 0.0), skala=(1.0, 1.0, 1.0)):
            T = Matrix.Translation(Vector(lokasi))
            Rx = Matrix.Rotation(rotasi_euler[0], 4, "X")
            Ry = Matrix.Rotation(rotasi_euler[1], 4, "Y")
            Rz = Matrix.Rotation(rotasi_euler[2], 4, "Z")
            S = Matrix.Diagonal((skala[0], skala[1], skala[2], 1.0))
            return T @ Rz @ Ry @ Rx @ S

        @classmethod
        def terapkan_matriks(cls, obj, lokasi=(0.0, 0.0, 0.0), rotasi_euler=(0.0, 0.0, 0.0), skala=(1.0, 1.0, 1.0), parent=None):
            M = cls.komposisi_trs(lokasi, rotasi_euler, skala)
            if parent is not None:
                obj.parent = parent
                obj.matrix_parent_inverse = Matrix.Identity(4)
                obj.matrix_local = M
            else:
                obj.matrix_world = M

    # --------------------------------------------------------------------------
    # 2. SceneManager & Box UV Generator
    # --------------------------------------------------------------------------
    class SceneManager:
        @staticmethod
        def bersihkan_scene():
            if bpy.context.active_object and bpy.context.active_object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.object.delete()
            for block_list in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.lights):
                for item in list(block_list):
                    block_list.remove(item)

        @staticmethod
        def buat_koleksi(nama_koleksi, parent_kol=None):
            if nama_koleksi in bpy.data.collections:
                return bpy.data.collections[nama_koleksi]
            kol = bpy.data.collections.new(nama_koleksi)
            if parent_kol:
                parent_kol.children.link(kol)
            else:
                bpy.context.scene.collection.children.link(kol)
            return kol

        @staticmethod
        def pindahkan_ke_koleksi(obj, koleksi):
            for c in list(obj.users_collection):
                c.objects.unlink(obj)
            koleksi.objects.link(obj)

        @staticmethod
        def generate_box_uv(obj):
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
    # 3. TextureMaterialFactory (Shader Nodes & Emissive Control)
    # --------------------------------------------------------------------------
    class TextureMaterialFactory:
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
            tex_type = spec.get("tex_type", "NONE").upper()
            uv_scale = tuple(spec.get("uv_scale", [4.0, 4.0, 4.0]))
            bump_val = float(spec.get("bump", 0.1))

            if bsdf:
                bsdf.inputs["Base Color"].default_value = rgba
                bsdf.inputs["Roughness"].default_value = float(spec.get("roughness", 0.5))
                if "Metallic" in bsdf.inputs:
                    bsdf.inputs["Metallic"].default_value = float(spec.get("metallic", 0.0))
                if spec.get("emission"):
                    em_in = bsdf.inputs.get("Emission Color") or bsdf.inputs.get("Emission")
                    if em_in:
                        em_in.default_value = tuple(spec["emission"])
                    if "Emission Strength" in bsdf.inputs:
                        bsdf.inputs["Emission Strength"].default_value = float(spec.get("emission_strength", 1.0))

            if tex_type != "NONE" and bsdf:
                coord = nodes.new(type="ShaderNodeTexCoord")
                mapping = nodes.new(type="ShaderNodeMapping")
                mapping.inputs["Scale"].default_value = uv_scale
                links.new(coord.outputs["Generated"], mapping.inputs["Vector"])

                bump = nodes.new(type="ShaderNodeBump")
                bump.inputs["Strength"].default_value = bump_val

                if tex_type == "BRICK":
                    tex = nodes.new(type="ShaderNodeTexBrick")
                    tex.inputs["Color1"].default_value = rgba
                    tex.inputs["Color2"].default_value = tuple(spec.get("color2", [0.6, 0.5, 0.4, 1.0]))
                    tex.inputs["Mortar Size"].default_value = 0.02
                    links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
                    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
                    links.new(tex.outputs["Fac"], bump.inputs["Height"])
                    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type == "CHECKER":
                    tex = nodes.new(type="ShaderNodeTexChecker")
                    tex.inputs["Color1"].default_value = rgba
                    tex.inputs["Color2"].default_value = tuple(spec.get("color2", [0.5, 0.5, 0.5, 1.0]))
                    links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
                    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
                    links.new(tex.outputs["Fac"], bump.inputs["Height"])
                    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type == "WOOD":
                    tex = nodes.new(type="ShaderNodeTexWave")
                    tex.inputs["Scale"].default_value = 3.0
                    tex.inputs["Distortion"].default_value = 4.0
                    mix = nodes.new(type="ShaderNodeMix")
                    mix.data_type = "RGBA"
                    mix.inputs["A"].default_value = rgba
                    mix.inputs["B"].default_value = tuple(spec.get("color2", [0.3, 0.2, 0.1, 1.0]))
                    links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
                    links.new(tex.outputs["Fac"], mix.inputs["Factor"])
                    links.new(mix.outputs["Result"], bsdf.inputs["Base Color"])
                    links.new(tex.outputs["Fac"], bump.inputs["Height"])
                    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

                elif tex_type == "NOISE":
                    tex = nodes.new(type="ShaderNodeTexNoise")
                    tex.inputs["Scale"].default_value = 15.0
                    links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
                    links.new(tex.outputs["Fac"], bump.inputs["Height"])
                    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

            mat.diffuse_color = rgba
            return mat

    # --------------------------------------------------------------------------
    # 4. LightingRigManager: Inti Materi 3 (Directional, Point, Spot, Area & Sky)
    # --------------------------------------------------------------------------
    class LightingRigManager:
        """
        MATERI 3 - PENCAHAYAAN & LINGKUNGAN (LIGHTING & ENVIRONMENT):
        Mengatur 4 komponen pencahayaan utama + World Sky Shader:
          1. Sun Light (Directional) : Cahaya matahari global & bayangan tajam
          2. World Environment       : Langit prosedural (Sky Texture) & Ambient
          3. Street Spot Lights      : Lampu PJU sepanjang jalan dengan kerucut sorot
          4. Interior Point Lights   : Lampu plafon tiap lantai di dalam 3 gedung
          5. Plaza Area Light        : Fill light lembut di atas taman air mancur
        """

        PRESETS_WAKTU = {
            "DAY": {
                "sun_energy": 4.5,
                "sun_color": (1.0, 0.98, 0.92),
                "sun_rot_deg": (38.0, 15.0, -35.0),
                "sky_bg_color": (0.45, 0.68, 0.95, 1.0),
                "sky_strength": 1.2,
                "street_light_energy": 0.0,      # PJU mati saat siang
                "interior_light_energy": 60.0,   # Lampu kantor redup saat siang
                "glass_emission": 0.15,
                "bulb_emission": 0.5,
            },
            "SUNSET": {
                "sun_energy": 2.8,
                "sun_color": (1.0, 0.52, 0.22),
                "sun_rot_deg": (74.0, 12.0, -65.0),
                "sky_bg_color": (0.85, 0.42, 0.25, 1.0),
                "sky_strength": 0.75,
                "street_light_energy": 450.0,    # PJU mulai menyala hangat
                "interior_light_energy": 180.0,
                "glass_emission": 1.2,
                "bulb_emission": 6.0,
            },
            "NIGHT": {
                "sun_energy": 0.15,              # Cahaya bulan redup kebiruan
                "sun_color": (0.45, 0.62, 0.95),
                "sun_rot_deg": (42.0, -20.0, 25.0),
                "sky_bg_color": (0.02, 0.04, 0.09, 1.0),
                "sky_strength": 0.20,
                "street_light_energy": 900.0,    # PJU menyala terang di malam hari
                "interior_light_energy": 320.0,  # Gedung bersinar terang dari dalam
                "glass_emission": 2.5,
                "bulb_emission": 12.0,
            },
        }

        @classmethod
        def bangun_world_sky(cls):
            """Membangun World Shader dengan Sky Texture + Background Node."""
            scene = bpy.context.scene
            if not scene.world:
                scene.world = bpy.data.worlds.new("World_Makro_M3")
            world = scene.world
            world.use_nodes = True
            nodes = world.node_tree.nodes
            links = world.node_tree.links
            nodes.clear()

            out_node = nodes.new(type="ShaderNodeOutputWorld")
            out_node.location = (300, 0)

            bg_node = nodes.new(type="ShaderNodeBackground")
            bg_node.name = "World_BG"
            bg_node.location = (80, 0)
            bg_node.inputs["Color"].default_value = (0.45, 0.68, 0.95, 1.0)
            bg_node.inputs["Strength"].default_value = 1.0

            links.new(bg_node.outputs["Background"], out_node.inputs["Surface"])

            # Aktifkan bayangan EEVEE & Ambient Occlusion
            if hasattr(scene.eevee, "use_gtao"):
                scene.eevee.use_gtao = True
            if hasattr(scene.eevee, "use_bloom"):
                scene.eevee.use_bloom = True

        @classmethod
        def bangun_matahari_dan_area_plasa(cls, ukuran_kawasan, koleksi_lampu):
            wx, wy = ukuran_kawasan
            cx, cy = wx / 2.0, wy / 2.0

            # 1. Directional Light (SUN)
            light_data = bpy.data.lights.new(name="Sun_MatahariUtama", type="SUN")
            light_data.energy = 4.5
            light_data.color = (1.0, 0.98, 0.92)
            light_data.angle = math.radians(1.5)
            sun_obj = bpy.data.objects.new(name="Sun_MatahariUtama", object_data=light_data)
            bpy.context.scene.collection.objects.link(sun_obj)
            Transform3DEngine.terapkan_matriks(
                sun_obj,
                lokasi=(cx, cy, 35.0),
                rotasi_euler=(math.radians(38), math.radians(15), math.radians(-35)),
            )
            SceneManager.pindahkan_ke_koleksi(sun_obj, koleksi_lampu)

            # 2. Area Light di atas Plasa Air Mancur (Fill Light Taman)
            area_data = bpy.data.lights.new(name="Area_PlasaTaman", type="AREA")
            area_data.energy = 250.0
            area_data.color = (0.75, 0.92, 1.0)
            area_data.size = 8.0
            area_obj = bpy.data.objects.new(name="Area_PlasaTaman", object_data=area_data)
            bpy.context.scene.collection.objects.link(area_obj)
            Transform3DEngine.terapkan_matriks(area_obj, lokasi=(cx, cy + 5.5, 8.0))
            SceneManager.pindahkan_ke_koleksi(area_obj, koleksi_lampu)

        @classmethod
        def tambah_point_light_interior(cls, nama, lokasi_xyz, koleksi_lampu, parent=None):
            """Menambahkan lampu Point Light di plafon tiap lantai gedung."""
            pt_data = bpy.data.lights.new(name=nama, type="POINT")
            pt_data.energy = 120.0
            pt_data.color = (1.0, 0.92, 0.78)
            pt_data.shadow_soft_size = 0.5
            pt_obj = bpy.data.objects.new(name=nama, object_data=pt_data)
            bpy.context.scene.collection.objects.link(pt_obj)
            Transform3DEngine.terapkan_matriks(pt_obj, lokasi=lokasi_xyz, parent=parent)
            SceneManager.pindahkan_ke_koleksi(pt_obj, koleksi_lampu)
            return pt_obj

        @classmethod
        def tambah_spot_light_pju(cls, nama, lokasi_xyz, rot_z, koleksi_lampu, parent=None):
            """Menambahkan lampu Spot Light pada kepala tiang PJU."""
            sp_data = bpy.data.lights.new(name=nama, type="SPOT")
            sp_data.energy = 450.0
            sp_data.color = (1.0, 0.85, 0.55)
            sp_data.spot_size = math.radians(78.0)   # Sudut kerucut sorot lampu jalan
            sp_data.spot_blend = 0.45                # Kelembutan tepi kerucut cahaya
            sp_data.shadow_soft_size = 0.35
            sp_obj = bpy.data.objects.new(name=nama, object_data=sp_data)
            bpy.context.scene.collection.objects.link(sp_obj)
            Transform3DEngine.terapkan_matriks(
                sp_obj,
                lokasi=lokasi_xyz,
                rotasi_euler=(math.radians(15), 0.0, rot_z),
                parent=parent,
            )
            SceneManager.pindahkan_ke_koleksi(sp_obj, koleksi_lampu)
            return sp_obj

        @classmethod
        def terapkan_preset_waktu(cls, nama_preset="SUNSET", pju_nyala=True, interior_nyala=True):
            spec = cls.PRESETS_WAKTU.get(nama_preset, cls.PRESETS_WAKTU["SUNSET"])

            # 1. Update Sun Light
            sun_obj = bpy.data.objects.get("Sun_MatahariUtama")
            if sun_obj and sun_obj.type == "LIGHT":
                sun_obj.data.energy = spec["sun_energy"]
                sun_obj.data.color = spec["sun_color"]
                r_deg = spec["sun_rot_deg"]
                sun_obj.rotation_euler = (math.radians(r_deg[0]), math.radians(r_deg[1]), math.radians(r_deg[2]))

            # 2. Update World Sky Background
            world = bpy.context.scene.world
            if world and world.use_nodes:
                bg = world.node_tree.nodes.get("World_BG")
                if bg:
                    bg.inputs["Color"].default_value = spec["sky_bg_color"]
                    bg.inputs["Strength"].default_value = spec["sky_strength"]

            # 3. Update seluruh Spot Light PJU & Point Light Interior
            for obj in bpy.data.objects:
                if obj.type == "LIGHT":
                    if obj.name.startswith("Spot_PJU"):
                        obj.data.energy = spec["street_light_energy"] if pju_nyala else 0.0
                    elif obj.name.startswith("Point_Lantai"):
                        obj.data.energy = spec["interior_light_energy"] if interior_nyala else 0.0

            # 4. Update Emission Strength pada Kaca Gedung & Bohlam PJU
            for mat_name, em_val in [
                ("kaca_fasad", spec["glass_emission"] if interior_nyala else 0.05),
                ("bohlam_lampu", spec["bulb_emission"] if pju_nyala else 0.1),
            ]:
                mat = bpy.data.materials.get(mat_name)
                if mat and mat.use_nodes:
                    bsdf = mat.node_tree.nodes.get("Principled BSDF")
                    if bsdf and "Emission Strength" in bsdf.inputs:
                        bsdf.inputs["Emission Strength"].default_value = em_val

    # --------------------------------------------------------------------------
    # 5. MacroAssetBuilder: Membangun 3 Gedung 2 Lantai, Jalan, Pohon, & PJU
    # --------------------------------------------------------------------------
    class MacroAssetBuilder:
        def __init__(self, mat_factory, palet, kol_utama, kol_lampu):
            self.mat_factory = mat_factory
            self.palet = palet
            self.kol_utama = kol_utama
            self.kol_lampu = kol_lampu

        def _mat(self, nama):
            spec = self.palet.get(nama, {"rgba": [0.8, 0.8, 0.8, 1.0]})
            return self.mat_factory.get_or_create(nama, spec)

        def buat_kotak(self, nama, dim, lokasi, rot=(0.0, 0.0, 0.0), mat_nama="dinding_interior", parent=None):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
            o = bpy.context.active_object
            o.name = nama
            Transform3DEngine.terapkan_matriks(o, lokasi=lokasi, rotasi_euler=rot, skala=dim, parent=parent)
            SceneManager.generate_box_uv(o)
            o.data.materials.append(self._mat(mat_nama))
            SceneManager.pindahkan_ke_koleksi(o, self.kol_utama)
            return o

        def buat_silinder(self, nama, radius, tinggi, lokasi, rot=(0.0, 0.0, 0.0), mat_nama="tiang_lampu", parent=None):
            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=(0.0, 0.0, 0.0))
            o = bpy.context.active_object
            o.name = nama
            Transform3DEngine.terapkan_matriks(o, lokasi=lokasi, rotasi_euler=rot, skala=(radius, radius, tinggi), parent=parent)
            o.data.materials.append(self._mat(mat_nama))
            SceneManager.pindahkan_ke_koleksi(o, self.kol_utama)
            return o

        # --- A. PEMBANGUN GEDUNG 2 LANTAI (MULTI-FLOOR BUILDING) ---
        def bangun_gedung_dua_lantai(self, spec_gedung):
            nama_g = spec_gedung["nama"]
            x1, y1 = spec_gedung["min_xy"]
            x2, y2 = spec_gedung["max_xy"]
            wx, wy = abs(x2 - x1), abs(y2 - y1)
            cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            jml_lantai = int(spec_gedung.get("jumlah_lantai", 2))

            mat_eks = (
                "dinding_eksterior_a" if "Gedung_A" in nama_g
                else ("dinding_eksterior_b" if "Gedung_B" in nama_g else "dinding_eksterior_c")
            )

            # Root Empty Gedung (Hierarki Induk Gedung)
            root_g = bpy.data.objects.new(nama_g, None)
            root_g.empty_display_type = "CUBE"
            root_g.empty_display_size = 1.0
            bpy.context.scene.collection.objects.link(root_g)
            Transform3DEngine.terapkan_matriks(root_g, lokasi=(cx, cy, 0.0))
            SceneManager.pindahkan_ke_koleksi(root_g, self.kol_utama)

            for lt in range(jml_lantai):
                z_base = lt * TINGGI_PER_LANTAI
                z_mid = z_base + TINGGI_PER_LANTAI / 2.0

                # 1. Pelat Lantai (Floor Slab) & Lantai Keramik Interior
                self.buat_kotak(
                    f"{nama_g}_Slab_Lt{lt+1}",
                    [wx + 0.3, wy + 0.3, TEBAL_SLAB_LANTAI],
                    (0.0, 0.0, z_base + TEBAL_SLAB_LANTAI / 2.0),
                    mat_nama="slab_beton",
                    parent=root_g,
                )
                self.buat_kotak(
                    f"{nama_g}_LantaiKeramik_Lt{lt+1}",
                    [wx - 0.2, wy - 0.2, 0.06],
                    (0.0, 0.0, z_base + TEBAL_SLAB_LANTAI + 0.03),
                    mat_nama="lantai_interior",
                    parent=root_g,
                )

                # 2. Dinding Eksterior 4 Sisi + Barisan Jendela Kaca (Fasad)
                # Sisi Utara & Selatan
                for s_idx, y_off in enumerate([-wy / 2.0, wy / 2.0]):
                    # Dinding Bawah (Spandrel) & Atas (Lintel)
                    self.buat_kotak(
                        f"{nama_g}_DindingNS_{lt+1}_{s_idx}_Bawah",
                        [wx, TEBAL_DINDING, 0.95],
                        (0.0, y_off, z_base + 0.475),
                        mat_nama=mat_eks,
                        parent=root_g,
                    )
                    self.buat_kotak(
                        f"{nama_g}_DindingNS_{lt+1}_{s_idx}_Atas",
                        [wx, TEBAL_DINDING, 0.65],
                        (0.0, y_off, z_base + TINGGI_PER_LANTAI - 0.325),
                        mat_nama=mat_eks,
                        parent=root_g,
                    )
                    # Panel Kaca Fasad Sepanjang Dinding
                    lebar_kaca = wx - 1.6
                    self.buat_kotak(
                        f"{nama_g}_KacaFasadNS_{lt+1}_{s_idx}",
                        [lebar_kaca, 0.06, 1.60],
                        (0.0, y_off, z_base + 0.95 + 0.80),
                        mat_nama="kaca_fasad",
                        parent=root_g,
                    )
                    # Pilar Sudut & Mullion Kusen
                    for px in [-wx / 2.0 + 0.4, 0.0, wx / 2.0 - 0.4]:
                        self.buat_kotak(
                            f"{nama_g}_PilarNS_{lt+1}_{s_idx}_{px:.1f}",
                            [0.45, TEBAL_DINDING + 0.08, TINGGI_PER_LANTAI],
                            (px, y_off, z_mid),
                            mat_nama="kusen_hitam",
                            parent=root_g,
                        )

                # Sisi Barat & Timur
                for s_idx, x_off in enumerate([-wx / 2.0, wx / 2.0]):
                    self.buat_kotak(
                        f"{nama_g}_DindingEW_{lt+1}_{s_idx}",
                        [TEBAL_DINDING, wy, TINGGI_PER_LANTAI],
                        (x_off, 0.0, z_mid),
                        mat_nama=mat_eks,
                        parent=root_g,
                    )
                    self.buat_kotak(
                        f"{nama_g}_KacaFasadEW_{lt+1}_{s_idx}",
                        [0.08, wy * 0.55, 1.50],
                        (x_off, 0.0, z_base + 1.75),
                        mat_nama="kaca_fasad",
                        parent=root_g,
                    )

                # 3. Partisi Dinding Dalam & Tangga Penghubung Lantai 1 -> Lantai 2
                self.buat_kotak(
                    f"{nama_g}_PartisiDalam_Lt{lt+1}",
                    [wx * 0.65, 0.14, TINGGI_PER_LANTAI - 0.2],
                    (0.0, 0.0, z_mid),
                    mat_nama="dinding_interior",
                    parent=root_g,
                )
                if lt == 0:
                    # Bangun Tangga Internal dari Lantai 1 ke Lantai 2
                    jml_step = 10
                    for st in range(jml_step):
                        t_step = (st + 1) * (TINGGI_PER_LANTAI / jml_step)
                        self.buat_kotak(
                            f"{nama_g}_TanggaLt1Ke2_{st}",
                            [0.35, 1.2, t_step],
                            (-wx * 0.25 + st * 0.36, -wy * 0.22, t_step / 2.0),
                            mat_nama="slab_beton",
                            parent=root_g,
                        )

                # 4. Pasang Point Light Interior di Plafon tiap Lantai (Materi 3)
                for lx in [-wx * 0.25, wx * 0.25]:
                    LightingRigManager.tambah_point_light_interior(
                        nama=f"Point_Lantai{lt+1}_{nama_g}_{lx:.1f}",
                        lokasi_xyz=(lx, 0.0, z_base + TINGGI_PER_LANTAI - 0.45),
                        koleksi_lampu=self.kol_lampu,
                        parent=root_g,
                    )

            # 5. Atap Rooftop, Parapet, & Unit Mesin HVAC di Lantai Paling Atas
            z_atap = jml_lantai * TINGGI_PER_LANTAI
            self.buat_kotak(
                f"{nama_g}_DakAtap",
                [wx + 0.5, wy + 0.5, 0.28],
                (0.0, 0.0, z_atap + 0.14),
                mat_nama="slab_beton",
                parent=root_g,
            )
            # Dinding Parapet Keliling Atap
            self.buat_kotak(f"{nama_g}_ParapetN", [wx + 0.5, 0.20, 0.65], (0.0, wy / 2.0 + 0.15, z_atap + 0.55), mat_nama=mat_eks, parent=root_g)
            self.buat_kotak(f"{nama_g}_ParapetS", [wx + 0.5, 0.20, 0.65], (0.0, -wy / 2.0 - 0.15, z_atap + 0.55), mat_nama=mat_eks, parent=root_g)
            # Unit HVAC Rooftop
            self.buat_kotak(f"{nama_g}_RooftopHVAC", [2.2, 1.4, 1.1], (wx * 0.2, 0.0, z_atap + 0.80), mat_nama="tiang_lampu", parent=root_g)

            return root_g

        # --- B. PEMBANGUN OBJEK LINGKUNGAN (POHON, PJU SPOTLIGHT, BANGKU, KOLAM, MOBIL) ---
        def bangun_pohon_modular(self, idx, xy):
            root = bpy.data.objects.new(f"Pohon_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(xy[0], xy[1], 0.0))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)

            self.buat_silinder(f"Batang_{idx}", 0.22, 1.8, (0.0, 0.0, 0.9), mat_nama="batang_pohon", parent=root)
            # Tajuk daun bertingkat bergaya modular low-poly/LEGO
            self.buat_kotak(f"Daun1_{idx}", [1.8, 1.8, 1.1], (0.0, 0.0, 2.1), mat_nama="daun_pohon", parent=root)
            self.buat_kotak(f"Daun2_{idx}", [1.3, 1.3, 0.9], (0.0, 0.0, 2.9), rot=(0.0, 0.0, math.radians(45)), mat_nama="daun_pohon", parent=root)
            self.buat_kotak(f"Daun3_{idx}", [0.7, 0.7, 0.6], (0.0, 0.0, 3.5), mat_nama="daun_pohon", parent=root)
            return root

        def bangun_lampu_jalan_pju(self, idx, xy, arah_hadap_jalan_y):
            """Membangun Tiang PJU + Bohlam Emisif + Spot Light Sorot Jalan."""
            root = bpy.data.objects.new(f"TiangPJU_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            rot_z = 0.0 if arah_hadap_jalan_y > 0 else math.pi
            Transform3DEngine.terapkan_matriks(root, lokasi=(xy[0], xy[1], 0.0), rotasi_euler=(0.0, 0.0, rot_z))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)

            # Tiang vertikal & lengan lampu menjorok ke jalan
            self.buat_silinder(f"Tiang_{idx}", 0.10, 4.8, (0.0, 0.0, 2.4), mat_nama="tiang_lampu", parent=root)
            self.buat_kotak(f"LenganPJU_{idx}", [0.16, 1.3, 0.14], (0.0, 0.55, 4.75), mat_nama="tiang_lampu", parent=root)
            self.buat_kotak(f"BohlamPJU_{idx}", [0.38, 0.55, 0.10], (0.0, 1.05, 4.65), mat_nama="bohlam_lampu", parent=root)

            # Pasang Spot Light tepat di bawah bohlam PJU
            LightingRigManager.tambah_spot_light_pju(
                nama=f"Spot_PJU_{idx:02d}",
                lokasi_xyz=(0.0, 1.05, 4.55),
                rot_z=0.0,
                koleksi_lampu=self.kol_lampu,
                parent=root,
            )
            return root

        def bangun_bangku_taman(self, idx, xy):
            root = bpy.data.objects.new(f"BangkuTaman_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(xy[0], xy[1], 0.0))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)

            self.buat_kotak(f"Dudukan_{idx}", [1.6, 0.55, 0.08], (0.0, 0.0, 0.45), mat_nama="kayu_bangku", parent=root)
            self.buat_kotak(f"Sandaran_{idx}", [1.6, 0.08, 0.45], (0.0, 0.24, 0.70), mat_nama="kayu_bangku", parent=root)
            self.buat_kotak(f"KakiL_{idx}", [0.12, 0.50, 0.45], (-0.65, 0.0, 0.225), mat_nama="tiang_lampu", parent=root)
            self.buat_kotak(f"KakiR_{idx}", [0.12, 0.50, 0.45], (0.65, 0.0, 0.225), mat_nama="tiang_lampu", parent=root)
            return root

        def bangun_mobil_lego(self, idx, xy):
            warna = "mobil_merah" if idx % 2 == 0 else "mobil_biru"
            root = bpy.data.objects.new(f"MobilLego_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(xy[0], xy[1], 0.0))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)

            self.buat_kotak(f"BodiBawah_{idx}", [2.6, 1.3, 0.50], (0.0, 0.0, 0.40), mat_nama=warna, parent=root)
            self.buat_kotak(f"KabinAtas_{idx}", [1.4, 1.15, 0.45], (-0.15, 0.0, 0.85), mat_nama="kaca_fasad", parent=root)
            for rx in [-0.8, 0.8]:
                for ry in [-0.65, 0.65]:
                    self.buat_silinder(
                        f"Roda_{idx}_{rx}_{ry}", 0.28, 0.22, (rx, ry, 0.28),
                        rot=(math.radians(90), 0.0, 0.0), mat_nama="roda_hitam", parent=root,
                    )
            return root

        def bangun_kawasan_lengkap(self, data_makro):
            wx, wy = data_makro["ukuran_kawasan"]
            cx, cy = wx / 2.0, wy / 2.0
            y_j1, y_j2 = data_makro["zona_jalan_y"]
            lebar_jalan = abs(y_j2 - y_j1)
            y_tengah_jalan = (y_j1 + y_j2) / 2.0

            # 1. Hamparan Dasar Taman Rumput Hijau
            self.buat_kotak("Tanah_TamanRumput", [wx + 4.0, wy + 4.0, 0.20], (cx, cy, -0.10), mat_nama="rumput_taman")

            # 2. Jalan Raya Aspal & Trotoar Kiri-Kanan
            self.buat_kotak("JalanRaya_Aspal", [wx + 4.0, lebar_jalan, 0.06], (cx, y_tengah_jalan, 0.03), mat_nama="aspal_jalan")
            self.buat_kotak("Trotoar_Utara", [wx + 4.0, 2.2, 0.14], (cx, y_j2 + 1.1, 0.07), mat_nama="trotoar_paving")
            self.buat_kotak("Trotoar_Selatan", [wx + 4.0, 2.2, 0.14], (cx, y_j1 - 1.1, 0.07), mat_nama="trotoar_paving")

            # 3. Marka Jalan Putih Putus-putus
            for idx, m_xy in enumerate(data_makro["marka"]):
                self.buat_kotak(f"MarkaJalan_{idx:02d}", [2.2, 0.22, 0.02], (m_xy[0], y_tengah_jalan, 0.07), mat_nama="marka_jalan")

            # 4. Kolam Air Mancur Plasa di antara Gedung A & Gedung B
            if data_makro["kolam_cells"]:
                kx = sum(p[0] for p in data_makro["kolam_cells"]) / len(data_makro["kolam_cells"])
                ky = sum(p[1] for p in data_makro["kolam_cells"]) / len(data_makro["kolam_cells"])
                self.buat_silinder("Kolam_BingkaiBeton", 2.8, 0.35, (kx, ky, 0.175), mat_nama="slab_beton")
                self.buat_silinder("Kolam_Air", 2.5, 0.30, (kx, ky, 0.20), mat_nama="air_kolam")
                self.buat_silinder("Tugu_AirMancur", 0.35, 1.4, (kx, ky, 0.70), mat_nama="kaca_fasad")

            # 5. Bangun 3 Gedung 2 Lantai
            for g_spec in data_makro["gedung"]:
                self.bangun_gedung_dua_lantai(g_spec)

            # 6. Bangun Pohon, Lampu PJU, Bangku Taman, & Mobil LEGO
            for idx, p_xy in enumerate(data_makro["pohon"]):
                self.bangun_pohon_modular(idx + 1, p_xy)

            for idx, l_xy in enumerate(data_makro["lampu_jalan"]):
                arah_y = 1.0 if l_xy[1] < y_tengah_jalan else -1.0
                self.bangun_lampu_jalan_pju(idx + 1, l_xy, arah_y)

            for idx, b_xy in enumerate(data_makro["bangku"]):
                self.bangun_bangku_taman(idx + 1, b_xy)

            for idx, c_xy in enumerate(data_makro["mobil"]):
                self.bangun_mobil_lego(idx + 1, c_xy)

    # ==========================================================================
    # BAGIAN 5: APLIKASI INTERAKTIF SIDEBAR UI (TAB 'MacroLight M3')
    # ==========================================================================
    class MacroLightAppProps(bpy.types.PropertyGroup):
        preset_waktu: bpy.props.EnumProperty(
            name="Suasana Waktu",
            items=[
                ("DAY",    "Siang Hari (Daylight)",        "Matahari terang, lampu PJU mati"),
                ("SUNSET", "Sore / Golden Hour (Sunset)",  "Cahaya jingga hangat, PJU menyala"),
                ("NIGHT",  "Malam Hari (Night City)",      "Langit malam, lampu jalan & gedung bersinar"),
            ],
            default="SUNSET",
        )
        pju_aktif: bpy.props.BoolProperty(name="Nyalakan Lampu Jalan (Spot PJU)", default=True)
        interior_aktif: bpy.props.BoolProperty(name="Nyalakan Lampu Gedung (Point Lt.1 & 2)", default=True)
        sun_elevation: bpy.props.FloatProperty(name="Sudut Elevasi Matahari", default=38.0, min=5.0, max=88.0)
        sun_azimuth: bpy.props.FloatProperty(name="Sudut Putar Matahari (Z)", default=-35.0, min=-180.0, max=180.0)
        spawn_tipe: bpy.props.EnumProperty(
            name="Objek Taman/Jalan",
            items=[
                ("POHON", "Pohon Taman Modular", ""),
                ("PJU",   "Tiang Lampu Jalan (Spot Light)", ""),
                ("MOBIL", "Mobil LEGO Jalan Raya", ""),
            ],
            default="POHON",
        )
        spawn_xy: bpy.props.FloatVectorProperty(name="Posisi XY", default=(32.0, 12.0), size=2)

    class MACROLIGHT_OT_apply_lighting(bpy.types.Operator):
        bl_idname = "macrolight.apply_lighting"
        bl_label = "Terapkan Suasana Pencahayaan"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            props = context.scene.macrolight_props
            LightingRigManager.terapkan_preset_waktu(
                nama_preset=props.preset_waktu,
                pju_nyala=props.pju_aktif,
                interior_nyala=props.interior_aktif,
            )
            self.report({"INFO"}, f"Mode Pencahayaan '{props.preset_waktu}' berhasil diterapkan!")
            return {"FINISHED"}

    class MACROLIGHT_OT_rotate_sun(bpy.types.Operator):
        bl_idname = "macrolight.rotate_sun"
        bl_label = "Putar Arah Bayangan Matahari"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            props = context.scene.macrolight_props
            sun = bpy.data.objects.get("Sun_MatahariUtama")
            if sun:
                sun.rotation_euler = (
                    math.radians(90.0 - props.sun_elevation),
                    math.radians(12.0),
                    math.radians(props.sun_azimuth),
                )
            self.report({"INFO"}, "Sudut matahari & arah bayangan diperbarui!")
            return {"FINISHED"}

    class MACROLIGHT_OT_spawn_env_object(bpy.types.Operator):
        bl_idname = "macrolight.spawn_env_object"
        bl_label = "Tambah Objek ke Kawasan"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            props = context.scene.macrolight_props
            kol_utama = SceneManager.buat_koleksi("KawasanMakro_Modul3")
            kol_lampu = SceneManager.buat_koleksi("LightingRig_Modul3", kol_utama)
            builder = MacroAssetBuilder(TextureMaterialFactory(), CONFIG_MATERIAL_MODUL3, kol_utama, kol_lampu)
            xy = [props.spawn_xy[0], props.spawn_xy[1]]
            idx = len(bpy.data.objects) + 1
            if props.spawn_tipe == "POHON":
                obj = builder.bangun_pohon_modular(idx, xy)
            elif props.spawn_tipe == "PJU":
                obj = builder.bangun_lampu_jalan_pju(idx, xy, 1.0)
            else:
                obj = builder.bangun_mobil_lego(idx, xy)
            context.view_layer.objects.active = obj
            obj.select_set(True)
            self.report({"INFO"}, f"{obj.name} ditambahkan di ({xy[0]:.1f}, {xy[1]:.1f})")
            return {"FINISHED"}

    class MACROLIGHT_PT_main_panel(bpy.types.Panel):
        bl_label = "Modul 3: Lighting & Kawasan Makro"
        bl_idname = "MACROLIGHT_PT_main_panel"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "MacroLight M3"

        def draw(self, context):
            layout = self.layout
            props = context.scene.macrolight_props

            box1 = layout.box()
            box1.label(text="1. Simulasi Waktu & Environment", icon="WORLD")
            box1.prop(props, "preset_waktu")
            box1.prop(props, "pju_aktif")
            box1.prop(props, "interior_aktif")
            box1.operator("macrolight.apply_lighting", icon="LIGHT_SUN")

            box2 = layout.box()
            box2.label(text="2. Arah Directional Light (Matahari)", icon="ORIENTATION_GIMBAL")
            box2.prop(props, "sun_elevation")
            box2.prop(props, "sun_azimuth")
            box2.operator("macrolight.rotate_sun", icon="FILE_REFRESH")

            box3 = layout.box()
            box3.label(text="3. Tambah Objek Taman & Jalan", icon="SCENE_DATA")
            box3.prop(props, "spawn_tipe")
            box3.prop(props, "spawn_xy")
            box3.operator("macrolight.spawn_env_object", icon="ADD")

    KELAS_UI_MODUL3 = (
        MacroLightAppProps,
        MACROLIGHT_OT_apply_lighting,
        MACROLIGHT_OT_rotate_sun,
        MACROLIGHT_OT_spawn_env_object,
        MACROLIGHT_PT_main_panel,
    )

    def register_modul3_ui():
        for cls in KELAS_UI_MODUL3:
            try:
                bpy.utils.unregister_class(cls)
            except Exception:
                pass
            bpy.utils.register_class(cls)
        bpy.types.Scene.macrolight_props = bpy.props.PointerProperty(type=MacroLightAppProps)

# ==============================================================================
# BAGIAN 6: ORKESTRASI UTAMA & PENGATURAN KAMERA MAKRO
# ==============================================================================
def atur_kamera_dan_viewport_makro(ukuran_kawasan):
    if not BLENDER_AVAILABLE:
        return
    wx, wy = ukuran_kawasan
    cx, cy = wx / 2.0, wy / 2.0

    bpy.ops.object.camera_add(location=(cx - 12.0, -wy * 0.55, 22.0))
    cam = bpy.context.active_object
    cam.name = "Kamera_Masterplan_M3"
    cam.rotation_euler = (math.radians(56), 0.0, math.radians(-14))
    cam.data.lens = 28.0
    bpy.context.scene.camera = cam

    # Aktifkan mode shading MATERIAL atau RENDERED beserta Scene Lights & World
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "RENDERED"
                    space.shading.use_scene_lights_render = True
                    space.shading.use_scene_world_render = True

def jalankan_modul_3(ascii_makro=PETA_MAKRO_ASCII):
    parser = AsciiMacroParser(scale=SKALA_MAKRO_METER)
    data_makro = parser.parse(ascii_makro)

    if BLENDER_AVAILABLE:
        SceneManager.bersihkan_scene()
        kol_utama = SceneManager.buat_koleksi("KawasanMakro_Modul3")
        kol_lampu = SceneManager.buat_koleksi("LightingRig_Modul3", kol_utama)

        LightingRigManager.bangun_world_sky()
        LightingRigManager.bangun_matahari_dan_area_plasa(data_makro["ukuran_kawasan"], kol_lampu)

        builder = MacroAssetBuilder(TextureMaterialFactory(), CONFIG_MATERIAL_MODUL3, kol_utama, kol_lampu)
        builder.bangun_kawasan_lengkap(data_makro)

        # Set default ke suasana Sore / Golden Hour agar efek lampu jalan & matahari terlihat dramatis
        LightingRigManager.terapkan_preset_waktu("SUNSET", pju_nyala=True, interior_nyala=True)
        atur_kamera_dan_viewport_makro(data_makro["ukuran_kawasan"])
        register_modul3_ui()

        print(
            f"MATERI 3 OK: Kawasan {data_makro['ukuran_kawasan'][0]}x{data_makro['ukuran_kawasan'][1]}m "
            f"({len(data_makro['gedung'])} Gedung 2 Lantai, {len(data_makro['pohon'])} Pohon, "
            f"{len(data_makro['lampu_jalan'])} Lampu Jalan SpotLight) berhasil dibangun!"
        )
    return data_makro

if __name__ == "__main__":
    jalankan_modul_3(PETA_MAKRO_ASCII)