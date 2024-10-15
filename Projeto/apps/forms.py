from django import forms
from .models import GrupoEstudo, Evento

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


class EventoForm(forms.ModelForm):
    OPCOES_PALESTRANTE = [
        ('nome', 'Informar nome'),
        ('indefinido', 'Indefinido / não informar'),
    ]

    opcao_palestrante = forms.ChoiceField(choices=OPCOES_PALESTRANTE, label="Palestrante", widget=forms.Select(attrs={'class': 'form-control', 'id': 'opcao-palestrante'}))
    palestrante = forms.CharField(required=False, label="Nome do palestrante", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome...', 'id': 'palestrante-input', 'style': 'display:none;'}))

    class Meta:
        model = Evento
        fields = ['tipo', 'titulo', 'descricao', 'inicio_evento', 'fim_evento', 'vagas', 'local', 'horario_de_inicio', 'horario_de_termino', 'opcao_palestrante', 'palestrante']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'inicio_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fim_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario_de_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_de_termino': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'vagas': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'instituicao': forms.TextInput(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        opcao = cleaned_data.get('opcao_palestrante')
        nome = cleaned_data.get('palestrante')

        # Validação para garantir que o nome seja preenchido quando a opção "nome" for escolhida
        if opcao == 'nome' and not nome:
            self.add_error('palestrante', 'Este campo é obrigatório quando "Informar nome" é selecionado.')