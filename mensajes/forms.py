from django.contrib.auth.forms import PasswordChangeForm
from django.utils.safestring import mark_safe

class CambiarContrasenaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Tu contraseña actual: '
        self.fields['new_password1'].label = 'Tu Contraseña nueva: '
        self.fields['new_password2'].label = 'Repetí la contraseña nueva: '

        intro = '<p>Las condiciones que debe cumplir la contraseña son las siguientes:</p>'
        self.fields['new_password1'].help_text = mark_safe(intro + str(self.fields['new_password1'].help_text))

        self.fields['new_password2'].help_text = 'Repetila porfi 🙏'