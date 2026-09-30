from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from main.models import Project
from main.project_views import PORTFOLIO_NAME, show_projects
from main.experience_views import show_experience


@require_GET
def show_main(request):
    return render(request, "index.html", {
        "name": PORTFOLIO_NAME,
        "npm": "2506536313",
        "study_program": "S1 Sistem Informasi",
        "bio": "Mahasiswa jurusan Sistem Informasi Fakultas Ilmu Komputer Universitas Indonesia yang saat ini berada di semester 3.",
        "last_login": request.COOKIES.get("last_login", "Belum ada sesi login"),
    })


@require_GET
def show_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_detail.html", {
        "name": PORTFOLIO_NAME,
        "project": project,
    })
