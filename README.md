# Engenharia-de-Software

# Django Application Setup Guide

Este guia descreve os passos necessários para configurar e rodar a aplicação Django.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em seu ambiente:

- [Python 3.12+](https://www.python.org/downloads/)
- [pip (Python package manager)](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Git](https://git-scm.com/)

## Passo a passo

### 1. Criar e ativar o ambiente virtual

Crie um ambiente virtual para garantir que as dependências da sua aplicação sejam isoladas:

```bash
# Crie o ambiente virtual no Windows
python -m venv venv

# Crie o ambiente virtual no Linux
python3 -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
```

### 2. Instalar as dependências do projeto

Com o ambiente virtual ativado, instale todas as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Dentro do arquivo `.env`, configure os valores adequados para o banco de dados e outras variáveis necessárias.


### 3. Configurar o banco de dados

#### 3.1. Migrar as tabelas existentes para o banco de dados

Com o ambiente virtual ativado e as configurações ajustadas no arquivo `.env`, você precisará aplicar as migrações para criar as tabelas no banco de dados.

Primeiro, aplique as migrações já existentes:

```bash
python manage.py migrate
```

#### 3.2. Fazer migrações do modelo atual

Se houver alguma alteração no modelo de dados, crie novas migrações:

```bash
python manage.py makemigrations
```

Depois, aplique essas novas migrações com o comando:

```bash
python manage.py migrate
```

### 4. Executar o servidor de desenvolvimento

Agora que o banco de dados está configurado, você pode iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará rodando por padrão no endereço [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### 5. Criar superusuário (opcional)

Se precisar acessar o painel administrativo do Django, crie um superusuário com o comando:

```bash
python manage.py createsuperuser
```
<br/>

### Caso queira começar com o banco de dados populado
### Windows
```python
python utils\create-educadores.py
```
### Linux
```python
python3 utils\create-educadores.py
```
---
<i>Haverá já um superusuário criado e também um educador.<i/>
> **Super usuário**:
> `login:` admin 
> `senha:` admin 
> **Educador**:
> `login:` educ1 
> `senha:` educ1 
--- 

