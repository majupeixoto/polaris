from django import forms
from .models import GrupoEstudo, Evento, Perfil, Voluntariado, Monitoria, IniciacaoCientifica, IniciativaEstudantil, Oportunidade, ProgramaOficial
import json, re

class PerfilForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
        min_length=8
    )

    class Meta:
        model = Perfil
        fields = ['nome', 'email', 'password']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Perfil.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        # Aqui você pode adicionar validações adicionais se necessário
        
        return cleaned_data

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.set_password(self.cleaned_data['password'])  # Criptografa a senha
        if commit:
            perfil.save()
        return perfil


class GrupoEstudoForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Digite uma tag e pressione Enter'
        }),
        label="Tags"
    )

    class Meta:
        model = GrupoEstudo
        fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'tema', 'numero_integrantes', 
                  'professor_orientador', 'carga_horaria_semanal', 'dias_reuniao', 'hora_reuniao']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Nome do grupo de estudos', 'class': 'form-control', 'required': True}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição do grupo', 'class': 'form-control', 'required': True}),
            'status_inscricoes': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tags': forms.TextInput(attrs={'placeholder': 'Digite uma tag', 'class': 'form-control'}),
            'tema': forms.TextInput(attrs={'placeholder': 'Área de estudo do grupo', 'class': 'form-control', 'required': True}),
            'numero_integrantes': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'professor_orientador': forms.TextInput(attrs={'placeholder': 'Nome do professor orientador', 'class': 'form-control', 'required': True}),
            'carga_horaria_semanal': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'dias_reuniao': forms.CheckboxSelectMultiple(attrs={'required': True}),  # Widget para múltipla seleção
            'hora_reuniao': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
        }

    def clean_dias_reuniao(self):
        dias_reuniao = self.cleaned_data.get('dias_reuniao')
        if not dias_reuniao:
            raise forms.ValidationError("Selecione pelo menos um dia de reunião.")
        return dias_reuniao

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        # Converte de JSON string para lista, se necessário
        if isinstance(tags, str):
            try:
                tags = json.loads(tags)  # Transforma em lista, caso seja uma string JSON
            except json.JSONDecodeError:
                tags = [tags]  # Se não for um JSON válido, coloca como uma lista de uma única tag

        # Remove qualquer ocorrência de \nx de cada tag
        cleaned_tags = []
        for tag in tags:
            # Remove qualquer sequência de escape (\n, \x) e qualquer 'x' no final da string
           
            tag = re.sub(r'\\n|\\x|\\|x$', '', tag.strip())
            tag = tag.replace('\\nx', '')  # Remove \nx diretamente
            tag = tag.replace('\n', '')    # Remove \n diretamente
            cleaned_tags.append(tag)
        
        return cleaned_tags

class EventoForm(forms.ModelForm):
    OPCOES_PALESTRANTE = [
        ('nome', 'Informar nome'),
        ('indefinido', 'Indefinido / não informar'),
    ]

    opcao_palestrante = forms.ChoiceField(
        choices=OPCOES_PALESTRANTE,
        label="Palestrante",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'opcao-palestrante'})
    )
    palestrante = forms.CharField(
        required=False,
        label="Nome do palestrante",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome...', 'id': 'palestrante-input', 'style': 'display:none;'})
    )
    participantes = forms.ModelMultipleChoiceField(
        queryset=Perfil.objects.all(),  # Adiciona a lista de Perfis
        required=False,
        label="Participantes",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    tags = forms.CharField(
        required=False,
        label="Tags",
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'inicio_evento', 'fim_evento', 'horario_de_inicio', 'horario_de_termino', 'opcao_palestrante', 'palestrante', 'vagas', 'tipo', 'local', 'status_inscricoes']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'inicio_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fim_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario_de_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M'),
            'horario_de_termino': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M'),
            'vagas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'status_inscricoes': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        opcao = cleaned_data.get('opcao_palestrante')
        nome = cleaned_data.get('palestrante')
        participantes = cleaned_data.get('participantes', [])
        tags = cleaned_data.get('tags', '')

        # Validação para garantir que o nome seja preenchido quando a opção "nome" for escolhida
        if opcao == 'nome' and not nome:
            self.add_error('palestrante', 'Este campo é obrigatório quando "Informar nome" é selecionado.')

        # Processa as tags, separando por vírgula e removendo espaços extras
        cleaned_data['tags'] = [t.strip() for t in tags.split(',') if t.strip()]

        return cleaned_data 
        
