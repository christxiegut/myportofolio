from django.shortcuts import render

from main.models import Experience

def show_main(request):
    context = {
        "name": "Angelica Christilia Talumewo",
        "npm": "2506536313",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa jurusan Sistem Informasi Fakultas Ilmu Komputer"
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