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

### Tugas 2

Pada tugas ini, saya menambahkan model `Project` dan halaman Projects untuk menampilkan proyek portofolio secara dinamis. Pengembangan tambahan meliputi pencarian proyek, halaman detail, serta pengujian otomatis.

#### 1. Alur request hingga halaman ditampilkan

Ketika pengguna membuka `/projects/`, Django mencocokkan alamat tersebut melalui `portofolio/urls.py`, kemudian meneruskannya ke `main/urls.py`. Rute tersebut menjalankan fungsi `show_projects` pada `main/views.py`.

View mengambil data melalui model `Project`. Jika terdapat parameter pencarian `q`, data disaring berdasarkan judul, deskripsi, atau teknologi. Data kemudian dikirim melalui context dengan kunci `name`, `project_list`, dan `query`.

Template `projects.html` menggunakan Django Template Language untuk menampilkan setiap proyek sebagai kartu. Jika daftar kosong, template menampilkan pesan yang sesuai. Hasil render dikirim sebagai respons HTML dan ditampilkan oleh browser dengan stylesheet yang terhubung.

Untuk halaman detail, rute `/projects/<int:pk>/` menjalankan `show_project_detail`. View mengambil proyek berdasarkan primary key dan merender `project_detail.html`. Proyek yang tidak ditemukan menghasilkan status 404 melalui `get_object_or_404`.

#### 2. Alasan menggunakan model dibandingkan data yang ditulis langsung dalam template

Model memisahkan penyimpanan data dari tampilan. Judul, deskripsi, teknologi, dan URL repositori dapat ditambahkan atau diperbarui melalui database tanpa mengubah struktur HTML setiap kartu.

Data yang sama juga dapat digunakan pada halaman daftar, hasil pencarian, dan halaman detail. Dengan demikian, perubahan informasi proyek cukup dilakukan pada satu sumber data.

Template tetap digunakan untuk mengatur struktur tampilan dan label antarmuka, sedangkan isi proyek berasal dari model. Pemisahan ini memudahkan pemeliharaan dan pengembangan fitur berikutnya.

#### 3. Perbedaan makemigrations dan migrate

`python manage.py makemigrations` membuat berkas migrasi yang mencatat perubahan definisi model.

`python manage.py migrate` menerapkan instruksi migrasi tersebut pada database.

Contoh pada tugas ini adalah penambahan model `Project`. Perintah `makemigrations` menghasilkan `main/migrations/0002_project.py`, kemudian `migrate` menerapkannya untuk membuat tabel yang diperlukan.

Penambahan atau perubahan isi data proyek tidak memerlukan migrasi selama struktur model tidak berubah.

#### Implementasi model

Model `Project` memiliki empat field selain primary key otomatis:

| Field | Tipe | Kegunaan |
| --- | --- | --- |
| `title` | `CharField(max_length=255)` | Menyimpan judul proyek |
| `description` | `TextField` | Menyimpan penjelasan proyek |
| `technologies` | `CharField(max_length=255)` | Menyimpan teknologi yang digunakan |
| `repository_url` | `URLField(blank=True)` | Menyimpan tautan repositori yang boleh dikosongkan |

`__str__()` mengembalikan judul proyek agar objek mudah dikenali.

#### Fitur dan keputusan implementasi

- Halaman Projects menampilkan data menggunakan perulangan template.
- Pesan “Belum ada proyek yang ditambahkan.” ditampilkan ketika daftar proyek kosong.
- Pencarian menggunakan `Q` dan `icontains` pada judul, deskripsi, serta teknologi. Kecocokan pada salah satu field sudah cukup untuk menampilkan proyek.
- Spasi di awal dan akhir kata kunci dibersihkan. Pencarian kosong menampilkan seluruh proyek.
- Pencarian tanpa kecocokan menampilkan pesan yang berbeda dari kondisi belum ada data.
- Halaman detail menampilkan informasi proyek sesuai ID pada URL.
- Tombol “Lihat repositori” ditampilkan hanya jika URL repositori tersedia.
- Navigasi dan tautan detail menggunakan named URL Django.
- Tombol “Lihat detail” dan “Lihat repositori” dikelompokkan di bawah deskripsi agar tindakan pada kartu mudah ditemukan.
- CSS pencarian dipisahkan dalam `project-search.css` dan dimuat setelah `style.css`.

Bentuk kolom pencarian menggunakan referensi visual SLCM yang saya berikan, kemudian disesuaikan dengan warna gelap dan aksen mint portofolio.

#### Menjalankan proyek dari clone baru

Kode Tugas 2 tersedia pada branch `master`.

Contoh berikut menggunakan Command Prompt Windows:

