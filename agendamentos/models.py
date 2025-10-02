from django.db import models
from servicos.models import OrdemServicos

class Agendamento(models.Model):
    horario = models.DateTimeField('Horario', help_text='Data e hora do atendimento')
    cliente = models.ForeignKey('clientes.Cliente', verbose_name='Cliente', help_text='Nome do Cliente', on_delete=models.PROTECT)
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name='Funcionário', help_text='Nome do funcionário', on_delete=models.PROTECT)
    servicos = models.ManyToManyField('servicos.Servico', verbose_name='Serviço', through='agendamentos.OrdemServicos')
    valor = models.DecimalField('Valor total', max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField('Status', max_length=1, help_text='Status do agendamento', default='A')
    
    @property
    def servicos(self):
        return OrdemServicos.objects.filter(agendamento=self)

    class Meta:
        permissions = (('fechar_agendamento', 'Permite fazer o fechamento de um agendamento'),)
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-horario']
    
