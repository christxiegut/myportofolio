"""Form dan data delivery Experience untuk Tugas 3."""

from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from main.forms import ExperienceForm
from main.models import Experience
from main.project_views import PORTFOLIO_NAME


def _filtered_experiences(request):
    """Gunakan filter yang sama untuk daftar HTML dan endpoint JSON."""
    experiences = Experience.objects.all().order_by("-started_at", "pk")
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    if query:
        experiences = experiences.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category:
        experiences = experiences.filter(category=category)
    if status in {"ongoing", "completed"}:
        experiences = experiences.filter(ended_at__isnull=(status == "ongoing"))
    return experiences


@require_GET
def get_experiences_json(request):
    """Serialisasi UUID, waktu, dan field model ke JSON yang bisa dikirim lewat HTTP."""
    data = serializers.serialize("json", _filtered_experiences(request))
    return HttpResponse(data, content_type="application/json")


@require_GET
def show_experience(request):
    """Ikuti alur tugas: QuerySet -> JSON -> deserialisasi -> context template.

    View JSON dipanggil sebagai fungsi Python, sehingga tidak membuat request
    HTTP tambahan ke aplikasi sendiri. Deserialisasi di sini tidak menyimpan data.
    """
    json_response = get_experiences_json(request)
    objects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experience_list = [item.object for item in objects]
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()
    context = {
        "name": PORTFOLIO_NAME,
        "experience_list": experience_list,
        "query": query,
        "selected_category": category,
        "selected_status": status,
        "category_choices": Experience.EXPERIENCE_CHOICES,
        "has_filters": bool(query or category or status),
        "filter_querystring": request.GET.urlencode(),
    }
    return render(request, "experience.html", context)


def _render_experience_form(request, *, instance=None):
    """Berbagi validasi dan template; instance membedakan tambah dengan edit."""
    is_edit = instance is not None
    form = ExperienceForm(
        request.POST if request.method == "POST" else None,
        instance=instance,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Pengalaman berhasil diperbarui!" if is_edit else "Pengalaman berhasil ditambahkan!",
        )
        return redirect("main:show_experience")

    return render(
        request,
        "experience_form.html",
        {
            "name": PORTFOLIO_NAME,
            "form": form,
            "experience": instance,
            "is_edit": is_edit,
        },
    )


@require_http_methods(["GET", "POST"])
def create_experience(request):
    return _render_experience_form(request)


@require_http_methods(["GET", "POST"])
def update_experience(request, experience_id):
    # UUID yang tidak ditemukan menghasilkan 404, bukan objek baru atau error 500.
    experience = get_object_or_404(Experience, pk=experience_id)
    return _render_experience_form(request, instance=experience)


@require_POST
def delete_experience(request, experience_id):
    """Perubahan data hanya melalui POST; form tetap memakai token CSRF."""
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")
