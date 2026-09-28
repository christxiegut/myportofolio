"""Uji perilaku CRUD, JSON, filter, dan perlindungan CSRF Experience."""

import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import serializers
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience


class ExperienceCRUDTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_superuser(
            username="experience_owner", email="owner@example.com", password=None
        )
        cls.ongoing = Experience.objects.create(
            title="Staff Dana dan Usaha",
            description="Mencari vendor dan menyiapkan promosi.",
            category="volunteer",
        )
        cls.completed = Experience.objects.create(
            title="Asisten Penelitian",
            description="Mengolah data survei kampus.",
            category="research",
            ended_at=timezone.now(),
        )

    def setUp(self):
        # Tugas 4: operasi CRUD yang valid diuji sebagai pemilik.
        self.client.force_login(self.owner)

    def payload(self, **overrides):
        data = {
            "title": "Panitia Dokumentasi",
            "description": "Mendokumentasikan kegiatan kampus.",
            "category": "volunteer",
            "thumbnail": "",
            "ended_at": "",
        }
        data.update(overrides)
        return data

    def edit_url(self, pk=None):
        return reverse("main:update_experience", args=[pk or self.ongoing.pk])

    def delete_url(self, pk=None):
        return reverse("main:delete_experience", args=[pk or self.ongoing.pk])

    def test_create_get_renders_shared_template_and_csrf_without_writing(self):
        response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertEqual(Experience.objects.count(), 2)

    def test_create_valid_data_and_show_success_message(self):
        response = self.client.post(
            reverse("main:create_experience"), self.payload(), follow=True
        )
        self.assertRedirects(response, reverse("main:show_experience"))
        created = Experience.objects.get(title="Panitia Dokumentasi")
        self.assertTrue(created.is_ongoing)
        self.assertEqual(created.description, self.payload()["description"])
        self.assertContains(response, "Pengalaman berhasil ditambahkan!")

    def test_empty_form_returns_field_errors_without_saving(self):
        response = self.client.post(reverse("main:create_experience"), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.assertIn("description", response.context["form"].errors)
        self.assertEqual(Experience.objects.count(), 2)

    def test_invalid_category_image_and_datetime_are_rejected(self):
        for field, value in (
            ("category", "kategori-tidak-terdaftar"),
            ("thumbnail", "bukan-sebuah-url"),
            ("ended_at", "bukan-tanggal"),
        ):
            with self.subTest(field=field):
                response = self.client.post(
                    reverse("main:create_experience"), self.payload(**{field: value})
                )
                self.assertIn(field, response.context["form"].errors)
        self.assertEqual(Experience.objects.count(), 2)

    def test_invalid_form_keeps_the_input_for_correction(self):
        response = self.client.post(
            reverse("main:create_experience"), self.payload(thumbnail="tidak-valid")
        )
        self.assertEqual(response.context["form"]["title"].value(), "Panitia Dokumentasi")
        self.assertContains(response, "Perubahan belum disimpan.")

    def test_edit_get_prefills_existing_data(self):
        response = self.client.get(self.edit_url())
        self.assertContains(response, "Staff Dana dan Usaha")
        self.assertEqual(response.context["form"].instance.pk, self.ongoing.pk)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertTemplateUsed(response, "base.html")

    def test_update_changes_same_uuid_without_creating_duplicate(self):
        original_started_at = self.ongoing.started_at
        response = self.client.post(
            self.edit_url(), self.payload(title="Koordinator Dana dan Usaha"), follow=True
        )
        self.assertRedirects(response, reverse("main:show_experience"))
        self.ongoing.refresh_from_db()
        self.assertEqual(self.ongoing.title, "Koordinator Dana dan Usaha")
        self.assertEqual(self.ongoing.started_at, original_started_at)
        self.assertEqual(Experience.objects.count(), 2)
        self.assertContains(response, "Pengalaman berhasil diperbarui!")

    def test_invalid_update_does_not_change_database(self):
        response = self.client.post(self.edit_url(), self.payload(title=""))
        self.assertEqual(response.status_code, 200)
        self.ongoing.refresh_from_db()
        self.assertEqual(self.ongoing.title, "Staff Dana dan Usaha")
        self.assertEqual(Experience.objects.count(), 2)

    def test_completion_date_can_be_set_and_cleared(self):
        response = self.client.post(
            self.edit_url(), self.payload(ended_at="2026-09-20T18:30")
        )
        self.assertEqual(response.status_code, 302)
        self.ongoing.refresh_from_db()
        self.assertFalse(self.ongoing.is_ongoing)
        edit_page = self.client.get(self.edit_url())
        self.assertContains(edit_page, 'value="2026-09-20T18:30"')
        self.client.post(self.edit_url(), self.payload(ended_at=""))
        self.ongoing.refresh_from_db()
        self.assertTrue(self.ongoing.is_ongoing)

    def test_missing_and_malformed_uuid_return_404(self):
        missing = uuid.uuid4()
        self.assertEqual(self.client.get(self.edit_url(missing)).status_code, 404)
        self.assertEqual(self.client.post(self.edit_url(missing), self.payload()).status_code, 404)
        self.assertEqual(self.client.post(self.delete_url(missing)).status_code, 404)
        self.assertEqual(self.client.get("/experience/not-a-uuid/edit/").status_code, 404)

    def test_delete_get_is_rejected_without_removing_data(self):
        response = self.client.get(self.delete_url())
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Experience.objects.filter(pk=self.ongoing.pk).exists())

    def test_delete_post_removes_only_the_selected_record(self):
        response = self.client.post(self.delete_url(), follow=True)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(pk=self.ongoing.pk).exists())
        self.assertTrue(Experience.objects.filter(pk=self.completed.pk).exists())
        self.assertContains(response, "Pengalaman berhasil dihapus!")

    def test_json_has_content_type_uuid_and_model_fields(self):
        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        records = response.json()
        item = next(item for item in records if item["pk"] == str(self.ongoing.pk))
        self.assertEqual(item["model"], "main.experience")
        self.assertEqual(item["fields"]["title"], "Staff Dana dan Usaha")
        self.assertIsNone(item["fields"]["ended_at"])
        self.assertIsNotNone(item["fields"]["started_at"])

    def test_json_endpoint_rejects_post(self):
        response = self.client.post(reverse("main:get_experiences_json"))
        self.assertEqual(response.status_code, 405)

    def test_search_matches_title_or_description_without_case_sensitivity(self):
        for query in ("dAnA", "VENDOR"):
            with self.subTest(query=query):
                response = self.client.get(reverse("main:get_experiences_json"), {"q": query})
                self.assertEqual([item["pk"] for item in response.json()], [str(self.ongoing.pk)])

    def test_combined_filters_agree_between_html_and_json(self):
        filters = {"q": "data", "category": "research", "status": "completed"}
        json_response = self.client.get(reverse("main:get_experiences_json"), filters)
        page = self.client.get(reverse("main:show_experience"), filters)
        json_ids = [item["pk"] for item in json_response.json()]
        html_ids = [str(item.pk) for item in page.context["experience_list"]]
        self.assertEqual(json_ids, [str(self.completed.pk)])
        self.assertEqual(html_ids, json_ids)
        self.assertContains(page, 'value="research" selected')

    def test_ongoing_status_filter(self):
        response = self.client.get(reverse("main:get_experiences_json"), {"status": "ongoing"})
        self.assertEqual([item["pk"] for item in response.json()], [str(self.ongoing.pk)])

    def test_no_search_match_shows_reset_and_empty_state(self):
        response = self.client.get(reverse("main:show_experience"), {"q": "tidak-ada-hasil"})
        self.assertContains(response, "Belum ada yang cocok")
        self.assertContains(response, "Tampilkan semua")
        self.assertEqual(response.context["experience_list"], [])

    def test_empty_database_renders_call_to_add_data(self):
        Experience.objects.all().delete()
        page = self.client.get(reverse("main:show_experience"))
        self.assertContains(page, "Belum ada pengalaman yang ditambahkan.")
        self.assertContains(page, reverse("main:create_experience"))
        self.assertEqual(self.client.get(reverse("main:get_experiences_json")).json(), [])

    def test_list_really_deserializes_json_without_saving_it(self):
        unsaved = Experience(
            title="Hanya berasal dari JSON", description="Payload uji", category="research"
        )
        response = HttpResponse(serializers.serialize("json", [unsaved]), content_type="application/json")
        with patch("main.experience_views.get_experiences_json", return_value=response):
            page = self.client.get(reverse("main:show_experience"))
        self.assertContains(page, "Hanya berasal dari JSON")
        self.assertNotContains(page, "Staff Dana dan Usaha")
        self.assertFalse(Experience.objects.filter(pk=unsaved.pk).exists())

    def test_user_content_is_escaped_in_cards_and_confirmation(self):
        self.ongoing.title = '<script>alert("uji")</script>'
        self.ongoing.save()
        page = self.client.get(reverse("main:show_experience"))
        self.assertContains(page, "&lt;script&gt;")
        self.assertNotContains(page, '<script>alert("uji")</script>')

    def test_forms_reject_missing_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        for url in (
            reverse("main:create_experience"), self.edit_url(), self.delete_url()
        ):
            with self.subTest(url=url):
                self.assertEqual(client.post(url, self.payload()).status_code, 403)
        self.assertEqual(Experience.objects.count(), 2)
        self.ongoing.refresh_from_db()
        self.assertEqual(self.ongoing.title, "Staff Dana dan Usaha")

    def test_real_csrf_token_allows_create_update_and_delete(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        client.get(reverse("main:create_experience"))
        token = client.cookies["csrftoken"].value
        payload = self.payload(csrfmiddlewaretoken=token)
        self.assertEqual(client.post(reverse("main:create_experience"), payload).status_code, 302)
        self.assertEqual(client.post(self.edit_url(), payload).status_code, 302)
        self.assertEqual(client.post(self.delete_url(), {"csrfmiddlewaretoken": token}).status_code, 302)

    def test_delete_confirmation_has_post_token_and_cancel_control(self):
        page = self.client.get(reverse("main:show_experience"))
        self.assertContains(page, 'role="dialog"')
        self.assertContains(page, 'popovertargetaction="hide"')
        self.assertContains(page, 'name="csrfmiddlewaretoken"')
        self.assertContains(page, 'action="' + self.delete_url() + '"')
        self.assertContains(page, "Ya, hapus")
