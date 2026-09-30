"""Uji kontrak AJAX, validasi, otorisasi, dan CSRF Tutorial 5."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from main.forms import ExperienceForm, ProjectForm
from main.models import Project


class Tutorial5Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner = User.objects.create_superuser("owner_ajax", "owner@example.com", password=None)
        cls.visitor = User.objects.create_user("visitor_ajax", password=None)
        cls.other = User.objects.create_user("other_ajax", password=None)
        cls.project = Project.objects.create(
            title="Portofolio", description="Cerita proses belajar.",
            technologies="Django, Python", repository_url="https://example.com/repo",
        )

    def payload(self, **changes):
        data = {"title": "Proyek AJAX", "description": "Deskripsi", "technologies": "Python", "repository_url": ""}
        data.update(changes)
        return data

    def test_projects_shell_is_public_and_has_no_server_project_list(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertNotIn("project_list", response.context)
        for element in ("projects-app", "grid", "loading", "error", "empty", "project-search-form"):
            self.assertContains(response, f'id="{element}"')
        self.assertContains(response, "/static/js/projects.js")
        self.assertContains(response, "/static/js/toast.js", count=1)
        self.assertIn("csrftoken", response.cookies)

    def test_only_owner_receives_modal_and_form(self):
        for account, visible in ((None, False), (self.visitor, False), (self.owner, True)):
            self.client.logout()
            if account:
                self.client.force_login(account)
            response = self.client.get(reverse("main:show_projects"))
            assertion = self.assertContains if visible else self.assertNotContains
            assertion(response, 'id="add-project-modal"')
            if visible:
                for field in ("title", "description", "technologies", "repository_url"):
                    self.assertContains(response, f'name="{field}"')

    def test_ajax_get_is_not_allowed_and_does_not_create(self):
        self.client.force_login(self.owner)
        count = Project.objects.count()
        response = self.client.get(reverse("main:create_project_ajax"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Project.objects.count(), count)

    def test_anonymous_ajax_post_is_json_403_without_redirect(self):
        response = self.client.post(reverse("main:create_project_ajax"), self.payload())
        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json())
        self.assertNotIn("Location", response)
        self.assertFalse(Project.objects.filter(title="Proyek AJAX").exists())

    def test_regular_and_staff_accounts_cannot_create_via_ajax(self):
        self.client.force_login(self.visitor)
        for staff in (False, True):
            self.visitor.is_staff = staff
            self.visitor.save(update_fields=["is_staff"])
            response = self.client.post(reverse("main:create_project_ajax"), self.payload(is_superuser="true"))
            self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Proyek AJAX").exists())

    def test_owner_creates_project_with_201_and_gets_it_from_api(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_project_ajax"), self.payload())
        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(pk=response.json()["pk"])
        self.assertEqual(project.title, "Proyek AJAX")
        self.assertEqual(project.repository_url, "")
        data = self.client.get(reverse("main:get_projects_json"), {"q": "Proyek AJAX"}).json()
        self.assertEqual([row["pk"] for row in data], [project.pk])

    def test_empty_fields_produce_json_errors_without_saving(self):
        self.client.force_login(self.owner)
        before = Project.objects.count()
        response = self.client.post(reverse("main:create_project_ajax"), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()["errors"]), {"title", "description", "technologies"})
        self.assertEqual(Project.objects.count(), before)

    def test_html_is_stripped_but_nonempty_text_is_saved(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_project_ajax"), self.payload(
            title="Halo <b>dunia</b>", description="<p>Deskripsi</p>", technologies="<b>Python</b>",
        ))
        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(pk=response.json()["pk"])
        self.assertEqual((project.title, project.description, project.technologies), ("Halo dunia", "Deskripsi", "Python"))

    def test_tag_only_or_whitespace_text_is_rejected(self):
        self.client.force_login(self.owner)
        for field in ("title", "description", "technologies"):
            for value in ('<img src="x" onerror="alert(1)">', "   "):
                with self.subTest(field=field, value=value):
                    response = self.client.post(reverse("main:create_project_ajax"), self.payload(**{field: value}))
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.json()["errors"])

    def test_invalid_or_executable_repository_urls_are_rejected(self):
        self.client.force_login(self.owner)
        for value in ("bukan-url", "javascript:alert(1)", "data:text/html,test", "ftp://example.com/file"):
            response = self.client.post(reverse("main:create_project_ajax"), self.payload(repository_url=value))
            self.assertEqual(response.status_code, 400)
            self.assertIn("repository_url", response.json()["errors"])

    def test_legacy_form_also_uses_cleaning_and_validation(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_project"), self.payload(title="<b></b>"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)

    def test_extra_post_fields_cannot_assign_stars_or_overwrite_id(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_project_ajax"), self.payload(
            id=self.project.pk, starred_by=[self.visitor.pk],
        ))
        self.assertEqual(response.status_code, 201)
        created = Project.objects.get(pk=response.json()["pk"])
        self.assertNotEqual(created.pk, self.project.pk)
        self.assertEqual(created.starred_by.count(), 0)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portofolio")

    def test_missing_csrf_fails_and_header_token_succeeds(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        url = reverse("main:create_project_ajax")
        self.assertEqual(client.post(url, self.payload()).status_code, 403)
        client.get(reverse("main:show_projects"))
        token = client.cookies["csrftoken"].value
        response = client.post(url, self.payload(), HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)

    def test_star_metadata_follows_request_user(self):
        self.project.starred_by.add(self.visitor)
        for account, starred in ((None, False), (self.visitor, True), (self.other, False)):
            self.client.logout()
            if account:
                self.client.force_login(account)
            response = self.client.get(reverse("main:get_projects_json"))
            fields = response.json()[0]["fields"]
            self.assertEqual(fields["star_count"], 1)
            self.assertEqual(fields["is_starred"], starred)
            self.assertEqual(fields["starred_by_names"], self.visitor.username)
            self.assertNotIn("password", fields)
            self.assertNotIn("email", fields)
            self.assertIn("no-store", response["Cache-Control"])

    def test_q_and_title_search_with_empty_results(self):
        url = reverse("main:get_projects_json")
        for query in ({"q": "PYTHON"}, {"q": "cerita"}, {"title": "porto"}):
            self.assertEqual(len(self.client.get(url, query).json()), 1)
        self.assertEqual(self.client.get(url, {"q": "tidak cocok"}).json(), [])

    def test_project_form_keeps_experience_fields_and_search_is_escaped(self):
        self.assertEqual(list(ExperienceForm().fields), ["title", "description", "category", "thumbnail", "ended_at"])
        self.assertNotIn("starred_by", ProjectForm().fields)
        query = '"><img src=x onerror=alert(1)>'
        response = self.client.get(reverse("main:show_projects"), {"q": query})
        self.assertNotContains(response, query)
        self.assertContains(response, "&lt;img")
