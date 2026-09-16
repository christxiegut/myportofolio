from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from main.models import Experience, Project

def show_main(request):
    context = {
        "name": "Angelica Christilia Talumewo",
        "npm": "2506536313",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa jurusan Sistem Informasi Fakultas Ilmu Komputer "
            "Universitas Indonesia yang saat ini berada di semester 3."
            ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Angelica Christilia Talumewo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    query = request.GET.get("q", "").strip()
    project_list = Project.objects.all().order_by("title", "pk")

    if query:
        project_list = project_list.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(technologies__icontains=query)
        )

    context = {
        "name": "Angelica Christilia Talumewo",
        "project_list": project_list,
        "query": query,
    }
    return render(request, "projects.html", context)

def show_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    context = {
        "name": "Angelica Christilia Talumewo",
        "project": project,
    }

    return render(request, "project_detail.html", context)