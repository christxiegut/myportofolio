"""Aturan peran Experience; grup Editor dikelola oleh pemilik melalui Django Admin."""


def is_editor(user):
    """Keanggotaan grup berasal dari database, bukan form atau cookie pengguna."""
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def can_edit_experience(user):
    return user.is_authenticated and (user.is_superuser or is_editor(user))
