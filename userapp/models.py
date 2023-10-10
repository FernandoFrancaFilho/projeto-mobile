from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

class Profissional(models.Model):
    id_profissional_saude = models.CharField(max_length=150)
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.CharField(max_length=150)
    senha = models.CharField(max_length=150)
    telefone = models.CharField(max_length=11, unique=True)
    tipo_profissional = models.CharField(max_length=150)
    conselho = models.CharField(max_length=150)

class Vacina(models.Model):
    id_vacina = models.AutoField(primary_key=True)
    tipo_vacina = models.CharField(max_length=150)
    profissional = models.CharField(max_length=150)
    data_vacina = models.DateField()  # Usando DateField para armazenar datas
    lote = models.CharField(max_length=150)
    fabricante = models.CharField(max_length=150)
    data_fabricacao = models.DateField()  # Usando DateField para armazenar datas
    id_agendamento = models.CharField(max_length=150)

