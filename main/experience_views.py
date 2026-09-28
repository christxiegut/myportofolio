"""Experience: empat peran, CRUD, JSON, detail, filter, dan Star untuk Tugas 4."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q, prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from main.forms import ExperienceForm
from main.access import can_edit_experience, is_editor
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
    if request.GET.get("starred") == "1":
        if not request.user.is_authenticated:
            return experiences.none()
        experiences = experiences.filter(starred_by=request.user)
    return experiences.prefetch_related("starred_by")


@require_GET
def get_experiences_json(request):
    """Serialisasi UUID, waktu, dan field model ke JSON yang bisa dikirim lewat HTTP."""
    data = serializers.serialize(
        "json",
        _filtered_experiences(request),
        fields=(
            "title", "description", "category", "thumbnail",
            "started_at", "ended_at", "starred_by",
        ),
        use_natural_foreign_keys=True,
    )
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
    # Baca relasi secara berkelompok; jangan simpan hasil deserialisasi ke DB.
    prefetch_related_objects(experience_list, "starred_by")
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()
    starred_only = request.GET.get("starred") == "1"
    context = {
        "name": PORTFOLIO_NAME,
        "experience_list": experience_list,
        "query": query,
        "selected_category": category,
        "selected_status": status,
        "category_choices": Experience.EXPERIENCE_CHOICES,
        "has_filters": bool(query or category or status or starred_only),
        "starred_only": starred_only,
        "is_editor": is_editor(request.user),
        "filter_querystring": request.GET.urlencode(),
    }
    return render(request, "experience.html", context)


@require_GET
def show_experience_detail(request, experience_id):
    """Detail tetap publik; kontrol perubahan mengikuti peran yang sedang login."""
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id
    )
    return render(request, "experience_detail.html", {
        "name": PORTFOLIO_NAME,
        "experience": experience,
        "is_editor": is_editor(request.user),
    })


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


@login_required(login_url="main:login")
@require_http_methods(["GET", "POST"])
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    return _render_experience_form(request)


@login_required(login_url="main:login")
@require_http_methods(["GET", "POST"])
def update_experience(request, experience_id):
    if not can_edit_experience(request.user):
        raise PermissionDenied
    # UUID yang tidak ditemukan menghasilkan 404, bukan objek baru atau error 500.
    experience = get_object_or_404(Experience, pk=experience_id)
    return _render_experience_form(request, instance=experience)


@login_required(login_url="main:login")
@require_POST
def delete_experience(request, experience_id):
    """Perubahan data hanya melalui POST; form tetap memakai token CSRF."""
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")


@login_required(login_url="main:login")
@require_POST
def toggle_experience_star(request, experience_id):
    """Semua akun boleh Star/Unstar hanya atas relasinya sendiri."""
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    # Pertahankan halaman/filter saat menekan Star; tolak pengalihan ke situs luar.
    return_url = request.POST.get("next", "")
    if return_url and url_has_allowed_host_and_scheme(
        return_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(return_url)
    return redirect("main:show_experience")
