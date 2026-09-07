# Personal Portfolio - Angelica Christilia Talumewo

## Identitas

**Nama:** Angelica Christilia Talumewo  
**NPM:** 2506536313  
**Kelas:** PBP D  

---

## Deskripsi Proyek

Proyek ini merupakan personal portfolio website yang dikembangkan untuk mata kuliah
**Pemrograman Berbasis Platform (PBP)**, Fakultas Ilmu Komputer, Universitas Indonesia.

Website ini merupakan pengembangan dari halaman **About Me** pada Tutorial 01.
Pada Tugas 1, saya menambahkan section baru berupa **Skills** dan **Experience**
menggunakan HTML5 dan CSS3 tanpa menggunakan JavaScript maupun frontend framework.

Meskipun proyek dijalankan melalui Django, pada tahap ini isi halaman masih bersifat
statis. Django digunakan untuk melakukan rendering template, sedangkan data pada
halaman masih ditulis langsung di dalam HTML dan belum menggunakan database.

---

## Fitur

Website saat ini memiliki beberapa fitur utama:

- Profile / About Me
- Skills
- Experience
- Navigasi antar-section menggunakan anchor link
- Responsive layout untuk desktop, tablet, dan mobile
- CSS Grid dan Flexbox
- Hover interaction pada card dan elemen navigasi
- Sticky navigation
- Smooth scrolling
- Responsive typography menggunakan `clamp()`
- CSS custom properties untuk mengelola tema
- Keyboard focus indicator
- Dukungan `prefers-reduced-motion` untuk aksesibilitas

---

## Teknologi yang Digunakan

- HTML5
- CSS3
- Django
- Python
- Git
- GitHub

Pada Tugas 1 ini saya belum menggunakan JavaScript, database, maupun frontend
framework.

---

## Struktur Proyek

```text
myportofolio/
├── manage.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       ├── foto_Angel.png
│       └── logo_title.jpg
└── portofolio/
    ├── settings.py
    ├── urls.py
    ├── views.py
    └── ...
```

---

## Cara Menjalankan Proyek Secara Lokal

### 1. Clone repository

```bash
git clone https://github.com/christxiegut/myportofolio
```

Masuk ke direktori proyek:

```bash
cd myportofolio
```

### 2. Membuat virtual environment

Windows:

```bash
python -m venv env
```

Aktifkan virtual environment:

```bash
.\env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Memeriksa konfigurasi Django

```bash
python manage.py check
```

Jika konfigurasi benar, akan muncul:

```text
System check identified no issues (0 silenced).
```

### 5. Menjalankan development server

```bash
python manage.py runserver
```

Kemudian buka:

```text
http://127.0.0.1:8000/
```

---

## Development Progress

### Tutorial 01

Pada Tutorial 01 saya:

- Menyiapkan struktur proyek Django.
- Menghubungkan view dengan template HTML.
- Mengatur folder `templates` dan `static`.
- Membuat halaman About Me.
- Menggunakan semantic HTML5.
- Menggunakan CSS Grid dan Flexbox.
- Membuat tampilan responsive untuk desktop dan mobile.
- Menambahkan informasi pribadi, foto, NPM, program studi, dan social links.

### Tugas 1

Pada Tugas 1 saya:

- Menambahkan section **Skills** dengan tiga item.
- Menambahkan section **Experience** dengan tiga item.
- Mengembangkan navigasi menjadi Profile, Skills, dan Experience.
- Menggunakan CSS Grid untuk menyusun card.
- Menambahkan hover interaction pada Skills dan Experience.
- Menambahkan sticky navigation dan smooth scrolling.
- Mengembangkan responsive layout untuk desktop, tablet, dan mobile.
- Menggunakan CSS custom properties agar styling lebih reusable.
- Menambahkan keyboard focus indicator.
- Menambahkan dukungan `prefers-reduced-motion`.
- Menggunakan feature branch dan conventional commit dalam proses pengembangan.
- Melakukan pengecekan proyek menggunakan `python manage.py check`.

---

# Refleksi

### Tugas 1

#### 1. Apakah penggunaan elemen semantik HTML5 seperti `<section>` dan `<article>` membantu dalam membuat static web, dan bagaimana peranannya?

Ya, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`,
`<main>`, `<section>`, `<article>`, dan `<footer>`.

Menurut saya, keuntungan utama semantic HTML bukan terletak pada perubahan tampilan
visual, karena elemen seperti `<section>` maupun `<article>` tetap dapat diberikan CSS
seperti elemen lainnya. Manfaat utamanya adalah memberikan makna yang lebih jelas
terhadap struktur dokumen.

Pada website saya, `<section>` digunakan untuk memisahkan kelompok konten utama,
yaitu Profile, Skills, dan Experience. Setiap section memiliki topik dan tujuan yang
berbeda sehingga penggunaan `<section>` membuat struktur halaman lebih mudah
dipahami.

