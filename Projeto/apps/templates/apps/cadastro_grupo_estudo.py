{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container mt-5">
    <h1 class="text-center">Cadastrar Grupo de Estudos</h1>
    <form method="post">
        {% csrf_token %}
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="titulo">Título do Grupo</label>
                    {{ form.titulo }}
                </div>
                <div class="form-group">
                    <label for="tema">Tema</label>
                    {{ form.tema }}
                </div>
                <div class="form-group">
                    <label for="numero_integrantes">Número de Integrantes</label>
                    {{ form.numero_integrantes }}
                </div>
                <div class="form-group">
                    <label for="professor_orientador">Professor Orientador</label>
                    {{ form.professor_orientador }}
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label for="carga_horaria_semanal">Carga Horária Semanal (horas)</label>
                    {{ form.carga_horaria_semanal }}
                </div>
                <div class="form-group">
                    <label for="dias_reuniao">Dias de Reunião</label>
                    {{ form.dias_reuniao }}
                </div>
                <div class="form-group">
                    <label for="hora_reuniao">Hora da Reunião</label>
                    {{ form.hora_reuniao }}
                </div>
                <div class="form-group">
                    <label for="descricao">Descrição</label>
                    {{ form.descricao }}
                </div>
            </div>
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary mt-3">Cadastrar</button>
        </div>
    </form>
</div>
{% endblock %}