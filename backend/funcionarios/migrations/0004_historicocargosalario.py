# Generated by Django 5.1.2 on 2024-10-17 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("funcionarios", "0003_cargo_remove_funcionario_descricao_cargo_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricoCargoSalario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("salario", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "salario_por_fora",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("data_mudanca", models.DateField(auto_now_add=True)),
                (
                    "cargo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="funcionarios.cargo",
                    ),
                ),
                (
                    "funcionario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="funcionarios.funcionario",
                    ),
                ),
            ],
        ),
    ]