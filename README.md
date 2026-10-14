# ArtemisBlanck

O **ArtemisBlanck** é uma plataforma para gerenciamento de Trabalhos de Conclusão de Curso (TCC), desenvolvida para facilitar a interação entre alunos e orientadores.

O sistema permite o cadastro e autenticação de usuários, consulta de orientadores e agendamento de reuniões, incluindo integração com o Google Calendar para consulta de disponibilidade.

Nesta etapa do projeto foram implementados e testados os componentes **Orientador** e **Reunião**, juntamente com suas interfaces.

---

## Componentes implementados

### Orientador

O componente **Orientador** é responsável por consultar os orientadores cadastrados no sistema e disponibilizar suas informações.

**Interface fornecida:**

- `iOrientador`

**Operação implementada:**

- `ListarOrientadores()`: retorna os orientadores cadastrados, incluindo nome, e-mail, área de atuação e quantidade de vagas.

> A operação `VerificarVagas()`, prevista na modelagem anterior, está relacionada ao fluxo de cadastro de TCC. Como essa funcionalidade ainda não foi implementada, ela não faz parte do escopo desta entrega.

---

### Reunião

O componente **Reunião** é responsável pela consulta de horários disponíveis e pelo registro de reuniões entre alunos e orientadores.

**Interface fornecida:**

- `iReuniao`

**Operações implementadas:**

- `MostrarAgenda()`: retorna os horários disponíveis de um orientador em uma determinada data.
- `RegistrarReuniao()`: registra uma reunião entre um aluno e um orientador.

**Interface requerida:**

- `iOrientador`: utilizada pelo componente Reunião para acessar as operações fornecidas pelo componente Orientador.

---

## Comunicação entre os componentes

O componente **Reunião** utiliza a interface `iOrientador`, fornecida pelo componente **Orientador**.

```text
Reunião
   |
   | requer
   v
iOrientador
   |
   | fornecida por
   v
Orientador
```

Na implementação, o componente `Reuniao` recebe uma implementação de `IOrientador`:

```python
componente_orientador = Orientador()
componente_reuniao = Reuniao(componente_orientador)
```

Dessa forma, o componente Reunião pode utilizar as operações disponibilizadas pelo componente Orientador através de sua interface.

---

## Integração com Google Calendar

O sistema utiliza a API do Google Calendar para consultar a disponibilidade dos orientadores e criar os eventos correspondentes às reuniões.

O fluxo de consulta da agenda ocorre da seguinte forma:

```text
Aluno
  |
  v
Reunião
  |
  v
MostrarAgenda()
  |
  v
Google Calendar API
  |
  v
Horários disponíveis
```

Após a escolha de um horário disponível, o evento é criado no Google Calendar e a reunião é registrada no banco de dados com o status `AGENDADA`.

---

## Estrutura do projeto

```text
backend/
├── componentes/
│   ├── __init__.py
│   ├── orientador.py
│   └── reuniao.py
│
├── interfaces/
│   ├── __init__.py
│   ├── iorientador.py
│   └── ireuniao.py
│
├── cadastro.py
├── google_calendar.py
├── login.py
└── main.py

tests/
├── __init__.py
├── test_orientador.py
├── test_reuniao.py
└── test_integracao.py
```

---

## Tecnologias utilizadas

- Python
- FastAPI
- Supabase / PostgreSQL
- Google Calendar API
- Jinja2
- HTML
- CSS
- Pytest

---

## Instalação

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd NOME_DO_PROJETO
```

### 2. Criar um ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

---

## Configuração do Google Calendar

Para utilizar as funcionalidades relacionadas à agenda, é necessário configurar as credenciais da API do Google Calendar.

O arquivo:

```text
credentials_web.json
```

deve ser colocado na raiz do projeto.

Por questões de segurança, esse arquivo não está incluído no repositório.

O orientador também precisa conectar sua conta Google ao Artemis para que sua disponibilidade possa ser consultada.

---

## Executando o sistema

Na raiz do projeto, execute:

```bash
python -m uvicorn backend.main:app --reload
```

Depois acesse no navegador:

```text
http://127.0.0.1:8000
```

---

## Fluxo para testar a aplicação

1. Inicie o servidor.
2. Faça login como orientador.
3. Conecte a conta do orientador ao Google Calendar.
4. Faça login como aluno.
5. Acesse a lista de orientadores.
6. Selecione um orientador.
7. Acesse a agenda do orientador.
8. Escolha uma data.
9. Selecione um dos horários disponíveis.
10. Confirme o agendamento.
11. Verifique a reunião registrada.

---

## Testes automatizados

Foram implementados testes para verificar as operações dos componentes e a integração entre eles.

Os testes estão localizados na pasta:

```text
tests/
```

### Instalar o Pytest

Antes de executar os testes, é necessário instalar o Pytest:

```bash
python -m pip install pytest
```

### Executar os testes

Para executar todos os testes:

```bash
python -m pytest -v
```

Os testes verificam:

- listagem de orientadores;
- consulta da agenda de um orientador;
- comportamento para orientador inexistente;
- registro de uma reunião;
- integração entre os componentes Reunião e Orientador.

As dependências externas, como Supabase e Google Calendar, são simuladas nos testes utilizando mocks, permitindo testar os componentes sem depender de serviços externos.

---

## Resultado

A implementação até agora  permite consultar os orientadores cadastrados, verificar horários disponíveis através do Google Calendar e registrar reuniões entre alunos e orientadores, futuramente serão implementadas novas funcionalidades como cadastro de TCC, tarefas, feebacks e notificação por e-mail.
