# Generated by Django 3.2.7 on 2021-12-01 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_cuenta_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analizisrs',
            name='smell_codigo',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='analizisru',
            name='smell_codigo',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='admin',
            field=models.CharField(choices=[('Si', 'Si'), ('No', 'No')], max_length=10),
        ),
        migrations.CreateModel(
            name='RequisitoSistema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='RS01', max_length=200)),
                ('titulo', models.CharField(max_length=200, null=True)),
                ('tipo', models.CharField(choices=[('Funcional', 'Funcional'), ('No Funcional', 'No Funcional'), ('Restriccion', 'Restriccion'), ('Calidad', 'Calidad')], max_length=200, null=True)),
                ('costo', models.CharField(max_length=200, null=True)),
                ('urgencia', models.CharField(choices=[('Urgente', 'Urgente'), ('Normal', 'Normal'), ('Si se puede', 'Si se puede')], max_length=200, null=True)),
                ('estado', models.CharField(choices=[('Cumple', 'Cumple'), ('No Cumple', 'No Cumple')], max_length=200, null=True)),
                ('descripcion', models.CharField(max_length=200, null=True)),
                ('version', models.CharField(default=1, max_length=200)),
                ('proyecto_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.proyecto')),
                ('requisito_usuario_codigo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.requisitodeusuario')),
            ],
        ),
        migrations.AlterField(
            model_name='analizisrs',
            name='rs_codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.requisitosistema'),
        ),
        migrations.DeleteModel(
            name='RequisitoDeSistema',
        ),
    ]
