from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

class Vacina(models.Model):
    id_vacina = models.AutoField(primary_key=True)
    tipo_vacina = models.CharField(max_length=50)
    profissional = models.CharField(max_length=50)
    data_vacina = models.DateField()  # Usando DateField para armazenar datas
    lote = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=50)
    data_fabricacao = models.DateField()  # Usando DateField para armazenar datas
    id_agendamento = models.CharField(max_length=50)