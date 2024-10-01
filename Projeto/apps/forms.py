from django import forms
from .models import GrupoEstudo

class GrupoEstudoForm(forms.ModelForm):
    class Meta:
        model = GrupoEstudo
        fields = ['titulo', 'tema', 'numero_integrantes', 'descricao', 'professor_orientador', 'carga_horaria_semanal', 'dias_reuniao', 'hora_reuniao']

        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título do grupo', 'class': 'form-control'}),
            'tema': forms.TextInput(attrs={'placeholder': 'Tema do grupo', 'class': 'form-control'}),
            'numero_integrantes': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição do grupo', 'class': 'form-control'}),
            'professor_orientador': forms.TextInput(attrs={'placeholder': 'Nome do professor orientador', 'class': 'form-control'}),
            'carga_horaria_semanal': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_reuniao': forms.TextInput(attrs={'placeholder': 'Ex: Segunda, Quarta', 'class': 'form-control'}),
            'hora_reuniao': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }