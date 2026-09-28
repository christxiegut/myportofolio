"""Uji autentikasi, cookie, izin, CSRF, dan star dengan database tes Django."""

import secrets

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from main.models import Project


User = get_user_model()


class Tutorial4Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = secrets.token_urlsafe(24)
        cls.visitor = User.objects.create_user("pengunjung_uji", password=cls.password)
        cls.other = User.objects.create_user("teman_uji", password=None)
        cls.owner = User.objects.create_superuser(
            "pemilik_uji", "owner@example.com", password=None
        )
        cls.project = Project.objects.create(
            title="Proyek Autentikasi", description="Latihan sesi dan izin.",
            technologies="Python, Django",
        )

    def payload(self):
        return {
            "title": "Proyek Baru", "description": "Deskripsi proyek.",
            "technologies": "Django", "repository_url": "",
        }

    def star_url(self):
        return reverse("main:toggle_star", args=[self.project.pk])

    def login(self, client=None):
        return (client or self.client).post(reverse("main:login"), {
            "username": self.visitor.username, "password": self.password,
        })

    def test_read_only_portfolio_pages_and_api_remain_public(self):
        for name in ("show_main", "show_experience", "show_projects", "get_projects_json", "get_projects_xml"):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f"main:{name}")).status_code, 200)
        self.assertEqual(self.client.get(reverse("main:show_project_detail", args=[self.project.pk])).status_code, 200)

    def test_auth_forms_use_base_template_and_csrf(self):
        for name, fields in (("register", ("username", "password1", "password2")), ("login", ("username", "password"))):
            with self.subTest(name=name):
                response = self.client.get(reverse(f"main:{name}"))
                self.assertTemplateUsed(response, "base.html")
                self.assertContains(response, 'name="csrfmiddlewaretoken"')
                for field in fields:
                    self.assertContains(response, f'name="{field}"')

    def test_register_hashes_password_without_granting_owner_or_logging_in(self):
        password = secrets.token_urlsafe(24)
        response = self.client.post(reverse("main:register"), {
            "username": "akun_baru", "password1": password, "password2": password,
            "is_superuser": "True", "is_staff": "True",
        }, follow=True)
        self.assertRedirects(response, reverse("main:login"))
        account = User.objects.get(username="akun_baru")
        self.assertTrue(account.check_password(password))
        self.assertNotEqual(account.password, password)
        self.assertFalse(account.is_superuser)
        self.assertFalse(account.is_staff)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Akun berhasil dibuat. Silakan login.", count=1)

    def test_register_rejects_mismatched_duplicate_and_empty_inputs(self):
        count = User.objects.count()
        cases = [
            ({}, "username"),
            ({"username": "baru", "password1": self.password, "password2": "berbeda"}, "password2"),
            ({"username": self.visitor.username, "password1": self.password, "password2": self.password}, "username"),
        ]
        for payload, error_field in cases:
            with self.subTest(error_field=error_field, payload_keys=list(payload)):
                response = self.client.post(reverse("main:register"), payload)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].is_bound)
                self.assertIn(error_field, response.context["form"].errors)
                self.assertEqual(User.objects.count(), count)

    def test_invalid_login_has_errors_and_does_not_open_session(self):
        response = self.client.post(reverse("main:login"), {
            "username": self.visitor.username, "password": "salah",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertNotIn("last_login", response.cookies)

    def test_empty_login_has_required_field_errors(self):
        response = self.client.post(reverse("main:login"), {})
        self.assertTrue(response.context["form"].is_bound)
        self.assertIn("username", response.context["form"].errors)
        self.assertIn("password", response.context["form"].errors)

    def test_login_sets_session_cookie_and_displays_timestamp(self):
        response = self.login()
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(self.client.session["_auth_user_id"], str(self.visitor.pk))
        cookie = response.cookies["last_login"]
        self.assertRegex(cookie.value, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        profile = self.client.get(reverse("main:show_main"))
        self.assertEqual(profile.context["last_login"], cookie.value)
        self.assertContains(profile, cookie.value)
        for name in ("show_experience", "show_projects"):
            page = self.client.get(reverse(f"main:{name}"))
            self.assertContains(page, f'<span class="nav-user">{self.visitor.username}</span>', html=True)

    def test_missing_cookie_has_fallback_and_cookie_cannot_grant_access(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.context["last_login"], "Belum ada sesi login")
        self.client.cookies["last_login"] = "<script>alert(1)</script>"
        self.client.cookies["is_superuser"] = "True"
        response = self.client.get(reverse("main:show_main"))
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        denied = self.client.get(reverse("main:create_project"))
        self.assertEqual(denied.status_code, 302)
        self.assertTrue(denied.url.startswith(reverse("main:login")))

    def test_login_redirects_to_profile_even_with_external_next(self):
        response = self.client.post(reverse("main:login") + "?next=https://example.org/", {
            "username": self.visitor.username, "password": self.password,
        })
        self.assertRedirects(response, reverse("main:show_main"))

    def test_logout_clears_session_and_expires_last_login_cookie(self):
        self.login()
        response = self.client.post(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"]["max-age"], 0)
        self.assertTrue(User.objects.filter(pk=self.visitor.pk).exists())

    def test_get_logout_does_not_change_session(self):
        self.login()
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

    def test_anonymous_write_requests_redirect_without_changing_data(self):
        count = Project.objects.count()
        endpoints = [
            (reverse("main:create_project"), self.payload()),
            (reverse("main:delete_project", args=[self.project.pk]), {}),
            (self.star_url(), {}),
        ]
        for url, payload in endpoints:
            with self.subTest(url=url):
                response = self.client.post(url, payload)
                self.assertRedirects(response, reverse("main:login") + "?next=" + url)
        self.assertEqual(Project.objects.count(), count)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_logged_in_regular_user_cannot_create_or_delete(self):
        self.client.force_login(self.visitor)
        count = Project.objects.count()
        url = reverse("main:create_project")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.post(url, self.payload()).status_code, 403)
        deletion = self.client.post(reverse("main:delete_project", args=[self.project.pk]))
        self.assertEqual(deletion.status_code, 403)
        self.assertEqual(Project.objects.count(), count)

    def test_staff_without_superuser_status_cannot_edit_portfolio(self):
        self.visitor.is_staff = True
        self.visitor.save(update_fields=["is_staff"])
        self.client.force_login(self.visitor)
        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 403)

    def test_mutation_controls_are_visible_only_to_owner(self):
        for account, visible in ((None, False), (self.visitor, False), (self.owner, True)):
            with self.subTest(account=getattr(account, "username", "anonymous")):
                self.client.logout()
                if account:
                    self.client.force_login(account)
                response = self.client.get(reverse("main:show_projects"))
                assertion = self.assertContains if visible else self.assertNotContains
                assertion(response, reverse("main:create_project"))
                assertion(response, reverse("main:delete_project", args=[self.project.pk]))
                self.assertContains(response, self.star_url())
                self.assertContains(response, reverse("main:show_project_detail", args=[self.project.pk]))

    def test_registered_users_can_star_independently_and_unstar_their_own_vote(self):
        self.client.force_login(self.visitor)
        self.assertRedirects(self.client.post(self.star_url()), reverse("main:show_projects"))
        self.assertEqual(self.project.starred_by.count(), 1)
        second_client = Client()
        second_client.force_login(self.other)
        second_client.post(self.star_url())
        self.assertEqual(self.project.starred_by.count(), 2)
        self.client.post(self.star_url())
        self.assertEqual(list(self.project.starred_by.values_list("pk", flat=True)), [self.other.pk])

    def test_owner_can_also_give_star(self):
        self.client.force_login(self.owner)
        self.client.post(self.star_url())
        self.assertTrue(self.project.starred_by.filter(pk=self.owner.pk).exists())

    def test_star_get_does_not_mutate_and_unknown_project_is_404(self):
        self.client.force_login(self.visitor)
        self.assertEqual(self.client.get(self.star_url()).status_code, 405)
        self.assertEqual(self.project.starred_by.count(), 0)
        self.assertEqual(self.client.post(reverse("main:toggle_star", args=[self.project.pk + 999])).status_code, 404)

    def test_json_uses_usernames_and_does_not_serialize_user_secrets(self):
        self.project.starred_by.add(self.visitor, self.other)
        response = self.client.get(reverse("main:get_projects_json"))
        fields = next(row["fields"] for row in response.json() if row["pk"] == self.project.pk)
        self.assertCountEqual(fields["starred_by"], [[self.visitor.username], [self.other.username]])
        self.assertNotIn("password", fields)
        self.assertNotIn("email", fields)
        self.assertNotContains(response, self.visitor.password)

    def test_html_keeps_star_state_after_json_deserialization(self):
        self.project.starred_by.add(self.visitor)
        self.client.force_login(self.visitor)
        count = Project.objects.count()
        response = self.client.get(reverse("main:show_projects"), {"q": "DJANGO"})
        self.assertEqual(len(response.context["project_list"]), 1)
        self.assertContains(response, "Unstar")
        self.assertContains(response, 'aria-pressed="true"')
        self.assertContains(response, '<span class="star-count">1</span>', html=True)
        self.assertContains(response, f"Dibintangi oleh {self.visitor.username}")
        self.assertEqual(Project.objects.count(), count)
        self.assertEqual(self.project.starred_by.count(), 1)

    def test_csrf_is_required_for_register_login_logout_and_star(self):
        client = Client(enforce_csrf_checks=True)
        for route in ("register", "login"):
            self.assertEqual(client.post(reverse(f"main:{route}"), {}).status_code, 403)
        client.force_login(self.visitor)
        self.assertEqual(client.post(reverse("main:logout")).status_code, 403)
        self.assertEqual(client.post(self.star_url()).status_code, 403)
        self.assertIn("_auth_user_id", client.session)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_real_csrf_login_star_logout_flow(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("main:login"))
        response = client.post(reverse("main:login"), {
            "username": self.visitor.username, "password": self.password,
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        })
        self.assertRedirects(response, reverse("main:show_main"))
        client.get(reverse("main:show_projects"))
        # Login merotasi token; ambil cookie yang sekarang, bukan token sebelumnya.
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.star_url(), {"csrfmiddlewaretoken": token}).status_code, 302)
        self.assertTrue(self.project.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertEqual(client.post(reverse("main:logout"), {"csrfmiddlewaretoken": token}).status_code, 302)
        self.assertNotIn("_auth_user_id", client.session)