```bat
git clone --branch master https://github.com/christxiegut/myportofolio.git
cd myportofolio
python -m venv env
env\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Halaman yang dapat dibuka:

- Profile: http://127.0.0.1:8000/
- Experience: http://127.0.0.1:8000/experience/
- Projects: http://127.0.0.1:8000/projects/

Halaman detail dibuka melalui tombol “Lihat detail” pada kartu proyek.

#### Menambahkan contoh data proyek

Untuk menyediakan data pada database lokal, hentikan server lalu jalankan:

```bat
python manage.py shell
```

Masukkan kode berikut:

```python
from main.models import Project

Project.objects.get_or_create(
    title="Website Portofolio Pribadi",
    defaults={
        "description": (
            "Website untuk menampilkan profil, pengalaman organisasi, "
            "dan proyek pribadi dengan pola Model-View-Template."
        ),
        "technologies": "Python, Django, HTML, CSS",
        "repository_url": "https://github.com/christxiegut/myportofolio",
    },
)
```

Penggunaan `get_or_create` memungkinkan contoh data ini dijalankan kembali tanpa membuat duplikat berdasarkan judul tersebut.

Keluar dengan `exit()`, kemudian jalankan kembali server.

#### Pengujian

Seluruh tes dijalankan menggunakan:

```bat
python manage.py test
```

Hasil pengujian lokal pada 14 September 2026:

```text
Found 18 test(s).
Ran 18 tests in 0.349s

OK
```

| Berkas | Jumlah tes | Cakupan |
| --- | ---: | --- |
| `main/tests.py` | 6 | Profil, Experience, model Experience, serta respons halaman |
| `main/test_projects.py` | 9 | Daftar proyek, template, isi data, kondisi kosong, URL repositori opsional, dan pencarian |
| `main/test_project_detail.py` | 3 | Data detail sesuai ID, proyek yang tidak ditemukan, dan tautan detail setiap kartu |
| **Total** | **18** | **Seluruh tes lulus** |

Pengujian menggunakan database terpisah dari data portofolio lokal. Hasil ini memverifikasi skenario yang diuji pada lingkungan lokal, termasuk pemilihan proyek yang benar dan kondisi data tidak ditemukan.

#### Penggunaan AI dan log bantuan

Saya menggunakan ChatGPT untuk membantu memahami instruksi, menyusun dan merevisi kode, serta membuat draf dokumentasi. Bagian yang dibantu mencakup model, view, routing, template, CSS, dan pengujian otomatis.

Saya menerapkan perubahan pada proyek, menjalankan perintah Django, memeriksa tampilan di browser, memberikan masukan desain, dan menjalankan seluruh tes.

Berikut ringkasan log bantuan AI ChatGPT:

| Kebutuhan | Arahan dan bantuan yang diperoleh | Penerapan |
| --- | --- | --- |
| Memahami implementasi Tugas 2 | Penjelasan dan contoh kode model, view, routing, serta template | Menambahkan model Project dan halaman yang menampilkan data secara dinamis |
| Mengembangkan tugas berdasarkan rubrik skala 4 | Saran fitur tambahan dan aspek yang perlu diperiksa | Menambahkan pencarian, halaman detail, dan pengujian fitur |
| Menyempurnakan tampilan | Arahan dan contoh HTML/CSS berdasarkan referensi yang saya berikan | Menyesuaikan kolom pencarian serta menempatkan kedua tombol bersebelahan |
| Memeriksa fungsi aplikasi | Arahan skenario pengujian dan contoh kode unit test | Menjalankan seluruh pengujian dengan hasil 18 tes lulus |
| Melengkapi README | Bantuan menyusun draf penjelasan implementasi, pengujian, dan refleksi | Menyesuaikan dokumentasi dengan pekerjaan dan hasil pengujian yang dilakukan |

#### Refleksi implementasi

Saya belajar bahwa fitur yang berfungsi tetap perlu diperiksa dari sisi penggunaannya. Pada halaman Projects, tombol detail awalnya berada di bawah judul, sedangkan tombol repositori berada di bawah deskripsi. Setelah melihat hasilnya, saya meminta keduanya dikelompokkan agar lebih rapi.

Pengujian juga perlu memeriksa isi halaman, bukan hanya keberhasilan akses. Tes detail menggunakan dua proyek untuk memastikan halaman menampilkan objek sesuai ID yang diminta. Tes pencarian memeriksa beberapa field, kata kunci kosong, spasi tambahan, dan hasil yang tidak ditemukan.

Saat ini teknologi proyek disimpan sebagai teks. Pendekatan ini cukup untuk portofolio sederhana, tetapi pengembangan filter teknologi yang lebih terstruktur dapat menggunakan model teknologi tersendiri agar penamaannya konsisten.

#### Referensi

- Materi Tutorial 2 dan instruksi Tugas 2 mata kuliah PBP.
- [Django: Making queries](https://docs.djangoproject.com/en/5.2/topics/db/queries/)
- [Django: Shortcut functions](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/)
- [Django: Writing and running tests](https://docs.djangoproject.com/en/5.2/topics/testing/overview/)