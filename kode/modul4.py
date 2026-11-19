#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODUL 4 KOMPUTER GRAFIK (V6) - VIRTUAL CAMERA, ANIMATION, MP4 RENDER & WEB GLB
File: modul4_kamera_animasi_citytour.py (Kompatibel Penuh Blender 4.3)

Fokus Materi 4:
  1. CameraRigManager     : Pengelolaan 4 kamera virtual dengan proyeksi berbeda:
                            - Cam_Drone_Orbit     (Perspektif 24mm + Follow Path Spline)
                            - Cam_Street_EyeLevel (Perspektif 35mm + Depth of Field Bokeh)
                            - Cam_Isometric_Ortho (Proyeksi Ortografis Isometrik)
                            - Cam_Car_Dashcam     (Kamera Hierarki di atas Mobil LEGO)
  2. SplinePathBuilder    : Pembuatan kurva Bezier 3D tertutup untuk jalur tur udara
                            dengan constraint FOLLOW_PATH dan TRACK_TO.
  3. KeyframeAnimator     : Implementasi interpolasi F-Curve (LINEAR vs BEZIER):
                            - Lift Kaca Gedung A naik-turun Lt.1 <-> Lt.2 (BEZIER)
                            - Mobil LEGO + Headlight Spot melaju & berputar (LINEAR)
                            - Kipas HVAC atap 3 gedung berputar konstan (LINEAR)
                            - Siklus Matahari & Lampu Jalan Siang-Malam (240 Frame)
  4. ExportPipelineManager: Render otomatis ke video MP4 (FFmpeg H.264) dan
                            ekspor kawasan makro 3D ke format Web .GLB (glTF 2.0).
  5. CityTourApp (UI)     : Panel Aplikasi Interaktif di Sidebar 3D Viewport
                            (Tekan 'N' -> tab 'CityTour M4').
