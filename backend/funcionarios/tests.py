from django.test import TestCase
from .models import Funcionario, Cargo

class FuncionarioTests(TestCase):

    def setUp(self):
        # Criação de um cargo para associar ao funcionário
        self.cargo = Cargo.objects.create(nome="Analista", cbo="12345")

        # Criação do funcionário com todos os campos obrigatórios preenchidos
        self.funcionario = Funcionario.objects.create(
            nome="João Silva",
            matricula="1234",
            departamento="TI",
            data_admissao="2023-01-01",  # Preenchemos a data de admissão
            cargo_atual=self.cargo,
            salario=5000,
            pagamento_por_fora=1000,
            tipo_contratacao="CLT",
            tipo_pagamento="Mensalista",
        )

    def test_historico_cargo_salario(self):
        # Atualizando o cargo do funcionário para verificar o histórico
        novo_cargo = Cargo.objects.create(nome="Gerente", cbo="54321")
        self.funcionario.cargo_atual = novo_cargo
        self.funcionario.salario = 6000
        self.funcionario.save()

        # Verificando se o histórico foi criado
        self.assertEqual(self.funcionario.historicocargosalario_set.count(), 1)
        historico = self.funcionario.historicocargosalario_set.first()
        self.assertEqual(historico.cargo, novo_cargo)
        self.assertEqual(historico.salario, 6000)
