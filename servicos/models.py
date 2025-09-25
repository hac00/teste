
from django.db import models
from django.db.models.functions import Upper


class Servico(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Nome completo do serviço', unique=True)
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2, help_text='Preço do serviço')
    descricao = models.TextField('Descrição', max_length=300, help_text='Descrição e observações do serviço')
    produto = models.ManyToManyField('produtos.Produto', through='servicos.ProdutosServico')

    @property
    def produtos(self):
        return ProdutosServico.objects.filter(servico=self)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = [Upper('nome')]

    def __str__(self):
        return self.nome

class ProdutosServico(models.Model):
    servico = models.ForeignKey('servicos.Servico', verbose_name='Serviço', help_text='Nome do Serviço', on_delete=models.CASCADE, related_name='servico')
    produto = models.ForeignKey('produtos.Produto', verbose_name='Produto', help_text='Nome do Produto', on_delete=models.PROTECT, related_name='produto')
    quantidade = models.DecimalField('Quantidade', max_digits=5, decimal_places=2, help_text='Quantidade utilizada do produto')

    class Meta:
        verbose_name = 'Produto Servico'
        verbose_name_plural = 'Produtos Servicos'

    def __str__(self):
        return f'{self.produto}'

class OrdemServicos(models.Model):
    SITUACAO_OPCOES = (
        ('A', 'Agendado'),
        ('R', 'Realizado'),
        ('C', 'Cancelado'),
    )
    agendamento = models.ForeignKey('agendamentos.Agendamento', verbose_name='Agendamento', on_delete=models.CASCADE, related_name='agendamento')
    servico = models.ForeignKey('servicos.Servico', verbose_name='Serviço', on_delete=models.PROTECT, related_name='ordem_servico')
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name='Funcionário', on_delete=models.PROTECT, related_name='funcionario')
    situacao = models.CharField('Situação', max_length=1, choices=SITUACAO_OPCOES, default='A')
    observacoes = models.TextField('Observações', max_length=300, blank=True, null=True)
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2, help_text='Preço do serviço', default=0.00)

    class Meta:
        verbose_name ='Serviço realizado'
        verbose_name_plural = 'Serviços realizados'

        constraints = [models.UniqueConstraint(fields=['agendamento', 'servico'], name='constraint_agendamento')]

    def __str__(self):
        return self.servico.nome

    def calcular_valor_ordem(self):
        valor_total = 0
        qs = OrdemServicos.objects.filter(agendamento=self.agendamento)
        for item in qs:
            if item.situacao != 'C':
                valor_total += item.preco
        self.agendamento.valor = valor_total
        self.agendamento.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.preco = self.servico.preco
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        self.calcular_valor_ordem()

    def delete(self, using=None, keep_parents=False):
        super().delete(using=None, keep_parents=False)
        self.calcular_valor_ordem()