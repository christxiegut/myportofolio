"""Register, login, logout, serta cookie waktu login untuk Tutorial 4."""

from zoneinfo import ZoneInfo

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from main.project_views import PORTFOLIO_NAME


@require_http_methods(["GET", "POST"])
def register(request):
    # POST kosong tetap merupakan form terikat, sehingga error tampil.
    form = UserCreationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    return render(request, "register.html", {"name": PORTFOLIO_NAME, "form": form})


@require_http_methods(["GET", "POST"])
def login_user(request):
    form = AuthenticationForm(
        request, data=request.POST if request.method == "POST" else None
    )
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        # Sesuai tutorial, login selalu kembali ke halaman profil.
        response = redirect("main:show_main")
        login_time = timezone.localtime(timezone.now(), ZoneInfo("Asia/Jakarta"))
        response.set_cookie(
            "last_login",
            login_time.strftime("%Y-%m-%d %H:%M:%S"),
            httponly=True,
            samesite="Lax",
            secure=request.is_secure(),
        )
        return response

    return render(request, "login.html", {"name": PORTFOLIO_NAME, "form": form})


@require_POST
def logout_user(request):
    # Navbar mengirim form POST + CSRF untuk mengakhiri sesi.
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login", samesite="Lax")
    return response
