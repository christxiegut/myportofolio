from django.test import TestCase
from django.urls import reverse

from main.models import Project


class ProjectTests(TestCase):
    def setUp(self):
        self.url = reverse("main:show_projects")
        self.project = Project.objects.create(
            title="Portofolio Pengujian",
            description="Proyek untuk menguji halaman daftar proyek.",
            technologies="Python, Django",
            repository_url="https://example.com/portofolio",
        )

    def test_projects_url_uses_correct_template(self):
        """Halaman Projects dapat diakses dan memakai template yang sesuai."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_projects_page_displays_model_data(self):
        """Data proyek dan tautan repositori berasal dari basis data."""
        response = self.client.get(self.url)

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.technologies)
        self.assertContains(response, f'href="{self.project.repository_url}"')

    def test_empty_projects_page_displays_message(self):
        """Pengunjung mendapat pesan ketika belum ada proyek."""
        Project.objects.all().delete()

        response = self.client.get(self.url)

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_projects_page_displays_multiple_projects(self):
        """Daftar menampilkan lebih dari satu objek proyek."""
        another_project = Project.objects.create(
            title="Aplikasi Catatan Pengujian",
            description="Proyek kedua untuk memeriksa daftar dinamis.",
            technologies="Python, SQLite",
            repository_url="https://example.com/catatan",
        )

        response = self.client.get(self.url)

        self.assertContains(response, self.project.title)
        self.assertContains(response, another_project.title)

    def test_project_without_repository_hides_repository_link(self):
        """Proyek tetap tampil tanpa tombol repositori jika URL kosong."""
        self.project.repository_url = ""
        self.project.save(update_fields=["repository_url"])

        response = self.client.get(self.url)

        self.assertContains(response, self.project.title)
        self.assertNotContains(response, "Lihat repositori")

    def test_search_matches_each_field_case_insensitively(self):
        """Judul, deskripsi, atau teknologi dapat menjadi kata kunci."""
        unrelated_project = Project.objects.create(
            title="Situs Cuaca",
            description="Prakiraan suhu harian.",
            technologies="JavaScript",
        )

        for keyword in ("PORTOFOLIO", "DAFTAR", "django"):
            with self.subTest(keyword=keyword):
                response = self.client.get(self.url, {"q": keyword})

                self.assertContains(response, self.project.title)
                self.assertNotContains(response, unrelated_project.title)

    def test_search_without_matches_displays_specific_message(self):
        """Hasil pencarian kosong dibedakan dari daftar proyek kosong."""
        response = self.client.get(self.url, {"q": "zzztidakcocokzzz"})

        self.assertContains(
            response, "Tidak ada proyek yang cocok dengan pencarianmu."
        )
        self.assertNotContains(response, self.project.title)
        self.assertNotContains(response, "Belum ada proyek yang ditambahkan.")

    def test_search_ignores_surrounding_spaces(self):
        """Spasi di awal dan akhir kata kunci tidak menghilangkan hasil."""
        response = self.client.get(self.url, {"q": "  DJANGO  "})

        self.assertContains(response, self.project.title)
        self.assertEqual(response.context["query"], "DJANGO")

    def test_blank_search_displays_all_projects(self):
        """Kata kunci kosong atau hanya spasi menampilkan seluruh proyek."""
        another_project = Project.objects.create(
            title="Situs Cuaca",
            description="Prakiraan suhu harian.",
            technologies="JavaScript",
        )

        for keyword in ("", "   "):
            with self.subTest(keyword=keyword):
                response = self.client.get(self.url, {"q": keyword})

                self.assertContains(response, self.project.title)
                self.assertContains(response, another_project.title)
                self.assertEqual(response.context["query"], "")
