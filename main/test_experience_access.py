"""Matriks empat peran, Star Experience, integritas JSON, dan CSRF Tugas 4."""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse

from main.models import Experience, Project


User = get_user_model()


class ExperienceAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("task4_owner", "owner@example.com", password=None)
        cls.editor = User.objects.create_user("task4_editor", password=None)
        cls.reader = User.objects.create_user("task4_reader", password=None)
        cls.other = User.objects.create_user("task4_other", password=None)
        cls.group = Group.objects.create(name="Editor")
        cls.editor.groups.add(cls.group)
        cls.experience = Experience.objects.create(
            title="Panitia Kampus", description="Mengelola dokumentasi acara.", category="volunteer"
        )
        cls.other_experience = Experience.objects.create(
            title="Asisten Riset", description="Mengolah data penelitian.", category="research"
        )

    def client_for(self, user=None, *, csrf=False):
        client = Client(enforce_csrf_checks=csrf)
        if user:
            client.force_login(user)
        return client

    def url(self, action, pk=None):
        return reverse(f"main:{action}", args=[pk or self.experience.pk])

    def payload(self, **changes):
        data = {"title": "Judul Baru", "description": "Deskripsi Baru", "category": "volunteer", "thumbnail": "", "ended_at": ""}
        data.update(changes)
        return data

    def test_list_detail_and_json_are_public_for_all_four_roles(self):
        for account in (None, self.reader, self.editor, self.owner):
            client = self.client_for(account)
            for url in (reverse("main:show_experience"), self.url("show_experience_detail"), reverse("main:get_experiences_json")):
                with self.subTest(user=getattr(account, "username", "anonymous"), url=url):
                    self.assertEqual(client.get(url).status_code, 200)

    def test_get_create_and_edit_follow_role_matrix(self):
        for account, create_status, edit_status in ((None, 302, 302), (self.reader, 403, 403), (self.editor, 403, 200), (self.owner, 200, 200)):
            with self.subTest(user=getattr(account, "username", "anonymous")):
                client = self.client_for(account)
                self.assertEqual(client.get(reverse("main:create_experience")).status_code, create_status)
                self.assertEqual(client.get(self.url("update_experience")).status_code, edit_status)

    def test_post_create_only_succeeds_for_owner(self):
        for account, expected in ((None, 302), (self.reader, 403), (self.editor, 403), (self.owner, 302)):
            with self.subTest(user=getattr(account, "username", "anonymous")):
                before = Experience.objects.count()
                response = self.client_for(account).post(reverse("main:create_experience"), self.payload())
                self.assertEqual(response.status_code, expected)
                self.assertEqual(Experience.objects.count(), before + int(account == self.owner))

    def test_post_update_succeeds_for_editor_and_owner_only(self):
        for account, expected, allowed in ((None, 302, False), (self.reader, 403, False), (self.editor, 302, True), (self.owner, 302, True)):
            with self.subTest(user=getattr(account, "username", "anonymous")):
                self.experience.refresh_from_db()
                old_title = self.experience.title
                new_title = f"Edit {getattr(account, 'username', 'anonymous')}"
                response = self.client_for(account).post(self.url("update_experience"), self.payload(title=new_title))
                self.assertEqual(response.status_code, expected)
                self.experience.refresh_from_db()
                self.assertEqual(self.experience.title, new_title if allowed else old_title)
                self.assertEqual(Experience.objects.count(), 2)

    def test_post_delete_only_succeeds_for_owner(self):
        for account, expected in ((None, 302), (self.reader, 403), (self.editor, 403), (self.owner, 302)):
            with self.subTest(user=getattr(account, "username", "anonymous")):
                response = self.client_for(account).post(self.url("delete_experience"))
                self.assertEqual(response.status_code, expected)
                self.assertEqual(Experience.objects.filter(pk=self.experience.pk).exists(), account != self.owner)
                self.assertTrue(Experience.objects.filter(pk=self.other_experience.pk).exists())

    def test_anonymous_writes_redirect_to_login_with_next(self):
        client = self.client_for()
        for url in (reverse("main:create_experience"), self.url("update_experience"), self.url("delete_experience"), self.url("toggle_experience_star")):
            with self.subTest(url=url):
                response = client.post(url, self.payload())
                self.assertRedirects(response, reverse("main:login") + "?next=" + url)

    def test_controls_in_list_and_detail_follow_roles(self):
        for account, edit_allowed, manage_allowed in ((None, False, False), (self.reader, False, False), (self.editor, True, False), (self.owner, True, True)):
            client = self.client_for(account)
            for url in (reverse("main:show_experience"), self.url("show_experience_detail")):
                with self.subTest(user=getattr(account, "username", "anonymous"), url=url):
                    response = client.get(url)
                    (self.assertContains if edit_allowed else self.assertNotContains)(response, self.url("update_experience"))
                    (self.assertContains if manage_allowed else self.assertNotContains)(response, self.url("delete_experience"))
                    self.assertContains(response, self.url("toggle_experience_star"))
                    self.assertEqual(response.context["is_editor"], account == self.editor)
            listing = client.get(reverse("main:show_experience"))
            (self.assertContains if manage_allowed else self.assertNotContains)(listing, reverse("main:create_experience"))

    def test_empty_list_does_not_offer_add_to_unauthorized_users(self):
        Experience.objects.all().delete()
        for account in (None, self.reader, self.editor):
            page = self.client_for(account).get(reverse("main:show_experience"))
            self.assertContains(page, "Belum ada pengalaman yang ditambahkan.")
            self.assertNotContains(page, reverse("main:create_experience"))

    def test_group_removal_revokes_edit_right_without_relogin(self):
        client = self.client_for(self.editor)
        self.assertEqual(client.get(self.url("update_experience")).status_code, 200)
        self.editor.groups.remove(self.group)
        self.assertEqual(client.post(self.url("update_experience"), self.payload()).status_code, 403)
        self.assertFalse(client.get(reverse("main:show_experience")).context["is_editor"])

    def test_staff_status_or_forged_cookie_cannot_grant_editor_right(self):
        self.reader.is_staff = True
        self.reader.save(update_fields=["is_staff"])
        client = self.client_for(self.reader)
        client.cookies["is_editor"] = "True"
        client.cookies["role"] = "Editor"
        response = client.post(self.url("update_experience"), self.payload(is_editor="True", groups="Editor"))
        self.assertEqual(response.status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Panitia Kampus")

    def test_editor_cannot_modify_identity_or_stars_through_edit_form(self):
        self.experience.starred_by.add(self.reader)
        old_started_at = self.experience.started_at
        response = self.client_for(self.editor).post(self.url("update_experience"), self.payload(
            id=str(uuid.uuid4()), started_at="2000-01-01", starred_by=[self.editor.pk]
        ))
        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.started_at, old_started_at)
        self.assertEqual(list(self.experience.starred_by.values_list("pk", flat=True)), [self.reader.pk])
        self.assertEqual(Experience.objects.count(), 2)

    def test_every_authenticated_role_can_toggle_own_star(self):
        for account in (self.reader, self.editor, self.owner):
            with self.subTest(user=account.username):
                client = self.client_for(account)
                url = self.url("toggle_experience_star")
                self.assertRedirects(client.post(url), reverse("main:show_experience"))
                self.assertTrue(self.experience.starred_by.filter(pk=account.pk).exists())
                client.post(url)
                self.assertFalse(self.experience.starred_by.filter(pk=account.pk).exists())

    def test_unstar_does_not_remove_another_users_star(self):
        self.experience.starred_by.add(self.reader, self.other)
        self.client_for(self.reader).post(self.url("toggle_experience_star"), {"user_id": self.other.pk})
        self.assertEqual(list(self.experience.starred_by.values_list("pk", flat=True)), [self.other.pk])

    def test_one_relation_per_user_and_separate_relations_for_projects(self):
        self.experience.starred_by.add(self.reader)
        self.experience.starred_by.add(self.reader)
        self.assertEqual(self.experience.starred_by.count(), 1)
        self.assertEqual(list(self.reader.starred_experiences.all()), [self.experience])
        project = Project.objects.create(title="Project", description="Test", technologies="Django")
        project.starred_by.add(self.reader)
        self.client_for(self.reader).post(self.url("toggle_experience_star"))
        self.assertTrue(project.starred_by.filter(pk=self.reader.pk).exists())

    def test_get_star_and_delete_do_not_change_data(self):
        client = self.client_for(self.owner)
        self.assertEqual(client.get(self.url("toggle_experience_star")).status_code, 405)
        self.assertEqual(client.get(self.url("delete_experience")).status_code, 405)
        self.assertEqual(self.experience.starred_by.count(), 0)
        self.assertEqual(Experience.objects.count(), 2)

    def test_nonexistent_ids_return_404_for_allowed_roles(self):
        missing = uuid.uuid4()
        self.assertEqual(self.client_for().get(self.url("show_experience_detail", missing)).status_code, 404)
        self.assertEqual(self.client_for(self.editor).post(self.url("update_experience", missing), self.payload()).status_code, 404)
        self.assertEqual(self.client_for(self.reader).post(self.url("toggle_experience_star", missing)).status_code, 404)
        self.assertEqual(self.client_for(self.owner).post(self.url("delete_experience", missing)).status_code, 404)

    def test_json_uses_usernames_and_explicit_public_fields(self):
        self.experience.starred_by.add(self.reader, self.editor)
        response = self.client_for().get(reverse("main:get_experiences_json"))
        self.assertEqual(response["Content-Type"], "application/json")
        record = next(item for item in response.json() if item["pk"] == str(self.experience.pk))
        fields = record["fields"]
        self.assertEqual(set(fields), {"title", "description", "category", "thumbnail", "started_at", "ended_at", "starred_by"})
        self.assertCountEqual(fields["starred_by"], [[self.reader.username], [self.editor.username]])
        for secret in (self.reader.password, self.owner.email, "sessionid", "is_superuser"):
            self.assertNotContains(response, secret)

    def test_json_does_not_accept_post(self):
        self.assertEqual(self.client_for(self.owner).post(reverse("main:get_experiences_json")).status_code, 405)

    def test_star_state_count_and_usernames_survive_list_deserialization(self):
        self.experience.starred_by.add(self.reader)
        page = self.client_for(self.reader).get(reverse("main:show_experience"), {"q": "Panitia"})
        self.assertContains(page, "Unstar")
        self.assertContains(page, 'aria-pressed="true"')
        self.assertContains(page, '<span class="star-count">1</span>', html=True)
        self.assertContains(page, f"Dibintangi oleh {self.reader.username}")
        self.assertEqual(Experience.objects.count(), 2)

    def test_favorites_filter_is_per_user_and_agrees_in_html_and_json(self):
        self.experience.starred_by.add(self.reader)
        self.other_experience.starred_by.add(self.other)
        for account, wanted in ((self.reader, self.experience), (self.other, self.other_experience)):
            client = self.client_for(account)
            response = client.get(reverse("main:get_experiences_json"), {"starred": "1"})
            page = client.get(reverse("main:show_experience"), {"starred": "1"})
            self.assertEqual([item["pk"] for item in response.json()], [str(wanted.pk)])
            self.assertEqual([item.pk for item in page.context["experience_list"]], [wanted.pk])
            self.assertContains(page, 'name="starred" value="1" checked')
        self.assertEqual(self.client_for().get(reverse("main:get_experiences_json"), {"starred": "1"}).json(), [])

    def test_favorites_combine_with_search_and_category(self):
        self.experience.starred_by.add(self.reader)
        self.other_experience.starred_by.add(self.reader)
        response = self.client_for(self.reader).get(reverse("main:get_experiences_json"), {"starred": "1", "q": "data", "category": "research"})
        self.assertEqual([item["pk"] for item in response.json()], [str(self.other_experience.pk)])

    def test_star_keeps_local_filter_or_detail_location(self):
        client = self.client_for(self.reader)
        for target in (reverse("main:show_experience") + "?q=Panitia&starred=1", self.url("show_experience_detail")):
            response = client.post(self.url("toggle_experience_star"), {"next": target})
            self.assertRedirects(response, target)

    def test_star_rejects_external_redirect_destinations(self):
        client = self.client_for(self.reader)
        for target in ("https://example.org/", "//example.org/", "\\\\example.org/", "javascript:alert(1)"):
            with self.subTest(target=target):
                self.assertRedirects(client.post(self.url("toggle_experience_star"), {"next": target}), reverse("main:show_experience"))

    def test_csrf_missing_token_blocks_star_and_editor_update(self):
        client = self.client_for(self.editor, csrf=True)
        self.assertEqual(client.post(self.url("toggle_experience_star")).status_code, 403)
        self.assertEqual(client.post(self.url("update_experience"), self.payload()).status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Panitia Kampus")
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_valid_csrf_allows_editor_update_and_star_but_not_delete(self):
        client = self.client_for(self.editor, csrf=True)
        client.get(self.url("update_experience"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.url("update_experience"), self.payload(csrfmiddlewaretoken=token)).status_code, 302)
        self.assertEqual(client.post(self.url("toggle_experience_star"), {"csrfmiddlewaretoken": token}).status_code, 302)
        self.assertEqual(client.post(self.url("delete_experience"), {"csrfmiddlewaretoken": token}).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_detail_escapes_user_content_and_uses_shared_template(self):
        self.experience.title = '<script>alert("test")</script>'
        self.experience.save(update_fields=["title"])
        response = self.client_for().get(self.url("show_experience_detail"))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "experience_detail.html")
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, '<script>alert("test")</script>')