class VoluntariadoForm(forms.ModelForm):
    class Meta:
        model = Voluntariado
        fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'inicio_evento', 'fim_evento', 'carga_horaria', 'link_inscricao', 'local_trabalho', 'organizacao_parceira', 'habilidades_requeridas']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Programa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'status_inscricoes': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags separadas por vírgula'}),
            'inicio_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fim_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carga horária'}),
            'link_inscricao': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link para inscrição'}),
            'local_trabalho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local de Trabalho'}),
            'organizacao_parceira': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organização Parceira'}),
            'habilidades_requeridas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Habilidades requeridas'}),
        }

class MonitoriaForm(forms.ModelForm):
    class Meta:
        model = Monitoria
        fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'inicio_evento', 'fim_evento', 'carga_horaria', 'link_inscricao', 'professor_orientador', 'disciplina', 'cadeiras_requeridas', 'requisitos']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Programa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'status_inscricoes': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags separadas por vírgula'}),
            'inicio_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fim_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carga horária'}),
            'link_inscricao': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link para inscrição'}),
            'professor_orientador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Professor Orientador'}),
            'disciplina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disciplina'}),
            'cadeiras_requeridas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Cadeiras Requeridas'}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Requisitos'}),
        }

class IniciacaoCientificaForm(forms.ModelForm):
    class Meta:
        model = IniciacaoCientifica
        fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'inicio_evento', 'fim_evento', 'carga_horaria', 'link_inscricao', 'duracao', 'professor_orientador', 'bolsa_pesquisa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Programa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'status_inscricoes': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags separadas por vírgula'}),
            'inicio_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fim_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carga horária'}),
            'link_inscricao': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link para inscrição'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duração em meses'}),
            'professor_orientador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Professor Orientador'}),
            'bolsa_pesquisa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class IniciativaEstudantilForm(forms.ModelForm):
    class Meta:
        model = IniciativaEstudantil
        fields = [
            'titulo', 'descricao', 'status_inscricoes', 'tags', 
            'objetivo', 'docente_supervisor', 'site'
        ]

    # Título (herdado de Oportunidade)
    titulo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da Oportunidade'}),
        label="Título"
    )
    
    # Descrição (herdado de Oportunidade)
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da Oportunidade'}),
        label="Descrição"
    )
    
    # Status das Inscrições (herdado de Oportunidade)
    status_inscricoes = forms.ChoiceField(
        choices=[('abertas', 'Abertas'), ('em_breve', 'Em breve'), ('fechadas', 'Fechadas')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status das Inscrições"
    )
    
    # Tags (herdado de Oportunidade)
    tags = forms.JSONField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tags (em formato JSON)'}),
        label="Tags",
        required=False
    )

    # Objetivo (específico de IniciativaEstudantil)
    objetivo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Objetivo da Iniciativa'}),
        label="Objetivo"
    )

    # Docente Supervisor (específico de IniciativaEstudantil)
    docente_supervisor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Docente Supervisor'}),
        label="Docente Supervisor"
    )

    # Site (específico de IniciativaEstudantil)
    site = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Site da Iniciativa'}),
        label="Site",
        required=False
    )

class FavoritarForm(forms.Form):
    evento_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(
        choices=[('favoritar', 'Favoritar'), ('desfavoritar', 'Desfavoritar')],
        widget=forms.HiddenInput()
    )

class ProgramaOficialForm(forms.ModelForm):
    class Meta:
        model = ProgramaOficial
        fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'inicio_evento', 'fim_evento', 'carga_horaria', 'tema', 'periodicidade', 'responsavel', 'links']

    titulo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Programa'}),
        label="Título"
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Programa'}),
        label="Descrição"
    )
    status_inscricoes = forms.ChoiceField(
        choices=Oportunidade.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status das Inscrições"
    )
    tags = forms.JSONField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tags do Programa'}),
        label="Tags"
    )
    inicio_evento = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Início do Evento'}),
        label="Início do Evento"
    )
    fim_evento = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Fim do Evento'}),
        label="Fim do Evento"
    )
    carga_horaria = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carga Horária'}),
        label="Carga Horária"
    )
    tema = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tema do Programa'}),
        label="Tema"
    )
    periodicidade = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Periodicidade'}),
        label="Periodicidade"
    )
    responsavel = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsável'}),
        label="Responsável"
    )
    links = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Links do Programa'}),
        label="Links",
        required=False
    )