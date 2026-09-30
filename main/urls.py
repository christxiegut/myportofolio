from django.urls import path

from main.auth_views import login_user, logout_user, register
from main.views import show_main, show_project_detail
from main.experience_views import (
    create_experience,
    delete_experience,
    get_experiences_json,
    show_experience,
    show_experience_detail,
    toggle_experience_star,
    update_experience,
)
from main.project_views import (
    create_project,
    create_project_ajax,
    delete_project,
    get_projects_json,
    get_projects_xml,
    show_projects,
    toggle_star,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/", show_experience_detail, name="show_experience_detail"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/<int:pk>/", show_project_detail, name="show_project_detail"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<int:project_id>/star/", toggle_star, name="toggle_star"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/projects/xml/", get_projects_xml, name="get_projects_xml"),
]
