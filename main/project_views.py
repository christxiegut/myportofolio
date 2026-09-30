"""Tutorial 5: JSON, pencarian, dan penambahan proyek melalui AJAX."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.views.decorators.vary import vary_on_cookie

from main.forms import ProjectForm
from main.models import Project


PORTFOLIO_NAME = "Angelica Christilia Talumewo"


def _filtered_projects(request):
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
@vary_on_cookie
def get_projects_json(request):
    data = []
    for project in _filtered_projects(request):
        starred_users = list(project.starred_by.all())
        names = [user.username for user in starred_users]
        data.append({
            "model": "main.project",
            "pk": project.pk,
            "fields": {
                "title": project.title,
                "description": project.description,
                "technologies": project.technologies,
                "repository_url": project.repository_url,
                "starred_by": [[name] for name in names],
                "star_count": len(starred_users),
                "is_starred": (
                    request.user.is_authenticated
                    and any(user.pk == request.user.pk for user in starred_users)
                ),
                "starred_by_names": ", ".join(names),
            },
            "urls": {
                "detail": reverse("main:show_project_detail", args=[project.pk]),
                "star": reverse("main:toggle_star", args=[project.pk]),
                "delete": (
                    reverse("main:delete_project", args=[project.pk])
                    if request.user.is_superuser else ""
                ),
            },
        })
    response = JsonResponse(data, safe=False)
    response["Cache-Control"] = "private, no-store"
    return response


@require_GET
def get_projects_xml(request):
    data = serializers.serialize(
        "xml", _filtered_projects(request), use_natural_foreign_keys=True
    )
    return HttpResponse(data, content_type="application/xml")


@require_GET
@ensure_csrf_cookie
def show_projects(request):
    # Browser mengambil kartu melalui get_projects_json setelah HTML dimuat.
    query = request.GET.get("q", "").strip() or request.GET.get("title", "").strip()
    return render(request, "projects.html", {
        "name": PORTFOLIO_NAME,
        "query": query,
        "form": ProjectForm() if request.user.is_superuser else None,
    })


@require_POST
def create_project_ajax(request):
    # Respons JSON 403, sehingga fetch tidak mengikuti redirect ke HTML login.
    if not request.user.is_superuser:
        return JsonResponse({
            "message": "Hanya pemilik portofolio yang dapat menambahkan proyek. Silakan login sebagai pemilik."
        }, status=403)

    form = ProjectForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    project = form.save()
    return JsonResponse({
        "message": "Proyek berhasil ditambahkan.",
        "pk": project.pk,
    }, status=201)


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
    return render(request, "projects_form.html", {"name": PORTFOLIO_NAME, "form": form})


@login_required(login_url="main:login")
@require_POST
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    get_object_or_404(Project, pk=project_id).delete()
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
