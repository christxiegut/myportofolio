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


### Tugas 3

Tugas 3 mengembangkan bagian **Experience** pada portofolio Angelica Christilia Talumewo. Data pengalaman dapat ditambah, diperbarui, dihapus, dan diakses dalam JSON. Halaman daftar mengikuti alur model → JSON → deserialisasi → template, sesuai instruksi Form & Data Delivery.

#### 1. Mengapa menggunakan ModelForm dan csrf_token?

`ModelForm` menghubungkan formulir dengan model Django sehingga tipe field, batas panjang, pilihan kategori, dan aturan field wajib dapat mengikuti definisi model. Pada proyek ini, `ExperienceForm` memakai model `Experience`. Kolom judul, deskripsi, kategori, URL gambar, dan waktu selesai didefinisikan secara eksplisit. HTML formulir tetap dapat ditata sendiri, sedangkan validasi dan penyimpanan dibantu Django. Hal ini mengurangi pengulangan aturan antara model dan formulir. [Dokumentasi ModelForm](https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/)

Pada proses tambah, form dibuat dari `request.POST`. Pada proses edit, form juga diberi `instance=experience` agar `save()` memperbarui pengalaman yang dipilih. Tanpa instance, penyimpanan akan membuat objek baru. Data hanya disimpan setelah `form.is_valid()` bernilai benar. Jika tidak valid, formulir ditampilkan kembali beserta kesalahannya dan masukan yang perlu diperbaiki.

