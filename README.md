# Criação da API com docker:

- Esse README possui o intuito de auxiliar na criação da API usando Django Rest Framework, PostgreSQL e Docker. Baseado nesse vídeo: https://youtu.be/UKZWWTqj-Vs?si=TB111Z2S4aB_nkQk

# Primeiros passos:

Inicialmente é preciso rodar, e ativar o ambiente virtual:

```ps1
python -m venv venv

.\venv\Scripts\activate.ps1 
```
Logo em seguida iremos acessar a venv, e realizar a instalação do Django,  realizar a atualização do pip, instalação do Django Rest Framework e a instalação de nosso banco de dados postgreSQL:

```ps1
cd venv

python -m pip install Django 

python.exe -m pip install --upgrade pip 

pip install djangorestframework 

pip install psycop2-binary==2.9.6 
```
Em seguida podemos sair da venv e realizar a criação do projeto e do nosso app:

```ps1
cd ..

django-admin startproject djangoconfig .

python manage.py startapp userapp 
```
# Configurações de nosso requirements.txt

- Como iremos utilizar o um Dockerfile em nossa aplicação, é extremamente importante que já possamos modificar nosso requirements com as bibliotecas que iremos usar. Como isso é apenas um teste utilizando poucas bibliotecas, ele ficará assim:

```ps1
Django==4.2
psycopg2-binary==2.9.6
djangorestframework==3.14.0
```

# Criação do Arquivo django.sh

- Para realizar as mudanças de migrações automaticamente, será preciso criar uma  arquivo django.sh que terá as seguintes configurações:

```ps1
#!/bin/bash
echo "Create migrations"
python manage.py makemigrations userapp
echo "=================================="

echo "Migrate"
python manage.py migrate 
echo "=================================="

echo "Start server"
python manage.py runserver 0.0.0.0:8000
```

# Criação do Arquivo Dockerfile

- Esse arquivo servirá para colocarmos as informações necessarias para realizar a integração do arquivo com o docker. (No vídeo citado anteriormente, esse arquivo é de outra forma, mas acaba não funcionando, esse aqui listado abaixo, possui modificações)

```ps1
FROM python:3.11.6-alpine3.17

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip \
    && apk del gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && rm -rf /var/cache/apk/*

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD ["sh", "/app/django.sh"]
```
# Criação do Arquivo docker-compose.yml

- Juntamente com o Dockerfile, também é de extrema importância a criação desse arquivo para que a intregração com o docker funcione corretamente.

```ps1
version: '4.2'

services:
  userapp:
    container_name: userapp
    build: .
    ports:
      - "8000:8000"
    environment:
      - PG_USER=postgres
      - PG_PASSWORD=postgres
      - PG_DB=postgres
      - PG_HOST=db
      - PG_PORT=5432
    depends_on:
      - db
  db:
    container_name: db
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    ports:
      - "5431:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata: {}
```

# Configurações no settings.py

- Como nosso app já foi criado, e também nosso banco de dados e nossa api, será preciso realizar algumas alterações no nosso ```settings.py```.

primeiramente adicionando logo no topo esse import:

```ps1
import os
```

Logo após podemos adicionar na parte de ```INSTALLED_APPS```:

```ps1
    'userapp',
    'rest_framework',
```

E para finalizar essa parte de configurações, iremos coloca o direcionamento para nosso banco de dados postgreSQL:

```ps1
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_DRIVER', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('PG_DB', 'postgres'),
        'USER': os.environ.get('PG_USER', 'postgres'),
        'PASSWORD': os.environ.get('PG_PASSWORD', 'postgres'),
        'HOST': os.environ.get('PG_HOST', 'localhost'),
        'PORT': os.environ.get('PG_PORT', '5432'),
    }
}
```

# Configurações basicas de nossa api:

Primeiramente iremos configurar nossa ```urls.py``` de nosso projeto:

```ps1

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('userapp.urls')),
]

```

Em seguida indo para nosso APP, iremos adicionar o arquivo ```serializers.py```:

```ps1
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
```

Depois partiremos para nosso ```models.py```:

```ps1
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
```

Após a antiga modificação, iremos adicionar ao nosso app o arquivo ```urls.py```:

```ps1
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getUsers),
    path('create', views.addUser),
    path('read/<str:pk>', views.getUser),
    path('update/<str:pk>', views.updateUser),
    path('delete/<str:pk>', views.deleteUser),
]
```

E para finalizar essa parte de configuração, vamos para nosso ```views.py```:

```ps1
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

# Create your views here.

#get all users
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

#get single user
@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

#add user
@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

#update user
@api_view(['PUT'])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

#delete user
@api_view(['DELETE'])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    
    return Response('Item successfully deleted!')
```

# Comandos para realizar o teste no docker:

-Logo após todas as configurações, iremos testar toda a integração com o docker, para isso precisaremos ter o docker instalado.

primeiramente iremos entrar no diretorio de nosso projeto:

```ps1
cd djangoconfig
```

Logo após iremos listar os volumes de nosso docker:

```ps1
docker volume ls
```

Em seguida iremos criar o conteiner DB:

```ps1
docker compose up -d db
```

Logo após iremos criar o container do APP:

```ps1
docker compose build userapp
```

E para finalizar iremos subir o mesmo para verificar se tudo correu bem:

```ps1
docker compose up userapp
```

Realizando essa última etapa e dando certo, podemos ir nesse link e verificar se está tudo certo:

```ps1
http://127.0.0.1:8000/users/

http://127.0.0.1:8000/admin/
```


> Todos os conhecimentos colocados nessa documentação foram absorvidos através do vídeo citado anteriormente, e de pesquisas realizadas pelo backend do projeto: SaúdeKids