Saya menggunakan `<article>` pada setiap item Skills dan Experience karena setiap
card merepresentasikan satu unit informasi yang dapat dipahami secara mandiri.

Dari sisi developer, penggunaan semantic HTML membuat kode lebih mudah dibaca dan
dipelihara. Jika seluruh struktur hanya menggunakan `<div>`, saya harus lebih bergantung
pada nama class untuk mengetahui fungsi setiap elemen.

Selain itu, elemen semantik juga memberikan informasi struktur kepada browser dan
assistive technology seperti screen reader. Oleh karena itu, saya memahami bahwa HTML
sebaiknya digunakan untuk menjelaskan struktur dan makna konten, sedangkan CSS
digunakan untuk mengatur bagaimana konten tersebut ditampilkan.

---

#### 2. Tantangan tata letak apa yang muncul saat mengatur CSS responsive, dan bagaimana mengevaluasi prioritas posisi atau ukuran elemen saat berpindah dari desktop ke mobile?

Tantangan utama yang saya temukan adalah bahwa responsive design tidak cukup hanya
dengan mengecilkan ukuran semua elemen ketika layar menjadi lebih sempit.

Pada desktop, terdapat ruang horizontal yang cukup besar sehingga informasi Profile
dapat ditampilkan menggunakan dua kolom. Teks identitas dan deskripsi dapat berada
di sebelah kiri sementara foto berada di sebelah kanan.

Namun, jika struktur dua kolom tersebut dipertahankan pada layar mobile, lebar teks
menjadi terlalu kecil dan foto juga menjadi kurang proporsional. Karena itu, pada mobile
saya mengubah layout menjadi satu kolom.

Saya menentukan urutan elemen berdasarkan prioritas informasi. Nama dan identitas
ditampilkan terlebih dahulu, kemudian foto, lalu informasi detail. Hal tersebut membuat
pengguna tetap memperoleh informasi utama terlebih dahulu walaupun ruang layar lebih
terbatas.

Pada section Skills dan Experience, jumlah kolom juga berubah berdasarkan ruang yang
tersedia. Pada desktop beberapa card dapat ditampilkan secara horizontal, sedangkan
pada mobile card menjadi satu kolom agar isi tetap nyaman dibaca.

Dari proses tersebut saya memahami bahwa responsive design bukan hanya mengenai
ukuran layar, tetapi juga mengenai **visual hierarchy**, keterbacaan, ukuran elemen,
spacing, kemungkinan overflow, serta urutan informasi.

Saya juga memahami bahwa breakpoint sebaiknya dipilih ketika layout mulai kehilangan
keterbacaan atau kenyamanan, bukan hanya berdasarkan kategori perangkat seperti
desktop atau smartphone.

---

#### 3. Apa batasan static web murni ini, dan fungsionalitas dinamis apa yang paling ingin dipersiapkan untuk iterasi proyek selanjutnya?

Batasan utama dari website saat ini adalah seluruh isi Profile, Skills, dan Experience
masih ditulis langsung di dalam file HTML.

Artinya, ketika saya ingin menambah pengalaman baru, mengubah skill, atau menambahkan
project, saya harus melakukan perubahan langsung terhadap source code.

Website juga belum dapat menerima atau memproses input pengguna. Sebagai contoh,
belum ada contact form yang benar-benar dapat mengirim atau menyimpan pesan, sistem
autentikasi, maupun data yang berasal dari database.

Ketika jumlah data semakin banyak, pendekatan hard-coded seperti sekarang juga akan
menghasilkan banyak markup yang berulang dan menjadi semakin sulit dipelihara.

Pada iterasi berikutnya, saya ingin mulai memisahkan data dari tampilan menggunakan
Django dan database. Skills, Experience, dan Projects nantinya dapat disimpan sebagai
data kemudian dirender secara dinamis melalui Django template.

Fitur dinamis yang paling ingin saya persiapkan adalah **Projects section yang datanya
berasal dari backend** dan **contact form** yang dapat menerima input dari pengguna.

Dengan perkembangan tersebut, website tidak lagi hanya berfungsi sebagai halaman
presentasi statis, tetapi dapat berkembang menjadi aplikasi web yang mampu mengelola
data dan memberikan interaksi kepada pengguna.

---

# AI Disclosure

## AI Tool yang Digunakan

Dalam pengerjaan Tugas 1, saya menggunakan **ChatGPT** sebagai alat bantu dalam
proses pengembangan dan problem-solving.

AI digunakan untuk membantu:

- Brainstorming struktur section Skills dan Experience.
- Memberikan alternatif penggunaan CSS Grid dan Flexbox.
- Memberikan contoh responsive layout.
- Memberikan ide CSS-only interaction seperti hover effect dan smooth transition.
- Membantu mengevaluasi struktur semantic HTML.
- Memberikan saran penggunaan Git feature branch dan conventional commits.
- Membantu menyusun kerangka README.
- Membantu mengembangkan kerangka jawaban pertanyaan reflektif.
- Membantu proses debugging ketika CSS yang baru tidak muncul pada browser.

