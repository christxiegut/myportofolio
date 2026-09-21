from django.forms import DateTimeInput, ModelForm, Textarea, TextInput, URLInput

from main.models import Experience, Project


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


class ExperienceForm(ModelForm):
    """Satu form untuk tambah/edit; UUID dan waktu pencatatan dikelola model."""

    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]
        labels = {
            "title": "Nama pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL gambar (opsional)",
            "ended_at": "Tanggal dan waktu selesai (opsional)",
        }
        help_texts = {
            "thumbnail": "Gunakan tautan langsung ke gambar jika tersedia.",
            "ended_at": "Kosongkan jika pengalaman ini masih berlangsung.",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Staff divisi Dana & Usaha"}),
            "description": Textarea(
                attrs={"rows": 5, "placeholder": "Ceritakan peran dan kontribusimu..."}
            ),
            "thumbnail": URLInput(attrs={"placeholder": "https://example.com/gambar.jpg"}),
            "ended_at": DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }
        error_messages = {
            "title": {"required": "Isi nama pengalaman terlebih dahulu."},
            "description": {"required": "Isi deskripsi pengalaman terlebih dahulu."},
            "category": {"invalid_choice": "Pilih kategori yang tersedia."},
            "thumbnail": {"invalid": "Masukkan URL gambar yang valid."},
            "ended_at": {"invalid": "Masukkan tanggal dan waktu yang valid."},
        }
