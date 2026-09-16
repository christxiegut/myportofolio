"""Pengujian form, data delivery, CSRF, dan penghapusan pada Tutorial 3."""

from xml.etree import ElementTree

from django.test import Client, TestCase
from django.urls import reverse

from main.models import Project


class Tutorial3Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portfolio = Project.objects.create(
            title="Portofolio Tutorial",
            description="Catatan pembelajaran dan karya pribadi.",
            technologies="Python, Django",
            repository_url="https://example.com/portfolio",
        )
        cls.other = Project.objects.create(
            title="Katalog Kegiatan",
            description="Daftar acara kampus.",
            technologies="HTML, CSS",
        )

    def project_payload(self, **changes):
        data = {
            "title": "Proyek dari Form",
            "description": "Proyek baru untuk mencoba formulir.",
            "technologies": "Python",
            "repository_url": "",
        }
        data.update(changes)
        return data

    def test_form_page_contains_four_fields_and_csrf(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertTemplateUsed(response, "base.html")
        for field in ("title", "description", "technologies", "repository_url"):
            self.assertContains(response, f'name="{field}"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_valid_post_creates_project_and_displays_success(self):
        response = self.client.post(
            reverse("main:create_project"),
            self.project_payload(),
            follow=True,
        )
        self.assertRedirects(response, reverse("main:show_projects"))
        created = Project.objects.get(title="Proyek dari Form")
        self.assertEqual(created.repository_url, "")
        self.assertEqual(created.technologies, "Python")
        self.assertContains(response, "Proyek baru berhasil ditambahkan!")
        self.assertContains(response, created.title)

    def test_empty_post_shows_errors_and_does_not_create_project(self):
        count = Project.objects.count()
        response = self.client.post(reverse("main:create_project"), {})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.is_bound)
        self.assertIn("title", form.errors)
        self.assertIn("description", form.errors)
        self.assertIn("technologies", form.errors)
        self.assertEqual(Project.objects.count(), count)

    def test_invalid_repository_url_is_rejected(self):
        count = Project.objects.count()
        response = self.client.post(
            reverse("main:create_project"),
            self.project_payload(repository_url="bukan url valid"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("repository_url", response.context["form"].errors)
        self.assertEqual(Project.objects.count(), count)

    def test_json_response_contains_saved_fields(self):
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"].split(";")[0], "application/json")
        objects = {row["pk"]: row for row in response.json()}
        self.assertEqual(set(objects), {self.portfolio.pk, self.other.pk})
        self.assertEqual(objects[self.portfolio.pk]["model"], "main.project")
        self.assertEqual(
            objects[self.portfolio.pk]["fields"]["technologies"], "Python, Django"
        )

    def test_json_title_filter_and_q_search(self):
        url = reverse("main:get_projects_json")
        for params in (
            {"title": "  PORTOFOLIO  "},
            {"q": "  DJANGO  "},
            {"q": "pembelajaran"},
        ):
            with self.subTest(params=params):
                response = self.client.get(url, params)
                self.assertEqual([row["pk"] for row in response.json()], [self.portfolio.pk])
        response = self.client.get(url, {"title": "tidak-ditemukan"})
        self.assertEqual(response.json(), [])

    def test_xml_response_and_title_filter(self):
        response = self.client.get(reverse("main:get_projects_xml"), {"title": "Portofolio"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"].split(";")[0], "application/xml")
        root = ElementTree.fromstring(response.content)
        self.assertEqual(root.tag, "django-objects")
        objects = root.findall("object")
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].attrib["pk"], str(self.portfolio.pk))
        self.assertEqual(objects[0].find("field[@name='title']").text, self.portfolio.title)

    def test_search_page_keeps_detail_link_and_delete_confirmation(self):
        response = self.client.get(reverse("main:show_projects"), {"q": "  DJANGO  "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["query"], "DJANGO")
        self.assertContains(response, self.portfolio.title)
        self.assertNotContains(response, self.other.title)
        self.assertContains(response, reverse("main:show_project_detail", args=[self.portfolio.pk]))
        self.assertContains(response, reverse("main:delete_project", args=[self.portfolio.pk]))
        self.assertContains(response, f'popovertarget="delete-project-{self.portfolio.pk}"')

    def test_get_cannot_delete_a_project(self):
        response = self.client.get(reverse("main:delete_project", args=[self.portfolio.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Project.objects.filter(pk=self.portfolio.pk).exists())

    def test_post_deletes_only_selected_project(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.portfolio.pk]), follow=True
        )
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.portfolio.pk).exists())
        self.assertTrue(Project.objects.filter(pk=self.other.pk).exists())
        self.assertContains(response, "Proyek berhasil dihapus!")

    def test_deleting_missing_project_returns_404(self):
        pk = self.portfolio.pk
        self.portfolio.delete()
        response = self.client.post(reverse("main:delete_project", args=[pk]))
        self.assertEqual(response.status_code, 404)

    def test_csrf_rejects_create_and_delete_without_token(self):
        client = Client(enforce_csrf_checks=True)
        count = Project.objects.count()
        create_response = client.post(reverse("main:create_project"), self.project_payload())
        delete_response = client.post(reverse("main:delete_project", args=[self.portfolio.pk]))
        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(Project.objects.count(), count)

    def test_csrf_token_from_form_allows_create_and_delete(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("main:create_project"))
        token = client.cookies["csrftoken"].value
        response = client.post(
            reverse("main:create_project"),
            {**self.project_payload(), "csrfmiddlewaretoken": token},
        )
        self.assertEqual(response.status_code, 302)
        created = Project.objects.get(title="Proyek dari Form")
        response = client.post(
            reverse("main:delete_project", args=[created.pk]),
            {"csrfmiddlewaretoken": token},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=created.pk).exists())