`{% csrf_token %}` menambahkan token tersembunyi pada formulir POST. Bersama middleware CSRF, token ini membantu Django menolak permintaan perubahan data yang tidak membawa token yang sesuai. Ini membantu mencegah situs lain memanfaatkan browser pengguna untuk mengirim permintaan yang tidak dikehendaki. Pada PWS, origin HTTPS situs juga didaftarkan dalam `CSRF_TRUSTED_ORIGINS`. Token CSRF tetap dibutuhkan pada form tambah, edit, dan hapus. [Dokumentasi pengaturan CSRF](https://docs.djangoproject.com/en/6.0/ref/settings/#csrf-trusted-origins)

#### 2. Mengapa JSON lebih disukai dibandingkan XML pada aplikasi web modern?

JSON merepresentasikan data sebagai objek, array, string, angka, boolean, dan `null`. Struktur ini mudah diproses di JavaScript menggunakan `JSON.parse()` serta dibuat kembali menggunakan `JSON.stringify()`. Karena antarmuka web banyak menggunakan JavaScript, JSON memudahkan pertukaran data dengan server. [Referensi JSON di MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON)

Untuk data portofolio berupa daftar pengalaman dan atributnya, penulisan JSON biasanya lebih ringkas karena tidak memerlukan tag pembuka dan penutup untuk setiap nilai seperti XML. Pada proyek ini, satu respons dapat memuat daftar pengalaman yang masing-masing memiliki identitas dan field model. XML tetap berguna untuk kebutuhan dokumen, namespace, atau integrasi sistem yang sudah memakai XML; pilihan format bergantung pada kebutuhan aplikasi.

#### 3. Bagaimana alur JSON dan mengapa diperlukan serialization?

Ketika endpoint `/api/experiences/` dibuka, routing menjalankan `get_experiences_json`. Fungsi ini mengambil `QuerySet` dari model `Experience`, menerapkan filter yang dikirim melalui query parameter, lalu memanggil `serializers.serialize("json", queryset)`. Hasilnya dikembalikan melalui `HttpResponse` dengan `content_type="application/json"`.

Objek model dan `QuerySet` merupakan objek Python yang tidak bisa langsung diperlakukan sebagai dokumen JSON oleh browser. Serialization mengubahnya menjadi representasi data yang dapat dikirim melalui HTTP, termasuk mengubah UUID dan nilai waktu ke bentuk yang sesuai untuk JSON. Serializer Django menyertakan informasi `model`, `pk`, dan `fields`, sehingga identitas serta data objek dapat direkonstruksi. [Dokumentasi serialization Django](https://docs.djangoproject.com/en/6.0/topics/serialization/)

Untuk halaman HTML `/experience/`, `show_experience` memanggil fungsi JSON tersebut, membaca isi responsnya, lalu memakai `serializers.deserialize("json", ...)`. Objek hasil deserialisasi dimasukkan ke `experience_list` dan ditampilkan oleh `experience.html`. Pemanggilan fungsi JSON dilakukan di Python, sehingga tidak membuat permintaan HTTP tambahan ke server sendiri. Objek hasil deserialisasi hanya ditampilkan; tidak disimpan ulang ke database.

#### Implementasi dan struktur kode

| Bagian | Implementasi |
| --- | --- |
| Model | Menggunakan `Experience` dari Tutorial 2 dengan primary key UUID |
| ModelForm | `ExperienceForm` pada `main/forms.py`; `ProjectForm` tetap tersedia |
| Field | `title` (CharField), `description` (TextField), `category` (choices), `thumbnail` (URLField), dan `ended_at` (DateTimeField opsional) |
| Field otomatis | `id` dan `started_at` dikelola model; tidak diedit melalui formulir |
| Tambah dan edit | Validasi serta template digunakan bersama; edit memakai `instance` |
| Hapus | POST dengan token CSRF dan konfirmasi sebelum pengiriman |
| JSON | `get_experiences_json` menyajikan objek yang sudah diserialisasi |
| Daftar | `show_experience` mengisi context dari hasil deserialisasi JSON |
| Tampilan bersama | Halaman penuh memakai `{% extends 'base.html' %}` |
| Komponen | Konfirmasi hapus merupakan potongan HTML yang dipasang dengan `{% include %}` |
| Fitur tambahan | Pencarian judul/deskripsi, filter kategori/status, jumlah hasil, reset filter, gambar opsional, notifikasi, dan empty state |

Model tidak diubah pada Tugas 3, sehingga tidak ada migration baru untuk fitur ini. `ended_at` adalah waktu selesai pengalaman yang dapat diisi pengguna; mengosongkannya menandai pengalaman masih berlangsung. `started_at` tetap merupakan waktu pencatatan otomatis sesuai model sebelumnya.

Routing Experience dikelola di `main/urls.py`, sedangkan implementasi view ditempatkan di `main/experience_views.py`. View `show_experience` yang dirujuk routing berasal dari modul baru tersebut. Definisi lama pada `main/views.py`, jika masih ada, tidak lagi menjadi target rute Experience.

| URL | Metode | Fungsi |
| --- | --- | --- |
| `/experience/` | GET | Daftar dari JSON yang dideserialisasi |
| `/experience/add/` | GET, POST | Form tambah dan penyimpanan |
| `/experience/<uuid>/edit/` | GET, POST | Form edit dan pembaruan |
| `/experience/<uuid>/delete/` | POST | Hapus pengalaman yang dipilih |
| `/api/experiences/` | GET | JSON seluruh pengalaman |
| `/api/experiences/?category=volunteer&status=ongoing` | GET | Contoh filter gabungan |
| `/api/experiences/?q=vendor` | GET | Contoh pencarian kata kunci |

Filter pada HTML dan JSON menggunakan fungsi yang sama. Tidak ada request HTTP internal untuk menghasilkan daftar. Bagian Projects, termasuk pencarian, detail, form tambah, JSON/XML, dan hapus dari Tutorial 3, tetap digunakan.

#### Setup dan pengujian mingguan

Lanjutkan setup dasar proyek pada bagian README sebelumnya. Dari folder yang berisi `manage.py`, jalankan perintah berikut pada PowerShell Windows:

```powershell
.\env\Scripts\python.exe manage.py migrate
.\env\Scripts\python.exe manage.py test
.\env\Scripts\python.exe manage.py runserver
```

Perintah tersebut memakai Python dari virtual environment secara langsung. Untuk pemasangan pada lingkungan baru, instal lebih dahulu dependensi proyek yang tercantum dalam `requirements.txt`.

Berkas `main/test_experience_crud.py` memuat 24 tes yang memeriksa antara lain penyimpanan valid, penolakan data tidak valid, pengeditan tanpa duplikasi UUID, data tidak berubah saat validasi gagal, metode hapus, objek tidak ditemukan, data JSON, filter gabungan, escaping, dan CSRF. Tiga belas tes Projects dari Tutorial 3 juga dipakai saat menyiapkan paket ini. Hasil uji paket pada lingkungan terpisah dengan Django 6.1: **37 tes lolos**. Hasil tersebut perlu dilengkapi dengan pengujian seluruh proyek pada lingkungan pemasangan.

Verifikasi manual yang perlu dilakukan setelah pemasangan:

1. Tambah pengalaman percobaan dan pastikan tampil pada daftar.
2. Edit judul pengalaman itu; pastikan jumlah kartu tidak bertambah.
3. Coba pencarian, filter kategori, dan filter status.
4. Buka JSON dan cocokkan judul serta ID dengan pengalaman yang ditambahkan.
5. Buka konfirmasi hapus lalu pilih Batal; data harus tetap ada.
6. Hapus pengalaman percobaan melalui tombol konfirmasi; data harus hilang.
7. Pastikan halaman Profile dan fitur Projects sebelumnya masih dapat digunakan.

PWS memiliki database yang terpisah dari database lokal. Data yang dibuat di laptop tidak otomatis terkirim ketika source code di-push. Data PWS dapat ditambahkan lewat formulir pada website setelah deployment berhasil.

#### Bantuan AI dan evaluasinya

ChatGPT digunakan untuk membaca ketentuan tugas, menyusun rancangan serta draf kode CRUD dan JSON Experience, menyiapkan template dan pengujian, serta menyusun draf dokumentasi dan penjelasan reflektif. Strategi yang digunakan adalah melanjutkan struktur Tutorial 3 dan memakai model serta tema yang sudah ada.

| Permintaan atau arahan | Bantuan yang digunakan |
| --- | --- |
| Meminta bantuan Tugas 3 dengan deadline 21 September 2026 pukul 23.59 WIB | Membaca checklist dan rubrik, lalu memetakan kebutuhan pada bagian Experience |
| Melanjutkan proyek Tutorial 3 yang dibahas sebelumnya | Menyusun ModelForm, routing UUID, view CRUD/JSON, dan template dengan tema pastel |
| Memeriksa kesesuaian sebelum pemasangan | Menyiapkan tes untuk validasi, pembaruan, penghapusan, filter, dan CSRF |
| Menyiapkan dokumentasi | Menyusun penjelasan implementasi, petunjuk uji, serta draf tiga jawaban reflektif |

Keterbatasan bantuan AI adalah tidak memiliki akses langsung ke berkas terbaru pada laptop dan konfigurasi server PWS. Karena itu, keberhasilan tes paket di lingkungan terpisah belum membuktikan bahwa seluruh konfigurasi lokal atau deployment sudah benar. Kode juga perlu dipahami, terutama perbedaan form tambah dan edit, arti UUID pada URL, serta alasan POST dan CSRF dipakai untuk perubahan data. Catatan perbaikan manual dan hasil verifikasi lokal perlu ditambahkan berdasarkan pengerjaan yang benar-benar dilakukan.

### Tugas 4 - Autentikasi, Otorisasi, dan Star Experience

Tugas 4 melanjutkan bagian **Experience** dari Tugas 3. Sistem akun, session, cookie `last_login`, dan Star Projects dari Tutorial 4 tetap digunakan. Halaman daftar/detail Experience dan API JSON dapat dibaca tanpa login. Perubahan Experience mengikuti empat peran berikut.

| Peran | Baca daftar/detail | Star/Unstar | Tambah | Edit | Hapus |
| --- | --- | --- | --- | --- | --- |
| Pengunjung tanpa login | Ya | Login dahulu | Login dahulu | Login dahulu | Login dahulu |
| Pengguna biasa | Ya | Ya | Tidak | Tidak | Tidak |
| Editor | Ya | Ya | Tidak | Ya | Tidak |
| Pemilik (`is_superuser=True`) | Ya | Ya | Ya | Ya | Ya |

#### Implementasi

- `main/access.py` menyimpan pemeriksaan keanggotaan Django Group bernama `Editor` dan aturan siapa yang boleh mengedit Experience.
- `main/experience_views.py` memakai `login_required` untuk aksi yang membutuhkan akun. Akun yang sudah login tetapi tidak berhak mendapatkan HTTP 403 melalui `PermissionDenied`. Pemeriksaan dilakukan sebelum perubahan database.
- Create/delete hanya diizinkan bagi superuser. Update diizinkan bagi superuser atau anggota grup Editor. Pengaturan grup dilakukan oleh pemilik melalui Django Admin; tidak tersedia pada form registrasi.
- Template daftar dan detail menampilkan kontrol sesuai peran. Tampilan tombol bukan pengganti pemeriksaan izin di view.
- `Experience.starred_by` merupakan `ManyToManyField` ke User dengan `related_name="starred_experiences"`. Tabel penghubung bawaan Django menjaga keunikan pasangan Experience-User.
- `toggle_experience_star` menerima POST dan dilindungi CSRF. Pengguna hanya dapat menambah atau menghapus star miliknya sendiri. ID akun yang dikirim lewat form tidak dipakai untuk menentukan pemberi star.
- API JSON memakai daftar field publik eksplisit serta `use_natural_foreign_keys=True`. Relasi `starred_by` ditampilkan sebagai username, bukan seluruh objek User. Password, email akun, session, dan flag peran tidak diserialisasi.
- Alur daftar dari Tugas 3 tetap dipertahankan: QuerySet diserialisasi ke JSON, hasilnya dideserialisasi, lalu objek dikirim ke template tanpa disimpan ulang. Relasi Star diprefetch untuk mengurangi query berulang saat template membaca jumlah/status star.

#### Fitur tambahan

1. Halaman detail Experience yang dapat diakses publik, dengan kontrol aksi sesuai peran.
2. Filter **Favorit saya** untuk menampilkan pengalaman yang diberi star oleh akun yang sedang login. Filter ini dapat digabungkan dengan pencarian, kategori, dan status.
3. Star/Unstar mempertahankan halaman detail atau filter yang sedang dibuka. Tujuan redirect diperiksa agar tidak mengarah ke situs luar.
4. Label peran pada halaman Experience menjelaskan tindakan yang tersedia bagi pengguna.
5. Tema pastel, konfirmasi hapus, pesan keberhasilan, navigasi keyboard, dan validasi form dari implementasi sebelumnya tetap digunakan.

#### Menjalankan versi ini

Gunakan environment dan dependencies proyek yang sudah tersedia. Dari direktori yang memuat `manage.py` di Windows:

```powershell
.\env\Scripts\python.exe manage.py makemigrations main
.\env\Scripts\python.exe manage.py migrate
.\env\Scripts\python.exe manage.py check
.\env\Scripts\python.exe manage.py test
.\env\Scripts\python.exe manage.py runserver
```

Migrasi baru menambahkan `starred_by` pada Experience. Setelah berkas migrasi ikut di-commit, pengguna yang baru meng-clone repositori cukup menjalankan `migrate`; `makemigrations` diperlukan ketika mengubah model.

Akun pemilik dibuat dengan `python manage.py createsuperuser`. Akun biasa dibuat lewat `/register/`. Untuk mengatur Editor:

1. Login ke `/admin/` dengan akun pemilik.
2. Pada Groups, buat grup bernama tepat `Editor`.
3. Pada Users, pilih akun yang akan menjadi editor dan masukkan ke grup `Editor`.
4. Biarkan `Staff status` dan `Superuser status` akun editor tidak dicentang. Simpan.

Implementasi ini memeriksa nama grup secara langsung, sehingga tidak perlu memberi permission admin tambahan kepada grup Editor. Editor bekerja melalui halaman Experience, bukan melalui dashboard admin.

#### Routing

| URL | Metode | Akses |
| --- | --- | --- |
| `/experience/` | GET | Publik; `q`, `category`, `status`, dan `starred=1` untuk filter |
| `/experience/<uuid>/` | GET | Detail publik |
| `/experience/add/` | GET, POST | Pemilik |
| `/experience/<uuid>/edit/` | GET, POST | Pemilik dan Editor |
| `/experience/<uuid>/delete/` | POST | Pemilik |
| `/experience/<uuid>/star/` | POST | Semua akun yang sudah login |
| `/api/experiences/` | GET | Data publik; filter favorit mengikuti akun peminta |

`starred=1` tanpa login menghasilkan daftar kosong. ID Experience tetap UUID; ID Project tetap integer. Relasi Star kedua model memiliki `related_name` yang berbeda.

#### Pengujian

`main/test_experience_access.py` menambahkan **26 tes** untuk matriks akses, penolakan request langsung, pencabutan keanggotaan Editor, kontrol template, Star/Unstar, CSRF, favorit per pengguna, redirect, dan field publik JSON. Tes CRUD dari Tugas 3 tetap dijalankan menggunakan akun pemilik agar sesuai aturan akses yang baru. Tes negatif terpisah memastikan pengguna biasa dan Editor tidak mendapat hak pemilik.

Sebanyak **85 tes lulus pada lingkungan pengujian paket yang terpisah**, mencakup 26 tes Tugas 4 dan 59 tes terdahulu yang tersedia. Hasil ini tidak dianggap sebagai hasil semua tes pada laptop atau PWS. Verifikasi proyek dilakukan dengan `python manage.py test` serta pemeriksaan browser untuk pengunjung, pengguna biasa, Editor, dan pemilik.

Migrasi juga dicoba pada salinan database pengujian yang telah memuat data. Data Experience/Project lama dan Star Project tetap tersimpan ketika tabel Star Experience ditambahkan.

#### Penggunaan AI dan catatan evaluasi

Alat yang digunakan adalah Gemini. Bantuan mencakup pembacaan rubrik, penyusunan draf kode dan tes, penyesuaian dengan struktur proyek sebelumnya, serta draf dokumentasi. Konteks yang diberikan berupa PDF tugas dan percakapan pengerjaan Tutorial 4. Salah satu permintaan yang digunakan:

>   Bertindak sebagai ahli dalam django dan design website dan bimbing saya mengerjakan tugas ini step by step

Ringkasan log bantuan:

| Bagian | Bantuan yang diberikan | Hal yang diperiksa |
| --- | --- | --- |
| Pemetaan rubrik | Melanjutkan Experience dari Tugas 3, dengan empat peran | Editor hanya boleh edit; pemilik boleh create/update/delete |
| Implementasi | Draf helper peran, view, template, relasi Star, dan routing | UUID Experience dan integer Project tetap sesuai model sebelumnya |
| Pengujian | Draf tes akses dan pembaruan fixture tes CRUD | Request langsung tetap ditolak meskipun melewati tombol di UI |
| API dan UI tambahan | Username pada JSON, detail, dan Favorit saya | Tidak menyerialisasi objek User lengkap; favorit tidak tertukar antar akun |
| Dokumentasi | Draf setup, matriks peran, dan panduan pengumpulan | Hasil tes paket dibedakan dari hasil pengujian lingkungan pengguna |

Keterbatasan bantuan AI adalah tidak dapat langsung memastikan kondisi seluruh berkas dan database pada laptop/PWS. Karena itu, penerapan migrasi, pemilihan akun Editor di Django Admin, percobaan browser, dan hasil tes lokal perlu diperiksa pada lingkungan proyek sendiri. Mempercayai tombol yang tersembunyi saja tidak cukup; penolakan request langsung dan perubahan jumlah data ikut diuji. Cookie tampilan `last_login` juga tidak dipakai untuk menentukan peran.

Penyesuaian terhadap kode sebelumnya meliputi pemisahan pemeriksaan akses, penggunaan UUID pada rute Experience, pembaruan tes CRUD agar berjalan sebagai pemilik, serta penggunaan nama relasi Star yang berbeda untuk Experience dan Project. Tidak ada klaim bahwa seluruh proyek diverifikasi hanya karena draf kode berhasil dibuat.

Referensi: instruksi Individual Assignment 4 yang dilampirkan, [autentikasi dan Groups Django](https://docs.djangoproject.com/en/6.1/topics/auth/default/), serta [serialisasi Django](https://docs.djangoproject.com/en/6.0/topics/serialization/).
