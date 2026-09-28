"""Daftar/API proyek, perubahan oleh pemilik, dan star oleh akun terdaftar."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q, prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from main.forms import ProjectForm
from main.models import Project


PORTFOLIO_NAME = "Angelica Christilia Talumewo"


def _filtered_projects(request):
    """q mencari di tiga kolom; title tetap didukung seperti Tutorial 3."""
    projects = Project.objects.all().order_by("title", "pk")
    query = request.GET.get("q", "").strip()
    title_query = request.GET.get("title", "").strip()
    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(technologies__icontains=query)
        )
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    return projects.prefetch_related("starred_by")


@require_GET
def get_projects_json(request):
    data = serializers.serialize(
        "json", _filtered_projects(request), use_natural_foreign_keys=True
    )
    return HttpResponse(data, content_type="application/json")


@require_GET
def get_projects_xml(request):
    data = serializers.serialize(
        "xml", _filtered_projects(request), use_natural_foreign_keys=True
    )
    return HttpResponse(data, content_type="application/xml")


@require_GET
def show_projects(request):
    # Pertahankan alur Tutorial 3: objek -> JSON -> objek -> template.
    json_response = get_projects_json(request)
    deserialized = serializers.deserialize(
        "json", json_response.content.decode("utf-8")
    )
    project_list = [item.object for item in deserialized]
    # Relasi dibaca dari database; hasil deserialisasi tidak disimpan ulang.
    prefetch_related_objects(project_list, "starred_by")
    query = (
        request.GET.get("q", "").strip()
        or request.GET.get("title", "").strip()
    )
    return render(request, "projects.html", {
        "name": PORTFOLIO_NAME,
        "project_list": project_list,
        "query": query,
    })


@login_required(login_url="main:login")
@require_http_methods(["GET", "POST"])
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    return render(request, "projects_form.html", {
        "name": PORTFOLIO_NAME, "form": form,
    })


@login_required(login_url="main:login")
@require_POST
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Proyek berhasil dihapus!")
    return redirect("main:show_projects")


@login_required(login_url="main:login")
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return redirect("main:show_projects")
