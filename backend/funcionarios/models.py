from django.db import models


class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    cbo = models.CharField(max_length=10, unique=True)  # Código Brasileiro de Ocupações (CBO)
    descricao_cargo = models.FileField(upload_to='descricoes_cargo/', null=True, blank=True)  # Descrição opcional em PDF ou DOCX

    def __str__(self):
        return self.nome

from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=4, unique=True)
    departamento = models.CharField(max_length=100)
    data_admissao = models.DateField()
    data_desligamento = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')

    responsavel = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    cargo_atual = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    pagamento_por_fora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Níveis de escolaridade completos, incluindo "Sem Escolaridade"
    ESCOLARIDADE_CHOICES = [
        ('Sem Escolaridade', 'Sem Escolaridade'),
        ('Ensino Fundamental Incompleto', 'Ensino Fundamental Incompleto'),
        ('Ensino Fundamental Completo', 'Ensino Fundamental Completo'),
        ('Ensino Médio Incompleto', 'Ensino Médio Incompleto'),
        ('Ensino Médio Completo', 'Ensino Médio Completo'),
        ('Técnico', 'Técnico'),
        ('Tecnólogo', 'Tecnólogo'),
        ('Graduação Incompleta', 'Graduação Incompleta'),
        ('Graduação', 'Graduação'),
        ('Pós-Graduação', 'Pós-Graduação'),
        ('Mestrado', 'Mestrado'),
        ('Doutorado', 'Doutorado'),
    ]
    nivel_escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE_CHOICES, default='Ensino Médio Completo')
    graduacao = models.CharField(max_length=255, null=True, blank=True)

    TIPO_CONTRATACAO_CHOICES = [
        ('CLT', 'CLT'),
        ('PJ', 'PJ'),
        ('Outros', 'Outros'),
    ]
    tipo_contratacao = models.CharField(max_length=20, choices=TIPO_CONTRATACAO_CHOICES)

    cargo_inicial = models.ForeignKey('Cargo', related_name='cargo_inicial', on_delete=models.SET_NULL, null=True)
    cargo_atual = models.ForeignKey('Cargo', related_name='cargo_atual', on_delete=models.SET_NULL, null=True)

    salario = models.DecimalField(max_digits=10, decimal_places=2)
    pagamento_por_fora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    TIPO_PAGAMENTO_CHOICES = [
        ('Horista', 'Horista'),
        ('Mensalista', 'Mensalista'),
    ]
    tipo_pagamento = models.CharField(max_length=20, choices=TIPO_PAGAMENTO_CHOICES)

    def __str__(self):
        return f'{self.nome} ({self.matricula})'
    

    def save(self, *args, **kwargs):
        if self.pk:
            # Verifica se o funcionário já existe (edição) para comparar as mudanças
            old_funcionario = Funcionario.objects.get(pk=self.pk)
            # Verifica se houve mudança no cargo atual ou salário
            if old_funcionario.cargo_atual != self.cargo_atual or old_funcionario.salario != self.salario:
                # Cria um novo registro de histórico de cargos e salários
                HistoricoCargoSalario.objects.create(
                    funcionario=self,
                    cargo=self.cargo_atual,
                    salario=self.salario,
                    salario_por_fora=self.pagamento_por_fora
                )
        
        # Define o status automaticamente com base na data de desligamento
        if self.data_desligamento:
            self.status = 'Inativo'
        else:
            self.status = 'Ativo'
        
        super().save(*args, **kwargs)


class HistoricoCargoSalario(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    salario_por_fora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_mudanca = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.funcionario.nome} - {self.cargo.nome} - {self.data_mudanca}'
