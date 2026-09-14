from django.test import TestCase
from django.urls import reverse

from main.models import Project


class ProjectDetailTests(TestCase):
    def setUp(self):
        self.first_project = Project.objects.create(
            title="Catatan Belajar",
            description="Aplikasi untuk menyimpan catatan.",
            technologies="HTML, CSS",
        )
        self.second_project = Project.objects.create(
            title="Dashboard Cuaca",
            description="Menampilkan informasi cuaca berdasarkan lokasi.",
            technologies="Python, Django",
            repository_url="https://example.com/cuaca",
        )

    def test_detail_displays_selected_project(self):
        """Halaman menampilkan proyek sesuai ID yang diminta."""
        url = reverse(
            "main:show_project_detail",
            args=[self.second_project.pk],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")
        self.assertContains(response, self.second_project.title)
        self.assertContains(response, self.second_project.description)
        self.assertContains(response, self.second_project.technologies)
        self.assertNotContains(response, self.first_project.title)
        self.assertContains(
            response,
            f'href="{self.second_project.repository_url}"',
        )

    def test_missing_project_returns_404(self):
        """Proyek yang sudah tidak ada menghasilkan status 404."""
        url = reverse(
            "main:show_project_detail",
            args=[self.first_project.pk],
        )
        self.first_project.delete()

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_cards_link_to_each_project_detail(self):
        """Setiap kartu memiliki tautan menuju detailnya sendiri."""
        response = self.client.get(reverse("main:show_projects"))

        for project in (self.first_project, self.second_project):
            detail_url = reverse(
                "main:show_project_detail",
                args=[project.pk],
            )
            self.assertContains(response, f'href="{detail_url}"')