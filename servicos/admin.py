# from django.contrib.gis import admin
#
# from .models import Servico, ProdutosServico
#
#
# class ProdutoServicoInLine(admin.TabularInline):
#     model = ProdutosServico
#     extra = 1
#
# @admin.register(Servico)
# class ServicoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'descricao', 'preco', 'get_produto')
#     inlines = [ProdutoServicoInLine]
#     search_fields = ('nome', 'descricao')
#
#     def get_produtos(self, obj):
#         return ', '.join([prd.nome for prd in ProdutosServico.objects.filter(servico=obj.id)])
#
#     get_produtos.short_description = 'Produtos utilizados'