from django.db import migrations, models
from datetime import time

class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_perfil_curso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='carga_horaria',
        ),
        migrations.AddField(
            model_name='evento',
            name='horario_de_inicio',
            field=models.TimeField(default=time(0, 0)),  # Usando time(0, 0) para 00:00
        ),
        migrations.AddField(
            model_name='evento',
            name='horario_de_termino',
            field=models.TimeField(default=time(0, 0)),  # Usando time(0, 0) para 00:00
        ),
    ]