---

## Strategi Penggunaan AI

Saya memberikan kepada AI kode dari Tutorial 01, requirement Tugas 1, data portfolio
saya, serta rubrik penilaian.

Saya kemudian meminta AI membantu mengembangkan solusi yang tetap mengikuti
batasan tugas, yaitu menggunakan HTML5 dan CSS3 tanpa JavaScript maupun frontend
framework.

Hasil dari AI tidak langsung saya gunakan tanpa pemeriksaan. Saya tetap membaca,
menguji, serta menyesuaikan kode dengan struktur proyek saya sendiri.

---

## Keterbatasan AI yang Saya Temukan

Selama pengerjaan, saya menemukan bahwa AI memiliki beberapa keterbatasan.

Pertama, AI tidak dapat mengetahui kondisi repository lokal saya secara langsung.
Contohnya, ketika styling pada Skills dan Experience tidak muncul, pada awalnya AI
menganggap masalah mungkin berasal dari kode CSS atau cache browser.

Setelah dilakukan pengecekan manual, ternyata Django masih membaca file
`style.css` lama dari Tutorial 01.

Saya kemudian menjalankan:

```bash
python manage.py findstatic css/style.css --verbosity 2
```

untuk mengetahui lokasi file CSS yang benar-benar digunakan Django. Setelah file
yang benar ditemukan dan diperbarui, styling Skills dan Experience dapat muncul
sebagaimana mestinya.

Pengalaman tersebut menunjukkan bahwa AI dapat memberikan hipotesis debugging,
tetapi tidak dapat memastikan kondisi sistem lokal tanpa hasil pemeriksaan yang saya
lakukan sendiri.

Kedua, AI tidak mengetahui kebenaran semua data pribadi saya. AI tidak dapat memastikan
URL LinkedIn saya, nama file gambar yang sebenarnya, ataupun penulisan resmi nama
organisasi kecuali saya memberikan informasi tersebut.

Ketiga, AI tidak dapat menjamin kualitas responsive design hanya dengan melihat kode.
Tampilan tetap perlu diuji langsung melalui browser dan responsive DevTools.

Keempat, AI terkadang dapat memberikan implementasi yang lebih kompleks daripada
yang dibutuhkan. Oleh karena itu, saya tetap perlu memahami alasan penggunaan setiap
elemen HTML dan properti CSS sebelum memutuskan untuk mempertahankannya.

---

## Verifikasi dan Perbaikan Manual

Setelah menggunakan AI, saya melakukan beberapa pengecekan dan perbaikan secara
manual, yaitu:

1. Memastikan struktur folder Django sesuai dengan Tutorial 01.
2. Menghapus folder `html` lama yang merupakan sisa proses rename folder template.
3. Memastikan Django menggunakan folder `templates`.
4. Memastikan lokasi stylesheet menggunakan `findstatic`.
5. Memperbaiki dan menguji path gambar portfolio.
6. Menjalankan:

   ```bash
   python manage.py check
   ```

   hingga menghasilkan:

   ```text
   System check identified no issues (0 silenced).
   ```

7. Menjalankan website menggunakan:

   ```bash
   python manage.py runserver
   ```

8. Menguji navigasi, hover interaction, layout Skills, dan Experience melalui browser.
9. Menguji tampilan pada ukuran desktop dan mobile.
10. Menyusun commit Git secara bertahap menggunakan feature branch dan conventional
    commits.
11. Membaca kembali kode yang digunakan agar saya dapat menjelaskan implementasinya.

Dengan demikian, saya menggunakan AI sebagai alat bantu untuk mempercepat proses
belajar dan problem-solving, tetapi keputusan akhir, proses pengujian, debugging, dan
verifikasi implementasi tetap saya lakukan secara manual.

---

## Git Development Workflow

Pengembangan Tugas 1 dilakukan menggunakan feature branch:

```text
feature/portfolio-sections
```

Contoh conventional commit yang digunakan:

```text
feat: add skills and experience sections
style: add responsive grid and css interactions
```

Penggunaan branching dan commit terpisah dilakukan agar riwayat perubahan lebih mudah
dipahami dan mencerminkan proses pengembangan secara bertahap.

---

## AI Conversation / Prompt Log

Dokumentasi percakapan AI:

```Saya menggunakan Gemini sebagai alat bantu. Gemini digunakan untuk bertanya hal seperti gimana cara kerja setiap hal-hal di html
<https://share.gemini.google/bgYhxTTqNPYf>
<https://share.gemini.google/rsQ1uK4bHzHy>
```

---

## Catatan

Portfolio ini akan terus dikembangkan pada tutorial dan tugas berikutnya seiring
bertambahnya materi pada mata kuliah Pemrograman Berbasis Platform.