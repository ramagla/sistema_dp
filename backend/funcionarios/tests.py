from django.test import TestCase
from .models import Funcionario, Cargo

class FuncionarioModelTest(TestCase):
    def setUp(self):
        # Criando um cargo de teste
        self.cargo = Cargo.objects.create(nome="Gerente de TI", cbo="123456", descricao_cargo=None)

        # Criando um funcionário de teste
        self.funcionario = Funcionario.objects.create(
            nome="João Silva",
            matricula="1234",
            departamento="TI",
            data_admissao="2022-01-01",
            status="Ativo",
            cargo_inicial=self.cargo,
            cargo_atual=self.cargo,
            salario=5000.00
        )

    def test_funcionario_criado(self):
        funcionario = Funcionario.objects.get(matricula="1234")
        self.assertEqual(funcionario.nome, "João Silva")
        self.assertEqual(funcionario.departamento, "TI")
        self.assertEqual(funcionario.status, "Ativo")
        self.assertEqual(funcionario.cargo_atual.nome, "Gerente de TI")
