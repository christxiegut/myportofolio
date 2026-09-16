"""View khusus proyek untuk Tutorial 3: form, JSON/XML, daftar, dan hapus."""

from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from main.forms import ProjectForm
from main.models import Project


PORTFOLIO_NAME = "Angelica Christilia Talumewo"


def _filtered_projects(request):
    """q mencari di tiga kolom; title mengikuti contoh filter pada PDF."""
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

    return projects


@require_GET
def get_projects_json(request):
    data = serializers.serialize("json", _filtered_projects(request))
    return HttpResponse(data, content_type="application/json")


@require_GET
def get_projects_xml(request):
    data = serializers.serialize("xml", _filtered_projects(request))
    return HttpResponse(data, content_type="application/xml")


@require_GET
def show_projects(request):
    # Latihan Tutorial 3: objek -> JSON -> objek Python -> template.
    # Pemanggilan ini terjadi di Python, bukan permintaan HTTP ke server lain.
    json_response = get_projects_json(request)
    deserialized = serializers.deserialize(
        "json", json_response.content.decode("utf-8")
    )
    project_list = [item.object for item in deserialized]
    query = (
        request.GET.get("q", "").strip()
        or request.GET.get("title", "").strip()
    )
    context = {
        "name": PORTFOLIO_NAME,
        "project_list": project_list,
        "query": query,
    }
    return render(request, "projects.html", context)


@require_http_methods(["GET", "POST"])
def create_project(request):
    form = ProjectForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {"name": PORTFOLIO_NAME, "form": form}
    return render(request, "projects_form.html", context)


@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Proyek berhasil dihapus!")
    return redirect("main:show_projects")
