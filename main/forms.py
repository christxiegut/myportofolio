from django.forms import ModelForm, Textarea, TextInput, URLInput

from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "technologies", "repository_url"]
        labels = {
            "title": "Nama proyek",
            "description": "Deskripsi proyek",
            "technologies": "Teknologi yang digunakan",
            "repository_url": "URL repositori (opsional)",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Website Portofolio Pribadi"}),
            "description": Textarea(
                attrs={"placeholder": "Ceritakan tujuan dan fitur proyekmu...", "rows": 5}
            ),
            "technologies": TextInput(
                attrs={"placeholder": "Python, Django, HTML, CSS"}
            ),
            "repository_url": URLInput(
                attrs={"placeholder": "https://github.com/christxiegut/myportofolio"}
            ),
        }
