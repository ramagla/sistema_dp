from django.contrib import admin
from django.utils.html import format_html
from .models import Funcionario, Cargo,HistoricoCargoSalario
import os
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cbo', 'descricao_icone')  # Adiciona o campo de ícone aqui

    # Método para exibir o ícone baseado na extensão do arquivo
    def descricao_icone(self, obj):
        if obj.descricao_cargo:  # Verifica se o arquivo foi anexado
            file_extension = os.path.splitext(obj.descricao_cargo.name)[1].lower()

            # Associa o tipo de arquivo a um ícone
            if file_extension == '.pdf':
                icon = 'pdf-icon.png'  # Aqui você pode usar um ícone de PDF
            elif file_extension in ['.doc', '.docx']:
                icon = 'word-icon.png'  # Aqui pode usar um ícone de Word
            else:
                icon = 'file-icon.png'  # Ícone padrão para outros arquivos

            # Renderiza o ícone como HTML
            return format_html('<img src="/static/icons/{}" width="20" height="20" alt="{}" />', icon, file_extension)
        return "Nenhum arquivo"  # Caso não tenha arquivo anexado
    
    # Nome amigável para exibir no admin
    descricao_icone.short_description = 'Arquivo Anexo'


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'departamento',
        'status',
        'cargo_atual',
        'data_admissao',
        'data_desligamento',
        'salario_formatado',
        'pagamento_por_fora_formatado',
        'salario_total_formatado',
    )
    search_fields = ('nome', 'matricula')
    list_filter = ('departamento', 'status', 'cargo_atual', 'tipo_contratacao', 'tipo_pagamento')
    readonly_fields = ('status',)  # Campo status será definido automaticamente

    def salario_formatado(self, obj):
        return locale.currency(obj.salario, grouping=True)
    salario_formatado.short_description = 'Salário'

    def pagamento_por_fora_formatado(self, obj):
        return locale.currency(obj.pagamento_por_fora or 0, grouping=True)
    pagamento_por_fora_formatado.short_description = 'Pagamento por Fora'

    def salario_total_formatado(self, obj):
        total = obj.salario + (obj.pagamento_por_fora or 0)
        return locale.currency(total, grouping=True)
    salario_total_formatado.short_description = 'Salário Total'

@admin.register(HistoricoCargoSalario)
class HistoricoCargoSalarioAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'cargo', 'salario', 'salario_por_fora', 'data_mudanca')
    search_fields = ('funcionario__nome', 'cargo__nome')
