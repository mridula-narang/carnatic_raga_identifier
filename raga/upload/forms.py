from django import forms
from raga_app.models import Audio

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['audio','audio1','selected_option']
        widgets = {
            'selected_option': forms.RadioSelect,
        }
        labels = {
            'selected_option': 'Select the type of the song:',
        }
    audio = forms.FileField(label='Upload the song audio:')
    audio1 = forms.FileField(label='Upload the Sa audio:')