================================================================================
"""

import math
import os
import tempfile

# ==============================================================================
# BAGIAN 1: KONFIGURASI KAWASAN MAKRO & PARAMETER ANIMASI (240 FRAME @ 24 FPS)
# ==============================================================================
SKALA_MAKRO_METER = 1.0
TINGGI_PER_LANTAI = 3.2
TEBAL_DINDING     = 0.18
TEBAL_SLAB_LANTAI = 0.22
TOTAL_FRAMES      = 240   # Durasi loop animasi = 10 detik (24 fps)

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

CONFIG_MATERIAL_MODUL4 = {
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
        "emission": [0.95, 0.85, 0.55, 1.0], "emission_strength": 1.20
    },
    "kaca_lift": {
        "rgba": [0.40, 0.85, 0.98, 1.0], "roughness": 0.05, "metallic": 0.20,
        "emission": [0.25, 0.75, 1.0, 1.0], "emission_strength": 1.80
    },
    "kusen_hitam": {"rgba": [0.15, 0.17, 0.20, 1.0], "roughness": 0.30, "metallic": 0.75},
    "aspal_jalan": {
        "rgba": [0.16, 0.17, 0.19, 1.0], "roughness": 0.88,
        "tex_type": "NOISE", "uv_scale": [25.0, 25.0, 1.0], "bump": 0.30
    },
    "marka_jalan": {
        "rgba": [0.96, 0.96, 0.92, 1.0], "roughness": 0.40,
        "emission": [0.95, 0.95, 0.85, 1.0], "emission_strength": 0.40
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
        "emission": [1.0, 0.88, 0.60, 1.0], "emission_strength": 8.0
    },
    "lampu_mobil": {
        "rgba": [1.0, 0.98, 0.85, 1.0], "roughness": 0.10,
        "emission": [1.0, 0.96, 0.80, 1.0], "emission_strength": 10.0
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
# BAGIAN 2: PARSER KAWASAN MAKRO ASCII
# ==============================================================================
class AsciiMacroParser:
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

        visited = [[False] * W for _ in range(H)]
        buildings = []
        building_cells = set()

        for r in range(H):
            for c in range(W):
                if grid[r][c] == "+" and not visited[r][c]:
                    c2 = c + 1
                    while c2 < W and grid[r][c2] == "-":
                        c2 += 1
                    if c2 < W and grid[r][c2] == "+":
                        r2 = r + 1
                        while r2 < H and grid[r2][c] == "|":
                            r2 += 1
                        if r2 < H and grid[r2][c] == "+":
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

        pohon_list, lampu_jalan_list, bangku_list, kolam_cells, mobil_list, marka_list = [], [], [], [], [], []
        jalan_rows = set()

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
                elif ch == "T":
                    pohon_list.append([x, y])
                elif ch == "L":
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
# BAGIAN 3: ENGINE BLENDER 4.3 (TRANSFORM, SHADER, LIGHTING, CAMERA & EXPORT)
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
    # 2. SceneManager & Box UV
    # --------------------------------------------------------------------------
    class SceneManager:
        @staticmethod
        def bersihkan_scene():
            if bpy.context.active_object and bpy.context.active_object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.object.delete()
            for block_list in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.actions):
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
    # 3. TextureMaterialFactory
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
    # 4. LightingRigManager
    # --------------------------------------------------------------------------
    class LightingRigManager:
        @classmethod
        def bangun_world_dan_lampu(cls, ukuran_kawasan, koleksi_lampu):
            scene = bpy.context.scene
            if not scene.world:
                scene.world = bpy.data.worlds.new("World_Makro_M4")
            world = scene.world
            world.use_nodes = True
            nodes = world.node_tree.nodes
            links = world.node_tree.links
            nodes.clear()

            out_node = nodes.new(type="ShaderNodeOutputWorld")
            bg_node = nodes.new(type="ShaderNodeBackground")
            bg_node.name = "World_BG"
            bg_node.inputs["Color"].default_value = (0.85, 0.42, 0.25, 1.0)
            bg_node.inputs["Strength"].default_value = 0.75
            links.new(bg_node.outputs["Background"], out_node.inputs["Surface"])

            # Compositor Glare (Bloom) untuk efek pendar lampu malam di Blender 4.3
            scene.use_nodes = True
            c_nodes = scene.node_tree.nodes
            c_links = scene.node_tree.links
            c_nodes.clear()
            rl = c_nodes.new(type="CompositorNodeRLayers")
            glare = c_nodes.new(type="CompositorNodeGlare")
            glare.glare_type = "FOG_GLOW"
            glare.quality = "MEDIUM"
            glare.threshold = 1.2
            comp_out = c_nodes.new(type="CompositorNodeComposite")
            c_links.new(rl.outputs["Image"], glare.inputs["Image"])
            c_links.new(glare.outputs["Image"], comp_out.inputs["Image"])

            wx, wy = ukuran_kawasan
            cx, cy = wx / 2.0, wy / 2.0

            light_data = bpy.data.lights.new(name="Sun_MatahariUtama", type="SUN")
            light_data.energy = 2.8
            light_data.color = (1.0, 0.52, 0.22)
            sun_obj = bpy.data.objects.new(name="Sun_MatahariUtama", object_data=light_data)
            bpy.context.scene.collection.objects.link(sun_obj)
            Transform3DEngine.terapkan_matriks(
                sun_obj,
                lokasi=(cx, cy, 35.0),
                rotasi_euler=(math.radians(74), math.radians(12), math.radians(-65)),
            )
            SceneManager.pindahkan_ke_koleksi(sun_obj, koleksi_lampu)

    # --------------------------------------------------------------------------
    # 5. KeyframeAnimator: Interpolasi LINEAR vs BEZIER
    # --------------------------------------------------------------------------
    class KeyframeAnimator:
        @staticmethod
        def set_interpolasi_fcurve(obj_atau_data, mode="LINEAR"):
            if not obj_atau_data or not obj_atau_data.animation_data or not obj_atau_data.animation_data.action:
                return
            for fcurve in obj_atau_data.animation_data.action.fcurves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = mode

        @classmethod
        def animasikan_lift_gedung(cls, kabin_obj, z_lantai1=0.35, z_lantai2=3.55, total_frames=240):
            x0, y0, _ = kabin_obj.location
            jadwal = [
                (1,   z_lantai1),
                (30,  z_lantai1),
                (95,  z_lantai2),
                (145, z_lantai2),
                (210, z_lantai1),
                (total_frames, z_lantai1),
            ]
            for frame, z_val in jadwal:
                kabin_obj.location = (x0, y0, z_val)
                kabin_obj.keyframe_insert(data_path="location", frame=frame)
            cls.set_interpolasi_fcurve(kabin_obj, mode="BEZIER")

        @classmethod
        def animasikan_mobil_lalu_lintas(cls, mobil_root, roda_list, x_mulai, x_akhir, total_frames=240):
            _, y0, z0 = mobil_root.location
            jarak = abs(x_akhir - x_mulai)
            radius_roda = 0.28
            sudut_putar_total = jarak / radius_roda

            mobil_root.location = (x_mulai, y0, z0)
            mobil_root.keyframe_insert(data_path="location", frame=1)

            mobil_root.location = (x_akhir, y0, z0)
            mobil_root.keyframe_insert(data_path="location", frame=total_frames)
            cls.set_interpolasi_fcurve(mobil_root, mode="LINEAR")

            arah_putar = 1.0 if x_akhir > x_mulai else -1.0
            for roda in roda_list:
                roda.rotation_euler = (math.radians(90), 0.0, 0.0)
                roda.keyframe_insert(data_path="rotation_euler", frame=1)
                roda.rotation_euler = (math.radians(90), arah_putar * sudut_putar_total, 0.0)
                roda.keyframe_insert(data_path="rotation_euler", frame=total_frames)
                cls.set_interpolasi_fcurve(roda, mode="LINEAR")

        @classmethod
        def animasikan_kipas_hvac(cls, kipas_obj, putaran_penuh=8, total_frames=240):
            kipas_obj.rotation_euler = (0.0, 0.0, 0.0)
            kipas_obj.keyframe_insert(data_path="rotation_euler", frame=1)
            kipas_obj.rotation_euler = (0.0, 0.0, math.pi * 2.0 * putaran_penuh)
            kipas_obj.keyframe_insert(data_path="rotation_euler", frame=total_frames)
            cls.set_interpolasi_fcurve(kipas_obj, mode="LINEAR")

        @classmethod
        def bake_siklus_siang_malam(cls, total_frames=240):
            sun = bpy.data.objects.get("Sun_MatahariUtama")
            if sun:
                tahap_sun = [
                    (1,   3.5, (1.0, 0.96, 0.88), (35.0,  15.0, -30.0)),
                    (110, 2.8, (1.0, 0.50, 0.20), (76.0,  12.0, -65.0)),
                    (170, 0.2, (0.45, 0.62, 0.95), (45.0, -20.0,  25.0)),
                    (total_frames, 0.2, (0.45, 0.62, 0.95), (45.0, -20.0,  25.0)),
                ]
                for f, energy, col, rot_deg in tahap_sun:
                    sun.data.energy = energy
                    sun.data.color = col
                    sun.data.keyframe_insert(data_path="energy", frame=f)
                    sun.data.keyframe_insert(data_path="color", frame=f)

                    sun.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
                    sun.keyframe_insert(data_path="rotation_euler", frame=f)

            # Keyframe warna langit World Background mengikuti fase waktu
            # (tanpa ini langit tetap jingga senja permanen saat malam)
            world = bpy.context.scene.world
            if world and world.use_nodes:
                bg = world.node_tree.nodes.get("World_BG")
                if bg:
                    tahap_sky = [
                        (1,   (0.55, 0.70, 0.95, 1.0), 1.00),   # siang biru
                        (110, (0.85, 0.42, 0.25, 1.0), 0.75),   # senja jingga
                        (170, (0.02, 0.04, 0.09, 1.0), 0.20),   # malam gelap
                        (total_frames, (0.02, 0.04, 0.09, 1.0), 0.20),
                    ]
                    for f, col_sky, strength_sky in tahap_sky:
                        bg.inputs["Color"].default_value = col_sky
                        bg.inputs["Strength"].default_value = strength_sky
                        bg.inputs["Color"].keyframe_insert("default_value", frame=f)
                        bg.inputs["Strength"].keyframe_insert("default_value", frame=f)

            for obj in bpy.data.objects:
                if obj.type == "LIGHT" and obj.name.startswith("Spot_PJU"):
                    obj.data.energy = 0.0
                    obj.data.keyframe_insert(data_path="energy", frame=1)
                    obj.data.energy = 0.0
                    obj.data.keyframe_insert(data_path="energy", frame=85)
                    obj.data.energy = 900.0
                    obj.data.keyframe_insert(data_path="energy", frame=130)
                    obj.data.energy = 900.0
                    obj.data.keyframe_insert(data_path="energy", frame=total_frames)

    # --------------------------------------------------------------------------
    # 6. CameraRigManager & SplinePathBuilder
    # --------------------------------------------------------------------------
    class CameraRigManager:
        @classmethod
        def buat_kurva_drone_elips(cls, pusat_xy, radius_x, radius_y, ketinggian_z, koleksi_cam, total_frames=240):
            cx, cy = pusat_xy
            curve_data = bpy.data.curves.new(name="Spline_DroneTour", type="CURVE")
            curve_data.dimensions = "3D"
            curve_data.use_path = True
            curve_data.path_duration = total_frames

            spline = curve_data.splines.new(type="BEZIER")
            jml_titik = 8
            spline.bezier_points.add(jml_titik - 1)

            for i in range(jml_titik):
                theta = (2.0 * math.pi * i) / jml_titik
                px = cx + radius_x * math.cos(theta)
                py = cy + radius_y * math.sin(theta)
                pz = ketinggian_z + 2.5 * math.sin(theta * 2.0)
                bp = spline.bezier_points[i]
                bp.co = (px, py, pz)
                bp.handle_left_type = "AUTO"
                bp.handle_right_type = "AUTO"

            spline.use_cyclic_u = True

            curve_obj = bpy.data.objects.new(name="Spline_DroneTour", object_data=curve_data)
            bpy.context.scene.collection.objects.link(curve_obj)
            SceneManager.pindahkan_ke_koleksi(curve_obj, koleksi_cam)

            curve_data.eval_time = 0.0
            curve_data.keyframe_insert(data_path="eval_time", frame=1)
            curve_data.eval_time = float(total_frames)
            curve_data.keyframe_insert(data_path="eval_time", frame=total_frames)
            KeyframeAnimator.set_interpolasi_fcurve(curve_data, mode="LINEAR")
            return curve_obj

        @classmethod
        def bangun_semua_kamera(cls, ukuran_kawasan, koleksi_cam, mobil_utama=None, total_frames=240):
            wx, wy = ukuran_kawasan
            cx, cy = wx / 2.0, wy / 2.0

            target_focus = bpy.data.objects.new("Target_PlasaFocus", None)
            target_focus.empty_display_type = "SPHERE"
            target_focus.empty_display_size = 0.8
            bpy.context.scene.collection.objects.link(target_focus)
            Transform3DEngine.terapkan_matriks(target_focus, lokasi=(cx, cy + 2.0, 2.5))
            SceneManager.pindahkan_ke_koleksi(target_focus, koleksi_cam)

            # 1. Cam_Drone_Orbit
            spline_drone = cls.buat_kurva_drone_elips(
                pusat_xy=(cx, cy),
                radius_x=wx * 0.44,
                radius_y=wy * 0.46,
                ketinggian_z=14.5,
                koleksi_cam=koleksi_cam,
                total_frames=total_frames,
            )
            cam1_data = bpy.data.cameras.new("Cam_Drone_Orbit")
            cam1_data.type = "PERSP"
            cam1_data.lens = 24.0
            cam1_data.clip_end = 500.0
            cam1 = bpy.data.objects.new("Cam_Drone_Orbit", cam1_data)
            cam1.location = (0.0, 0.0, 0.0)
            bpy.context.scene.collection.objects.link(cam1)
            SceneManager.pindahkan_ke_koleksi(cam1, koleksi_cam)

            c_follow = cam1.constraints.new(type="FOLLOW_PATH")
            c_follow.target = spline_drone
            c_track = cam1.constraints.new(type="TRACK_TO")
            c_track.target = target_focus
            c_track.track_axis = "TRACK_NEGATIVE_Z"
            c_track.up_axis = "UP_Y"

            # 2. Cam_Street_EyeLevel
            cam2_data = bpy.data.cameras.new("Cam_Street_EyeLevel")
            cam2_data.type = "PERSP"
            cam2_data.lens = 35.0
            cam2_data.dof.use_dof = True
            cam2_data.dof.focus_object = target_focus
            cam2_data.dof.aperture_fstop = 2.0
            cam2 = bpy.data.objects.new("Cam_Street_EyeLevel", cam2_data)
            bpy.context.scene.collection.objects.link(cam2)
            Transform3DEngine.terapkan_matriks(cam2, lokasi=(6.0, cy - 3.2, 1.75))
            # Aim kamera tepat ke Target_PlasaFocus agar bidang fokus DOF jatuh di subjek
            arah_street = (Vector((cx, cy + 2.0, 2.5)) - Vector((6.0, cy - 3.2, 1.75))).normalized()
            cam2.rotation_euler = arah_street.to_track_quat("-Z", "Y").to_euler()
            SceneManager.pindahkan_ke_koleksi(cam2, koleksi_cam)

            # 3. Cam_Isometric_Ortho
            cam3_data = bpy.data.cameras.new("Cam_Isometric_Ortho")
            cam3_data.type = "ORTHO"
            cam3_data.ortho_scale = max(wx, wy) * 0.95
            cam3 = bpy.data.objects.new("Cam_Isometric_Ortho", cam3_data)
            bpy.context.scene.collection.objects.link(cam3)
            Transform3DEngine.terapkan_matriks(
                cam3,
                lokasi=(cx - 28.0, cy - 28.0, 32.0),
                rotasi_euler=(math.radians(54.736), 0.0, math.radians(-45.0)),
            )
            SceneManager.pindahkan_ke_koleksi(cam3, koleksi_cam)

            # 4. Cam_Car_Dashcam
            cam4_data = bpy.data.cameras.new("Cam_Car_Dashcam")
            cam4_data.type = "PERSP"
            cam4_data.lens = 22.0
            cam4 = bpy.data.objects.new("Cam_Car_Dashcam", cam4_data)
            bpy.context.scene.collection.objects.link(cam4)
            # Dashcam memandang ke DEPAN mobil (sumbu +X lokal) sedikit menunduk
            arah_dash = Vector((1.0, 0.0, -0.10)).normalized()
            Transform3DEngine.terapkan_matriks(
                cam4,
                lokasi=(1.0, 0.0, 1.32),
                rotasi_euler=arah_dash.to_track_quat("-Z", "Y").to_euler(),
                parent=mobil_utama,
            )
            SceneManager.pindahkan_ke_koleksi(cam4, koleksi_cam)

            bpy.context.scene.camera = cam1
            return cam1

    # --------------------------------------------------------------------------
    # 7. ExportPipelineManager: Render Video MP4 (FFmpeg H.264) & Web 3D (.GLB)
    # --------------------------------------------------------------------------
    class ExportPipelineManager:
        """
        MATERI 4 - RENDERING PIPELINE & WEB 3D EXPORT:
          1. resolve_output_dir() : Menentukan folder simpan aman (folder .blend
                                    jika sudah tersimpan, atau Desktop/Temp jika belum).
          2. render_animasi_mp4() : Merender timeline 1..240 ke MP4 (H.264 + EEVEE).
          3. export_web_glb()     : Mengekspor seluruh scene (Mesh, Hierarki, Animasi,
                                    Kamera & Lampu) ke format biner glTF 2.0 (.glb).
        """

        @staticmethod
        def resolve_output_dir(custom_dir=""):
            if custom_dir and custom_dir.strip():
                abs_dir = bpy.path.abspath(custom_dir.strip())
                os.makedirs(abs_dir, exist_ok=True)
                return abs_dir
            if bpy.data.filepath:
                return os.path.dirname(bpy.data.filepath)
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if os.path.isdir(desktop):
                return desktop
            return tempfile.gettempdir()

        @classmethod
        def render_animasi_mp4(cls, output_dir="", resolusi="720P"):
            scene = bpy.context.scene
            target_dir = cls.resolve_output_dir(output_dir)
            mp4_path = os.path.join(target_dir, "CityTour_Modul4.mp4")

            # Resolusi video
            if resolusi == "1080P":
                scene.render.resolution_x = 1920
                scene.render.resolution_y = 1080
            else:
                scene.render.resolution_x = 1280
                scene.render.resolution_y = 720
            scene.render.resolution_percentage = 100

            # Konfigurasi FFmpeg MPEG-4 / H.264 di Blender 4.3
            scene.render.image_settings.file_format = "FFMPEG"
            scene.render.ffmpeg.format = "MPEG4"
            scene.render.ffmpeg.codec = "H264"
            scene.render.ffmpeg.constant_rate_factor = "HIGH"
            scene.render.ffmpeg.ffmpeg_preset = "GOOD"
            scene.render.filepath = mp4_path

            # Jalankan render animasi dengan jendela progres live
            bpy.ops.render.render("INVOKE_DEFAULT", animation=True)
            return mp4_path

        @classmethod
        def export_web_glb(cls, output_dir="", sertakan_animasi=True):
            target_dir = cls.resolve_output_dir(output_dir)
            glb_path = os.path.join(target_dir, "KawasanMakro_Modul4.glb")

            # Pastikan mode OBJECT sebelum ekspor glTF
            if bpy.context.active_object and bpy.context.active_object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")

            try:
                bpy.ops.export_scene.gltf(
                    filepath=glb_path,
                    export_format="GLB",
                    use_selection=False,
                    export_yup=True,
                    export_cameras=True,
                    export_lights=True,
                    export_animations=sertakan_animasi,
                )
            except TypeError:
                # Fallback jika versi add-on glTF memiliki perbedaan parameter minor
                bpy.ops.export_scene.gltf(
                    filepath=glb_path,
                    export_format="GLB",
                    export_animations=sertakan_animasi,
                )
            return glb_path

    # --------------------------------------------------------------------------
    # 8. MacroAnimatedBuilder: Membangun 3 Gedung 2 Lantai + Lift + Mobil + HVAC
    # --------------------------------------------------------------------------
    class MacroAnimatedBuilder:
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

        def bangun_gedung_dua_lantai(self, spec_gedung, total_frames=240):
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

            root_g = bpy.data.objects.new(nama_g, None)
            bpy.context.scene.collection.objects.link(root_g)
            Transform3DEngine.terapkan_matriks(root_g, lokasi=(cx, cy, 0.0))
            SceneManager.pindahkan_ke_koleksi(root_g, self.kol_utama)

            for lt in range(jml_lantai):
                z_base = lt * TINGGI_PER_LANTAI
                z_mid = z_base + TINGGI_PER_LANTAI / 2.0

                self.buat_kotak(f"{nama_g}_Slab_Lt{lt+1}", [wx + 0.3, wy + 0.3, TEBAL_SLAB_LANTAI], (0.0, 0.0, z_base + TEBAL_SLAB_LANTAI / 2.0), mat_nama="slab_beton", parent=root_g)
                self.buat_kotak(f"{nama_g}_Lantai_Lt{lt+1}", [wx - 0.2, wy - 0.2, 0.06], (0.0, 0.0, z_base + TEBAL_SLAB_LANTAI + 0.03), mat_nama="lantai_interior", parent=root_g)

                for s_idx, y_off in enumerate([-wy / 2.0, wy / 2.0]):
                    self.buat_kotak(f"{nama_g}_DindingNS_{lt+1}_{s_idx}_B", [wx, TEBAL_DINDING, 0.95], (0.0, y_off, z_base + 0.475), mat_nama=mat_eks, parent=root_g)
                    self.buat_kotak(f"{nama_g}_DindingNS_{lt+1}_{s_idx}_A", [wx, TEBAL_DINDING, 0.65], (0.0, y_off, z_base + TINGGI_PER_LANTAI - 0.325), mat_nama=mat_eks, parent=root_g)
                    self.buat_kotak(f"{nama_g}_KacaNS_{lt+1}_{s_idx}", [wx - 1.6, 0.06, 1.60], (0.0, y_off, z_base + 1.75), mat_nama="kaca_fasad", parent=root_g)
                    for px in [-wx / 2.0 + 0.4, 0.0, wx / 2.0 - 0.4]:
                        self.buat_kotak(f"{nama_g}_PilarNS_{lt+1}_{s_idx}_{px:.1f}", [0.45, TEBAL_DINDING + 0.08, TINGGI_PER_LANTAI], (px, y_off, z_mid), mat_nama="kusen_hitam", parent=root_g)

                for s_idx, x_off in enumerate([-wx / 2.0, wx / 2.0]):
                    self.buat_kotak(f"{nama_g}_DindingEW_{lt+1}_{s_idx}", [TEBAL_DINDING, wy, TINGGI_PER_LANTAI], (x_off, 0.0, z_mid), mat_nama=mat_eks, parent=root_g)

                for lx in [-wx * 0.25, wx * 0.25]:
                    pt_data = bpy.data.lights.new(name=f"Point_Lantai{lt+1}_{nama_g}_{lx:.1f}", type="POINT")
                    pt_data.energy = 180.0
                    pt_data.color = (1.0, 0.92, 0.78)
                    pt_obj = bpy.data.objects.new(name=pt_data.name, object_data=pt_data)
                    bpy.context.scene.collection.objects.link(pt_obj)
                    Transform3DEngine.terapkan_matriks(pt_obj, lokasi=(lx, 0.0, z_base + TINGGI_PER_LANTAI - 0.45), parent=root_g)
                    SceneManager.pindahkan_ke_koleksi(pt_obj, self.kol_lampu)

            z_atap = jml_lantai * TINGGI_PER_LANTAI
            self.buat_kotak(f"{nama_g}_DakAtap", [wx + 0.5, wy + 0.5, 0.28], (0.0, 0.0, z_atap + 0.14), mat_nama="slab_beton", parent=root_g)
            self.buat_kotak(f"{nama_g}_UnitHVAC", [2.2, 1.4, 0.9], (wx * 0.2, 0.0, z_atap + 0.70), mat_nama="tiang_lampu", parent=root_g)
            kipas = self.buat_kotak(f"{nama_g}_KipasHVAC", [1.3, 0.18, 0.08], (wx * 0.2, 0.0, z_atap + 1.22), mat_nama="kaca_lift", parent=root_g)
            KeyframeAnimator.animasikan_kipas_hvac(kipas, putaran_penuh=10, total_frames=total_frames)

            if "Gedung_A" in nama_g:
                self.buat_kotak("ShaftLift_GedungA", [0.15, 1.8, z_atap + 0.4], (wx / 2.0 + 0.85, 0.0, (z_atap + 0.4) / 2.0), mat_nama="kusen_hitam", parent=root_g)
                kabin_lift = self.buat_kotak("KabinLift_GedungA", [1.4, 1.5, 2.2], (wx / 2.0 + 0.75, 0.0, 1.3), mat_nama="kaca_lift", parent=root_g)
                KeyframeAnimator.animasikan_lift_gedung(kabin_lift, z_lantai1=1.35, z_lantai2=1.35 + TINGGI_PER_LANTAI, total_frames=total_frames)

            return root_g

        def bangun_pohon_modular(self, idx, xy):
            root = bpy.data.objects.new(f"Pohon_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(xy[0], xy[1], 0.0))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)
            self.buat_silinder(f"Batang_{idx}", 0.22, 1.8, (0.0, 0.0, 0.9), mat_nama="batang_pohon", parent=root)
            self.buat_kotak(f"Daun1_{idx}", [1.8, 1.8, 1.1], (0.0, 0.0, 2.1), mat_nama="daun_pohon", parent=root)
            self.buat_kotak(f"Daun2_{idx}", [1.3, 1.3, 0.9], (0.0, 0.0, 2.9), rot=(0.0, 0.0, math.radians(45)), mat_nama="daun_pohon", parent=root)
            return root

        def bangun_lampu_jalan_pju(self, idx, xy, arah_y):
            root = bpy.data.objects.new(f"TiangPJU_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(xy[0], xy[1], 0.0), rotasi_euler=(0.0, 0.0, 0.0 if arah_y > 0 else math.pi))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)

            self.buat_silinder(f"Tiang_{idx}", 0.10, 4.8, (0.0, 0.0, 2.4), mat_nama="tiang_lampu", parent=root)
            self.buat_kotak(f"LenganPJU_{idx}", [0.16, 1.3, 0.14], (0.0, 0.55, 4.75), mat_nama="tiang_lampu", parent=root)
            self.buat_kotak(f"BohlamPJU_{idx}", [0.38, 0.55, 0.10], (0.0, 1.05, 4.65), mat_nama="bohlam_lampu", parent=root)

            sp_data = bpy.data.lights.new(name=f"Spot_PJU_{idx:02d}", type="SPOT")
            sp_data.energy = 450.0
            sp_data.color = (1.0, 0.85, 0.55)
            sp_data.spot_size = math.radians(78.0)
            sp_data.spot_blend = 0.45
            sp_obj = bpy.data.objects.new(name=sp_data.name, object_data=sp_data)
            bpy.context.scene.collection.objects.link(sp_obj)
            Transform3DEngine.terapkan_matriks(sp_obj, lokasi=(0.0, 1.05, 4.55), rotasi_euler=(math.radians(15), 0.0, 0.0), parent=root)
            SceneManager.pindahkan_ke_koleksi(sp_obj, self.kol_lampu)
            return root

        def bangun_mobil_animated(self, idx, y_jalur, x_start, x_end, total_frames=240):
            warna = "mobil_merah" if idx == 1 else "mobil_biru"
            arah_x = 1.0 if x_end > x_start else -1.0
            rot_z = 0.0 if arah_x > 0 else math.pi

            root = bpy.data.objects.new(f"MobilLego_{idx:02d}", None)
            bpy.context.scene.collection.objects.link(root)
            Transform3DEngine.terapkan_matriks(root, lokasi=(x_start, y_jalur, 0.0), rotasi_euler=(0.0, 0.0, rot_z))
            SceneManager.pindahkan_ke_koleksi(root, self.kol_utama)

            self.buat_kotak(f"BodiBawah_{idx}", [2.6, 1.3, 0.50], (0.0, 0.0, 0.40), mat_nama=warna, parent=root)
            self.buat_kotak(f"KabinAtas_{idx}", [1.4, 1.15, 0.45], (-0.15, 0.0, 0.85), mat_nama="kaca_fasad", parent=root)
            self.buat_kotak(f"HeadlightL_{idx}", [0.12, 0.25, 0.16], (1.32, 0.42, 0.45), mat_nama="lampu_mobil", parent=root)
            self.buat_kotak(f"HeadlightR_{idx}", [0.12, 0.25, 0.16], (1.32, -0.42, 0.45), mat_nama="lampu_mobil", parent=root)

            hl_data = bpy.data.lights.new(name=f"Spot_Mobil_{idx}", type="SPOT")
            hl_data.energy = 600.0
            hl_data.color = (1.0, 0.96, 0.82)
            hl_data.spot_size = math.radians(55.0)
            hl_obj = bpy.data.objects.new(name=hl_data.name, object_data=hl_data)
            bpy.context.scene.collection.objects.link(hl_obj)
            Transform3DEngine.terapkan_matriks(hl_obj, lokasi=(1.4, 0.0, 0.5), rotasi_euler=(math.radians(82), 0.0, math.radians(-90)), parent=root)
            SceneManager.pindahkan_ke_koleksi(hl_obj, self.kol_lampu)

            roda_list = []
            for rx in [-0.8, 0.8]:
                for ry in [-0.65, 0.65]:
                    r_obj = self.buat_silinder(
                        f"Roda_{idx}_{rx}_{ry}", 0.28, 0.22, (rx, ry, 0.28),
                        rot=(math.radians(90), 0.0, 0.0), mat_nama="roda_hitam", parent=root,
                    )
                    roda_list.append(r_obj)

            KeyframeAnimator.animasikan_mobil_lalu_lintas(root, roda_list, x_start, x_end, total_frames=total_frames)
            return root

        def bangun_kawasan_lengkap(self, data_makro, total_frames=240):
            wx, wy = data_makro["ukuran_kawasan"]
            cx, cy = wx / 2.0, wy / 2.0
            y_j1, y_j2 = data_makro["zona_jalan_y"]
            lebar_jalan = abs(y_j2 - y_j1)
            y_tengah_jalan = (y_j1 + y_j2) / 2.0

            self.buat_kotak("Tanah_TamanRumput", [wx + 4.0, wy + 4.0, 0.20], (cx, cy, -0.10), mat_nama="rumput_taman")
            self.buat_kotak("JalanRaya_Aspal", [wx + 4.0, lebar_jalan, 0.06], (cx, y_tengah_jalan, 0.03), mat_nama="aspal_jalan")
            self.buat_kotak("Trotoar_Utara", [wx + 4.0, 2.2, 0.14], (cx, y_j2 + 1.1, 0.07), mat_nama="trotoar_paving")
            self.buat_kotak("Trotoar_Selatan", [wx + 4.0, 2.2, 0.14], (cx, y_j1 - 1.1, 0.07), mat_nama="trotoar_paving")

            for idx, m_xy in enumerate(data_makro["marka"]):
                self.buat_kotak(f"MarkaJalan_{idx:02d}", [2.2, 0.22, 0.02], (m_xy[0], y_tengah_jalan, 0.07), mat_nama="marka_jalan")

            if data_makro["kolam_cells"]:
                kx = sum(p[0] for p in data_makro["kolam_cells"]) / len(data_makro["kolam_cells"])
                ky = sum(p[1] for p in data_makro["kolam_cells"]) / len(data_makro["kolam_cells"])
                self.buat_silinder("Kolam_BingkaiBeton", 2.8, 0.35, (kx, ky, 0.175), mat_nama="slab_beton")
                self.buat_silinder("Kolam_Air", 2.5, 0.30, (kx, ky, 0.20), mat_nama="air_kolam")
                self.buat_silinder("Tugu_AirMancur", 0.35, 1.4, (kx, ky, 0.70), mat_nama="kaca_fasad")

            for g_spec in data_makro["gedung"]:
                self.bangun_gedung_dua_lantai(g_spec, total_frames=total_frames)

            for idx, p_xy in enumerate(data_makro["pohon"]):
                self.bangun_pohon_modular(idx + 1, p_xy)

            for idx, l_xy in enumerate(data_makro["lampu_jalan"]):
                arah_y = 1.0 if l_xy[1] < y_tengah_jalan else -1.0
                self.bangun_lampu_jalan_pju(idx + 1, l_xy, arah_y)

            mobil_1 = self.bangun_mobil_animated(1, y_tengah_jalan - 0.85, x_start=2.0, x_end=wx - 2.0, total_frames=total_frames)
            self.bangun_mobil_animated(2, y_tengah_jalan + 0.85, x_start=wx - 2.0, x_end=2.0, total_frames=total_frames)
            return mobil_1

    # ==========================================================================
    # BAGIAN 4: APLIKASI INTERAKTIF SIDEBAR UI (TAB 'CityTour M4')
    # ==========================================================================
    class CityTourAppProps(bpy.types.PropertyGroup):
        kamera_aktif: bpy.props.EnumProperty(
            name="Pilih Kamera",
            items=[
                ("Cam_Drone_Orbit",     "1. Drone Flythrough (Spline Path)", "Tur udara mengelilingi 3 gedung"),
                ("Cam_Street_EyeLevel", "2. Eye-Level Pejalan Kaki (DoF)",   "Perspektif 35mm sejajar mata"),
                ("Cam_Isometric_Ortho", "3. Isometrik Ortografis (Blueprint)","Proyeksi paralel tanpa distorsi"),
                ("Cam_Car_Dashcam",     "4. Dashcam Mobil LEGO (Hierarki)",   "Ikut bergerak bersama mobil"),
            ],
            default="Cam_Drone_Orbit",
        )
        tipe_proyeksi: bpy.props.EnumProperty(
            name="Tipe Proyeksi",
            items=[
                ("PERSP", "Perspektif (Titik Hilang)", ""),
                ("ORTHO", "Ortografis (Paralel)", ""),
            ],
            default="PERSP",
        )
        focal_length: bpy.props.FloatProperty(name="Focal Length (mm)", default=24.0, min=12.0, max=120.0)
        aktif_dof: bpy.props.BoolProperty(name="Depth of Field (Bokeh Malam)", default=True)
        aperture_fstop: bpy.props.FloatProperty(name="Aperture (f-stop)", default=2.0, min=0.8, max=16.0)

        # Properti Render MP4 & Ekspor Web 3D (.GLB)
        output_dir: bpy.props.StringProperty(
            name="Folder Output",
            description="Kosongkan untuk menyimpan otomatis ke Desktop / folder file .blend",
            default="",
            subtype="DIR_PATH",
        )
        render_res: bpy.props.EnumProperty(
            name="Resolusi MP4",
            items=[
                ("720P",  "720p HD (1280x720 - Cepat)",      "Cocok untuk uji coba praktikum"),
                ("1080P", "1080p Full HD (1920x1080 - Tajam)","Cocok untuk presentasi final"),
            ],
            default="720P",
        )
        glb_include_anim: bpy.props.BoolProperty(
            name="Sertakan Animasi & Kamera di .GLB",
            default=True,
        )

    class CITYTOUR_OT_switch_camera(bpy.types.Operator):
        bl_idname = "citytour.switch_camera"
        bl_label = "Aktifkan Kamera & Pengaturan Optik"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            props = context.scene.citytour_props
            cam = bpy.data.objects.get(props.kamera_aktif)
            if not cam:
                self.report({"WARNING"}, f"Kamera {props.kamera_aktif} tidak ditemukan!")
                return {"CANCELLED"}

            context.scene.camera = cam
            cam.data.type = props.tipe_proyeksi
            if props.tipe_proyeksi == "PERSP":
                cam.data.lens = props.focal_length
            cam.data.dof.use_dof = props.aktif_dof
            cam.data.dof.aperture_fstop = props.aperture_fstop

            for area in context.screen.areas:
                if area.type == "VIEW_3D":
                    for space in area.spaces:
                        if space.type == "VIEW_3D":
                            space.region_3d.view_perspective = "CAMERA"

            self.report({"INFO"}, f"Kamera aktif: {cam.name} ({props.tipe_proyeksi})")
            return {"FINISHED"}

    class CITYTOUR_OT_toggle_play(bpy.types.Operator):
        bl_idname = "citytour.toggle_play"
        bl_label = "Play / Pause Simulasi Animasi"

        def execute(self, context):
            bpy.ops.screen.animation_play()
            return {"FINISHED"}

    class CITYTOUR_OT_bake_day_night(bpy.types.Operator):
        bl_idname = "citytour.bake_day_night"
        bl_label = "Aktifkan Siklus Siang -> Malam (240 Frame)"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            KeyframeAnimator.bake_siklus_siang_malam(total_frames=TOTAL_FRAMES)
            self.report({"INFO"}, "Siklus animasi Matahari & Lampu PJU otomatis (Frame 1-240) aktif!")
            return {"FINISHED"}

    class CITYTOUR_OT_render_mp4(bpy.types.Operator):
        bl_idname = "citytour.render_mp4"
        bl_label = "Render Animasi ke Video MP4"
        bl_description = "Merender timeline (Frame 1-240) menjadi file video H.264 MP4"

        def execute(self, context):
            props = context.scene.citytour_props
            mp4_path = ExportPipelineManager.render_animasi_mp4(
                output_dir=props.output_dir,
                resolusi=props.render_res,
            )
            self.report({"INFO"}, f"Rendering MP4 dimulai -> {mp4_path}")
            return {"FINISHED"}

    class CITYTOUR_OT_export_glb(bpy.types.Operator):
        bl_idname = "citytour.export_glb"
        bl_label = "Ekspor Kawasan Makro ke .GLB (Web 3D)"
        bl_description = "Mengekspor 3 Gedung, Taman, Kamera, & Animasi ke format glTF Binary (.glb)"

        def execute(self, context):
            props = context.scene.citytour_props
            glb_path = ExportPipelineManager.export_web_glb(
                output_dir=props.output_dir,
                sertakan_animasi=props.glb_include_anim,
            )
            self.report({"INFO"}, f"Ekspor Web 3D .GLB berhasil -> {glb_path}")
            return {"FINISHED"}

    class CITYTOUR_PT_main_panel(bpy.types.Panel):
        bl_label = "Modul 4: Kamera, Animasi & Ekspor"
        bl_idname = "CITYTOUR_PT_main_panel"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "CityTour M4"

        def draw(self, context):
            layout = self.layout
            props = context.scene.citytour_props

            box1 = layout.box()
            box1.label(text="1. Kamera Virtual & Proyeksi", icon="CAMERA_DATA")
            box1.prop(props, "kamera_aktif")
            box1.prop(props, "tipe_proyeksi")
            box1.prop(props, "focal_length")
            box1.prop(props, "aktif_dof")
            box1.prop(props, "aperture_fstop")
            box1.operator("citytour.switch_camera", icon="VIEW_CAMERA")

            box2 = layout.box()
            box2.label(text="2. Kontrol Animasi & Siklus Waktu", icon="PLAY")
            box2.operator("citytour.toggle_play", icon="TIME")
            box2.operator("citytour.bake_day_night", icon="LIGHT_SUN")

            box3 = layout.box()
            box3.label(text="3. Render Video & Ekspor Web 3D", icon="EXPORT")
            box3.prop(props, "output_dir")
            box3.prop(props, "render_res")
            box3.operator("citytour.render_mp4", icon="RENDER_ANIMATION")
            box3.separator()
            box3.prop(props, "glb_include_anim")
            box3.operator("citytour.export_glb", icon="MESH_CUBE")

    KELAS_UI_MODUL4 = (
        CityTourAppProps,
        CITYTOUR_OT_switch_camera,
        CITYTOUR_OT_toggle_play,
        CITYTOUR_OT_bake_day_night,
        CITYTOUR_OT_render_mp4,
        CITYTOUR_OT_export_glb,
        CITYTOUR_PT_main_panel,
    )

    def register_modul4_ui():
        for cls in KELAS_UI_MODUL4:
            try:
                bpy.utils.unregister_class(cls)
            except Exception:
                pass
            bpy.utils.register_class(cls)
        bpy.types.Scene.citytour_props = bpy.props.PointerProperty(type=CityTourAppProps)

# ==============================================================================
# BAGIAN 5: ORKESTRASI UTAMA MODUL 4
# ==============================================================================
def jalankan_modul_4(ascii_makro=PETA_MAKRO_ASCII):
    parser = AsciiMacroParser(scale=SKALA_MAKRO_METER)
    data_makro = parser.parse(ascii_makro)

    if BLENDER_AVAILABLE:
        SceneManager.bersihkan_scene()
        scene = bpy.context.scene
        scene.frame_start = 1
        scene.frame_end = TOTAL_FRAMES
        scene.frame_current = 1
        scene.render.fps = 24

        kol_utama = SceneManager.buat_koleksi("KawasanMakro_Modul4")
        kol_lampu = SceneManager.buat_koleksi("LightingRig_Modul4", kol_utama)
        kol_cam = SceneManager.buat_koleksi("CameraRig_Modul4", kol_utama)

        LightingRigManager.bangun_world_dan_lampu(data_makro["ukuran_kawasan"], kol_lampu)
        builder = MacroAnimatedBuilder(TextureMaterialFactory(), CONFIG_MATERIAL_MODUL4, kol_utama, kol_lampu)
        mobil_utama = builder.bangun_kawasan_lengkap(data_makro, total_frames=TOTAL_FRAMES)

        CameraRigManager.bangun_semua_kamera(
            data_makro["ukuran_kawasan"],
            kol_cam,
            mobil_utama=mobil_utama,
            total_frames=TOTAL_FRAMES,
        )

        KeyframeAnimator.bake_siklus_siang_malam(total_frames=TOTAL_FRAMES)
        register_modul4_ui()

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.shading.type = "RENDERED"
                        space.shading.use_scene_lights_render = True
                        space.shading.use_scene_world_render = True
                        space.region_3d.view_perspective = "CAMERA"

        print(
            f"MATERI 4 OK: Simulasi Kamera Spline, Animasi, Render MP4, & Ekspor .GLB "
            f"siap digunakan di panel 'CityTour M4'!"
        )
    return data_makro

if __name__ == "__main__":
    jalankan_modul_4(PETA_MAKRO_ASCII)