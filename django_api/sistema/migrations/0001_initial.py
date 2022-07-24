# Generated by Django 4.0.4 on 2022-07-24 20:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estudante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.IntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('matricula', models.CharField(max_length=11)),
                ('pontuacao', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['nome'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='listaTitulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataHora', models.DateTimeField(auto_now_add=True)),
                ('tituloAtual', models.BooleanField(default=1)),
                ('fkestudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.estudante')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senha', models.IntegerField()),
                ('cpf', models.IntegerField()),
                ('eh_usuario', models.BooleanField(default=False)),
                ('dataHora', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Postagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=10000)),
                ('texto', models.CharField(max_length=10000)),
                ('dataHora', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('qtdPontos', models.IntegerField(default=15)),
                ('fkusuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.estudante')),
            ],
        ),
        migrations.CreateModel(
            name='PostagemArmazenada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=10000)),
                ('texto', models.CharField(max_length=10000)),
                ('dataHora', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.IntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('siape', models.IntegerField()),
            ],
            options={
                'ordering': ['nome'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Visualizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foiVisualizado', models.BooleanField(default=False)),
                ('ehPontoExtra', models.BooleanField(default=False)),
                ('qtdPontos', models.IntegerField()),
                ('fkpostagem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.postagem')),
                ('fkprogramada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.postagemarmazenada')),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('Pontuação: 0 - 840', 'Bonnie Prado Pinto'), ('Pontuação: 841 - 1680', 'Angelica Ross'), ('Pontuação: 1681 - 3360', 'Shirley Ann Jackson'), ('Pontuação: 3361 - 6720', 'Timnit Gebru'), ('Pontuação: 6721 - oo', 'Marie Van Brittan Brown')], default='Pontuação: 0 - 840', max_length=100)),
                ('desc', models.CharField(default='Bonnie Prado Pinto', max_length=30)),
                ('qtdPontos', models.IntegerField()),
                ('estudante', models.ManyToManyField(through='sistema.listaTitulo', to='sistema.estudante')),
            ],
        ),
        migrations.AddField(
            model_name='postagemarmazenada',
            name='fkusuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.professor'),
        ),
        migrations.AddField(
            model_name='listatitulo',
            name='fktitulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.titulo'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=10000)),
                ('dataHora', models.DateTimeField(auto_now_add=True)),
                ('qtdPontos', models.IntegerField(default=10)),
                ('object_id', models.PositiveIntegerField(default=None)),
                ('content_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('fkestudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.estudante')),
            ],
        ),
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('DC1', 'Ler uma postagem.'), ('DC2', 'Publicar um comentário.'), ('DC3', 'Publicar uma postagem.')], default='DC1', max_length=30)),
                ('desc', models.CharField(default='Ler uma postagem.', max_length=30)),
                ('dataHora', models.DateField(auto_now_add=True, db_column='data')),
                ('cumprida', models.BooleanField(default=0)),
                ('qtdPontos', models.IntegerField(default=0)),
                ('fkestudante', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sistema.estudante')),
            ],
            options={
                'unique_together': {('tipo', 'dataHora')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='listatitulo',
            unique_together={('fkestudante', 'fktitulo')},
        ),
    ]
