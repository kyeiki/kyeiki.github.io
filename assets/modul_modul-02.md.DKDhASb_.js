import{_ as s,o as n,c as p,a0 as t}from"./chunks/framework.B7o6dWmz.js";const i="/assets/v-user-iso.DRBaBASw.png",e="/assets/p-menara-iso.CFZnlxA0.png",l="/assets/v-numpad7-top.BwTCOjXc.png",o="/assets/v-numpad1-front.CxU7k_-I.png",r="/assets/v-numpad3-right.D1ZlbuUa.png",u="/assets/v-ctrl1-back.D_lDx8ew.png",d="/assets/v-ctrl3-left.X-qFy9yz.png",c="/assets/v-ctrl7-bottom.DRXYHRSr.png",k="/assets/v-numpad0-camera.BWzcQfOO.png",h="/assets/p-brick-2x4.C9pklSiQ.png",q="/assets/p-brick-shear.DWl4zWMP.png",g="/assets/ui-outliner.DkjHtmy7.png",m="/assets/p-menara-top.Dxs1TjuS.png",_="/assets/p-menara-front.CZj0Rif5.png",E="/assets/p-meja-hierarki.Zigo-vvR.png",y="/assets/p-tekstur-brick.02W8qeyv.png",b="/assets/p-tekstur-checker.DQY24baa.png",f="/assets/p-tekstur-wood.BhSJ9K-q.png",x="/assets/p-brick-texture.BmHs4Xq_.png",A="/assets/ui-panel-app.Z2vr9Otz.png",S=JSON.parse('{"title":"Modul 2 -Transformasi 3D Matriks Homogen, Hierarki LEGO & Texture","description":"","frontmatter":{"title":"Modul 2 -Transformasi 3D Matriks Homogen, Hierarki LEGO & Texture","outline":{"level":[2,3]}},"headers":[],"relativePath":"modul/modul-02.md","filePath":"modul/modul-02.md"}'),F={name:"modul/modul-02.md"};function C(T,a,B,I,M,R){return n(),p("div",null,[...a[0]||(a[0]=[t('<h2 id="lembar-persetujuan" tabindex="-1">LEMBAR PERSETUJUAN <a class="header-anchor" href="#lembar-persetujuan" aria-label="Permalink to &quot;LEMBAR PERSETUJUAN&quot;">​</a></h2><p><strong>TRANSFORMASI 3D MATRIKS HOMOGEN, HIERARKI SCENE GRAPH LEGO, DAN PROSEDURAL TEXTURE</strong></p><table tabindex="0"><thead><tr><th>Proses</th><th>Jabatan</th><th>Nama</th><th>Tanda Tangan</th></tr></thead><tbody><tr><td>Disusun oleh</td><td>Pengampu Praktikum Mata Kuliah Komputer Grafik</td><td></td><td></td></tr><tr><td>Diperiksa oleh</td><td>Ketua Kelompok Bidang Keahlian (KBK) Multimedia</td><td></td><td></td></tr><tr><td>Disahkan oleh</td><td>Ketua Program Studi D-3 Teknik Informatika</td><td></td><td></td></tr></tbody></table><p><strong>PUBLISHED BY</strong>, Jurusan Teknik Komputer &amp; Informatika Politeknik Negeri Bandung, Jl. Gegerkalong Hilir, Ciwaruga, Parongpong, Kab. Bandung Barat 40559. Copyright © 2026 by JTK POLBAN, All rights reserved.</p><table tabindex="0"><thead><tr><th></th><th></th></tr></thead><tbody><tr><td>Penanggung jawab</td><td>: Yudi Widhiyasana</td></tr><tr><td>Penanggung jawab</td><td>: Trisna Gelar A</td></tr><tr><td>Penanggung jawab</td><td>: Muhammad Rizqi Sholahuddin</td></tr><tr><td>Tim Penulis</td><td>: Tim Praktikum Komputer Grafik</td></tr></tbody></table><h2 id="kata-pengantar" tabindex="-1">KATA PENGANTAR <a class="header-anchor" href="#kata-pengantar" aria-label="Permalink to &quot;KATA PENGANTAR&quot;">​</a></h2><p>Modul 2 menggeser fokus dari sekadar membangun bentuk dasar (Modul 1) menjadi menyusun komponen modular layaknya balok LEGO: seluruh penempatan objek dihitung melalui <strong>komposisi matriks transformasi homogen 4×4</strong>, dirakit dalam <strong>hierarki Parent-Child (Scene Graph)</strong>, lalu dibungkus <strong>tekstur prosedural/UV</strong> melalui jaringan Shader Node Blender 4.3.</p><p>Melalui skrip terpadu <code>modul2.py</code>, mahasiswa menjalankan ulang denah Modul 1 -kini setiap grup furnitur dan balok LEGO dirakit menggunakan <strong>Root Pivot (Empty)</strong> dengan relasi <code>M_world = M_parent · M_local</code>, dan material diperluas dengan node Brick / Checker / Wave / Noise / Image Texture lengkap dengan kontrol skala UV (<code>uv_scale</code>) dan relief permukaan (bump normal). Skrip juga otomatis mendaftarkan Add-on Panel UI (<strong>N-Panel → tab LegoApp M2</strong>) sehingga praktikum terasa seperti aplikasi interaktif: spawn balok LEGO, terapkan matriks 4×4, dan ganti tekstur secara langsung dari viewport.</p><p>Bandung, 2026</p><h2 id="daftar-isi" tabindex="-1">DAFTAR ISI <a class="header-anchor" href="#daftar-isi" aria-label="Permalink to &quot;DAFTAR ISI&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Judul</th><th>Halaman</th></tr></thead><tbody><tr><td>LEMBAR PERSETUJUAN / KATA PENGANTAR / DAFTAR ISI / GAMBAR / TABEL</td><td>i-vi</td></tr><tr><td>IDENTITAS MATA KULIAH</td><td>vii</td></tr><tr><td>CAPAIAN PEMBELAJARAN</td><td>viii</td></tr><tr><td>BAGIAN I. BAHAN KAJIAN</td><td>1</td></tr><tr><td>BAGIAN II. PENYIAPAN (PREPARATION)</td><td>5</td></tr><tr><td>BAGIAN III. PROSEDUR: Task I Sudut Pandang Numpad; Task II Matriks Homogen; Task III Hierarki LEGO; Task IV Texture &amp; UV; Task V Panel LegoApp M2</td><td>7</td></tr><tr><td>BAGIAN IV. MEDIA DAN MEKANISME PENGUMPULAN</td><td>18</td></tr><tr><td>BAGIAN V. PEMBAHASAN DAN EVALUASI</td><td>19</td></tr><tr><td>LAMPIRAN A. GLOSSARIUM</td><td>20</td></tr><tr><td>LAMPIRAN B. COOKBOOK RESEP CEPAT</td><td>21</td></tr><tr><td>LAMPIRAN C. BEDAH DETAIL &amp; KODE INTI <code>modul2.py</code></td><td>23</td></tr><tr><td>DAFTAR PUSTAKA</td><td>32</td></tr></tbody></table><h2 id="daftar-gambar" tabindex="-1">DAFTAR GAMBAR <a class="header-anchor" href="#daftar-gambar" aria-label="Permalink to &quot;DAFTAR GAMBAR&quot;">​</a></h2><p>Gambar 1. Scene <code>RumahLego_Modul2</code> dari sudut pandang bebas (perspektif) Gambar 2. Denah dari atas -Numpad 7 (Top Orthographic) Gambar 3. Sudut pandang Numpad 1 (Front) dan Numpad 3 (Right) Gambar 4. Sisi lain bangunan: Ctrl+Numpad 1 (Back), Ctrl+Numpad 3 (Left), Ctrl+Numpad 7 (Bottom), dan Numpad 0 (Camera) Gambar 5. Menara LEGO 4 lapisan: iso, top, front, dan hierarki Outliner Gambar 6. Demo matriks homogen: balok LEGO 2×4 → shear + rotasi → image texture Gambar 7. Hierarki furnitur: grup meja kerja dengan Root Pivot Gambar 8. Closeup tekstur prosedural: Brick, Checker, Wood Gambar 9. Panel aplikasi LegoApp M2 (popup + sidebar)</p><h2 id="daftar-tabel" tabindex="-1">DAFTAR TABEL <a class="header-anchor" href="#daftar-tabel" aria-label="Permalink to &quot;DAFTAR TABEL&quot;">​</a></h2><p>Tabel 1. Pemetaan CPMK (fokus CPMK 1, 2) Tabel 2. Kelas inti <code>modul2.py</code> dan tanggung jawabnya Tabel 3. Rumus matriks transformasi homogen 4×4 di <code>Transform3DEngine</code> Tabel 4. Preset tekstur prosedural dan node jaringannya Tabel 5. Rubrik penilaian</p><h2 id="identitas-mata-kuliah-program-studi-dan-kurikulum" tabindex="-1">IDENTITAS MATA KULIAH, PROGRAM STUDI DAN KURIKULUM <a class="header-anchor" href="#identitas-mata-kuliah-program-studi-dan-kurikulum" aria-label="Permalink to &quot;IDENTITAS MATA KULIAH, PROGRAM STUDI DAN KURIKULUM&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Atribut</th><th>Keterangan</th></tr></thead><tbody><tr><td>Mata Kuliah</td><td>: Komputer Grafik (Praktikum) / Computer Graphics (Practicum)</td></tr><tr><td>Kode Mata Kuliah</td><td>: 25TI3103</td></tr><tr><td>SKS</td><td>: 3 (2 Teori, 1 Praktikum) · Wajib · PBL</td></tr><tr><td>Semester</td><td>: III · KBK Multimedia</td></tr><tr><td>Program Pendidikan</td><td>: Diploma Tiga (D-3) Prodi Teknik Informatika</td></tr><tr><td>Jurusan</td><td>: Teknik Komputer &amp; Informatika</td></tr><tr><td>Penyusun</td><td>: Trisna Gelar A, Muhammad Rizqi Sholahuddin</td></tr></tbody></table><h2 id="capaian-pembelajaran" tabindex="-1">CAPAIAN PEMBELAJARAN <a class="header-anchor" href="#capaian-pembelajaran" aria-label="Permalink to &quot;CAPAIAN PEMBELAJARAN&quot;">​</a></h2><p><strong>Tabel 1. Pemetaan CPMK</strong>, fokus modul ini: <strong>CPMK 1</strong> (konsep transformasi geometri 3D &amp; texture mapping) dan <strong>CPMK 2</strong> (perakitan objek modular berbasis matriks &amp; hierarki melalui otomatisasi skrip). Peta lengkap lihat Modul 1 V1.</p><h2 id="bagian-i-bahan-kajian" tabindex="-1">BAGIAN I. BAHAN KAJIAN <a class="header-anchor" href="#bagian-i-bahan-kajian" aria-label="Permalink to &quot;BAGIAN I. BAHAN KAJIAN&quot;">​</a></h2><h3 id="i-1-penggunaan-pedoman" tabindex="-1">I.1. Penggunaan Pedoman <a class="header-anchor" href="#i-1-penggunaan-pedoman" aria-label="Permalink to &quot;I.1. Penggunaan Pedoman&quot;">​</a></h3><p>Titik awal praktikum adalah skrip mandiri <strong><code>modul2.py</code></strong> (pengembangan <code>ascii_to_blender_3d.py</code> Modul 1). Saat dijalankan di <strong>Blender 4.3</strong> (<strong>Run Script / <code>Alt + P</code></strong>), skrip membangun ulang denah gedung kantor -kali ini seluruh furnitur dan menara LEGO dirakit sebagai <strong>hierarki Parent-Child</strong> dan material diperluas dengan <strong>jaringan Shader Node tekstur prosedural</strong> -ke dalam koleksi <code>RumahLego_Modul2</code>, sekaligus mendaftarkan panel interaktif <strong>LegoApp M2</strong> di N-Panel viewport.</p><blockquote><p><strong>Dokumen pendamping (unduhan):</strong><a href="/dokumen/Suplemen-Dosen-Modul-2.docx" download>Suplemen Dosen - Panduan Detail Pengerjaan Task I-V (.docx)</a> - penjelasan langkah demi langkah tiap task untuk dosen/instruktur. <a href="/dokumen/Jobsheet-Mahasiswa-Modul-2.docx" download>Jobsheet Mahasiswa Modul 2 (.docx)</a> - lembar kerja siap cetak yang diisi mahasiswa saat praktikum. <a href="/kode/modul2.py" download>Kode sumber modul2.py</a> - skrip utama modul ini (unduh lalu jalankan di Blender 4.3). Semua berkas praktikum terkumpul di halaman <a href="/unduh.html">Unduh Berkas</a>.</p></blockquote><p><img src="'+i+`" alt="Tampilan keseluruhan scene Modul 2"></p><p>Gambar 1. Scene <code>RumahLego_Modul2</code> -denah ASCII Modul 1 dibangun ulang dalam mode Material Preview: dinding bata (Brick + Bump), lantai Checker/Kayu, dan dua menara LEGO di tengah zona Workstation.</p><h3 id="i-2-ruang-lingkup" tabindex="-1">I.2. Ruang Lingkup <a class="header-anchor" href="#i-2-ruang-lingkup" aria-label="Permalink to &quot;I.2. Ruang Lingkup&quot;">​</a></h3><p>Aljabar matriks homogen 4×4 (Translasi, Rotasi Euler XYZ, Skala, Shear) dan komposisinya; hierarki transformasi <strong>Scene Graph / Parent-Child</strong> (<code>matrix_local</code> vs <code>matrix_world</code>); perakitan komponen modular gaya LEGO (balok + stud silinder) melalui Root Pivot (Empty); pemetaan tekstur: koordinat UV (Generated/UV), node Mapping (skala UV), tekstur prosedural Brick/Checker/Wave-Wood/Noise, Image Texture piksel prosedural, dan Bump Normal; pengembangan material <code>Principled BSDF</code> Blender 4.3; serta pembuatan Add-on UI sederhana (Panel + Operator) di Sidebar 3D Viewport.</p><h3 id="i-3-teknologi" tabindex="-1">I.3. Teknologi <a class="header-anchor" href="#i-3-teknologi" aria-label="Permalink to &quot;I.3. Teknologi&quot;">​</a></h3><ul><li><strong>Blender 4.3</strong> (API <code>bpy</code>, <code>bmesh</code>, <code>mathutils.Matrix</code>, Shader Node <code>ShaderNodeTexCoord/Mapping/TexBrick/TexChecker/TexWave/TexNoise/TexImage/Bump</code>).</li><li><strong><code>modul2.py</code></strong>: skrip all-in-one -<code>AsciiDenahParser</code> (warisan Modul 1), <code>Transform3DEngine</code>, <code>SceneManager</code>, <code>TextureMaterialFactory</code>, <code>AssetBuilder</code>, <code>DenahBuilder</code>, dan paket UI <code>LegoApp</code> (<code>LegoTransformAppProps</code>, tiga Operator, satu Panel).</li><li><strong>Panel interaktif</strong>: N-Panel (tombol <code>N</code>) → tab <strong>LegoApp M2</strong>.</li></ul><h3 id="i-4-konsep-kunci-1-matriks-transformasi-homogen-4×4-transform3dengine" tabindex="-1">I.4. Konsep Kunci 1 -Matriks Transformasi Homogen 4×4 (<code>Transform3DEngine</code>) <a class="header-anchor" href="#i-4-konsep-kunci-1-matriks-transformasi-homogen-4×4-transform3dengine" aria-label="Permalink to &quot;I.4. Konsep Kunci 1 -Matriks Transformasi Homogen 4×4 (\`Transform3DEngine\`)&quot;">​</a></h3><p>Pada Modul 1, posisi dan rotasi diatur lewat atribut <code>.location</code> dan <code>.rotation_euler</code> secara terpisah. Modul 2 menghitungnya sebagai <strong>satu kesatuan perkalian matriks</strong> (kelas <code>Transform3DEngine</code>) yang diterapkan langsung ke <code>obj.matrix_world</code>:</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>M = T(tx,ty,tz) · Rz(γ) · Ry(β) · Rx(α) · Shear_xy(shx,shy) · S(sx,sy,sz)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        | 1 0 0 tx |          | cγ -sγ 0 0 |</span></span>
<span class="line"><span>T   =   | 0 1 0 ty |    Rz =  | sγ  cγ 0 0 |</span></span>
<span class="line"><span>        | 0 0 1 tz |          | 0   0  1 0 |</span></span>
<span class="line"><span>        | 0 0 0 1  |          | 0   0  0 1 |</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        | cβ 0 sβ 0 |         | 1 0   0  0 |</span></span>
<span class="line"><span>Ry  =   | 0  1 0  0 |   Rx =  | 0 cα -sα 0 |</span></span>
<span class="line"><span>        |-sβ 0 cβ 0 |         | 0 sα  cα 0 |</span></span>
<span class="line"><span>        | 0  0 0  1 |         | 0 0   0  1 |</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        | 1 0 shx 0 |         | sx 0  0  0 |</span></span>
<span class="line"><span>Shear = | 0 1 shy 0 |   S =   | 0  sy 0  0 |</span></span>
<span class="line"><span>        | 0 0 1   0 |         | 0  0  sz 0 |</span></span>
<span class="line"><span>        | 0 0 0   1 |         | 0  0  0  1 |</span></span></code></pre></div><p><strong>Tabel 3. Rumus matriks transformasi homogen 4×4 di <code>Transform3DEngine</code></strong></p><table tabindex="0"><thead><tr><th>Komponen</th><th>Rumus</th><th>Efek Geometris</th></tr></thead><tbody><tr><td><code>matriks_translasi(tx,ty,tz)</code></td><td>T</td><td>Menggeser objek tanpa mengubah bentuk</td></tr><tr><td><code>matriks_rotasi_x/y/z(rad)</code></td><td>Rx, Ry, Rz</td><td>Memutar mengelilingi sumbu kartesian</td></tr><tr><td><code>matriks_skala(sx,sy,sz)</code></td><td>S</td><td>Membesar/kecil non-uniform</td></tr><tr><td><code>matriks_shear_xy(sh_x,sh_y)</code></td><td>Shear</td><td><strong>Memiringkan</strong> geometri (x,y bergeser proporsional terhadap z)</td></tr><tr><td><code>komposisi_trs(...)</code></td><td>T·Rz·Ry·Rx·Shear·S</td><td>Gabungan semua transformasi dalam satu matriks</td></tr></tbody></table><p>Urutan perkalian penting: matriks paling kanan diterapkan paling dulu terhadap geometri lokal (<code>S → Shear → Rx → Ry → Rz → T</code>). Operasi <strong>Shearing</strong> memiringkan geometri dinding/balok LEGO -sesuatu yang <strong>tidak mungkin</strong> direpresentasikan oleh triplet location/rotation/scale standar tanpa matriks penuh 4×4.</p><h3 id="i-5-konsep-kunci-2-hierarki-scene-graph-parent-child" tabindex="-1">I.5. Konsep Kunci 2 -Hierarki Scene Graph / Parent-Child <a class="header-anchor" href="#i-5-konsep-kunci-2-hierarki-scene-graph-parent-child" aria-label="Permalink to &quot;I.5. Konsep Kunci 2 -Hierarki Scene Graph / Parent-Child&quot;">​</a></h3><p>Modul 1 menyatukan mesh dengan <code>bpy.ops.object.join()</code> menjadi satu objek statis. Modul 2 membuang <code>join()</code> dan menggantinya dengan <strong>Root Pivot (Empty)</strong> per komponen; setiap bagian menjadi anak dengan matriks lokal sendiri:</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>M_world(anak) = M_world(parent) · M_local(anak)</span></span></code></pre></div><p>Konsekuensinya: memutar/menggeser <code>MenaraLego_Utara</code> di Outliner akan membawa seluruh bata LEGO dan stud silinder di atasnya bertransformasi secara utuh -inti transformasi hierarki layaknya rig karakter atau perakitan CAD.</p><blockquote><p><strong>Apa itu &quot;Empty&quot;?</strong> Empty adalah objek Blender <strong>tanpa geometri</strong> (tidak memiliki mesh; hanya titik poros dengan gizmo penanda). Di modul ini Empty berperan sebagai <strong>Root Pivot</strong> -jangkar transformasi yang memegang seluruh anak lewat relasi <code>M_world = M_parent · M_local</code>. Bentuk gizmonya diatur lewat <code>empty_display_type</code>: menara LEGO memakai <code>&quot;ARROWS&quot;</code> (tiga panah sumbu X-Y-Z merah/hijau/biru pada Gambar 5a, agar arah rotasinya terbaca), sedangkan bata LEGO dan grup furnitur memakai <code>&quot;PLAIN_AXES&quot;</code> (silang sumbu). Empty <strong>tidak muncul di render final</strong>; ia hanya terlihat di viewport dan Outliner. Catatan: di Outliner, saat objek Empty di-expand muncul baris anak bertuliskan <code>(Empty)</code> -itu adalah <em>data-block</em> kosong milik objek tersebut, penanda tipenya, bukan error.</p></blockquote><p><img src="`+e+`" alt="Menara LEGO 4 lapisan"></p><p>Gambar 5a. <code>MenaraLego_Utara</code> -4 lapisan bata LEGO (merah 4×4 → kuning 3×3 rotasi 15° → biru 2×4 rotasi 30° → hijau 2×2 rotasi 45°); setiap bata berisi badan kubus + stud silinder sebagai anak Root Pivot.</p><h3 id="i-6-konsep-kunci-3-jaringan-node-tekstur-uv-texturematerialfactory" tabindex="-1">I.6. Konsep Kunci 3 -Jaringan Node Tekstur &amp; UV (<code>TextureMaterialFactory</code>) <a class="header-anchor" href="#i-6-konsep-kunci-3-jaringan-node-tekstur-uv-texturematerialfactory" aria-label="Permalink to &quot;I.6. Konsep Kunci 3 -Jaringan Node Tekstur &amp; UV (\`TextureMaterialFactory\`)&quot;">​</a></h3><p>Skrip otomatis membangun Shader Node Tree:</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>[Texture Coordinate] → [Mapping (UV Scale)] → [Brick / Checker / Wave Wood /</span></span>
<span class="line"><span>                                                Noise / Image Texture]</span></span>
<span class="line"><span>                                              → [Bump Normal] → [Principled BSDF]</span></span></code></pre></div><p>Viewport otomatis diubah ke mode <strong>Material Preview</strong> agar tekstur langsung terlihat. Parameter penting per material di <code>DEFAULT_CONFIG_ASSETS</code>: <code>uv_scale</code> (kepadatan pola pada node Mapping), <code>bump_strength</code> (kedalaman relief), <code>color2</code> (warna kedua pola).</p><p><strong>Tabel 4. Preset tekstur prosedural dan node jaringannya</strong></p><table tabindex="0"><thead><tr><th>Preset (<code>tex_type</code>)</th><th>Node Utama</th><th>Ciri Visual</th></tr></thead><tbody><tr><td><code>BRICK</code></td><td><code>ShaderNodeTexBrick</code></td><td>Bata + nat mortar, relief dari Fac→Bump</td></tr><tr><td><code>CHECKER</code></td><td><code>ShaderNodeTexChecker</code></td><td>Ubin catur dua warna</td></tr><tr><td><code>WOOD</code></td><td><code>ShaderNodeTexWave</code> (Bands + Distortion) + <code>Mix RGBA</code></td><td>Serat kayu bergelombang</td></tr><tr><td><code>NOISE</code></td><td><code>ShaderNodeTexNoise</code></td><td>Bintik granit halus</td></tr><tr><td><code>LEGO_PLASTIC</code></td><td><code>ShaderNodeTexNoise</code> (scale 25, bump 0.03)</td><td>Plastik glossy halus</td></tr><tr><td><code>IMAGE_CHECKER</code></td><td><code>ShaderNodeTexImage</code> (piksel dibuat prosedural di memori)</td><td>Citra UV piksel biru-kuning bergaris</td></tr></tbody></table><h3 id="i-7-perubahan-arsitektur-modul-1-→-modul-2" tabindex="-1">I.7. Perubahan Arsitektur Modul 1 → Modul 2 <a class="header-anchor" href="#i-7-perubahan-arsitektur-modul-1-→-modul-2" aria-label="Permalink to &quot;I.7. Perubahan Arsitektur Modul 1 → Modul 2&quot;">​</a></h3><p><strong>Tabel 2. Kelas inti <code>modul2.py</code> dan tanggung jawabnya</strong></p><table tabindex="0"><thead><tr><th>Kelas</th><th>Peran</th><th>Pengganti / Pengembangan dari Modul 1</th></tr></thead><tbody><tr><td><code>Transform3DEngine</code></td><td>Komposisi matriks homogen T·Rz·Ry·Rx·Shear·S + relasi parent-child</td><td>Pengganti pengaturan <code>.location</code>/<code>.rotation_euler</code> manual</td></tr><tr><td><code>SceneManager</code></td><td>Lifecycle scene, koleksi, <strong>UV cube-projection otomatis</strong> (<code>generate_box_uv</code>)</td><td>Tambahan fungsi UV</td></tr><tr><td><code>TextureMaterialFactory</code></td><td>Shader node tree prosedural + image texture + bump</td><td>Pengembangan <code>MaterialFactory</code> warna polos</td></tr><tr><td><code>AssetBuilder</code></td><td>Registry 10 tipe aset; perakitan hierarki <code>_rakit_hierarki_lokal</code>, LEGO <code>_bangun_bata_lego</code>/<code>_bangun_menara_lego</code></td><td>Pengganti <code>bpy.ops.object.join()</code></td></tr><tr><td><code>LegoApp UI</code> (Props, 3 Operator, Panel)</td><td>Panel interaktif N-Panel → tab <strong>LegoApp M2</strong></td><td>Baru di Modul 2</td></tr></tbody></table><h2 id="bagian-ii-penyiapan-pelaksanaan-praktikum" tabindex="-1">BAGIAN II. PENYIAPAN (PELAKSANAAN PRAKTIKUM) <a class="header-anchor" href="#bagian-ii-penyiapan-pelaksanaan-praktikum" aria-label="Permalink to &quot;BAGIAN II. PENYIAPAN (PELAKSANAAN PRAKTIKUM)&quot;">​</a></h2><h3 id="ii-1-perangkat-keras-dan-lunak" tabindex="-1">II.1. Perangkat Keras dan Lunak <a class="header-anchor" href="#ii-1-perangkat-keras-dan-lunak" aria-label="Permalink to &quot;II.1. Perangkat Keras dan Lunak&quot;">​</a></h3><table tabindex="0"><thead><tr><th>Komponen</th><th>Spesifikasi Minimum</th></tr></thead><tbody><tr><td>Perangkat Keras</td><td>Laptop/PC: RAM ≥ 8 GB, GPU yang mendukung OpenGL 4.3</td></tr><tr><td>Sistem Operasi</td><td>Windows 10/11 64-bit</td></tr><tr><td>Perangkat Lunak</td><td>Blender 4.3 LTS; VS Code/Notepad++ (editor teks)</td></tr><tr><td>Berkas</td><td><code>modul2.py</code> (skrip utama), <code>prak2_[NIM].blend</code> (hasil simpan), tangkapan layar</td></tr></tbody></table><h3 id="ii-2-langkah-awal-menjalankan-skrip" tabindex="-1">II.2. Langkah Awal Menjalankan Skrip <a class="header-anchor" href="#ii-2-langkah-awal-menjalankan-skrip" aria-label="Permalink to &quot;II.2. Langkah Awal Menjalankan Skrip&quot;">​</a></h3><ol><li>Unduh/copy <code>modul2.py</code> ke folder kerja praktikum.</li><li>Buka <strong>Blender 4.3</strong> → tab <strong>Scripting</strong> → <strong>Text → Open</strong> → pilih <code>modul2.py</code>.</li><li>Tekan <strong>Run Script (<code>Alt + P</code>)</strong> → seluruh gedung + menara LEGO muncul di koleksi <code>RumahLego_Modul2</code> (±668 objek), viewport otomatis berubah ke <strong>Material Preview</strong>.</li><li>Tekan <code>N</code> di 3D Viewport → pilih tab <strong>LegoApp M2</strong> → panel aplikasi siap digunakan.</li><li>Simpan sebagai <code>prak2_[NIM].blend</code> (<strong>File → Save As</strong>).</li></ol><h2 id="bagian-iii-prosedur-pelaksanaan-praktikum-step-by-step" tabindex="-1">BAGIAN III. PROSEDUR (PELAKSANAAN PRAKTIKUM STEP-BY-STEP) <a class="header-anchor" href="#bagian-iii-prosedur-pelaksanaan-praktikum-step-by-step" aria-label="Permalink to &quot;BAGIAN III. PROSEDUR (PELAKSANAAN PRAKTIKUM STEP-BY-STEP)&quot;">​</a></h2><h3 id="iii-0-alur-praktikum" tabindex="-1">III.0. Alur Praktikum <a class="header-anchor" href="#iii-0-alur-praktikum" aria-label="Permalink to &quot;III.0. Alur Praktikum&quot;">​</a></h3><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>[Denah ASCII]  --parse--&gt;  [JSON config]  --build--&gt;  [Hierarki objek + Material</span></span>
<span class="line"><span>                        (AsciiDenahParser)              bertekstur + Panel UI]</span></span>
<span class="line"><span>                                                      (Transform3DEngine +</span></span>
<span class="line"><span>                                                       AssetBuilder +</span></span>
<span class="line"><span>                                                       TextureMaterialFactory)</span></span></code></pre></div><h3 id="iii-1-task-i-eksplorasi-sudut-pandang-numpad-view" tabindex="-1">III.1. Task I: Eksplorasi Sudut Pandang (Numpad View) <a class="header-anchor" href="#iii-1-task-i-eksplorasi-sudut-pandang-numpad-view" aria-label="Permalink to &quot;III.1. Task I: Eksplorasi Sudut Pandang (Numpad View)&quot;">​</a></h3><p>Sebelum memanipulasi transformasi, kenali objek dari semua sisi. Gunakan tombol <strong>Numpad</strong> di 3D Viewport:</p><table tabindex="0"><thead><tr><th>Tombol</th><th>Sudut Pandang</th><th>yang Perlu Diamati</th></tr></thead><tbody><tr><td><code>Numpad 7</code></td><td><strong>Top</strong> (orthographic)</td><td>Denah 3D penuh: lantai Checker Workstation, Wood ruang R, dua menara LEGO</td></tr><tr><td><code>Numpad 1</code></td><td><strong>Front</strong> (dari Selatan)</td><td>Fasad dinding eksterior bertekstur bata + celah pintu</td></tr><tr><td><code>Numpad 3</code></td><td><strong>Right</strong> (dari Timur)</td><td>Dinding samping; perbedaan tekstur eksterior vs interior</td></tr><tr><td><code>Ctrl+Numpad 1/3</code></td><td>Back / Left</td><td>Sisi Utara &amp; Barat bangunan</td></tr><tr><td><code>Ctrl+Numpad 7</code></td><td>Bottom</td><td>Susunan slab lantai dari bawah</td></tr><tr><td><code>Numpad 5</code></td><td>Toggle Persp/Ortho</td><td>Gabungkan dengan 7 untuk denah perspektif</td></tr><tr><td><code>Numpad 0</code></td><td>Camera view</td><td>Pratinjau kamera <code>Kamera_Modul2</code> siap render</td></tr></tbody></table><p><img src="`+l+'" alt="Denah dari atas (Numpad 7)"></p><p>Gambar 2. <strong>Numpad 7 (Top Orthographic)</strong> -seluruh denah terlihat: lantai checker besar di zona Workstation Utara &amp; Selatan, lantai kayu pada barisan ruang <code>[R]</code>, serta dua menara LEGO di tengah tiap zona.</p><p><img src="'+o+'" alt="Front view"></p><p>Gambar 3a. <strong>Numpad 1 (Front)</strong> -fasad selatan; perhatikan bump relief pada nat bata dan celah pintu tinggi 2,1 m hasil pemotongan interval Modul 1 yang kini bertekstur.</p><p><img src="'+r+'" alt="Right view"></p><p>Gambar 3b. <strong>Numpad 3 (Right)</strong> -elevasi timur; dinding eksterior bata kasar kontras dengan dinding interior halus.</p><p><img src="'+u+'" alt="Back view"></p><p>Gambar 4a. <strong>Ctrl+Numpad 1 (Back)</strong> -sisi utara; dua menara LEGO di zona Workstation terlihat dari belakang.</p><p><img src="'+d+'" alt="Left view"></p><p>Gambar 4b. <strong>Ctrl+Numpad 3 (Left)</strong> -sisi barat; ambang jendela (bukaan 1,0 m di atas 1,1 m) hasil injeksi otomatis Modul 1.</p><p><img src="'+c+'" alt="Bottom view"></p><p>Gambar 4c. <strong>Ctrl+Numpad 7 (Bottom)</strong> -pandangan dari bawah; susunan slab lantai tiap zona berdampingan.</p><p><img src="'+k+'" alt="Camera view"></p><p>Gambar 4d. <strong>Numpad 0 (Camera)</strong> -pratinjau <code>Kamera_Modul2</code> yang dipasang otomatis oleh <code>atur_kamera_cahaya_dan_viewport()</code>.</p><h3 id="iii-2-task-ii-matriks-homogen-4×4-dalam-praktik" tabindex="-1">III.2. Task II: Matriks Homogen 4×4 dalam Praktik <a class="header-anchor" href="#iii-2-task-ii-matriks-homogen-4×4-dalam-praktik" aria-label="Permalink to &quot;III.2. Task II: Matriks Homogen 4×4 dalam Praktik&quot;">​</a></h3><ol><li>Buka <code>modul2.py</code> → kelas <code>Transform3DEngine</code> → pahami <code>komposisi_trs()</code> dan <code>terapkan_matriks()</code>.</li><li>Di panel LegoApp M2 → box <strong>2. Matriks Transformasi 3D (4x4)</strong> → atur <code>Translasi (T)</code>, <code>Rotasi Euler (deg)</code>, <code>Skala (S)</code>, <code>Shear XY</code>.</li><li>Pilih objek apa pun → klik <strong>Terapkan Matriks 4x4 ke Objek Aktif</strong> → operator membangun <code>M = T·Rz·Ry·Rx·Shear·S</code> dan menulisnya ke <code>obj.matrix_world</code>.</li></ol><p><img src="'+h+'" alt="Balok LEGO 2x4 hasil spawn"></p><p>Gambar 6a. Balok LEGO 2×4 kuning hasil operator <strong>Tambah Balok LEGO (Matriks 4x4)</strong> -badan kubus + 8 stud silinder, semuanya anak dari satu Root Pivot <code>Lego_2x4</code>.</p><p><img src="'+q+'" alt="Balok LEGO sheared"></p><p>Gambar 6b. Hasil penerapan matriks dengan <code>Shear XY = (0.55, 0)</code> dan <code>Rotasi Z = 20°</code> -sisi balok tidak lagi vertikal; inilah deformasi shearing yang hanya mungkin melalui matriks homogen penuh, bukan triplet transformasi standar.</p><h3 id="iii-3-task-iii-hierarki-scene-graph-lego" tabindex="-1">III.3. Task III: Hierarki Scene Graph LEGO <a class="header-anchor" href="#iii-3-task-iii-hierarki-scene-graph-lego" aria-label="Permalink to &quot;III.3. Task III: Hierarki Scene Graph LEGO&quot;">​</a></h3><ol><li>Buka <strong>Outliner</strong> → cari <code>MenaraLego_Utara</code> -objek bertipe <strong>Empty</strong> dengan tampilan panah sumbu XYZ (<code>empty_display_type = &quot;ARROWS&quot;</code>); di viewport ia tampak sebagai tiga panah kecil di dasar menara.</li><li>Klik panah expand → lihat anak <code>…_Lapis1..4</code> (masing-masing Root Pivot bata) → expand lagi → <code>…_Body</code> dan <code>…_Stud_x_y</code> (lihat Gambar 5d). Baris <code>(Empty)</code> yang muncul saat expand adalah data-block kosong milik objek Empty -bukan error.</li><li>Klik <code>MenaraLego_Utara</code> → tekan <code>R Z 4 5 Enter</code> (rotasi 45° di sumbu Z) → seluruh 4 lapisan + puluhan stud ikut berputar utuh. Inilah <code>M_world = M_parent · M_local</code>.</li><li>Bandingkan dengan Modul 1 yang menggunakan <code>join()</code> -tidak ada lagi objek statis; setiap bagian tetap modular dan bisa diedit sendiri-sendiri.</li></ol><p><img src="'+g+'" alt="Hierarki Outliner MenaraLego"></p><p>Gambar 5d. Outliner (crop) -di dalam koleksi <code>RumahLego_Modul2</code> (±668 objek), <code>MenaraLego_Utara</code> yang di-expand menampilkan anak <code>…_Lapis1..4</code> (Root Pivot tiap bata); expand lagi untuk melihat <code>…_Body</code> dan <code>…_Stud_x_y</code>.</p><p><img src="'+m+'" alt="Menara dari atas"></p><p>Gambar 5b. Menara LEGO dari atas -stud silinder tiap lapisan terlihat; lapisan atas terotasi 15°/30°/45° bertingkat (<code>math.radians</code> di <code>_bangun_menara_lego</code>).</p><p><img src="'+_+'" alt="Menara dari depan"></p><p>Gambar 5c. Menara LEGO dari depan -tumpukan 4 warna (merah-kuning-biru-hijau) dengan tinggi total ±1,3 m pada skala <code>unit_size = 0.28</code>.</p><p><img src="'+E+'" alt="Grup meja kerja"></p><p>Gambar 7. Grup <code>Kubikel_U_R1_1</code> hasil <code>_rakit_hierarki_lokal()</code> -meja kayu (tekstur Wave Wood), partisi kubikel (Noise), monitor emissive, dan kursi; semua bagian anak Root Pivot yang sama sehingga bisa dipindah sebagai satu kesatuan.</p><h3 id="iii-4-task-iv-texture-uv-mapping" tabindex="-1">III.4. Task IV: Texture &amp; UV Mapping <a class="header-anchor" href="#iii-4-task-iv-texture-uv-mapping" aria-label="Permalink to &quot;III.4. Task IV: Texture &amp; UV Mapping&quot;">​</a></h3><ol><li>Pelajari <code>TextureMaterialFactory.get_or_create()</code> di <code>modul2.py</code>.</li><li>Pilih mesh (mis. lantai) → LegoApp M2 → box <strong>3. Shader Texture &amp; UV Mapping</strong> → pilih <strong>Preset Tekstur</strong> → atur <strong>Skala UV</strong> → klik <strong>Terapkan Tekstur &amp; Skala UV</strong>.</li><li>Amati: <code>ShaderNodeMapping.Scale</code> mengubah kepadatan pola; <code>ShaderNodeBump.Strength</code> memberi relief permukaan.</li></ol><p><img src="'+y+'" alt="Tekstur bata"></p><p>Gambar 8a. Closeup <strong>Brick Texture</strong> pada dinding eksterior -<code>Color1/Color2</code> bata + <code>Mortar</code> abu-abu; nat menonjol karena <code>Fac → Bump Height</code>.</p><p><img src="'+b+'" alt="Tekstur checker"></p><p>Gambar 8b. Closeup <strong>Checker Texture</strong> lantai Workstation (<code>uv_scale</code> 12×12) -pola ubin dua warna lembut.</p><p><img src="'+f+'" alt="Tekstur kayu"></p><p>Gambar 8c. Closeup <strong>Wave Wood Texture</strong> lantai ruang <code>[R]</code> -<code>Bands + Distortion 4.5</code> dikomposisi lewat node <code>Mix RGBA</code> dua warna cokelat.</p><p><img src="'+x+'" alt="Balok dengan image texture"></p><p>Gambar 6c. Balok demo setelah preset <strong>Image Texture (UV Pixel Map)</strong> -citra checker piksel dibuat prosedural di memori (<code>buat_tekstur_citra_checker</code>) lalu dipetakan lewat koordinat <strong>UV</strong> (bukan Generated) dan <code>generate_box_uv</code>.</p><h3 id="iii-5-task-v-panel-aplikasi-legoapp-m2" tabindex="-1">III.5. Task V: Panel Aplikasi LegoApp M2 <a class="header-anchor" href="#iii-5-task-v-panel-aplikasi-legoapp-m2" aria-label="Permalink to &quot;III.5. Task V: Panel Aplikasi LegoApp M2&quot;">​</a></h3><ol><li>Tekan <code>N</code> di 3D Viewport → sidebar terbuka → klik tab <strong>LegoApp M2</strong> (di samping Item/Tool/View).</li><li>Gunakan ketiga box-nya: <strong>(1)</strong> Generator Balok LEGO Modular (warna + ukuran stud, tombol <em>Tambah Balok LEGO</em>), <strong>(2)</strong> Matriks Transformasi 3D (4x4) (Translasi/Rotasi/Skala/Shear, tombol <em>Terapkan Matriks</em>), <strong>(3)</strong> Shader Texture &amp; UV Mapping (preset tekstur + skala UV, tombol <em>Terapkan Tekstur</em>).</li><li>Screenshot di bawah menampilkan panel yang sama dibuka sebagai <strong>popup</strong> di atas viewport (dipanggil programatik lewat <code>bpy.ops.wm.call_panel</code> untuk keperluan dokumentasi); pada praktiknya panel ini menetap di sidebar tab LegoApp M2.</li></ol><p><img src="'+A+`" alt="Panel LegoApp M2"></p><p>Gambar 9. Panel <strong>Modul 2: LEGO 3D Transform &amp; Texture</strong> ditampilkan sebagai popup di atas viewport, dengan N-sidebar terbuka di kanan -tiga box: Generator Balok LEGO Modular, Matriks Transformasi 3D (4x4), dan Shader Texture &amp; UV Mapping; tombol operatornya dijalankan langsung dari viewport seperti aplikasi.</p><h2 id="bagian-iv-media-dan-mekanisme-pengumpulan" tabindex="-1">BAGIAN IV. MEDIA DAN MEKANISME PENGUMPULAN <a class="header-anchor" href="#bagian-iv-media-dan-mekanisme-pengumpulan" aria-label="Permalink to &quot;BAGIAN IV. MEDIA DAN MEKANISME PENGUMPULAN&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Artefak</th><th>Format</th><th>Ketentuan</th></tr></thead><tbody><tr><td>File praktikum</td><td><code>prak2_[NIM].blend</code></td><td>Berisi scene hasil <code>modul2.py</code> + minimal 1 balok LEGO hasil panel LegoApp M2</td></tr><tr><td>Tangkapan sudut pandang</td><td>PNG</td><td>Numpad 1, 3, 7 (dan 0 bila perlu) setelah transformasi hierarki diterapkan</td></tr><tr><td>Tangkapan panel</td><td>PNG</td><td>Panel LegoApp M2 terbuka + Outliner hierarki menara</td></tr><tr><td>Laporan singkat</td><td>PDF/MD</td><td>Penjelasan urutan komposisi matriks yang dipakai + preset tekstur yang dicoba</td></tr></tbody></table><p>Kumpulkan sesuai deadline yang ditentukan dosen pengampu.</p><h2 id="bagian-v-pembahasan-dan-evaluasi-hasil-praktikum" tabindex="-1">BAGIAN V. PEMBAHASAN DAN EVALUASI HASIL PRAKTIKUM <a class="header-anchor" href="#bagian-v-pembahasan-dan-evaluasi-hasil-praktikum" aria-label="Permalink to &quot;BAGIAN V. PEMBAHASAN DAN EVALUASI HASIL PRAKTIKUM&quot;">​</a></h2><ol><li>Mengapa <code>join()</code> Modul 1 diganti hierarki Parent-Child? Kaitkan dengan fleksibilitas edit per-bagian dan <code>matrix_local</code>.</li><li>Jelaskan urutan <code>T·Rz·Ry·Rx·Shear·S</code> -apa yang berubah bila <code>S</code> diletakkan paling kiri? Buktikan lewat panel.</li><li>Apa beda koordinat <strong>Generated</strong> vs <strong>UV</strong> pada <code>ShaderNodeTexCoord</code>? Kapan <code>generate_box_uv</code> dibutuhkan?</li><li>Bagaimana <code>uv_scale</code> pada node Mapping mempengaruhi kepadatan Brick/Checker? Tunjukkan dengan dua nilai berbeda.</li></ol><p><strong>Tabel 5. Rubrik Penilaian</strong></p><table tabindex="0"><thead><tr><th>Kriteria</th><th>Bobot</th></tr></thead><tbody><tr><td>Task I–II: pemahaman matriks homogen (demo shear/rotasi sukses)</td><td>25%</td></tr><tr><td>Task III: demonstrasi hierarki (menara &amp; grup furnitur)</td><td>25%</td></tr><tr><td>Task IV: tekstur &amp; UV (min. 3 preset + variasi skala)</td><td>25%</td></tr><tr><td>Task V: penggunaan panel + kelengkapan artefak pengumpulan</td><td>15%</td></tr><tr><td>Laporan &amp; penjelasan konsep</td><td>10%</td></tr></tbody></table><h2 id="lampiran-a-glossarium" tabindex="-1">LAMPIRAN A. GLOSSARIUM <a class="header-anchor" href="#lampiran-a-glossarium" aria-label="Permalink to &quot;LAMPIRAN A. GLOSSARIUM&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Istilah</th><th>Definisi Singkat</th></tr></thead><tbody><tr><td>Matriks Homogen 4×4</td><td>Representasi transformasi affine 3D (T, R, S, Shear) dalam satu matriks 4×4 menggunakan koordinat homogen (x, y, z, 1)</td></tr><tr><td>Shearing</td><td>Transformasi geser yang memiringkan geometri terhadap suatu sumbu tanpa mengubah volume relatif</td></tr><tr><td>Scene Graph</td><td>Struktur pohon objek; transformasi parent diwariskan ke seluruh anak (<code>M_world = M_parent · M_local</code>)</td></tr><tr><td>Empty</td><td>Objek Blender tanpa geometri (tanpa mesh), hanya poros + gizmo penanda; tampilan diatur <code>empty_display_type</code> (<code>PLAIN_AXES</code>, <code>ARROWS</code>, dll); tidak muncul di render final</td></tr><tr><td>Root Pivot</td><td>Empty object sebagai poros grup; diputar/digeser untuk menggerakkan seluruh anak</td></tr><tr><td>matrix_local / matrix_world</td><td>Matriks transformasi relatif parent vs absolut dunia</td></tr><tr><td>UV Mapping</td><td>Pemetaan permukaan mesh ke bidang 2D tekstur</td></tr><tr><td>Generated Coordinates</td><td>Koordinat otomatis Blender berbasis bounding box objek (0–1)</td></tr><tr><td>Procedural Texture</td><td>Tekstur dihitung dari fungsi/node (Brick, Checker, Wave, Noise) tanpa berkas citra</td></tr><tr><td>Bump Normal</td><td>Ilusi relief permukaan dengan menggeser normal berdasarkan peta ketinggian</td></tr><tr><td>Principled BSDF</td><td>Shader PBR standar Blender 4.3 (Base Color, Roughness, Metallic, Emission)</td></tr><tr><td>Operator (bpy)</td><td>Fungsi aksi Blender yang bisa dipanggil UI (mis. <code>legoapp.spawn_brick</code>)</td></tr><tr><td>N-Panel</td><td>Sidebar viewport yang muncul saat menekan <code>N</code>; tab custom muncul lewat <code>bl_category</code></td></tr></tbody></table><h2 id="lampiran-b-cookbook-resep-cepat" tabindex="-1">LAMPIRAN B. COOKBOOK RESEP CEPAT <a class="header-anchor" href="#lampiran-b-cookbook-resep-cepat" aria-label="Permalink to &quot;LAMPIRAN B. COOKBOOK RESEP CEPAT&quot;">​</a></h2><p><strong>B1. Menambah lapisan menara</strong> -di <code>_bangun_menara_lego</code>, tambahkan tuple pada daftar <code>lapis</code>: <code>(&quot;lego_biru&quot;, 3, 2, 1.20, math.radians(60))</code> → (warna, studs_x, studs_y, z_pos, rotasi_z).</p><p><strong>B2. Balok LEGO custom via panel</strong> -Warna LEGO → <code>Hijau LEGO</code>; Stud X=4, Stud Y=2; Translasi=(20, 8, 0); Rotasi=(0, 0, 35); klik <strong>Tambah Balok LEGO (Matriks 4x4)</strong>.</p><p><strong>B3. Ganti kepadatan bata dinding</strong> -pilih dinding → Preset <code>Bata Prosedural (Brick + Bump)</code> → Skala UV <code>8</code> → <strong>Terapkan Tekstur &amp; Skala UV</strong>; bandingkan dengan Skala UV <code>2</code>.</p><p><strong>B4. Memperbesar ubin lantai</strong> -ubah <code>uv_scale</code> palet <code>lantai_workstation</code> di <code>DEFAULT_CONFIG_ASSETS</code> menjadi <code>[6.0, 6.0, 1.0]</code> lalu jalankan ulang skrip (konfigurasi terpusat, tanpa hardcode -pola Modul 1 tetap berlaku).</p><p><strong>B5. Shear dinding miring</strong> -pilih segmen dinding → Shear XY=(0.35, 0) → Rotasi Z=0 → <strong>Terapkan Matriks 4x4 ke Objek Aktif</strong> (dinding menjadi condong seperti bangunan dekonstruktivis).</p><h2 id="lampiran-c-bedah-detail-kode-inti-modul2-py" tabindex="-1">LAMPIRAN C. BEDAH DETAIL &amp; KODE INTI <code>modul2.py</code> <a class="header-anchor" href="#lampiran-c-bedah-detail-kode-inti-modul2-py" aria-label="Permalink to &quot;LAMPIRAN C. BEDAH DETAIL &amp; KODE INTI \`modul2.py\`&quot;">​</a></h2><blockquote><p>Kode sumber lengkap: <code>modul2.py</code> (±1.365 baris). Bagian <code>AsciiDenahParser</code> identik dengan Modul 1 (<code>ascii_to_blender_3d.py</code>); lampiran ini membedakan komponen baru Materi 2.</p></blockquote><h3 id="c-1-transform3dengine-matriks-homogen-hierarki" tabindex="-1">C.1 <code>Transform3DEngine</code> -Matriks Homogen &amp; Hierarki <a class="header-anchor" href="#c-1-transform3dengine-matriks-homogen-hierarki" aria-label="Permalink to &quot;C.1 \`Transform3DEngine\` -Matriks Homogen &amp; Hierarki&quot;">​</a></h3><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">class</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> Transform3DEngine</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>
<span class="line"><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">    &quot;&quot;&quot;M = T @ Rz @ Ry @ Rx @ Shear_xy @ S diterapkan ke matrix_world/local.&quot;&quot;&quot;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">    @</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">staticmethod</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> matriks_translasi</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(tx, ty, tz):</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Matrix(((</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">float</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(tx)),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">float</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(ty)),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">float</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(tz)),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)))</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">    @</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">staticmethod</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> matriks_rotasi_z</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(rad):</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        c, s </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> math.cos(rad), math.sin(rad)</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Matrix(((c, </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">-</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">s, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), (s, c, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)))</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">    @</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">staticmethod</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> matriks_shear_xy</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(sh_x</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, sh_y</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">):</span></span>
<span class="line"><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">        &quot;&quot;&quot;Matriks Geser (Shearing) pada sumbu X/Y terhadap Z.&quot;&quot;&quot;</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Matrix(((</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">float</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(sh_x), </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">float</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(sh_y), </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                       (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)))</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">    @</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">classmethod</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> komposisi_trs</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(cls, lokasi</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), rotasi_euler</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                      skala</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), shear</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)):</span></span>
<span class="line"><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">        &quot;&quot;&quot;Menghasilkan matriks komposit M = T @ Rz @ Ry @ Rx @ Shear @ S.&quot;&quot;&quot;</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        T </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.matriks_translasi(</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">*</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">lokasi)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        Rx </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.matriks_rotasi_x(rotasi_euler[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        Ry </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.matriks_rotasi_y(rotasi_euler[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        Rz </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.matriks_rotasi_z(rotasi_euler[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">2</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        Sh </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.matriks_shear_xy(shear[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], shear[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        S </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.matriks_skala(</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">*</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">skala)</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> T </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">@</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Rz </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">@</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Ry </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">@</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Rx </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">@</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Sh </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">@</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> S</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">    @</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">classmethod</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> terapkan_matriks</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(cls, obj, lokasi</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), rotasi_euler</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">),</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                         skala</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), parent</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">None</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">):</span></span>
<span class="line"><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">        &quot;&quot;&quot;Bila berparent: matrix_local relatif parent → M_world = M_parent @ M_local.&quot;&quot;&quot;</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        M_lokal </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.komposisi_trs(lokasi, rotasi_euler, skala)</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        if</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> parent </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">is</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;"> not</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> None</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">            obj.parent </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> parent</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">            obj.matrix_parent_inverse </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> Matrix.Identity(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">4</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">            obj.matrix_local </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> M_lokal</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        else</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">            obj.matrix_world </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> M_lokal</span></span></code></pre></div><h3 id="c-2-texturematerialfactory-jaringan-shader-node" tabindex="-1">C.2 <code>TextureMaterialFactory</code> -Jaringan Shader Node <a class="header-anchor" href="#c-2-texturematerialfactory-jaringan-shader-node" aria-label="Permalink to &quot;C.2 \`TextureMaterialFactory\` -Jaringan Shader Node&quot;">​</a></h3><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">coord_node </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> nodes.new(</span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">type</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;ShaderNodeTexCoord&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">map_node </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> nodes.new(</span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">type</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;ShaderNodeMapping&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">map_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Scale&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">].default_value </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> uv_scale          </span><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;"># kontrol skala UV</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">bump_node </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> nodes.new(</span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">type</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;ShaderNodeBump&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">bump_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Strength&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">].default_value </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> bump_strength</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;"># Contoh BRICK: warna bata + nat + bump relief</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">tex_node </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> nodes.new(</span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">type</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;ShaderNodeTexBrick&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">tex_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Color1&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">].default_value </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> rgba</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">tex_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Color2&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">].default_value </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> tuple</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(spec.get(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;color2&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, [</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.6</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.5</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.4</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">]))</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">tex_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Mortar&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">].default_value </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> (</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.35</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.35</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0.35</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1.0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">links.new(coord_node.outputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Generated&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], map_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Vector&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">links.new(map_node.outputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Vector&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], tex_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Vector&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">links.new(tex_node.outputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Color&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], bsdf.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Base Color&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">links.new(tex_node.outputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Fac&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], bump_node.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Height&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">links.new(bump_node.outputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Normal&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], bsdf.inputs[</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Normal&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span></code></pre></div><h3 id="c-3-assetbuilder-bangun-bata-lego-root-pivot-anak-modular" tabindex="-1">C.3 <code>AssetBuilder._bangun_bata_lego</code> -Root Pivot &amp; Anak Modular <a class="header-anchor" href="#c-3-assetbuilder-bangun-bata-lego-root-pivot-anak-modular" aria-label="Permalink to &quot;C.3 \`AssetBuilder._bangun_bata_lego\` -Root Pivot &amp; Anak Modular&quot;">​</a></h3><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;"># 1) Empty sebagai Root Pivot balok (bukan join!)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">root </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> bpy.data.objects.new(spec.get(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;nama&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;LegoBrick&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">), </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">None</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">root.empty_display_type </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &quot;PLAIN_AXES&quot;</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">bpy.context.scene.collection.objects.link(root)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">Transform3DEngine.terapkan_matriks(</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    root, </span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">lokasi</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(di[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">0</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], di[</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">], z_alas), </span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">rotasi_euler</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">rot, </span><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">skala</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">skala,</span></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">    parent</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">spec.get(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;parent&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">None</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">))</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;"># 2) Badan kubus + stud silinder menjadi anak root</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">self</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">._bangun_kotak({</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;name&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">f</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">{</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">root.name</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">}</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">_Body&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;parent&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: root, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">...</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">})</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">for</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> ix </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">in</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> range</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(studs_x):</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    for</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> iy </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">in</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> range</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(studs_y):</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">        self</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">._bangun_silinder({</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;name&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">f</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">{</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">root.name</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">}</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">_Stud_</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">{</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">ix</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">}</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">_</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">{</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">iy</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">}</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">,</span></span>
<span class="line"><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">                               &quot;di&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: [sx, sy], </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;parent&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: root, </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">...</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">})</span></span></code></pre></div><h3 id="c-4-legoapp-m2-panel-operator-add-on" tabindex="-1">C.4 LegoApp M2 -Panel &amp; Operator Add-on <a class="header-anchor" href="#c-4-legoapp-m2-panel-operator-add-on" aria-label="Permalink to &quot;C.4 LegoApp M2 -Panel &amp; Operator Add-on&quot;">​</a></h3><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">class</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> LEGOAPP_PT_main_panel</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">bpy</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">types</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;">Panel</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">):</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    bl_label </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &quot;Modul 2: LEGO 3D Transform &amp; Texture&quot;</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    bl_space_type </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &quot;VIEW_3D&quot;</span><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;">      # panel muncul di 3D Viewport</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    bl_region_type </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &quot;UI&quot;</span><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;">          # wilayah sidebar (N-Panel)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    bl_category </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &quot;LegoApp M2&quot;</span><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;">     # nama tab</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> draw</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(self, context):</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        props </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> context.scene.lego_app_props</span></span>
<span class="line"><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;">        # box 1: Generator Balok LEGO Modular (warna, studs, tombol spawn)</span></span>
<span class="line"><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;">        # box 2: Matriks Transformasi 3D (T, rotasi, skala, shear)</span></span>
<span class="line"><span style="--shiki-light:#6A737D;--shiki-dark:#6A737D;">        # box 3: Shader Texture &amp; UV Mapping (preset, skala UV)</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> register_lego_ui</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">():</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    for</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> cls</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;"> in</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> DAFTAR_KELAS_UI</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">        bpy.utils.register_class(</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">cls</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    bpy.types.Scene.lego_app_props </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> bpy.props.PointerProperty(</span></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">        type</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">LegoTransformAppProps)</span></span></code></pre></div><h3 id="kode-lengkap" tabindex="-1">Kode Lengkap <a class="header-anchor" href="#kode-lengkap" aria-label="Permalink to &quot;Kode Lengkap&quot;">​</a></h3><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>#!/usr/bin/env python3</span></span>
<span class="line"><span># -*- coding: utf-8 -*-</span></span>
<span class="line"><span>&quot;&quot;&quot;</span></span>
<span class="line"><span>================================================================================</span></span>
<span class="line"><span>MODUL 2 KOMPUTER GRAFIK (V3) - 3D TRANSFORMATION, HIERARCHY, TEXTURE &amp; LEGO APP</span></span>
<span class="line"><span>File: modul2_transform_texture_lego.py (Kompatibel Blender 4.3)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>Fokus Materi 2:</span></span>
<span class="line"><span>  1. Transform3DEngine  : Implementasi eksplisit Matriks Transformasi Homogen 4x4</span></span>
<span class="line"><span>                          (Translasi T, Rotasi Euler Rx/Ry/Rz, Skala S, Shear)</span></span>
<span class="line"><span>                          serta Hierarki Scene Graph (Parent-Child Matrix).</span></span>
<span class="line"><span>  2. TextureFactory     : Pembuatan Shader Node Tree (UV Mapping + Procedural</span></span>
<span class="line"><span>                          Brick, Checker, Wood Wave, Noise Bump, &amp; Image Texture).</span></span>
<span class="line"><span>  3. LegoBrickBuilder   : Perakitan objek modular bergaya LEGO (Studs + Bricks)</span></span>
<span class="line"><span>                          menggunakan komposisi transformasi lokal-ke-dunia.</span></span>
<span class="line"><span>  4. LegoAppPanel (UI)  : Mini-App di Sidebar 3D Viewport Blender (Tekan &#39;N&#39; -&gt;</span></span>
<span class="line"><span>                          tab &#39;LegoApp M2&#39;) untuk manipulasi Transformasi 3D,</span></span>
<span class="line"><span>                          susun balok LEGO interaktif, dan ganti tekstur real-time.</span></span>
<span class="line"><span>================================================================================</span></span>
<span class="line"><span>&quot;&quot;&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>import json</span></span>
<span class="line"><span>import math</span></span>
<span class="line"><span>import os</span></span>
<span class="line"><span>import re</span></span>
<span class="line"><span>from collections import deque</span></span>
<span class="line"><span></span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span># BAGIAN 1: KONFIGURASI DENAH ASCII &amp; PARAMETER SKALA</span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span>SKALA_X_METER_PER_KARAKTER = 0.5</span></span>
<span class="line"><span>SKALA_Y_METER_PER_KARAKTER = 0.5</span></span>
<span class="line"><span>TINGGI_DINDING_DEFAULT     = 3.0</span></span>
<span class="line"><span>TEBAL_DINDING_DEFAULT      = 0.15</span></span>
<span class="line"><span></span></span>
<span class="line"><span>DENAH_ASCII = r&quot;&quot;&quot;</span></span>
<span class="line"><span>+---+---------------------------------------------------------+---+</span></span>
<span class="line"><span>|   | [R] | [R] | [R] |     |     |     | [R] | [R] | [R] | [R] |   |</span></span>
<span class="line"><span>|   +-----+-----+-----+     |     |     +-----+-----+-----+-----+   |</span></span>
<span class="line"><span>|   |                 |                                   |     |   |</span></span>
<span class="line"><span>| R |                                                           | R |</span></span>
<span class="line"><span>| . |                    WORK STATION (UTARA)                   | . |</span></span>
<span class="line"><span>| A |                                                           | A |</span></span>
<span class="line"><span>| R |                                                           | R |</span></span>
<span class="line"><span>| S |                                                           | S |</span></span>
<span class="line"><span>| I |                                                           | I |</span></span>
<span class="line"><span>| P |                                                           | P |</span></span>
<span class="line"><span>+---+-------+-------------------+-----+-------------------+-----+---+</span></span>
<span class="line"><span>|   |       |    TOILET PRIA    |     |  LIFT  |  PANTRY  |     |   |</span></span>
<span class="line"><span>|   |       +-------------------+     +--------+----------+     |   |</span></span>
<span class="line"><span>|   |       | R.AHU | [LIFT-1]  |  C  |  LIFT  |  TANGGA  |     |   |</span></span>
<span class="line"><span>|   |       |       | [LIFT-2]  |  O  +--------+ DARURAT  |     |   |</span></span>
<span class="line"><span>|   |       +-------+-----------+  R  | [LIFT] |          |     |   |</span></span>
<span class="line"><span>|   |       |                   |  I  +--------+----------+     |   |</span></span>
<span class="line"><span>|   |       |   TOILET WANITA   |  D  |    TANGGA DARURAT |     |   |</span></span>
<span class="line"><span>|   |       |                   |  O  +-------------------+     |   |</span></span>
<span class="line"><span>|   |       |                   |  R  |      R. PANEL     |     |   |</span></span>
<span class="line"><span>+---+-------+-------------------+-----+-------------------+-----+---+</span></span>
<span class="line"><span>|   |                                                           |   |</span></span>
<span class="line"><span>| R |                                                           | R |</span></span>
<span class="line"><span>| . |                    WORK STATION (SELATAN)                 | . |</span></span>
<span class="line"><span>| A |                                                           | A |</span></span>
<span class="line"><span>| R |                                                           | R |</span></span>
<span class="line"><span>| S |                                                           | S |</span></span>
<span class="line"><span>| I |                                                           | I |</span></span>
<span class="line"><span>| P |                 |                                   |     | P |</span></span>
<span class="line"><span>|   +---+---+---+-----+---+---+---+---+---+---+---+---+---+-----+   |</span></span>
<span class="line"><span>|   | R | R | R |  R  | R | R | R | R | R | R | R | R | R |  R  |   |</span></span>
<span class="line"><span>+---+---+---+---+-----+---+---+---+---+---+---+---+---+---+-----+---+</span></span>
<span class="line"><span>&quot;&quot;&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span># BAGIAN 2: PALET MATERIAL &amp; KONFIGURASI TEKSTUR PROSEDURAL (MATERI 2)</span></span>
<span class="line"><span># Mendukung tipe tekstur: &quot;NONE&quot;, &quot;BRICK&quot;, &quot;CHECKER&quot;, &quot;WOOD&quot;, &quot;NOISE&quot;, &quot;LEGO_PLASTIC&quot;</span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span>DEFAULT_CONFIG_ASSETS = {</span></span>
<span class="line"><span>    &quot;palet&quot;: {</span></span>
<span class="line"><span>        &quot;dinding_eksterior&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.88, 0.84, 0.78, 1.0], &quot;roughness&quot;: 0.85,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;BRICK&quot;, &quot;color2&quot;: [0.65, 0.58, 0.50, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [4.0, 4.0, 4.0], &quot;bump_strength&quot;: 0.25</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;dinding_interior&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.90, 0.91, 0.93, 1.0], &quot;roughness&quot;: 0.75,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;NOISE&quot;, &quot;uv_scale&quot;: [8.0, 8.0, 8.0], &quot;bump_strength&quot;: 0.08</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;dinding_core&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.72, 0.76, 0.80, 1.0], &quot;roughness&quot;: 0.65,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;BRICK&quot;, &quot;color2&quot;: [0.55, 0.58, 0.62, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [3.0, 3.0, 3.0], &quot;bump_strength&quot;: 0.20</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;kusen_kayu&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.42, 0.25, 0.12, 1.0], &quot;roughness&quot;: 0.55,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;WOOD&quot;, &quot;color2&quot;: [0.25, 0.14, 0.06, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [6.0, 6.0, 6.0], &quot;bump_strength&quot;: 0.12</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;kusen_aluminium&quot;: {&quot;rgba&quot;: [0.22, 0.25, 0.28, 1.0], &quot;roughness&quot;: 0.25, &quot;metallic&quot;: 0.8},</span></span>
<span class="line"><span>        &quot;kaca_jendela&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.65, 0.85, 0.95, 1.0], &quot;roughness&quot;: 0.10,</span></span>
<span class="line"><span>            &quot;emission&quot;: [0.4, 0.6, 0.7, 1.0], &quot;emission_strength&quot;: 0.20</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_workstation&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.85, 0.82, 0.75, 1.0], &quot;roughness&quot;: 0.45,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;CHECKER&quot;, &quot;color2&quot;: [0.72, 0.68, 0.60, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [12.0, 12.0, 1.0], &quot;bump_strength&quot;: 0.05</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_koridor&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.78, 0.80, 0.83, 1.0], &quot;roughness&quot;: 0.35,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;CHECKER&quot;, &quot;color2&quot;: [0.60, 0.63, 0.68, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [8.0, 8.0, 1.0], &quot;bump_strength&quot;: 0.05</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_ruang_r&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.68, 0.48, 0.30, 1.0], &quot;roughness&quot;: 0.50,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;WOOD&quot;, &quot;color2&quot;: [0.48, 0.32, 0.18, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [5.0, 5.0, 5.0], &quot;bump_strength&quot;: 0.10</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_arsip&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.58, 0.60, 0.62, 1.0], &quot;roughness&quot;: 0.80,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;NOISE&quot;, &quot;uv_scale&quot;: [10.0, 10.0, 1.0], &quot;bump_strength&quot;: 0.15</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_toilet&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.82, 0.94, 0.96, 1.0], &quot;roughness&quot;: 0.25,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;CHECKER&quot;, &quot;color2&quot;: [0.62, 0.82, 0.86, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [16.0, 16.0, 1.0], &quot;bump_strength&quot;: 0.08</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_pantry&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.90, 0.84, 0.72, 1.0], &quot;roughness&quot;: 0.40,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;CHECKER&quot;, &quot;color2&quot;: [0.76, 0.66, 0.52, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [10.0, 10.0, 1.0], &quot;bump_strength&quot;: 0.06</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;lantai_teknis&quot;: {&quot;rgba&quot;: [0.42, 0.45, 0.48, 1.0], &quot;roughness&quot;: 0.85, &quot;tex_type&quot;: &quot;NOISE&quot;},</span></span>
<span class="line"><span>        &quot;lantai_tangga&quot;: {&quot;rgba&quot;: [0.52, 0.50, 0.48, 1.0], &quot;roughness&quot;: 0.80},</span></span>
<span class="line"><span>        &quot;lantai_lift&quot;:   {&quot;rgba&quot;: [0.30, 0.32, 0.35, 1.0], &quot;roughness&quot;: 0.35, &quot;metallic&quot;: 0.6},</span></span>
<span class="line"><span>        &quot;kayu_meja&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.76, 0.55, 0.34, 1.0], &quot;roughness&quot;: 0.45,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;WOOD&quot;, &quot;color2&quot;: [0.55, 0.38, 0.20, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [4.0, 4.0, 4.0], &quot;bump_strength&quot;: 0.08</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;kayu_gelap&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.32, 0.20, 0.11, 1.0], &quot;roughness&quot;: 0.50,</span></span>
<span class="line"><span>            &quot;tex_type&quot;: &quot;WOOD&quot;, &quot;color2&quot;: [0.18, 0.10, 0.05, 1.0],</span></span>
<span class="line"><span>            &quot;uv_scale&quot;: [5.0, 5.0, 5.0], &quot;bump_strength&quot;: 0.10</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;partisi_kubikel&quot;: {&quot;rgba&quot;: [0.46, 0.56, 0.68, 1.0], &quot;roughness&quot;: 0.80, &quot;tex_type&quot;: &quot;NOISE&quot;},</span></span>
<span class="line"><span>        &quot;kursi_kantor&quot;:    {&quot;rgba&quot;: [0.18, 0.20, 0.24, 1.0], &quot;roughness&quot;: 0.65},</span></span>
<span class="line"><span>        &quot;kain_sofa&quot;:       {&quot;rgba&quot;: [0.26, 0.42, 0.58, 1.0], &quot;roughness&quot;: 0.85, &quot;tex_type&quot;: &quot;NOISE&quot;},</span></span>
<span class="line"><span>        &quot;kain_kasur&quot;:      {&quot;rgba&quot;: [0.92, 0.90, 0.86, 1.0], &quot;roughness&quot;: 0.80},</span></span>
<span class="line"><span>        &quot;selimut_biru&quot;:    {&quot;rgba&quot;: [0.30, 0.50, 0.72, 1.0], &quot;roughness&quot;: 0.85},</span></span>
<span class="line"><span>        &quot;logam_abu&quot;:       {&quot;rgba&quot;: [0.65, 0.68, 0.72, 1.0], &quot;roughness&quot;: 0.30, &quot;metallic&quot;: 0.75},</span></span>
<span class="line"><span>        &quot;logam_lift&quot;:      {&quot;rgba&quot;: [0.80, 0.82, 0.85, 1.0], &quot;roughness&quot;: 0.20, &quot;metallic&quot;: 0.85},</span></span>
<span class="line"><span>        &quot;keramik_putih&quot;:   {&quot;rgba&quot;: [0.96, 0.97, 0.98, 1.0], &quot;roughness&quot;: 0.15},</span></span>
<span class="line"><span>        &quot;layar_monitor&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.08, 0.12, 0.18, 1.0], &quot;roughness&quot;: 0.15,</span></span>
<span class="line"><span>            &quot;emission&quot;: [0.15, 0.50, 0.95, 1.0], &quot;emission_strength&quot;: 0.8</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;hijau_daun&quot;:      {&quot;rgba&quot;: [0.22, 0.58, 0.26, 1.0], &quot;roughness&quot;: 0.65},</span></span>
<span class="line"><span>        &quot;pot_terakota&quot;:    {&quot;rgba&quot;: [0.72, 0.38, 0.22, 1.0], &quot;roughness&quot;: 0.75, &quot;tex_type&quot;: &quot;NOISE&quot;},</span></span>
<span class="line"><span>        &quot;panel_listrik&quot;:   {&quot;rgba&quot;: [0.25, 0.32, 0.38, 1.0], &quot;roughness&quot;: 0.45, &quot;metallic&quot;: 0.5},</span></span>
<span class="line"><span>        &quot;lampu_indikator&quot;: {</span></span>
<span class="line"><span>            &quot;rgba&quot;: [0.10, 0.90, 0.30, 1.0], &quot;roughness&quot;: 0.20,</span></span>
<span class="line"><span>            &quot;emission&quot;: [0.10, 0.95, 0.30, 1.0], &quot;emission_strength&quot;: 2.5</span></span>
<span class="line"><span>        },</span></span>
<span class="line"><span>        &quot;mesin_hvac&quot;:      {&quot;rgba&quot;: [0.35, 0.52, 0.65, 1.0], &quot;roughness&quot;: 0.40, &quot;metallic&quot;: 0.5},</span></span>
<span class="line"><span>        &quot;kardus_arsip&quot;:    {&quot;rgba&quot;: [0.78, 0.64, 0.44, 1.0], &quot;roughness&quot;: 0.85},</span></span>
<span class="line"><span>        &quot;rail_tangga&quot;:     {&quot;rgba&quot;: [0.85, 0.22, 0.18, 1.0], &quot;roughness&quot;: 0.35},</span></span>
<span class="line"><span>        &quot;teks_label&quot;:      {&quot;rgba&quot;: [0.12, 0.14, 0.18, 1.0], &quot;roughness&quot;: 0.50},</span></span>
<span class="line"><span>        # Material Khusus Balok LEGO (Materi 2)</span></span>
<span class="line"><span>        &quot;lego_merah&quot;:      {&quot;rgba&quot;: [0.85, 0.12, 0.12, 1.0], &quot;roughness&quot;: 0.20, &quot;tex_type&quot;: &quot;LEGO_PLASTIC&quot;},</span></span>
<span class="line"><span>        &quot;lego_kuning&quot;:     {&quot;rgba&quot;: [0.95, 0.78, 0.08, 1.0], &quot;roughness&quot;: 0.20, &quot;tex_type&quot;: &quot;LEGO_PLASTIC&quot;},</span></span>
<span class="line"><span>        &quot;lego_biru&quot;:       {&quot;rgba&quot;: [0.10, 0.38, 0.82, 1.0], &quot;roughness&quot;: 0.20, &quot;tex_type&quot;: &quot;LEGO_PLASTIC&quot;},</span></span>
<span class="line"><span>        &quot;lego_hijau&quot;:      {&quot;rgba&quot;: [0.12, 0.68, 0.28, 1.0], &quot;roughness&quot;: 0.20, &quot;tex_type&quot;: &quot;LEGO_PLASTIC&quot;}</span></span>
<span class="line"><span>    }</span></span>
<span class="line"><span>}</span></span>
<span class="line"><span></span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span># BAGIAN 3: KELAS AsciiDenahParser (Tetap kompatibel dengan Modul 1)</span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span>class AsciiDenahParser:</span></span>
<span class="line"><span>    def __init__(self, scale_x=0.5, scale_y=0.5, tinggi_dinding=3.0, tebal_dinding=0.15):</span></span>
<span class="line"><span>        self.scale_x = float(scale_x)</span></span>
<span class="line"><span>        self.scale_y = float(scale_y)</span></span>
<span class="line"><span>        self.tinggi_dinding = float(tinggi_dinding)</span></span>
<span class="line"><span>        self.tebal_dinding = float(tebal_dinding)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    @staticmethod</span></span>
<span class="line"><span>    def _normalisasi_baris(ascii_text):</span></span>
<span class="line"><span>        raw_lines = [l.rstrip(&quot;\\r\\n&quot;) for l in ascii_text.strip().splitlines() if l.strip()]</span></span>
<span class="line"><span>        if not raw_lines:</span></span>
<span class="line"><span>            raise ValueError(&quot;Teks ASCII kosong!&quot;)</span></span>
<span class="line"><span>        max_len = max(len(l) for l in raw_lines)</span></span>
<span class="line"><span>        grid = []</span></span>
<span class="line"><span>        for l in raw_lines:</span></span>
<span class="line"><span>            if len(l) &lt; max_len and &quot;---&quot; in l:</span></span>
<span class="line"><span>                diff = max_len - len(l)</span></span>
<span class="line"><span>                runs = [(m.end() - m.start(), m.start(), m.end()) for m in re.finditer(r&quot;-+&quot;, l)]</span></span>
<span class="line"><span>                runs.sort(reverse=True)</span></span>
<span class="line"><span>                _, start_idx, _ = runs[0]</span></span>
<span class="line"><span>                l = l[:start_idx] + (&quot;-&quot; * diff) + l[start_idx:]</span></span>
<span class="line"><span>            grid.append(l.ljust(max_len))</span></span>
<span class="line"><span>        return grid</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    @staticmethod</span></span>
<span class="line"><span>    def _is_horizontal_wall_char(grid, r, c):</span></span>
<span class="line"><span>        W = len(grid[0])</span></span>
<span class="line"><span>        ch = grid[r][c]</span></span>
<span class="line"><span>        if ch == &quot;+&quot;:</span></span>
<span class="line"><span>            return True</span></span>
<span class="line"><span>        if ch == &quot;-&quot;:</span></span>
<span class="line"><span>            left = grid[r][c - 1] if c &gt; 0 else &quot; &quot;</span></span>
<span class="line"><span>            right = grid[r][c + 1] if c + 1 &lt; W else &quot; &quot;</span></span>
<span class="line"><span>            return (left in (&quot;+&quot;, &quot;-&quot;)) or (right in (&quot;+&quot;, &quot;-&quot;))</span></span>
<span class="line"><span>        return False</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    @staticmethod</span></span>
<span class="line"><span>    def _is_vertical_wall_char(grid, r, c):</span></span>
<span class="line"><span>        return grid[r][c] in (&quot;+&quot;, &quot;|&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _is_any_wall(self, grid, r, c):</span></span>
<span class="line"><span>        ch = grid[r][c]</span></span>
<span class="line"><span>        if ch in (&quot;+&quot;, &quot;|&quot;):</span></span>
<span class="line"><span>            return True</span></span>
<span class="line"><span>        if ch == &quot;-&quot;:</span></span>
<span class="line"><span>            return self._is_horizontal_wall_char(grid, r, c)</span></span>
<span class="line"><span>        return False</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _rc_to_xy(self, r, c, max_r):</span></span>
<span class="line"><span>        x = round(c * self.scale_x, 3)</span></span>
<span class="line"><span>        y = round((max_r - r) * self.scale_y, 3)</span></span>
<span class="line"><span>        return x, y</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _ekstrak_ruangan(self, grid):</span></span>
<span class="line"><span>        H, W = len(grid), len(grid[0])</span></span>
<span class="line"><span>        max_r = H - 1</span></span>
<span class="line"><span>        visited = [[False] * W for _ in range(H)]</span></span>
<span class="line"><span>        rooms = []</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        for r in range(H):</span></span>
<span class="line"><span>            for c in range(W):</span></span>
<span class="line"><span>                if not visited[r][c] and not self._is_any_wall(grid, r, c):</span></span>
<span class="line"><span>                    q = deque([(r, c)])</span></span>
<span class="line"><span>                    visited[r][c] = True</span></span>
<span class="line"><span>                    cells = []</span></span>
<span class="line"><span>                    while q:</span></span>
<span class="line"><span>                        cr, cc = q.popleft()</span></span>
<span class="line"><span>                        cells.append((cr, cc))</span></span>
<span class="line"><span>                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:</span></span>
<span class="line"><span>                            nr, nc = cr + dr, cc + dc</span></span>
<span class="line"><span>                            if 0 &lt;= nr &lt; H and 0 &lt;= nc &lt; W and not visited[nr][nc] and not self._is_any_wall(grid, nr, nc):</span></span>
<span class="line"><span>                                visited[nr][nc] = True</span></span>
<span class="line"><span>                                q.append((nr, nc))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                    min_r, max_r_cell = min(p[0] for p in cells), max(p[0] for p in cells)</span></span>
<span class="line"><span>                    min_c, max_c_cell = min(p[1] for p in cells), max(p[1] for p in cells)</span></span>
<span class="line"><span>                    r1, r2 = max(0, min_r - 1), min(max_r, max_r_cell + 1)</span></span>
<span class="line"><span>                    c1, c2 = max(0, min_c - 1), min(W - 1, max_c_cell + 1)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                    cell_set = set(cells)</span></span>
<span class="line"><span>                    row_texts = []</span></span>
<span class="line"><span>                    for rr in range(min_r, max_r_cell + 1):</span></span>
<span class="line"><span>                        s = &quot;&quot;.join(grid[rr][cc] for cc in range(min_c, max_c_cell + 1) if (rr, cc) in cell_set)</span></span>
<span class="line"><span>                        s_clean = &quot; &quot;.join(s.split())</span></span>
<span class="line"><span>                        if s_clean:</span></span>
<span class="line"><span>                            row_texts.append(s_clean)</span></span>
<span class="line"><span>                    raw_label = &quot; &quot;.join(row_texts)</span></span>
<span class="line"><span>                    norm_label = raw_label</span></span>
<span class="line"><span>                    if raw_label.replace(&quot; &quot;, &quot;&quot;) == &quot;R.ARSIP&quot;:</span></span>
<span class="line"><span>                        norm_label = &quot;R. ARSIP&quot;</span></span>
<span class="line"><span>                    elif raw_label.replace(&quot; &quot;, &quot;&quot;) == &quot;CORIDOR&quot;:</span></span>
<span class="line"><span>                        norm_label = &quot;CORIDOR&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                    x1, y2 = self._rc_to_xy(r1, c1, max_r)</span></span>
<span class="line"><span>                    x2, y1 = self._rc_to_xy(r2, c2, max_r)</span></span>
<span class="line"><span>                    rooms.append({</span></span>
<span class="line"><span>                        &quot;id&quot;: len(rooms), &quot;r1&quot;: r1, &quot;r2&quot;: r2, &quot;c1&quot;: c1, &quot;c2&quot;: c2,</span></span>
<span class="line"><span>                        &quot;x1&quot;: min(x1, x2), &quot;x2&quot;: max(x1, x2), &quot;y1&quot;: min(y1, y2), &quot;y2&quot;: max(y1, y2),</span></span>
<span class="line"><span>                        &quot;area_cells&quot;: len(cells), &quot;raw_label&quot;: raw_label, &quot;label&quot;: norm_label,</span></span>
<span class="line"><span>                    })</span></span>
<span class="line"><span>        return rooms</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _ekstrak_segmen_dinding(self, grid):</span></span>
<span class="line"><span>        H, W = len(grid), len(grid[0])</span></span>
<span class="line"><span>        max_r = H - 1</span></span>
<span class="line"><span>        horiz_segments, vert_segments = [], []</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        for r in range(H):</span></span>
<span class="line"><span>            c = 0</span></span>
<span class="line"><span>            while c &lt; W:</span></span>
<span class="line"><span>                if self._is_horizontal_wall_char(grid, r, c):</span></span>
<span class="line"><span>                    start_c = c</span></span>
<span class="line"><span>                    has_dash = False</span></span>
<span class="line"><span>                    while c &lt; W and self._is_horizontal_wall_char(grid, r, c):</span></span>
<span class="line"><span>                        if grid[r][c] == &quot;-&quot;:</span></span>
<span class="line"><span>                            has_dash = True</span></span>
<span class="line"><span>                        c += 1</span></span>
<span class="line"><span>                    end_c = c - 1</span></span>
<span class="line"><span>                    if has_dash and end_c &gt; start_c:</span></span>
<span class="line"><span>                        x1, y = self._rc_to_xy(r, start_c, max_r)</span></span>
<span class="line"><span>                        x2, _ = self._rc_to_xy(r, end_c, max_r)</span></span>
<span class="line"><span>                        mat = &quot;dinding_eksterior&quot; if r in (0, max_r) else (&quot;dinding_core&quot; if 11 &lt;= r &lt;= 21 else &quot;dinding_interior&quot;)</span></span>
<span class="line"><span>                        horiz_segments.append({</span></span>
<span class="line"><span>                            &quot;nama&quot;: f&quot;Dinding_H_R{r:02d}_C{start_c:02d}_{end_c:02d}&quot;,</span></span>
<span class="line"><span>                            &quot;orientasi&quot;: &quot;H&quot;, &quot;r&quot;: r, &quot;c1&quot;: start_c, &quot;c2&quot;: end_c,</span></span>
<span class="line"><span>                            &quot;dari&quot;: [x1, y], &quot;ke&quot;: [x2, y], &quot;material&quot;: mat, &quot;celah&quot;: [],</span></span>
<span class="line"><span>                        })</span></span>
<span class="line"><span>                else:</span></span>
<span class="line"><span>                    c += 1</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        for c in range(W):</span></span>
<span class="line"><span>            r = 0</span></span>
<span class="line"><span>            while r &lt; H:</span></span>
<span class="line"><span>                if self._is_vertical_wall_char(grid, r, c):</span></span>
<span class="line"><span>                    start_r = r</span></span>
<span class="line"><span>                    has_pipe = False</span></span>
<span class="line"><span>                    while r &lt; H and self._is_vertical_wall_char(grid, r, c):</span></span>
<span class="line"><span>                        if grid[r][c] == &quot;|&quot;:</span></span>
<span class="line"><span>                            has_pipe = True</span></span>
<span class="line"><span>                        r += 1</span></span>
<span class="line"><span>                    end_r = r - 1</span></span>
<span class="line"><span>                    if has_pipe:</span></span>
<span class="line"><span>                        if start_r &gt; 0 and self._is_horizontal_wall_char(grid, start_r - 1, c):</span></span>
<span class="line"><span>                            start_r -= 1</span></span>
<span class="line"><span>                        if end_r + 1 &lt; H and self._is_horizontal_wall_char(grid, end_r + 1, c):</span></span>
<span class="line"><span>                            end_r += 1</span></span>
<span class="line"><span>                        if end_r == start_r:</span></span>
<span class="line"><span>                            end_r = min(max_r, start_r + 1)</span></span>
<span class="line"><span>                        x, y2 = self._rc_to_xy(start_r, c, max_r)</span></span>
<span class="line"><span>                        _, y1 = self._rc_to_xy(end_r, c, max_r)</span></span>
<span class="line"><span>                        mat = &quot;dinding_eksterior&quot; if c in (0, W - 1) else (&quot;dinding_core&quot; if (12 &lt;= c &lt;= 58 and start_r &gt;= 11 and end_r &lt;= 21) else &quot;dinding_interior&quot;)</span></span>
<span class="line"><span>                        vert_segments.append({</span></span>
<span class="line"><span>                            &quot;nama&quot;: f&quot;Dinding_V_C{c:02d}_R{start_r:02d}_{end_r:02d}&quot;,</span></span>
<span class="line"><span>                            &quot;orientasi&quot;: &quot;V&quot;, &quot;c&quot;: c, &quot;r1&quot;: start_r, &quot;r2&quot;: end_r,</span></span>
<span class="line"><span>                            &quot;dari&quot;: [x, min(y1, y2)], &quot;ke&quot;: [x, max(y1, y2)], &quot;material&quot;: mat, &quot;celah&quot;: [],</span></span>
<span class="line"><span>                        })</span></span>
<span class="line"><span>                else:</span></span>
<span class="line"><span>                    r += 1</span></span>
<span class="line"><span>        return horiz_segments, vert_segments</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    @staticmethod</span></span>
<span class="line"><span>    def _tambah_celah_ke_segmen(seg_list, orientasi, garis_idx, pos_tengah, lebar_celah, tinggi_bukaan=2.1, ambang_bawah=0.0):</span></span>
<span class="line"><span>        half = round(lebar_celah / 2.0, 3)</span></span>
<span class="line"><span>        c_dari, c_ke = round(pos_tengah - half, 3), round(pos_tengah + half, 3)</span></span>
<span class="line"><span>        for seg in seg_list:</span></span>
<span class="line"><span>            if orientasi == &quot;H&quot; and seg[&quot;r&quot;] == garis_idx:</span></span>
<span class="line"><span>                s_min, s_max = min(seg[&quot;dari&quot;][0], seg[&quot;ke&quot;][0]), max(seg[&quot;dari&quot;][0], seg[&quot;ke&quot;][0])</span></span>
<span class="line"><span>            elif orientasi == &quot;V&quot; and seg[&quot;c&quot;] == garis_idx:</span></span>
<span class="line"><span>                s_min, s_max = min(seg[&quot;dari&quot;][1], seg[&quot;ke&quot;][1]), max(seg[&quot;dari&quot;][1], seg[&quot;ke&quot;][1])</span></span>
<span class="line"><span>            else:</span></span>
<span class="line"><span>                continue</span></span>
<span class="line"><span>            if c_dari &gt;= s_min + 0.05 and c_ke &lt;= s_max - 0.05:</span></span>
<span class="line"><span>                if not any(not (c_ke &lt;= ex[&quot;dari&quot;] or c_dari &gt;= ex[&quot;ke&quot;]) for ex in seg[&quot;celah&quot;]):</span></span>
<span class="line"><span>                    seg[&quot;celah&quot;].append({&quot;dari&quot;: c_dari, &quot;ke&quot;: c_ke, &quot;tinggi_bukaan&quot;: round(tinggi_bukaan, 2), &quot;ambang_bawah&quot;: round(ambang_bawah, 2)})</span></span>
<span class="line"><span>                return True</span></span>
<span class="line"><span>        return False</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _injeksi_pintu_dan_jendela_otomatis(self, rooms, horiz_segments, vert_segments, max_r, max_c):</span></span>
<span class="line"><span>        for rm in rooms:</span></span>
<span class="line"><span>            lbl = rm[&quot;label&quot;].upper()</span></span>
<span class="line"><span>            r1, r2, c1, c2 = rm[&quot;r1&quot;], rm[&quot;r2&quot;], rm[&quot;c1&quot;], rm[&quot;c2&quot;]</span></span>
<span class="line"><span>            cx, cy = round((rm[&quot;x1&quot;] + rm[&quot;x2&quot;]) / 2.0, 2), round((rm[&quot;y1&quot;] + rm[&quot;y2&quot;]) / 2.0, 2)</span></span>
<span class="line"><span>            width_x, height_y = rm[&quot;x2&quot;] - rm[&quot;x1&quot;], rm[&quot;y2&quot;] - rm[&quot;y1&quot;]</span></span>
<span class="line"><span>            lebar_pintu = max(0.7, min(0.9, round(min(width_x, height_y) * 0.45, 2)))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            if lbl == &quot;[R]&quot; and r1 == 0:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r2, cx, lebar_pintu, 2.1, 0.0)</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r1, cx, min(1.2, width_x * 0.5), 1.0, 1.0)</span></span>
<span class="line"><span>            elif lbl == &quot;R&quot; and r2 == max_r:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r1, cx, lebar_pintu, 2.1, 0.0)</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r2, cx, min(1.0, width_x * 0.5), 1.0, 1.0)</span></span>
<span class="line"><span>            elif &quot;ARSIP&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c2 if c1 == 0 else c1, cy, 1.0, 2.1, 0.0)</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c1 if c1 == 0 else c2, cy, 1.6, 1.0, 1.1)</span></span>
<span class="line"><span>            elif &quot;CORIDOR&quot; in lbl or &quot;KORIDOR&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r1, cx, min(2.0, width_x - 0.6), 2.5, 0.0)</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r2, cx, min(2.0, width_x - 0.6), 2.5, 0.0)</span></span>
<span class="line"><span>            elif &quot;TOILET&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c2, cy, 0.9, 2.1, 0.0)</span></span>
<span class="line"><span>            elif &quot;LIFT-1&quot; in lbl or &quot;LIFT-2&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c2, cy, 1.1, 2.2, 0.0)</span></span>
<span class="line"><span>            elif lbl in (&quot;LIFT&quot;, &quot;[LIFT]&quot;):</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c1, cy, 0.8, 2.1, 0.0)</span></span>
<span class="line"><span>            elif &quot;AHU&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c1, cy, 0.9, 2.1, 0.0)</span></span>
<span class="line"><span>            elif &quot;PANTRY&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(horiz_segments, &quot;H&quot;, r1, cx, 0.9, 2.1, 0.0)</span></span>
<span class="line"><span>            elif &quot;TANGGA&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c1 if c1 == 38 else c2, cy, 0.85, 2.1, 0.0)</span></span>
<span class="line"><span>            elif &quot;PANEL&quot; in lbl:</span></span>
<span class="line"><span>                self._tambah_celah_ke_segmen(vert_segments, &quot;V&quot;, c1, cy, 0.8, 2.1, 0.0)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _tentukan_material_lantai(self, label):</span></span>
<span class="line"><span>        lbl = label.upper()</span></span>
<span class="line"><span>        if &quot;WORK STATION&quot; in lbl or &quot;TAMU&quot; in lbl: return &quot;lantai_workstation&quot;</span></span>
<span class="line"><span>        if &quot;CORIDOR&quot; in lbl or lbl == &quot;&quot;: return &quot;lantai_koridor&quot;</span></span>
<span class="line"><span>        if lbl in (&quot;[R]&quot;, &quot;R&quot;) or &quot;KAMAR&quot; in lbl: return &quot;lantai_ruang_r&quot;</span></span>
<span class="line"><span>        if &quot;ARSIP&quot; in lbl: return &quot;lantai_arsip&quot;</span></span>
<span class="line"><span>        if &quot;TOILET&quot; in lbl or &quot;MANDI&quot; in lbl: return &quot;lantai_toilet&quot;</span></span>
<span class="line"><span>        if &quot;PANTRY&quot; in lbl or &quot;DAPUR&quot; in lbl: return &quot;lantai_pantry&quot;</span></span>
<span class="line"><span>        if &quot;TANGGA&quot; in lbl: return &quot;lantai_tangga&quot;</span></span>
<span class="line"><span>        if &quot;LIFT&quot; in lbl: return &quot;lantai_lift&quot;</span></span>
<span class="line"><span>        return &quot;lantai_teknis&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def _bangun_furnitur_dan_label_otomatis(self, rooms):</span></span>
<span class="line"><span>        furnitur, label_ruang = [], []</span></span>
<span class="line"><span>        for rm in rooms:</span></span>
<span class="line"><span>            lbl = rm[&quot;label&quot;].upper()</span></span>
<span class="line"><span>            x1, x2, y1, y2 = rm[&quot;x1&quot;], rm[&quot;x2&quot;], rm[&quot;y1&quot;], rm[&quot;y2&quot;]</span></span>
<span class="line"><span>            cx, cy = round((x1 + x2) / 2.0, 2), round((y1 + y2) / 2.0, 2)</span></span>
<span class="line"><span>            wx, wy = round(x2 - x1, 2), round(y2 - y1, 2)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            if rm[&quot;label&quot;]:</span></span>
<span class="line"><span>                label_ruang.append({</span></span>
<span class="line"><span>                    &quot;teks&quot;: rm[&quot;label&quot;], &quot;di&quot;: [cx, cy],</span></span>
<span class="line"><span>                    &quot;ukuran&quot;: 0.45 if wx &gt;= 6.0 else (0.28 if wx &gt;= 2.5 else 0.22),</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            if &quot;WORK STATION&quot; in lbl:</span></span>
<span class="line"><span>                is_utara = &quot;UTARA&quot; in lbl</span></span>
<span class="line"><span>                y_base = round(y1 + 1.8, 2) if is_utara else round(y2 - 1.8, 2)</span></span>
<span class="line"><span>                y_row2 = round(y1 + 3.4, 2) if is_utara else round(y2 - 3.4, 2)</span></span>
<span class="line"><span>                for idx, x_pos in enumerate([5.5, 9.0, 12.5, 21.5, 25.0, 28.5]):</span></span>
<span class="line"><span>                    if x1 + 1.0 &lt; x_pos &lt; x2 - 1.0:</span></span>
<span class="line"><span>                        # Menambahkan atribut transformasi 3D eksplisit (scale &amp; rotasi)</span></span>
<span class="line"><span>                        furnitur.append({</span></span>
<span class="line"><span>                            &quot;nama&quot;: f&quot;Kubikel_{&#39;U&#39; if is_utara else &#39;S&#39;}_R1_{idx+1}&quot;,</span></span>
<span class="line"><span>                            &quot;type&quot;: &quot;meja_kerja&quot;, &quot;di&quot;: [x_pos, y_base],</span></span>
<span class="line"><span>                            &quot;rot&quot;: [0.0, 0.0, 0.0 if is_utara else round(math.pi, 4)],</span></span>
<span class="line"><span>                            &quot;scale&quot;: [1.0, 1.0, 1.0],</span></span>
<span class="line"><span>                        })</span></span>
<span class="line"><span>                        furnitur.append({</span></span>
<span class="line"><span>                            &quot;nama&quot;: f&quot;Kubikel_{&#39;U&#39; if is_utara else &#39;S&#39;}_R2_{idx+1}&quot;,</span></span>
<span class="line"><span>                            &quot;type&quot;: &quot;meja_kerja&quot;, &quot;di&quot;: [x_pos, y_row2],</span></span>
<span class="line"><span>                            &quot;rot&quot;: [0.0, 0.0, round(math.pi, 4) if is_utara else 0.0],</span></span>
<span class="line"><span>                            &quot;scale&quot;: [1.0, 1.0, 1.0],</span></span>
<span class="line"><span>                        })</span></span>
<span class="line"><span>                # Tambahkan Monumen LEGO Modular di tengah Workstation (Materi 2)</span></span>
<span class="line"><span>                furnitur.append({</span></span>
<span class="line"><span>                    &quot;nama&quot;: f&quot;MenaraLego_{&#39;Utara&#39; if is_utara else &#39;Selatan&#39;}&quot;,</span></span>
<span class="line"><span>                    &quot;type&quot;: &quot;menara_lego&quot;,</span></span>
<span class="line"><span>                    &quot;di&quot;: [cx, round((y_base + y_row2) / 2.0, 2)],</span></span>
<span class="line"><span>                    &quot;rot&quot;: [0.0, 0.0, round(math.pi / 4.0, 4)],</span></span>
<span class="line"><span>                    &quot;scale&quot;: [1.1, 1.1, 1.1],</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            elif lbl in (&quot;[R]&quot;, &quot;R&quot;):</span></span>
<span class="line"><span>                furnitur.append({</span></span>
<span class="line"><span>                    &quot;nama&quot;: f&quot;SetRuangR_{rm[&#39;id&#39;]}&quot;, &quot;type&quot;: &quot;set_ruang_r&quot;,</span></span>
<span class="line"><span>                    &quot;di&quot;: [cx, cy], &quot;rot&quot;: [0.0, 0.0, round(math.pi, 4) if lbl == &quot;[R]&quot; else 0.0],</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span>            elif &quot;ARSIP&quot; in lbl:</span></span>
<span class="line"><span>                for idx, ry in enumerate([round(y1 + 1.4, 2), round(cy, 2), round(y2 - 1.4, 2)]):</span></span>
<span class="line"><span>                    furnitur.append({</span></span>
<span class="line"><span>                        &quot;nama&quot;: f&quot;RakArsip_{rm[&#39;id&#39;]}_{idx+1}&quot;, &quot;type&quot;: &quot;rak_arsip&quot;,</span></span>
<span class="line"><span>                        &quot;di&quot;: [cx, ry], &quot;rot&quot;: [0.0, 0.0, round(math.pi / 2.0, 4)],</span></span>
<span class="line"><span>                    })</span></span>
<span class="line"><span>            elif &quot;TOILET&quot; in lbl:</span></span>
<span class="line"><span>                furnitur.append({&quot;nama&quot;: f&quot;Wastafel_{rm[&#39;id&#39;]}&quot;, &quot;type&quot;: &quot;wastafel&quot;, &quot;di&quot;: [cx, round(y1 + 0.4, 2)]})</span></span>
<span class="line"><span>            elif &quot;PANTRY&quot; in lbl:</span></span>
<span class="line"><span>                furnitur.append({&quot;nama&quot;: f&quot;MejaPantry_{rm[&#39;id&#39;]}&quot;, &quot;type&quot;: &quot;meja_pantry&quot;, &quot;di&quot;: [cx, round(y1 + 0.45, 2)]})</span></span>
<span class="line"><span>            elif &quot;TANGGA&quot; in lbl:</span></span>
<span class="line"><span>                furnitur.append({</span></span>
<span class="line"><span>                    &quot;nama&quot;: f&quot;TanggaDarurat_{rm[&#39;id&#39;]}&quot;, &quot;type&quot;: &quot;tangga_darurat&quot;,</span></span>
<span class="line"><span>                    &quot;di&quot;: [cx, cy], &quot;panjang&quot;: round(max(2.5, wx - 1.2), 2), &quot;lebar&quot;: round(max(0.8, wy - 0.3), 2),</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span>        return furnitur, label_ruang</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def parse_to_dict(self, ascii_text):</span></span>
<span class="line"><span>        grid = self._normalisasi_baris(ascii_text)</span></span>
<span class="line"><span>        H, W = len(grid), len(grid[0])</span></span>
<span class="line"><span>        max_r, max_c = H - 1, W - 1</span></span>
<span class="line"><span>        rooms = self._ekstrak_ruangan(grid)</span></span>
<span class="line"><span>        horiz_segments, vert_segments = self._ekstrak_segmen_dinding(grid)</span></span>
<span class="line"><span>        self._injeksi_pintu_dan_jendela_otomatis(rooms, horiz_segments, vert_segments, max_r, max_c)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        segmen_dinding = [</span></span>
<span class="line"><span>            {</span></span>
<span class="line"><span>                &quot;nama&quot;: s[&quot;nama&quot;], &quot;dari&quot;: s[&quot;dari&quot;], &quot;ke&quot;: s[&quot;ke&quot;],</span></span>
<span class="line"><span>                &quot;material&quot;: s[&quot;material&quot;], &quot;celah&quot;: sorted(s[&quot;celah&quot;], key=lambda item: item[&quot;dari&quot;]),</span></span>
<span class="line"><span>            }</span></span>
<span class="line"><span>            for s in horiz_segments + vert_segments</span></span>
<span class="line"><span>        ]</span></span>
<span class="line"><span>        zona_lantai = [</span></span>
<span class="line"><span>            {</span></span>
<span class="line"><span>                &quot;nama&quot;: f&quot;Lantai_{rm[&#39;id&#39;]:02d}_{re.sub(r&#39;[^A-Za-z0-9]+&#39;, &#39;_&#39;, rm[&#39;label&#39;] or &#39;Koridor&#39;).strip(&#39;_&#39;)}&quot;,</span></span>
<span class="line"><span>                &quot;min_xy&quot;: [rm[&quot;x1&quot;], rm[&quot;y1&quot;]], &quot;max_xy&quot;: [rm[&quot;x2&quot;], rm[&quot;y2&quot;]],</span></span>
<span class="line"><span>                &quot;material&quot;: self._tentukan_material_lantai(rm[&quot;label&quot;]),</span></span>
<span class="line"><span>            }</span></span>
<span class="line"><span>            for rm in rooms</span></span>
<span class="line"><span>        ]</span></span>
<span class="line"><span>        furnitur, label_ruang = self._bangun_furnitur_dan_label_otomatis(rooms)</span></span>
<span class="line"><span>        return {</span></span>
<span class="line"><span>            &quot;meta&quot;: {&quot;modul&quot;: &quot;Modul 2 - Transformasi 3D, Hierarki LEGO &amp; Texture Shader&quot;},</span></span>
<span class="line"><span>            &quot;rumah&quot;: {</span></span>
<span class="line"><span>                &quot;grid&quot;: [round(max_c * self.scale_x, 2), round(max_r * self.scale_y, 2)],</span></span>
<span class="line"><span>                &quot;tinggi_dinding&quot;: self.tinggi_dinding,</span></span>
<span class="line"><span>                &quot;tebal_dinding&quot;: self.tebal_dinding,</span></span>
<span class="line"><span>                &quot;segmen_dinding&quot;: segmen_dinding,</span></span>
<span class="line"><span>                &quot;zona_lantai&quot;: zona_lantai,</span></span>
<span class="line"><span>                &quot;furnitur&quot;: furnitur,</span></span>
<span class="line"><span>                &quot;label_ruang&quot;: label_ruang,</span></span>
<span class="line"><span>            },</span></span>
<span class="line"><span>        }</span></span>
<span class="line"><span></span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span># BAGIAN 4: INTI MATERI 2 - ENGINE TRANSFORMASI 3D, SHADER TEXTURE, &amp; LEGO APP</span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span>try:</span></span>
<span class="line"><span>    import bpy</span></span>
<span class="line"><span>    import bmesh</span></span>
<span class="line"><span>    from mathutils import Matrix, Vector, Euler</span></span>
<span class="line"><span>    BLENDER_AVAILABLE = True</span></span>
<span class="line"><span>except ImportError:</span></span>
<span class="line"><span>    BLENDER_AVAILABLE = False</span></span>
<span class="line"><span></span></span>
<span class="line"><span>if BLENDER_AVAILABLE:</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    # 1. Transform3DEngine: Matriks Homogen 4x4 Eksplisit &amp; Hierarki Parent-Child</span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    class Transform3DEngine:</span></span>
<span class="line"><span>        &quot;&quot;&quot;</span></span>
<span class="line"><span>        MATERI 2 - TRANSFORMASI 3D:</span></span>
<span class="line"><span>        Mengimplementasikan rumus aljabar linear matriks transformasi homogen 4x4:</span></span>
<span class="line"><span>          M = T(tx, ty, tz) @ Rz(gamma) @ Ry(beta) @ Rx(alpha) @ S(sx, sy, sz) @ Shear</span></span>
<span class="line"><span>        Semua transformasi objek dihitung dengan perkalian matriks 4x4 sebelum</span></span>
<span class="line"><span>        diterapkan ke obj.matrix_world atau obj.matrix_local.</span></span>
<span class="line"><span>        &quot;&quot;&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def matriks_translasi(tx, ty, tz):</span></span>
<span class="line"><span>            return Matrix((</span></span>
<span class="line"><span>                (1.0, 0.0, 0.0, float(tx)),</span></span>
<span class="line"><span>                (0.0, 1.0, 0.0, float(ty)),</span></span>
<span class="line"><span>                (0.0, 0.0, 1.0, float(tz)),</span></span>
<span class="line"><span>                (0.0, 0.0, 0.0, 1.0),</span></span>
<span class="line"><span>            ))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def matriks_skala(sx, sy, sz):</span></span>
<span class="line"><span>            return Matrix((</span></span>
<span class="line"><span>                (float(sx), 0.0,       0.0,       0.0),</span></span>
<span class="line"><span>                (0.0,       float(sy), 0.0,       0.0),</span></span>
<span class="line"><span>                (0.0,       0.0,       float(sz), 0.0),</span></span>
<span class="line"><span>                (0.0,       0.0,       0.0,       1.0),</span></span>
<span class="line"><span>            ))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def matriks_rotasi_x(rad):</span></span>
<span class="line"><span>            c, s = math.cos(rad), math.sin(rad)</span></span>
<span class="line"><span>            return Matrix((</span></span>
<span class="line"><span>                (1.0, 0.0, 0.0, 0.0),</span></span>
<span class="line"><span>                (0.0, c,  -s,   0.0),</span></span>
<span class="line"><span>                (0.0, s,   c,   0.0),</span></span>
<span class="line"><span>                (0.0, 0.0, 0.0, 1.0),</span></span>
<span class="line"><span>            ))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def matriks_rotasi_y(rad):</span></span>
<span class="line"><span>            c, s = math.cos(rad), math.sin(rad)</span></span>
<span class="line"><span>            return Matrix((</span></span>
<span class="line"><span>                ( c,  0.0, s,   0.0),</span></span>
<span class="line"><span>                (0.0, 1.0, 0.0, 0.0),</span></span>
<span class="line"><span>                (-s,  0.0, c,   0.0),</span></span>
<span class="line"><span>                (0.0, 0.0, 0.0, 1.0),</span></span>
<span class="line"><span>            ))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def matriks_rotasi_z(rad):</span></span>
<span class="line"><span>            c, s = math.cos(rad), math.sin(rad)</span></span>
<span class="line"><span>            return Matrix((</span></span>
<span class="line"><span>                (c,  -s,   0.0, 0.0),</span></span>
<span class="line"><span>                (s,   c,   0.0, 0.0),</span></span>
<span class="line"><span>                (0.0, 0.0, 1.0, 0.0),</span></span>
<span class="line"><span>                (0.0, 0.0, 0.0, 1.0),</span></span>
<span class="line"><span>            ))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def matriks_shear_xy(sh_x=0.0, sh_y=0.0):</span></span>
<span class="line"><span>            &quot;&quot;&quot;Matriks Geser (Shearing) pada sumbu X/Y terhadap Z.&quot;&quot;&quot;</span></span>
<span class="line"><span>            return Matrix((</span></span>
<span class="line"><span>                (1.0, 0.0, float(sh_x), 0.0),</span></span>
<span class="line"><span>                (0.0, 1.0, float(sh_y), 0.0),</span></span>
<span class="line"><span>                (0.0, 0.0, 1.0,         0.0),</span></span>
<span class="line"><span>                (0.0, 0.0, 0.0,         1.0),</span></span>
<span class="line"><span>            ))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @classmethod</span></span>
<span class="line"><span>        def komposisi_trs(cls, lokasi=(0.0, 0.0, 0.0), rotasi_euler=(0.0, 0.0, 0.0), skala=(1.0, 1.0, 1.0), shear=(0.0, 0.0)):</span></span>
<span class="line"><span>            &quot;&quot;&quot;Menghasilkan matriks komposit M = T @ Rz @ Ry @ Rx @ Shear @ S.&quot;&quot;&quot;</span></span>
<span class="line"><span>            T = cls.matriks_translasi(*lokasi)</span></span>
<span class="line"><span>            Rx = cls.matriks_rotasi_x(rotasi_euler[0])</span></span>
<span class="line"><span>            Ry = cls.matriks_rotasi_y(rotasi_euler[1])</span></span>
<span class="line"><span>            Rz = cls.matriks_rotasi_z(rotasi_euler[2])</span></span>
<span class="line"><span>            Sh = cls.matriks_shear_xy(shear[0], shear[1])</span></span>
<span class="line"><span>            S = cls.matriks_skala(*skala)</span></span>
<span class="line"><span>            return T @ Rz @ Ry @ Rx @ Sh @ S</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @classmethod</span></span>
<span class="line"><span>        def terapkan_matriks(cls, obj, lokasi=(0.0, 0.0, 0.0), rotasi_euler=(0.0, 0.0, 0.0), skala=(1.0, 1.0, 1.0), parent=None):</span></span>
<span class="line"><span>            &quot;&quot;&quot;</span></span>
<span class="line"><span>            Menerapkan matriks transformasi 4x4 ke objek.</span></span>
<span class="line"><span>            Jika memiliki parent (Hierarki LEGO), maka transformasi dihitung</span></span>
<span class="line"><span>            relatif terhadap koordinat lokal parent-nya (M_world = M_parent @ M_local).</span></span>
<span class="line"><span>            &quot;&quot;&quot;</span></span>
<span class="line"><span>            M_lokal = cls.komposisi_trs(lokasi, rotasi_euler, skala)</span></span>
<span class="line"><span>            if parent is not None:</span></span>
<span class="line"><span>                obj.parent = parent</span></span>
<span class="line"><span>                obj.matrix_parent_inverse = Matrix.Identity(4)</span></span>
<span class="line"><span>                obj.matrix_local = M_lokal</span></span>
<span class="line"><span>            else:</span></span>
<span class="line"><span>                obj.matrix_world = M_lokal</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    # 2. SceneManager: Lifecycle Scene &amp; UV Unwrapping Otomatis</span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    class SceneManager:</span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def bersihkan_scene():</span></span>
<span class="line"><span>            if bpy.context.active_object and bpy.context.active_object.mode != &quot;OBJECT&quot;:</span></span>
<span class="line"><span>                bpy.ops.object.mode_set(mode=&quot;OBJECT&quot;)</span></span>
<span class="line"><span>            bpy.ops.object.select_all(action=&quot;SELECT&quot;)</span></span>
<span class="line"><span>            bpy.ops.object.delete()</span></span>
<span class="line"><span>            for block_list in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.textures, bpy.data.images):</span></span>
<span class="line"><span>                for item in list(block_list):</span></span>
<span class="line"><span>                    block_list.remove(item)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def buat_koleksi(nama_koleksi):</span></span>
<span class="line"><span>            if nama_koleksi in bpy.data.collections:</span></span>
<span class="line"><span>                return bpy.data.collections[nama_koleksi]</span></span>
<span class="line"><span>            kol = bpy.data.collections.new(nama_koleksi)</span></span>
<span class="line"><span>            bpy.context.scene.collection.children.link(kol)</span></span>
<span class="line"><span>            return kol</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def pindahkan_ke_koleksi(obj, koleksi):</span></span>
<span class="line"><span>            for c in list(obj.users_collection):</span></span>
<span class="line"><span>                c.objects.unlink(obj)</span></span>
<span class="line"><span>            koleksi.objects.link(obj)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def generate_box_uv(obj):</span></span>
<span class="line"><span>            &quot;&quot;&quot;Memastikan mesh memiliki UV Map proporsional (Cube Projection) untuk tekstur.&quot;&quot;&quot;</span></span>
<span class="line"><span>            if not obj or obj.type != &quot;MESH&quot;:</span></span>
<span class="line"><span>                return</span></span>
<span class="line"><span>            bm = bmesh.new()</span></span>
<span class="line"><span>            bm.from_mesh(obj.data)</span></span>
<span class="line"><span>            uv_layer = bm.loops.layers.uv.verify()</span></span>
<span class="line"><span>            for face in bm.faces:</span></span>
<span class="line"><span>                n = face.normal</span></span>
<span class="line"><span>                for loop in face.loops:</span></span>
<span class="line"><span>                    co = loop.vert.co</span></span>
<span class="line"><span>                    if abs(n.z) &gt; 0.5:</span></span>
<span class="line"><span>                        loop[uv_layer].uv = (co.x, co.y)</span></span>
<span class="line"><span>                    elif abs(n.x) &gt; 0.5:</span></span>
<span class="line"><span>                        loop[uv_layer].uv = (co.y, co.z)</span></span>
<span class="line"><span>                    else:</span></span>
<span class="line"><span>                        loop[uv_layer].uv = (co.x, co.z)</span></span>
<span class="line"><span>            bm.to_mesh(obj.data)</span></span>
<span class="line"><span>            bm.free()</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    # 3. TextureMaterialFactory: Procedural Shader Nodes &amp; Image Texture (Materi 2)</span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    class TextureMaterialFactory:</span></span>
<span class="line"><span>        &quot;&quot;&quot;</span></span>
<span class="line"><span>        MATERI 2 - TEXTURE MAPPING &amp; SHADING:</span></span>
<span class="line"><span>        Membangun jaringan Node Shader di Blender 4.3:</span></span>
<span class="line"><span>          [TexCoord] -&gt; [Mapping (UV Scale/Rot/Trans)] -&gt; [Procedural/Image Texture]</span></span>
<span class="line"><span>                                                       -&gt; [Bump Node] -&gt; [Principled BSDF]</span></span>
<span class="line"><span>        &quot;&quot;&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def buat_tekstur_citra_checker(nama_img=&quot;Tekstur_Lego_Checker&quot;, ukuran=256):</span></span>
<span class="line"><span>            &quot;&quot;&quot;Membuat Image Texture piksel secara prosedural di memori Blender (tanpa file eksternal).&quot;&quot;&quot;</span></span>
<span class="line"><span>            if nama_img in bpy.data.images:</span></span>
<span class="line"><span>                return bpy.data.images[nama_img]</span></span>
<span class="line"><span>            img = bpy.data.images.new(nama_img, width=ukuran, height=ukuran)</span></span>
<span class="line"><span>            pixels = [0.0] * (ukuran * ukuran * 4)</span></span>
<span class="line"><span>            for y in range(ukuran):</span></span>
<span class="line"><span>                for x in range(ukuran):</span></span>
<span class="line"><span>                    idx = (y * ukuran + x) * 4</span></span>
<span class="line"><span>                    kotak = ((x // 32) + (y // 32)) % 2 == 0</span></span>
<span class="line"><span>                    border = (x % 32 &lt; 2) or (y % 32 &lt; 2)</span></span>
<span class="line"><span>                    if border:</span></span>
<span class="line"><span>                        r, g, b = 0.15, 0.18, 0.22</span></span>
<span class="line"><span>                    elif kotak:</span></span>
<span class="line"><span>                        r, g, b = 0.92, 0.78, 0.20</span></span>
<span class="line"><span>                    else:</span></span>
<span class="line"><span>                        r, g, b = 0.18, 0.48, 0.85</span></span>
<span class="line"><span>                    pixels[idx : idx + 4] = [r, g, b, 1.0]</span></span>
<span class="line"><span>            img.pixels = pixels</span></span>
<span class="line"><span>            img.pack()</span></span>
<span class="line"><span>            return img</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @classmethod</span></span>
<span class="line"><span>        def get_or_create(cls, nama_mat, spec):</span></span>
<span class="line"><span>            if nama_mat in bpy.data.materials:</span></span>
<span class="line"><span>                return bpy.data.materials[nama_mat]</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            mat = bpy.data.materials.new(name=nama_mat)</span></span>
<span class="line"><span>            mat.use_nodes = True</span></span>
<span class="line"><span>            nodes = mat.node_tree.nodes</span></span>
<span class="line"><span>            links = mat.node_tree.links</span></span>
<span class="line"><span>            bsdf = nodes.get(&quot;Principled BSDF&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            rgba = tuple(spec.get(&quot;rgba&quot;, [0.8, 0.8, 0.8, 1.0]))</span></span>
<span class="line"><span>            roughness = float(spec.get(&quot;roughness&quot;, 0.5))</span></span>
<span class="line"><span>            metallic = float(spec.get(&quot;metallic&quot;, 0.0))</span></span>
<span class="line"><span>            tex_type = spec.get(&quot;tex_type&quot;, &quot;NONE&quot;).upper()</span></span>
<span class="line"><span>            uv_scale = tuple(spec.get(&quot;uv_scale&quot;, [4.0, 4.0, 4.0]))</span></span>
<span class="line"><span>            bump_strength = float(spec.get(&quot;bump_strength&quot;, 0.1))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            if bsdf:</span></span>
<span class="line"><span>                bsdf.inputs[&quot;Base Color&quot;].default_value = rgba</span></span>
<span class="line"><span>                bsdf.inputs[&quot;Roughness&quot;].default_value = roughness</span></span>
<span class="line"><span>                if &quot;Metallic&quot; in bsdf.inputs:</span></span>
<span class="line"><span>                    bsdf.inputs[&quot;Metallic&quot;].default_value = metallic</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                if spec.get(&quot;emission&quot;) and spec.get(&quot;emission_strength&quot;, 0) &gt; 0:</span></span>
<span class="line"><span>                    em_in = bsdf.inputs.get(&quot;Emission Color&quot;) or bsdf.inputs.get(&quot;Emission&quot;)</span></span>
<span class="line"><span>                    if em_in:</span></span>
<span class="line"><span>                        em_in.default_value = tuple(spec[&quot;emission&quot;])</span></span>
<span class="line"><span>                    if &quot;Emission Strength&quot; in bsdf.inputs:</span></span>
<span class="line"><span>                        bsdf.inputs[&quot;Emission Strength&quot;].default_value = float(spec[&quot;emission_strength&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            if tex_type != &quot;NONE&quot; and bsdf:</span></span>
<span class="line"><span>                # Buat Node Texture Coordinate &amp; Mapping (Transformasi UV 2D/3D)</span></span>
<span class="line"><span>                coord_node = nodes.new(type=&quot;ShaderNodeTexCoord&quot;)</span></span>
<span class="line"><span>                coord_node.location = (-850, 200)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                map_node = nodes.new(type=&quot;ShaderNodeMapping&quot;)</span></span>
<span class="line"><span>                map_node.name = &quot;UV_Mapping&quot;</span></span>
<span class="line"><span>                map_node.location = (-650, 200)</span></span>
<span class="line"><span>                map_node.inputs[&quot;Scale&quot;].default_value = uv_scale</span></span>
<span class="line"><span>                links.new(coord_node.outputs[&quot;Generated&quot;], map_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                bump_node = nodes.new(type=&quot;ShaderNodeBump&quot;)</span></span>
<span class="line"><span>                bump_node.location = (-200, -120)</span></span>
<span class="line"><span>                bump_node.inputs[&quot;Strength&quot;].default_value = bump_strength</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                if tex_type == &quot;BRICK&quot;:</span></span>
<span class="line"><span>                    tex_node = nodes.new(type=&quot;ShaderNodeTexBrick&quot;)</span></span>
<span class="line"><span>                    tex_node.location = (-420, 200)</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Color1&quot;].default_value = rgba</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Color2&quot;].default_value = tuple(spec.get(&quot;color2&quot;, [0.6, 0.5, 0.4, 1.0]))</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Mortar&quot;].default_value = (0.35, 0.35, 0.35, 1.0)</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Mortar Size&quot;].default_value = 0.025</span></span>
<span class="line"><span>                    links.new(map_node.outputs[&quot;Vector&quot;], tex_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Color&quot;], bsdf.inputs[&quot;Base Color&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Fac&quot;], bump_node.inputs[&quot;Height&quot;])</span></span>
<span class="line"><span>                    links.new(bump_node.outputs[&quot;Normal&quot;], bsdf.inputs[&quot;Normal&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                elif tex_type == &quot;CHECKER&quot;:</span></span>
<span class="line"><span>                    tex_node = nodes.new(type=&quot;ShaderNodeTexChecker&quot;)</span></span>
<span class="line"><span>                    tex_node.location = (-420, 200)</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Color1&quot;].default_value = rgba</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Color2&quot;].default_value = tuple(spec.get(&quot;color2&quot;, [0.5, 0.5, 0.5, 1.0]))</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Scale&quot;].default_value = 1.0</span></span>
<span class="line"><span>                    links.new(map_node.outputs[&quot;Vector&quot;], tex_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Color&quot;], bsdf.inputs[&quot;Base Color&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Fac&quot;], bump_node.inputs[&quot;Height&quot;])</span></span>
<span class="line"><span>                    links.new(bump_node.outputs[&quot;Normal&quot;], bsdf.inputs[&quot;Normal&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                elif tex_type == &quot;WOOD&quot;:</span></span>
<span class="line"><span>                    tex_node = nodes.new(type=&quot;ShaderNodeTexWave&quot;)</span></span>
<span class="line"><span>                    tex_node.location = (-450, 200)</span></span>
<span class="line"><span>                    tex_node.wave_type = &quot;BANDS&quot;</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Scale&quot;].default_value = 2.5</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Distortion&quot;].default_value = 4.5</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Detail&quot;].default_value = 3.0</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                    mix_node = nodes.new(type=&quot;ShaderNodeMix&quot;)</span></span>
<span class="line"><span>                    mix_node.data_type = &quot;RGBA&quot;</span></span>
<span class="line"><span>                    mix_node.location = (-230, 220)</span></span>
<span class="line"><span>                    mix_node.inputs[&quot;A&quot;].default_value = rgba</span></span>
<span class="line"><span>                    mix_node.inputs[&quot;B&quot;].default_value = tuple(spec.get(&quot;color2&quot;, [0.35, 0.20, 0.10, 1.0]))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                    links.new(map_node.outputs[&quot;Vector&quot;], tex_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Fac&quot;], mix_node.inputs[&quot;Factor&quot;])</span></span>
<span class="line"><span>                    links.new(mix_node.outputs[&quot;Result&quot;], bsdf.inputs[&quot;Base Color&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Fac&quot;], bump_node.inputs[&quot;Height&quot;])</span></span>
<span class="line"><span>                    links.new(bump_node.outputs[&quot;Normal&quot;], bsdf.inputs[&quot;Normal&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                elif tex_type in (&quot;NOISE&quot;, &quot;LEGO_PLASTIC&quot;):</span></span>
<span class="line"><span>                    tex_node = nodes.new(type=&quot;ShaderNodeTexNoise&quot;)</span></span>
<span class="line"><span>                    tex_node.location = (-420, 100)</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Scale&quot;].default_value = 25.0 if tex_type == &quot;LEGO_PLASTIC&quot; else 12.0</span></span>
<span class="line"><span>                    tex_node.inputs[&quot;Detail&quot;].default_value = 4.0</span></span>
<span class="line"><span>                    bump_node.inputs[&quot;Strength&quot;].default_value = 0.03 if tex_type == &quot;LEGO_PLASTIC&quot; else bump_strength</span></span>
<span class="line"><span>                    links.new(map_node.outputs[&quot;Vector&quot;], tex_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Fac&quot;], bump_node.inputs[&quot;Height&quot;])</span></span>
<span class="line"><span>                    links.new(bump_node.outputs[&quot;Normal&quot;], bsdf.inputs[&quot;Normal&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                elif tex_type == &quot;IMAGE_CHECKER&quot;:</span></span>
<span class="line"><span>                    img = cls.buat_tekstur_citra_checker()</span></span>
<span class="line"><span>                    tex_node = nodes.new(type=&quot;ShaderNodeTexImage&quot;)</span></span>
<span class="line"><span>                    tex_node.location = (-420, 200)</span></span>
<span class="line"><span>                    tex_node.image = img</span></span>
<span class="line"><span>                    links.new(coord_node.outputs[&quot;UV&quot;], map_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span>                    links.new(map_node.outputs[&quot;Vector&quot;], tex_node.inputs[&quot;Vector&quot;])</span></span>
<span class="line"><span>                    links.new(tex_node.outputs[&quot;Color&quot;], bsdf.inputs[&quot;Base Color&quot;])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            mat.diffuse_color = rgba</span></span>
<span class="line"><span>            return mat</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    # 4. AssetBuilder: Hierarki Modular LEGO (Parent-Child) &amp; Transformasi 3D</span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    class AssetBuilder:</span></span>
<span class="line"><span>        &quot;&quot;&quot;</span></span>
<span class="line"><span>        MATERI 2 - MODULAR LEGO BUILDER:</span></span>
<span class="line"><span>        Alih-alih menggabungkan mesh dengan bpy.ops.object.join() yang merusak</span></span>
<span class="line"><span>        koordinat lokal tiap sub-bagian, AssetBuilder merakit komponen sebagai</span></span>
<span class="line"><span>        HIERARKI PARENT-CHILD (Scene Graph) menggunakan Transform3DEngine.</span></span>
<span class="line"><span>        &quot;&quot;&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def __init__(self, mat_factory, palet):</span></span>
<span class="line"><span>            self.mat_factory = mat_factory</span></span>
<span class="line"><span>            self.palet = palet</span></span>
<span class="line"><span>            self._registry = {</span></span>
<span class="line"><span>                &quot;box&quot;: self._bangun_kotak,</span></span>
<span class="line"><span>                &quot;silinder&quot;: self._bangun_silinder,</span></span>
<span class="line"><span>                &quot;lego_brick&quot;: self._bangun_bata_lego,</span></span>
<span class="line"><span>                &quot;menara_lego&quot;: self._bangun_menara_lego,</span></span>
<span class="line"><span>                &quot;meja_kerja&quot;: self._bangun_meja_kerja,</span></span>
<span class="line"><span>                &quot;set_ruang_r&quot;: self._bangun_set_ruang_r,</span></span>
<span class="line"><span>                &quot;rak_arsip&quot;: self._bangun_rak_arsip,</span></span>
<span class="line"><span>                &quot;wastafel&quot;: self._bangun_wastafel,</span></span>
<span class="line"><span>                &quot;meja_pantry&quot;: self._bangun_meja_pantry,</span></span>
<span class="line"><span>                &quot;tangga_darurat&quot;: self._bangun_tangga_darurat,</span></span>
<span class="line"><span>            }</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _mat(self, nama_mat):</span></span>
<span class="line"><span>            if nama_mat not in self.palet:</span></span>
<span class="line"><span>                return self.mat_factory.get_or_create(nama_mat, {&quot;rgba&quot;: [0.8, 0.8, 0.8, 1.0]})</span></span>
<span class="line"><span>            return self.mat_factory.get_or_create(nama_mat, self.palet[nama_mat])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def membangun(self, spec):</span></span>
<span class="line"><span>            fn = self._registry.get(spec[&quot;type&quot;])</span></span>
<span class="line"><span>            if fn is None:</span></span>
<span class="line"><span>                raise ValueError(f&quot;Tipe aset tak dikenal: {spec[&#39;type&#39;]!r}&quot;)</span></span>
<span class="line"><span>            return fn(spec)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_kotak(self, spec):</span></span>
<span class="line"><span>            dim = spec[&quot;dimensions&quot;]</span></span>
<span class="line"><span>            di = spec.get(&quot;di&quot;, [0.0, 0.0])</span></span>
<span class="line"><span>            z = spec.get(&quot;z&quot;, dim[2] / 2.0)</span></span>
<span class="line"><span>            rot = spec.get(&quot;rot&quot;, [0.0, 0.0, 0.0])</span></span>
<span class="line"><span>            skala = spec.get(&quot;scale&quot;, [1.0, 1.0, 1.0])</span></span>
<span class="line"><span>            shear = spec.get(&quot;shear&quot;, [0.0, 0.0])</span></span>
<span class="line"><span>            parent = spec.get(&quot;parent&quot;, None)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            # Buat kubus satuan (size=1.0), lalu transformasikan menggunakan Matriks 4x4</span></span>
<span class="line"><span>            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))</span></span>
<span class="line"><span>            o = bpy.context.active_object</span></span>
<span class="line"><span>            o.name = spec.get(&quot;name&quot;, spec.get(&quot;nama&quot;, &quot;Kotak&quot;))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            skala_total = (dim[0] * skala[0], dim[1] * skala[1], dim[2] * skala[2])</span></span>
<span class="line"><span>            M = Transform3DEngine.komposisi_trs(</span></span>
<span class="line"><span>                lokasi=(di[0], di[1], z),</span></span>
<span class="line"><span>                rotasi_euler=rot,</span></span>
<span class="line"><span>                skala=skala_total,</span></span>
<span class="line"><span>                shear=shear,</span></span>
<span class="line"><span>            )</span></span>
<span class="line"><span>            if parent is not None:</span></span>
<span class="line"><span>                o.parent = parent</span></span>
<span class="line"><span>                o.matrix_parent_inverse = Matrix.Identity(4)</span></span>
<span class="line"><span>                o.matrix_local = M</span></span>
<span class="line"><span>            else:</span></span>
<span class="line"><span>                o.matrix_world = M</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            SceneManager.generate_box_uv(o)</span></span>
<span class="line"><span>            o.data.materials.append(self._mat(spec[&quot;material&quot;]))</span></span>
<span class="line"><span>            return o</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_silinder(self, spec):</span></span>
<span class="line"><span>            r = spec.get(&quot;radius&quot;, 0.25)</span></span>
<span class="line"><span>            t = spec.get(&quot;depth&quot;, 1.0)</span></span>
<span class="line"><span>            di = spec.get(&quot;di&quot;, [0.0, 0.0])</span></span>
<span class="line"><span>            z = spec.get(&quot;z&quot;, t / 2.0)</span></span>
<span class="line"><span>            rot = spec.get(&quot;rot&quot;, [0.0, 0.0, 0.0])</span></span>
<span class="line"><span>            skala = spec.get(&quot;scale&quot;, [1.0, 1.0, 1.0])</span></span>
<span class="line"><span>            parent = spec.get(&quot;parent&quot;, None)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=(0.0, 0.0, 0.0))</span></span>
<span class="line"><span>            o = bpy.context.active_object</span></span>
<span class="line"><span>            o.name = spec.get(&quot;name&quot;, spec.get(&quot;nama&quot;, &quot;Silinder&quot;))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            Transform3DEngine.terapkan_matriks(</span></span>
<span class="line"><span>                o,</span></span>
<span class="line"><span>                lokasi=(di[0], di[1], z),</span></span>
<span class="line"><span>                rotasi_euler=rot,</span></span>
<span class="line"><span>                skala=(r * skala[0], r * skala[1], t * skala[2]),</span></span>
<span class="line"><span>                parent=parent,</span></span>
<span class="line"><span>            )</span></span>
<span class="line"><span>            o.data.materials.append(self._mat(spec[&quot;material&quot;]))</span></span>
<span class="line"><span>            return o</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_bata_lego(self, spec):</span></span>
<span class="line"><span>            &quot;&quot;&quot;</span></span>
<span class="line"><span>            Membangun 1 Balok LEGO Modular (Studs X * Studs Y) dengan hierarki Parent-Child.</span></span>
<span class="line"><span>            Saat balok induk ditranslasikan/dirotasi/diskalakan, seluruh stud di atasnya</span></span>
<span class="line"><span>            ikut bertransformasi secara otomatis melalui perkalian matriks parent.</span></span>
<span class="line"><span>            &quot;&quot;&quot;</span></span>
<span class="line"><span>            studs_x = int(spec.get(&quot;studs_x&quot;, 2))</span></span>
<span class="line"><span>            studs_y = int(spec.get(&quot;studs_y&quot;, 4))</span></span>
<span class="line"><span>            unit = float(spec.get(&quot;unit_size&quot;, 0.25))</span></span>
<span class="line"><span>            tinggi_bata = float(spec.get(&quot;height&quot;, 0.30))</span></span>
<span class="line"><span>            mat_name = spec.get(&quot;material&quot;, &quot;lego_merah&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            wx, wy = studs_x * unit, studs_y * unit</span></span>
<span class="line"><span>            di = spec.get(&quot;di&quot;, [0.0, 0.0])</span></span>
<span class="line"><span>            z_alas = float(spec.get(&quot;z&quot;, 0.0))</span></span>
<span class="line"><span>            rot = spec.get(&quot;rot&quot;, [0.0, 0.0, 0.0])</span></span>
<span class="line"><span>            skala = spec.get(&quot;scale&quot;, [1.0, 1.0, 1.0])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            # Buat Empty sebagai Root Pivot di tengah alas balok LEGO</span></span>
<span class="line"><span>            root = bpy.data.objects.new(spec.get(&quot;nama&quot;, &quot;LegoBrick&quot;), None)</span></span>
<span class="line"><span>            root.empty_display_type = &quot;PLAIN_AXES&quot;</span></span>
<span class="line"><span>            root.empty_display_size = 0.2</span></span>
<span class="line"><span>            bpy.context.scene.collection.objects.link(root)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            Transform3DEngine.terapkan_matriks(</span></span>
<span class="line"><span>                root,</span></span>
<span class="line"><span>                lokasi=(di[0], di[1], z_alas),</span></span>
<span class="line"><span>                rotasi_euler=rot,</span></span>
<span class="line"><span>                skala=skala,</span></span>
<span class="line"><span>                parent=spec.get(&quot;parent&quot;, None),</span></span>
<span class="line"><span>            )</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            # Badan utama balok LEGO (anak dari root)</span></span>
<span class="line"><span>            self._bangun_kotak({</span></span>
<span class="line"><span>                &quot;name&quot;: f&quot;{root.name}_Body&quot;,</span></span>
<span class="line"><span>                &quot;dimensions&quot;: [wx * 0.98, wy * 0.98, tinggi_bata],</span></span>
<span class="line"><span>                &quot;di&quot;: [0.0, 0.0],</span></span>
<span class="line"><span>                &quot;z&quot;: tinggi_bata / 2.0,</span></span>
<span class="line"><span>                &quot;material&quot;: mat_name,</span></span>
<span class="line"><span>                &quot;parent&quot;: root,</span></span>
<span class="line"><span>            })</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            # Stud silinder di atas balok LEGO (anak dari root)</span></span>
<span class="line"><span>            tinggi_stud = unit * 0.22</span></span>
<span class="line"><span>            radius_stud = unit * 0.30</span></span>
<span class="line"><span>            start_x = -wx / 2.0 + unit / 2.0</span></span>
<span class="line"><span>            start_y = -wy / 2.0 + unit / 2.0</span></span>
<span class="line"><span>            for ix in range(studs_x):</span></span>
<span class="line"><span>                for iy in range(studs_y):</span></span>
<span class="line"><span>                    sx = start_x + ix * unit</span></span>
<span class="line"><span>                    sy = start_y + iy * unit</span></span>
<span class="line"><span>                    self._bangun_silinder({</span></span>
<span class="line"><span>                        &quot;name&quot;: f&quot;{root.name}_Stud_{ix}_{iy}&quot;,</span></span>
<span class="line"><span>                        &quot;radius&quot;: radius_stud,</span></span>
<span class="line"><span>                        &quot;depth&quot;: tinggi_stud,</span></span>
<span class="line"><span>                        &quot;di&quot;: [sx, sy],</span></span>
<span class="line"><span>                        &quot;z&quot;: tinggi_bata + tinggi_stud / 2.0,</span></span>
<span class="line"><span>                        &quot;material&quot;: mat_name,</span></span>
<span class="line"><span>                        &quot;parent&quot;: root,</span></span>
<span class="line"><span>                    })</span></span>
<span class="line"><span>            return root</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_menara_lego(self, spec):</span></span>
<span class="line"><span>            &quot;&quot;&quot;Membangun struktur modular bertumpuk dari beberapa Lego Brick (Hierarchy Demo).&quot;&quot;&quot;</span></span>
<span class="line"><span>            di = spec.get(&quot;di&quot;, [0.0, 0.0])</span></span>
<span class="line"><span>            rot = spec.get(&quot;rot&quot;, [0.0, 0.0, 0.0])</span></span>
<span class="line"><span>            skala = spec.get(&quot;scale&quot;, [1.0, 1.0, 1.0])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            root = bpy.data.objects.new(spec.get(&quot;nama&quot;, &quot;MenaraLego&quot;), None)</span></span>
<span class="line"><span>            root.empty_display_type = &quot;ARROWS&quot;</span></span>
<span class="line"><span>            root.empty_display_size = 0.5</span></span>
<span class="line"><span>            bpy.context.scene.collection.objects.link(root)</span></span>
<span class="line"><span>            Transform3DEngine.terapkan_matriks(root, lokasi=(di[0], di[1], 0.0), rotasi_euler=rot, skala=skala)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            lapis = [</span></span>
<span class="line"><span>                (&quot;lego_merah&quot;,  4, 4, 0.00, 0.0),</span></span>
<span class="line"><span>                (&quot;lego_kuning&quot;, 3, 3, 0.30, math.radians(15)),</span></span>
<span class="line"><span>                (&quot;lego_biru&quot;,   2, 4, 0.60, math.radians(30)),</span></span>
<span class="line"><span>                (&quot;lego_hijau&quot;,  2, 2, 0.90, math.radians(45)),</span></span>
<span class="line"><span>            ]</span></span>
<span class="line"><span>            for idx, (warna, sx, sy, z_pos, r_z) in enumerate(lapis):</span></span>
<span class="line"><span>                self._bangun_bata_lego({</span></span>
<span class="line"><span>                    &quot;nama&quot;: f&quot;{root.name}_Lapis{idx+1}&quot;,</span></span>
<span class="line"><span>                    &quot;studs_x&quot;: sx, &quot;studs_y&quot;: sy,</span></span>
<span class="line"><span>                    &quot;unit_size&quot;: 0.28, &quot;height&quot;: 0.30,</span></span>
<span class="line"><span>                    &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: z_pos,</span></span>
<span class="line"><span>                    &quot;rot&quot;: [0.0, 0.0, r_z],</span></span>
<span class="line"><span>                    &quot;material&quot;: warna,</span></span>
<span class="line"><span>                    &quot;parent&quot;: root,</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span>            return root</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _rakit_hierarki_lokal(self, spec, daftar_komponen):</span></span>
<span class="line"><span>            &quot;&quot;&quot;</span></span>
<span class="line"><span>            Membangun grup furnitur menggunakan Root Empty (Hierarchy Transform)</span></span>
<span class="line"><span>            sehingga seluruh bagian anak tetap memiliki matriks lokal masing-masing.</span></span>
<span class="line"><span>            &quot;&quot;&quot;</span></span>
<span class="line"><span>            di = spec.get(&quot;di&quot;, [0.0, 0.0])</span></span>
<span class="line"><span>            z_root = float(spec.get(&quot;z&quot;, 0.0))</span></span>
<span class="line"><span>            rot = spec.get(&quot;rot&quot;, [0.0, 0.0, 0.0])</span></span>
<span class="line"><span>            skala = spec.get(&quot;scale&quot;, [1.0, 1.0, 1.0])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            root = bpy.data.objects.new(spec.get(&quot;nama&quot;, &quot;GrupLego&quot;), None)</span></span>
<span class="line"><span>            root.empty_display_type = &quot;PLAIN_AXES&quot;</span></span>
<span class="line"><span>            root.empty_display_size = 0.35</span></span>
<span class="line"><span>            bpy.context.scene.collection.objects.link(root)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            Transform3DEngine.terapkan_matriks(</span></span>
<span class="line"><span>                root,</span></span>
<span class="line"><span>                lokasi=(di[0], di[1], z_root),</span></span>
<span class="line"><span>                rotasi_euler=rot,</span></span>
<span class="line"><span>                skala=skala,</span></span>
<span class="line"><span>            )</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            for idx, komp in enumerate(daftar_komponen):</span></span>
<span class="line"><span>                k_spec = dict(komp)</span></span>
<span class="line"><span>                k_spec[&quot;name&quot;] = f&quot;{root.name}_part{idx+1}&quot;</span></span>
<span class="line"><span>                k_spec[&quot;parent&quot;] = root</span></span>
<span class="line"><span>                self.membangun(k_spec)</span></span>
<span class="line"><span>            return root</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_meja_kerja(self, spec):</span></span>
<span class="line"><span>            komp = [</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [1.4, 0.7, 0.05], &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: 0.73, &quot;material&quot;: &quot;kayu_meja&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.06, 0.66, 0.71], &quot;di&quot;: [-0.65, 0.0], &quot;z&quot;: 0.355, &quot;material&quot;: &quot;logam_abu&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.06, 0.66, 0.71], &quot;di&quot;: [0.65, 0.0], &quot;z&quot;: 0.355, &quot;material&quot;: &quot;logam_abu&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [1.42, 0.05, 1.15], &quot;di&quot;: [0.0, 0.35], &quot;z&quot;: 0.575, &quot;material&quot;: &quot;partisi_kubikel&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.52, 0.04, 0.32], &quot;di&quot;: [0.0, 0.15], &quot;z&quot;: 0.98, &quot;material&quot;: &quot;layar_monitor&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.48, 0.48, 0.07], &quot;di&quot;: [0.0, -0.55], &quot;z&quot;: 0.46, &quot;material&quot;: &quot;kursi_kantor&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.46, 0.06, 0.48], &quot;di&quot;: [0.0, -0.77], &quot;z&quot;: 0.72, &quot;material&quot;: &quot;kursi_kantor&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;silinder&quot;, &quot;radius&quot;: 0.06, &quot;depth&quot;: 0.44, &quot;di&quot;: [0.0, -0.55], &quot;z&quot;: 0.22, &quot;material&quot;: &quot;logam_abu&quot;},</span></span>
<span class="line"><span>            ]</span></span>
<span class="line"><span>            return self._rakit_hierarki_lokal(spec, komp)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_set_ruang_r(self, spec):</span></span>
<span class="line"><span>            komp = [</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.95, 0.45, 0.05], &quot;di&quot;: [0.0, 0.12], &quot;z&quot;: 0.73, &quot;material&quot;: &quot;kayu_meja&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.38, 0.04, 0.26], &quot;di&quot;: [0.0, 0.22], &quot;z&quot;: 0.90, &quot;material&quot;: &quot;layar_monitor&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [0.40, 0.40, 0.45], &quot;di&quot;: [0.0, -0.22], &quot;z&quot;: 0.225, &quot;material&quot;: &quot;kursi_kantor&quot;},</span></span>
<span class="line"><span>            ]</span></span>
<span class="line"><span>            return self._rakit_hierarki_lokal(spec, komp)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_rak_arsip(self, spec):</span></span>
<span class="line"><span>            komp = []</span></span>
<span class="line"><span>            for sz in [0.20, 0.75, 1.30, 1.85]:</span></span>
<span class="line"><span>                komp.append({&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [1.35, 0.48, 0.04], &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: sz, &quot;material&quot;: &quot;logam_abu&quot;})</span></span>
<span class="line"><span>                if sz &lt; 1.80:</span></span>
<span class="line"><span>                    komp.append({&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [1.10, 0.38, 0.32], &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: sz + 0.18, &quot;material&quot;: &quot;kardus_arsip&quot;})</span></span>
<span class="line"><span>            return self._rakit_hierarki_lokal(spec, komp)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_wastafel(self, spec):</span></span>
<span class="line"><span>            komp = [</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [1.60, 0.52, 0.82], &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: 0.41, &quot;material&quot;: &quot;keramik_putih&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [1.50, 0.04, 0.95], &quot;di&quot;: [0.0, -0.24], &quot;z&quot;: 1.35, &quot;material&quot;: &quot;kaca_jendela&quot;},</span></span>
<span class="line"><span>            ]</span></span>
<span class="line"><span>            return self._rakit_hierarki_lokal(spec, komp)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_meja_pantry(self, spec):</span></span>
<span class="line"><span>            komp = [</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [2.2, 0.60, 0.85], &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: 0.425, &quot;material&quot;: &quot;kayu_meja&quot;},</span></span>
<span class="line"><span>                {&quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [2.24, 0.64, 0.05], &quot;di&quot;: [0.0, 0.0], &quot;z&quot;: 0.875, &quot;material&quot;: &quot;keramik_putih&quot;},</span></span>
<span class="line"><span>            ]</span></span>
<span class="line"><span>            return self._rakit_hierarki_lokal(spec, komp)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_tangga_darurat(self, spec):</span></span>
<span class="line"><span>            panjang = spec.get(&quot;panjang&quot;, 4.0)</span></span>
<span class="line"><span>            lebar = spec.get(&quot;lebar&quot;, 1.2)</span></span>
<span class="line"><span>            jml_anak = 8</span></span>
<span class="line"><span>            dx, dz = panjang / float(jml_anak), 2.4 / float(jml_anak)</span></span>
<span class="line"><span>            komp = []</span></span>
<span class="line"><span>            for i in range(jml_anak):</span></span>
<span class="line"><span>                x_pos = -panjang / 2.0 + (i + 0.5) * dx</span></span>
<span class="line"><span>                t_blok = (i + 1) * dz</span></span>
<span class="line"><span>                komp.append({</span></span>
<span class="line"><span>                    &quot;type&quot;: &quot;box&quot;, &quot;dimensions&quot;: [dx * 0.96, lebar, t_blok],</span></span>
<span class="line"><span>                    &quot;di&quot;: [x_pos, 0.0], &quot;z&quot;: t_blok / 2.0, &quot;material&quot;: &quot;lantai_tangga&quot;,</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span>            return self._rakit_hierarki_lokal(spec, komp)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    # 5. DenahBuilder: Membangun Lantai Bertekstur, Dinding Bata &amp; Aset Modular</span></span>
<span class="line"><span>    # --------------------------------------------------------------------------</span></span>
<span class="line"><span>    class DenahBuilder:</span></span>
<span class="line"><span>        def __init__(self, builder, cfg_rumah):</span></span>
<span class="line"><span>            self.builder = builder</span></span>
<span class="line"><span>            self.cfg = cfg_rumah</span></span>
<span class="line"><span>            self.tinggi = float(cfg_rumah.get(&quot;tinggi_dinding&quot;, 3.0))</span></span>
<span class="line"><span>            self.tebal = float(cfg_rumah.get(&quot;tebal_dinding&quot;, 0.15))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        @staticmethod</span></span>
<span class="line"><span>        def _potong_dengan_celah(a1, a2, celah_list):</span></span>
<span class="line"><span>            batas = [(min(a1, a2), max(a1, a2))]</span></span>
<span class="line"><span>            for c in celah_list:</span></span>
<span class="line"><span>                baru = []</span></span>
<span class="line"><span>                for (s, e) in batas:</span></span>
<span class="line"><span>                    if c[&quot;ke&quot;] &lt;= s or c[&quot;dari&quot;] &gt;= e:</span></span>
<span class="line"><span>                        baru.append((s, e))</span></span>
<span class="line"><span>                    else:</span></span>
<span class="line"><span>                        if c[&quot;dari&quot;] &gt; s:</span></span>
<span class="line"><span>                            baru.append((s, c[&quot;dari&quot;]))</span></span>
<span class="line"><span>                        if c[&quot;ke&quot;] &lt; e:</span></span>
<span class="line"><span>                            baru.append((c[&quot;ke&quot;], e))</span></span>
<span class="line"><span>                batas = baru</span></span>
<span class="line"><span>            return [(s, e) for (s, e) in batas if e - s &gt; 0.01]</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_dinding(self):</span></span>
<span class="line"><span>            for seg in self.cfg.get(&quot;segmen_dinding&quot;, []):</span></span>
<span class="line"><span>                x1, y1 = float(seg[&quot;dari&quot;][0]), float(seg[&quot;dari&quot;][1])</span></span>
<span class="line"><span>                x2, y2 = float(seg[&quot;ke&quot;][0]), float(seg[&quot;ke&quot;][1])</span></span>
<span class="line"><span>                horizontal = abs(y1 - y2) &lt; 1e-4</span></span>
<span class="line"><span>                mat = seg.get(&quot;material&quot;, &quot;dinding_interior&quot;)</span></span>
<span class="line"><span>                celah_list = seg.get(&quot;celah&quot;, [])</span></span>
<span class="line"><span></span></span>
<span class="line"><span>                a1, a2 = (min(x1, x2), max(x1, x2)) if horizontal else (min(y1, y2), max(y1, y2))</span></span>
<span class="line"><span>                for idx, (s, e) in enumerate(self._potong_dengan_celah(a1, a2, celah_list)):</span></span>
<span class="line"><span>                    panjang = e - s</span></span>
<span class="line"><span>                    tengah = (s + e) / 2.0</span></span>
<span class="line"><span>                    dim = [panjang, self.tebal, self.tinggi] if horizontal else [self.tebal, panjang, self.tinggi]</span></span>
<span class="line"><span>                    pos = [tengah, y1] if horizontal else [x1, tengah]</span></span>
<span class="line"><span>                    self.builder.membangun({</span></span>
<span class="line"><span>                        &quot;type&quot;: &quot;box&quot;, &quot;name&quot;: f&quot;{seg[&#39;nama&#39;]}_seg{idx}&quot;,</span></span>
<span class="line"><span>                        &quot;dimensions&quot;: dim, &quot;di&quot;: pos, &quot;z&quot;: self.tinggi / 2.0, &quot;material&quot;: mat,</span></span>
<span class="line"><span>                    })</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_lantai(self):</span></span>
<span class="line"><span>            for z in self.cfg.get(&quot;zona_lantai&quot;, []):</span></span>
<span class="line"><span>                x1, y1 = float(z[&quot;min_xy&quot;][0]), float(z[&quot;min_xy&quot;][1])</span></span>
<span class="line"><span>                x2, y2 = float(z[&quot;max_xy&quot;][0]), float(z[&quot;max_xy&quot;][1])</span></span>
<span class="line"><span>                self.builder.membangun({</span></span>
<span class="line"><span>                    &quot;type&quot;: &quot;box&quot;, &quot;name&quot;: z[&quot;nama&quot;],</span></span>
<span class="line"><span>                    &quot;dimensions&quot;: [abs(x2 - x1), abs(y2 - y1), 0.10],</span></span>
<span class="line"><span>                    &quot;di&quot;: [(x1 + x2) / 2.0, (y1 + y2) / 2.0],</span></span>
<span class="line"><span>                    &quot;z&quot;: -0.05, &quot;material&quot;: z.get(&quot;material&quot;, &quot;lantai_koridor&quot;),</span></span>
<span class="line"><span>                })</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def _bangun_furnitur(self):</span></span>
<span class="line"><span>            for f in self.cfg.get(&quot;furnitur&quot;, []):</span></span>
<span class="line"><span>                self.builder.membangun(f)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def bangun_semua(self):</span></span>
<span class="line"><span>            self._bangun_lantai()</span></span>
<span class="line"><span>            self._bangun_dinding()</span></span>
<span class="line"><span>            self._bangun_furnitur()</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # ==========================================================================</span></span>
<span class="line"><span>    # BAGIAN 5: LEGO BUILDER &amp; 3D TRANSFORM INTERACTIVE APP (SIDEBAR N-PANEL)</span></span>
<span class="line"><span>    # Menjadikan script ini seperti Aplikasi di dalam Blender!</span></span>
<span class="line"><span>    # ==========================================================================</span></span>
<span class="line"><span>    class LegoTransformAppProps(bpy.types.PropertyGroup):</span></span>
<span class="line"><span>        brick_color: bpy.props.EnumProperty(</span></span>
<span class="line"><span>            name=&quot;Warna LEGO&quot;,</span></span>
<span class="line"><span>            items=[</span></span>
<span class="line"><span>                (&quot;lego_merah&quot;,  &quot;Merah LEGO&quot;,  &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;lego_kuning&quot;, &quot;Kuning LEGO&quot;, &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;lego_biru&quot;,   &quot;Biru LEGO&quot;,   &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;lego_hijau&quot;,  &quot;Hijau LEGO&quot;,  &quot;&quot;),</span></span>
<span class="line"><span>            ],</span></span>
<span class="line"><span>            default=&quot;lego_merah&quot;,</span></span>
<span class="line"><span>        )</span></span>
<span class="line"><span>        studs_x: bpy.props.IntProperty(name=&quot;Stud X&quot;, default=2, min=1, max=8)</span></span>
<span class="line"><span>        studs_y: bpy.props.IntProperty(name=&quot;Stud Y&quot;, default=4, min=1, max=8)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        # Parameter Transformasi Matriks 3D</span></span>
<span class="line"><span>        trans_xyz: bpy.props.FloatVectorProperty(name=&quot;Translasi (T)&quot;, default=(18.0, 9.0, 0.0), subtype=&quot;TRANSLATION&quot;)</span></span>
<span class="line"><span>        rot_deg: bpy.props.FloatVectorProperty(name=&quot;Rotasi Euler (deg)&quot;, default=(0.0, 0.0, 0.0), subtype=&quot;XYZ&quot;)</span></span>
<span class="line"><span>        scale_xyz: bpy.props.FloatVectorProperty(name=&quot;Skala (S)&quot;, default=(1.0, 1.0, 1.0), min=0.1, max=10.0, subtype=&quot;XYZ&quot;)</span></span>
<span class="line"><span>        shear_xy: bpy.props.FloatVectorProperty(name=&quot;Shear XY&quot;, default=(0.0, 0.0), size=2, min=-1.5, max=1.5)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        # Parameter Texture &amp; UV Mapping</span></span>
<span class="line"><span>        preset_tekstur: bpy.props.EnumProperty(</span></span>
<span class="line"><span>            name=&quot;Preset Tekstur&quot;,</span></span>
<span class="line"><span>            items=[</span></span>
<span class="line"><span>                (&quot;BRICK&quot;,         &quot;Bata Prosedural (Brick + Bump)&quot;, &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;CHECKER&quot;,       &quot;Ubin Catur (Checker)&quot;,           &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;WOOD&quot;,          &quot;Serat Kayu (Wave Wood)&quot;,         &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;IMAGE_CHECKER&quot;, &quot;Image Texture (UV Pixel Map)&quot;,   &quot;&quot;),</span></span>
<span class="line"><span>                (&quot;LEGO_PLASTIC&quot;,  &quot;Plastik LEGO Glossy&quot;,            &quot;&quot;),</span></span>
<span class="line"><span>            ],</span></span>
<span class="line"><span>            default=&quot;BRICK&quot;,</span></span>
<span class="line"><span>        )</span></span>
<span class="line"><span>        uv_scale_val: bpy.props.FloatProperty(name=&quot;Skala UV&quot;, default=4.0, min=0.2, max=30.0)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    class LEGOAPP_OT_spawn_brick(bpy.types.Operator):</span></span>
<span class="line"><span>        bl_idname = &quot;legoapp.spawn_brick&quot;</span></span>
<span class="line"><span>        bl_label = &quot;Tambah Balok LEGO (Matriks 4x4)&quot;</span></span>
<span class="line"><span>        bl_options = {&quot;REGISTER&quot;, &quot;UNDO&quot;}</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def execute(self, context):</span></span>
<span class="line"><span>            props = context.scene.lego_app_props</span></span>
<span class="line"><span>            builder = AssetBuilder(TextureMaterialFactory(), DEFAULT_CONFIG_ASSETS[&quot;palet&quot;])</span></span>
<span class="line"><span>            rot_rad = [math.radians(a) for a in props.rot_deg]</span></span>
<span class="line"><span>            brick = builder.membangun({</span></span>
<span class="line"><span>                &quot;type&quot;: &quot;lego_brick&quot;,</span></span>
<span class="line"><span>                &quot;nama&quot;: f&quot;Lego_{props.studs_x}x{props.studs_y}&quot;,</span></span>
<span class="line"><span>                &quot;studs_x&quot;: props.studs_x,</span></span>
<span class="line"><span>                &quot;studs_y&quot;: props.studs_y,</span></span>
<span class="line"><span>                &quot;unit_size&quot;: 0.35,</span></span>
<span class="line"><span>                &quot;height&quot;: 0.40,</span></span>
<span class="line"><span>                &quot;di&quot;: [props.trans_xyz[0], props.trans_xyz[1]],</span></span>
<span class="line"><span>                &quot;z&quot;: props.trans_xyz[2],</span></span>
<span class="line"><span>                &quot;rot&quot;: rot_rad,</span></span>
<span class="line"><span>                &quot;scale&quot;: list(props.scale_xyz),</span></span>
<span class="line"><span>                &quot;material&quot;: props.brick_color,</span></span>
<span class="line"><span>            })</span></span>
<span class="line"><span>            context.view_layer.objects.active = brick</span></span>
<span class="line"><span>            brick.select_set(True)</span></span>
<span class="line"><span>            self.report({&quot;INFO&quot;}, f&quot;Balok LEGO {brick.name} berhasil dirakit!&quot;)</span></span>
<span class="line"><span>            return {&quot;FINISHED&quot;}</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    class LEGOAPP_OT_apply_matrix(bpy.types.Operator):</span></span>
<span class="line"><span>        bl_idname = &quot;legoapp.apply_matrix&quot;</span></span>
<span class="line"><span>        bl_label = &quot;Terapkan Matriks 4x4 ke Objek Aktif&quot;</span></span>
<span class="line"><span>        bl_options = {&quot;REGISTER&quot;, &quot;UNDO&quot;}</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def execute(self, context):</span></span>
<span class="line"><span>            obj = context.active_object</span></span>
<span class="line"><span>            if not obj:</span></span>
<span class="line"><span>                self.report({&quot;WARNING&quot;}, &quot;Pilih objek terlebih dahulu di 3D Viewport!&quot;)</span></span>
<span class="line"><span>                return {&quot;CANCELLED&quot;}</span></span>
<span class="line"><span>            props = context.scene.lego_app_props</span></span>
<span class="line"><span>            rot_rad = [math.radians(a) for a in props.rot_deg]</span></span>
<span class="line"><span>            M = Transform3DEngine.komposisi_trs(</span></span>
<span class="line"><span>                lokasi=tuple(props.trans_xyz),</span></span>
<span class="line"><span>                rotasi_euler=rot_rad,</span></span>
<span class="line"><span>                skala=tuple(props.scale_xyz),</span></span>
<span class="line"><span>                shear=tuple(props.shear_xy),</span></span>
<span class="line"><span>            )</span></span>
<span class="line"><span>            obj.matrix_world = M</span></span>
<span class="line"><span>            self.report({&quot;INFO&quot;}, f&quot;Matriks 4x4 (T*R*Shear*S) diterapkan ke {obj.name}&quot;)</span></span>
<span class="line"><span>            return {&quot;FINISHED&quot;}</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    class LEGOAPP_OT_apply_texture(bpy.types.Operator):</span></span>
<span class="line"><span>        bl_idname = &quot;legoapp.apply_texture&quot;</span></span>
<span class="line"><span>        bl_label = &quot;Terapkan Tekstur &amp; Skala UV&quot;</span></span>
<span class="line"><span>        bl_options = {&quot;REGISTER&quot;, &quot;UNDO&quot;}</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def execute(self, context):</span></span>
<span class="line"><span>            obj = context.active_object</span></span>
<span class="line"><span>            if not obj or obj.type != &quot;MESH&quot;:</span></span>
<span class="line"><span>                self.report({&quot;WARNING&quot;}, &quot;Pilih objek MESH (Lantai/Dinding/Bata) terlebih dahulu!&quot;)</span></span>
<span class="line"><span>                return {&quot;CANCELLED&quot;}</span></span>
<span class="line"><span>            props = context.scene.lego_app_props</span></span>
<span class="line"><span>            s = props.uv_scale_val</span></span>
<span class="line"><span>            nama_mat = f&quot;Mat_Custom_{props.preset_tekstur}_{int(s*10)}&quot;</span></span>
<span class="line"><span>            spec = {</span></span>
<span class="line"><span>                &quot;rgba&quot;: [0.85, 0.78, 0.68, 1.0],</span></span>
<span class="line"><span>                &quot;color2&quot;: [0.35, 0.28, 0.22, 1.0],</span></span>
<span class="line"><span>                &quot;roughness&quot;: 0.35,</span></span>
<span class="line"><span>                &quot;tex_type&quot;: props.preset_tekstur,</span></span>
<span class="line"><span>                &quot;uv_scale&quot;: [s, s, s],</span></span>
<span class="line"><span>                &quot;bump_strength&quot;: 0.20,</span></span>
<span class="line"><span>            }</span></span>
<span class="line"><span>            if nama_mat in bpy.data.materials:</span></span>
<span class="line"><span>                bpy.data.materials.remove(bpy.data.materials[nama_mat])</span></span>
<span class="line"><span>            mat = TextureMaterialFactory.get_or_create(nama_mat, spec)</span></span>
<span class="line"><span>            SceneManager.generate_box_uv(obj)</span></span>
<span class="line"><span>            obj.data.materials.clear()</span></span>
<span class="line"><span>            obj.data.materials.append(mat)</span></span>
<span class="line"><span>            self.report({&quot;INFO&quot;}, f&quot;Tekstur {props.preset_tekstur} (UV Scale={s:.1f}) diterapkan ke {obj.name}&quot;)</span></span>
<span class="line"><span>            return {&quot;FINISHED&quot;}</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    class LEGOAPP_PT_main_panel(bpy.types.Panel):</span></span>
<span class="line"><span>        bl_label = &quot;Modul 2: LEGO 3D Transform &amp; Texture&quot;</span></span>
<span class="line"><span>        bl_idname = &quot;LEGOAPP_PT_main_panel&quot;</span></span>
<span class="line"><span>        bl_space_type = &quot;VIEW_3D&quot;</span></span>
<span class="line"><span>        bl_region_type = &quot;UI&quot;</span></span>
<span class="line"><span>        bl_category = &quot;LegoApp M2&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        def draw(self, context):</span></span>
<span class="line"><span>            layout = self.layout</span></span>
<span class="line"><span>            props = context.scene.lego_app_props</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            box1 = layout.box()</span></span>
<span class="line"><span>            box1.label(text=&quot;1. Generator Balok LEGO Modular&quot;, icon=&quot;MESH_CUBE&quot;)</span></span>
<span class="line"><span>            box1.prop(props, &quot;brick_color&quot;)</span></span>
<span class="line"><span>            row = box1.row(align=True)</span></span>
<span class="line"><span>            row.prop(props, &quot;studs_x&quot;)</span></span>
<span class="line"><span>            row.prop(props, &quot;studs_y&quot;)</span></span>
<span class="line"><span>            box1.operator(&quot;legoapp.spawn_brick&quot;, icon=&quot;ADD&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            box2 = layout.box()</span></span>
<span class="line"><span>            box2.label(text=&quot;2. Matriks Transformasi 3D (4x4)&quot;, icon=&quot;ORIENTATION_GLOBAL&quot;)</span></span>
<span class="line"><span>            box2.prop(props, &quot;trans_xyz&quot;)</span></span>
<span class="line"><span>            box2.prop(props, &quot;rot_deg&quot;)</span></span>
<span class="line"><span>            box2.prop(props, &quot;scale_xyz&quot;)</span></span>
<span class="line"><span>            box2.prop(props, &quot;shear_xy&quot;)</span></span>
<span class="line"><span>            box2.operator(&quot;legoapp.apply_matrix&quot;, icon=&quot;CHECKMARK&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>            box3 = layout.box()</span></span>
<span class="line"><span>            box3.label(text=&quot;3. Shader Texture &amp; UV Mapping&quot;, icon=&quot;MATERIAL&quot;)</span></span>
<span class="line"><span>            box3.prop(props, &quot;preset_tekstur&quot;)</span></span>
<span class="line"><span>            box3.prop(props, &quot;uv_scale_val&quot;)</span></span>
<span class="line"><span>            box3.operator(&quot;legoapp.apply_texture&quot;, icon=&quot;TEXTURE&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    DAFTAR_KELAS_UI = (</span></span>
<span class="line"><span>        LegoTransformAppProps,</span></span>
<span class="line"><span>        LEGOAPP_OT_spawn_brick,</span></span>
<span class="line"><span>        LEGOAPP_OT_apply_matrix,</span></span>
<span class="line"><span>        LEGOAPP_OT_apply_texture,</span></span>
<span class="line"><span>        LEGOAPP_PT_main_panel,</span></span>
<span class="line"><span>    )</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def register_lego_ui():</span></span>
<span class="line"><span>        for cls in DAFTAR_KELAS_UI:</span></span>
<span class="line"><span>            try:</span></span>
<span class="line"><span>                bpy.utils.unregister_class(cls)</span></span>
<span class="line"><span>            except Exception:</span></span>
<span class="line"><span>                pass</span></span>
<span class="line"><span>            bpy.utils.register_class(cls)</span></span>
<span class="line"><span>        bpy.types.Scene.lego_app_props = bpy.props.PointerProperty(type=LegoTransformAppProps)</span></span>
<span class="line"><span></span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span># BAGIAN 6: ORKESTRASI UTAMA &amp; PENCAHAYAAN PRATINJAU MATERIAL</span></span>
<span class="line"><span># ==============================================================================</span></span>
<span class="line"><span>def atur_kamera_cahaya_dan_viewport(grid_xy):</span></span>
<span class="line"><span>    if not BLENDER_AVAILABLE:</span></span>
<span class="line"><span>        return</span></span>
<span class="line"><span>    gx, gy = float(grid_xy[0]), float(grid_xy[1])</span></span>
<span class="line"><span>    cx, cy = gx / 2.0, gy / 2.0</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    bpy.ops.object.light_add(type=&quot;SUN&quot;, location=(cx + 10.0, cy - 12.0, 25.0))</span></span>
<span class="line"><span>    sun = bpy.context.active_object</span></span>
<span class="line"><span>    sun.name = &quot;Matahari_Modul2&quot;</span></span>
<span class="line"><span>    sun.data.energy = 4.0</span></span>
<span class="line"><span>    sun.rotation_euler = (math.radians(38), math.radians(18), math.radians(-25))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    bpy.ops.object.camera_add(location=(cx, -gy * 0.65, max(gx, gy) * 0.95))</span></span>
<span class="line"><span>    cam = bpy.context.active_object</span></span>
<span class="line"><span>    cam.name = &quot;Kamera_Modul2&quot;</span></span>
<span class="line"><span>    cam.rotation_euler = (math.radians(46), 0.0, 0.0)</span></span>
<span class="line"><span>    cam.data.lens = 32.0</span></span>
<span class="line"><span>    bpy.context.scene.camera = cam</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    # Otomatis aktifkan mode shading &#39;MATERIAL&#39; agar tekstur langsung terlihat</span></span>
<span class="line"><span>    for area in bpy.context.screen.areas:</span></span>
<span class="line"><span>        if area.type == &quot;VIEW_3D&quot;:</span></span>
<span class="line"><span>            for space in area.spaces:</span></span>
<span class="line"><span>                if space.type == &quot;VIEW_3D&quot;:</span></span>
<span class="line"><span>                    space.shading.type = &quot;MATERIAL&quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span>def jalankan_modul_2(ascii_str=DENAH_ASCII):</span></span>
<span class="line"><span>    parser = AsciiDenahParser(</span></span>
<span class="line"><span>        scale_x=SKALA_X_METER_PER_KARAKTER,</span></span>
<span class="line"><span>        scale_y=SKALA_Y_METER_PER_KARAKTER,</span></span>
<span class="line"><span>        tinggi_dinding=TINGGI_DINDING_DEFAULT,</span></span>
<span class="line"><span>        tebal_dinding=TEBAL_DINDING_DEFAULT,</span></span>
<span class="line"><span>    )</span></span>
<span class="line"><span>    cfg_denah = parser.parse_to_dict(ascii_str)</span></span>
<span class="line"><span>    cfg_assets = DEFAULT_CONFIG_ASSETS</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    if BLENDER_AVAILABLE:</span></span>
<span class="line"><span>        SceneManager.bersihkan_scene()</span></span>
<span class="line"><span>        koleksi = SceneManager.buat_koleksi(&quot;RumahLego_Modul2&quot;)</span></span>
<span class="line"><span>        builder = AssetBuilder(TextureMaterialFactory(), cfg_assets[&quot;palet&quot;])</span></span>
<span class="line"><span>        DenahBuilder(builder, cfg_denah[&quot;rumah&quot;]).bangun_semua()</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        for obj in list(bpy.context.scene.objects):</span></span>
<span class="line"><span>            SceneManager.pindahkan_ke_koleksi(obj, koleksi)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>        atur_kamera_cahaya_dan_viewport(cfg_denah[&quot;rumah&quot;][&quot;grid&quot;])</span></span>
<span class="line"><span>        register_lego_ui()</span></span>
<span class="line"><span>        print(&quot;MATERI 2 OK: Transformasi Matriks 4x4, Tekstur Prosedural, &amp; Panel UI &#39;LegoApp M2&#39; aktif!&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    return cfg_denah</span></span>
<span class="line"><span></span></span>
<span class="line"><span>if __name__ == &quot;__main__&quot;:</span></span>
<span class="line"><span>    jalankan_modul_2(DENAH_ASCII)</span></span></code></pre></div><h2 id="daftar-pustaka" tabindex="-1">DAFTAR PUSTAKA <a class="header-anchor" href="#daftar-pustaka" aria-label="Permalink to &quot;DAFTAR PUSTAKA&quot;">​</a></h2><ol><li>Blender Foundation. <em>Blender 4.3 Python API Documentation</em>. <a href="https://docs.blender.org/api/4.3/" target="_blank" rel="noreferrer">https://docs.blender.org/api/4.3/</a></li><li>Blender Foundation. <em>Blender 4.3 Manual -Nodes: Texture, Bump, Mapping</em>. <a href="https://docs.blender.org/manual/en/4.3/" target="_blank" rel="noreferrer">https://docs.blender.org/manual/en/4.3/</a></li><li>Shirley, P., et al. <em>Fundamentals of Computer Graphics</em>, 4th ed. CRC Press.</li><li>Marschner, S., &amp; Hughes, J. F. <em>Computer Graphics: Principles and Practice</em>, 3rd ed. Addison-Wesley.</li><li>Tim Praktikum Komputer Grafik. <em>Modul 1 (V2): Dasar Blender &amp; Denah 2D (ASCII &amp; JSON) Menjadi 3D</em>. JTK POLBAN, 2026.</li></ol>`,135)])])}const D=s(F,[["render",C]]);export{S as __pageData,D as default};
