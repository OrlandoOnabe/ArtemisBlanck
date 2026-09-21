# Modelagem de Componentes

## 1. Diagrama de Casos de Uso
![UC](UC_Artemis.png)


## 2. Análise dos Fluxos dos Casos de Uso

### Aplicar Feedback

| Caso de Uso | Fluxo analisado | Operação identificada |
|---|---|---|
| Aplicar Feedback | 1. O orientador deve realizar login na plataforma.<br>2. O orientador deve acessar a lista de TCCs sob sua orientação.<br>3. O sistema deve mostrar os TCCs vinculados àquele orientador.<br>4. O orientador deve selecionar um TCC.<br>5. O sistema mostra o quadro com as tarefas daquele TCC.<br>6. O orientador seleciona a tarefa que deseja avaliar.<br>7. O orientador escreve o feedback no campo de escrita.<br>8. O orientador deve selecionar a opção de "Enviar Feedback".<br>9. O sistema valida as informações.<br>10. O sistema registra o feedback.<br>11. O sistema disponibiliza o feedback ao aluno e o notifica por e-mail.<br>12. O sistema confirma a aplicação do feedback. | 3: `+ListarTCCsOrientados()`<br>5: `+MostrarTarefas()`<br>9: `+ValidarDadosFeedback()`<br>10: `+RegistrarFeedback()`<br>11: `+EnviarNotificacao()` |

### Criar Tarefa

| Caso de Uso | Fluxo analisado | Operação identificada |
|---|---|---|
| Criar Tarefa | 1. O aluno deve fazer login na plataforma.<br>2. O aluno deve acessar o seu TCC.<br>3. O sistema mostra as informações do TCC.<br>4. O aluno deve entrar na aba tarefas.<br>5. O sistema mostra o quadro de tarefas do seu TCC.<br>6. O aluno deve clicar em criar tarefa.<br>7. O aluno informa os dados associados à tarefa.<br>8. O aluno clica em confirmar.<br>9. O sistema valida os dados informados.<br>10. O sistema cria a tarefa com status "A Fazer". | 3: `+VerTCC()`<br>5: `+MostrarTarefas()`<br>9: `+ValidarDadosTarefa()`<br>10: `+CriarTarefa()` |

### Cadastrar TCC

| Caso de Uso | Fluxo analisado | Operação identificada |
|---|---|---|
| Cadastrar TCC | 1. O aluno deve fazer login na plataforma.<br>2. O aluno deve entrar na aba de cadastrar TCC.<br>3. O sistema apresenta o formulário de cadastro de TCC.<br>4. O aluno informa o título e demais informações sobre o TCC.<br>5. O aluno clica para selecionar um orientador.<br>6. O sistema mostra a lista de orientadores.<br>7. O aluno seleciona um orientador.<br>8. O sistema verifica se o orientador possui vagas.<br>9. O aluno confirma o cadastro de TCC.<br>10. O sistema valida as informações.<br>11. O sistema envia uma solicitação para o professor orientador.<br>12. O sistema confirma o envio da solicitação.<br>13. O orientador aceita a solicitação.<br>14. O sistema registra o TCC e o associa ao aluno e ao orientador. | 6: `+ListarOrientadores()`<br>8: `+VerificarVagas()`<br>10: `+ValidarDadosTCC()`<br>11: `+EnviarNotificacao()`<br>14: `+CadastrarTCC()` |

### Agendar Reunião

| Caso de Uso | Fluxo analisado | Operação identificada |
|---|---|---|
| Agendar Reunião | 1. O aluno realiza o login na plataforma.<br>2. O aluno acessa a opção "Orientadores".<br>3. O sistema apresenta a lista de orientadores cadastrados.<br>4. O aluno verifica as informações dos orientadores, como área de atuação e número de vagas.<br>5. O aluno seleciona um orientador.<br>6. O sistema apresenta as informações do orientador e abre o calendário com os horários disponíveis.<br>7. O aluno seleciona um horário.<br>8. O aluno confirma o agendamento.<br>9. O sistema registra a reunião associada ao aluno e orientador.<br>10. O sistema adiciona a reunião ao calendário.<br>11. O sistema envia uma notificação sobre a reunião para aluno e orientador.<br>12. O sistema confirma o agendamento. | 3: `+ListarOrientadores()`<br>6: `+MostrarAgenda()`<br>9: `+RegistrarReuniao()`<br>11: `+EnviarNotificacao()` |

## 3. Agrupamento das Operações

Agrupe as operações identificadas de acordo com responsabilidades relacionadas.

| Responsabilidade | Operações relacionadas |
|---|---|
| **Gerenciar Orientadores** | `+ListarOrientadores()`, `+VerificarVagas()` |
| **Gerenciar TCC** | `+CadastrarTCC()`, `+ValidarDadosTCC()`, `+ListarTCCsOrientados()`, `+VerTCC()` |
| **Gerenciar Feedback** | `+RegistrarFeedback()`, `+ValidarDadosFeedback()` |
| **Gerenciar Notificações** | `+EnviarNotificacao()` |
| **Gerenciar Tarefas** | `+MostrarTarefas()`, `+ValidarDadosTarefa()`, `+CriarTarefa()` |
| **Gerenciar Reuniões** | `+MostrarAgenda()`, `+RegistrarReuniao()` |

## 4. Identificação dos Componentes

| Componente | Responsabilidade | Operações realizadas |
|---|---|---|
| **Orientador** | Consultar orientadores e verificar sua disponibilidade | `+ListarOrientadores()`<br>`+VerificarVagas()` |
| **Reunião** | Controlar o agendamento e horário de reuniões entre aluno e orientador | `+RegistrarReuniao()`<br>`+MostrarAgenda()` |
| **TCC** | Cadastrar e consultar TCCs | `+CadastrarTCC()`<br>`+VerTCC()`<br>`+ListarTCCsOrientados()`<br>`+ValidarDadosTCC()` |
| **Tarefa** | Criar e acompanhar as tarefas relacionadas ao TCC | `+MostrarTarefas()`<br>`+ValidarDadosTarefa()`<br>`+CriarTarefa()` |
| **Feedback** | Registrar e disponibilizar feedbacks dos orientadores para alunos | `+ValidarDadosFeedback()`<br>`+RegistrarFeedback()` |
| **Notificações** | Enviar notificações sobre eventos importantes aos usuários | `+EnviarNotificacao()` |


## 5. Interfaces

| Interface | Componente | Tipo | Operações |
|---|---|---|---|
| `IOrientador` | Orientador | Fornecida | `+ListarOrientadores()`<br>`+VerificarVagas()` |
| `IReuniao` | Reunião | Fornecida | `+RegistrarReuniao()`<br>`+MostrarAgenda()` |
| `ITCC` | TCC | Fornecida | `+CadastrarTCC()`<br>`+VerTCC()`<br>`+ValidarDadosTCC()`<br>`+ListarTCCsOrientados()` |
| `ITarefa` | Tarefa | Fornecida | `+MostrarTarefas()`<br>`+ValidarDadosTarefa()`<br>`+CriarTarefa()` |
| `IFeedback` | Feedback | Fornecida | `+ValidarDadosFeedback()`<br>`+RegistrarFeedback()` |
| `INotificacao` | Notificações | Fornecida | `+EnviarNotificacao()` |
| `IOrientador` | Reunião | Requerida | `+ListarOrientadores()` |
| `IOrientador` | TCC | Requerida | `+ListarOrientadores()`<br>`+VerificarVagas()` |
| `INotificacao` | Reunião | Requerida | `+EnviarNotificacao()` |
| `ITCC` | Tarefa | Requerida | `+VerTCC()` |
| `ITCC` | Feedback | Requerida | `+ListarTCCsOrientados()` |
| `ITarefa` | Feedback | Requerida | `+MostrarTarefas()` |
| `INotificacao` | Feedback | Requerida | `+EnviarNotificacao()` |
| `INotificacao` | TCC | Requerida | `+EnviarNotificacao()` |


## 6. Dependências entre Componentes

As dependências entre os componentes foram identificadas a partir das interfaces requeridas e fornecidas.

| Componente | Depende de | Interface utilizada | Justificativa |
|---|---|---|---|
| **Reunião** | Orientador | `IOrientador` | Necessita consultar os orientadores e suas informações para permitir que o aluno escolha com quem deseja agendar uma reunião. |
| **Reunião** | Notificação | `INotificacao` | Após o agendamento da reunião, necessita solicitar o envio de notificações ao aluno e ao orientador. |
| **TCC** | Orientador | `IOrientador` | Necessita listar os orientadores e verificar a existência de vagas antes de enviar uma solicitação de orientação. |
| **TCC** | Notificação | `INotificacao` | Necessita enviar uma notificação ao orientador solicitando a aprovação do cadastro do TCC com ele como orientador. |
| **Tarefa** | TCC | `ITCC` | As tarefas são vinculadas a um TCC, sendo necessário acessar as informações do TCC ao criar e visualizar suas tarefas. |
| **Feedback** | TCC | `ITCC` | O orientador precisa visualizar a lista de TCCs sob sua orientação para selecionar em qual deseja registrar o feedback. |
| **Feedback** | Tarefa | `ITarefa` | O feedback pode ser associado às tarefas do TCC, sendo necessário visualizar as tarefas para selecionar aquela que será avaliada. |
| **Feedback** | Notificação | `INotificacao` | Após o registro de um feedback, necessita solicitar o envio de uma notificação ao aluno. |


## 7. Diagrama de Componentes

![componentes](Componentes_artemis.png)


## 8. Rastreabilidade da Modelagem

Visão resumida da relação entre os elementos identificados:

**Caso de Uso → Operação → Responsabilidade → Interface → Componente**

| Caso de Uso | Operação | Responsabilidade | Interface | Componente |
|---|---|---|---|---|
| **Agendar Reunião** | `ListarOrientadores()` | Consultar orientadores e suas informações | `IOrientador` | Orientador |
| **Agendar Reunião** | `MostrarAgenda()` | Mostrar o calendário com data e horário para reuniões | `IReuniao` | Reunião |
| **Agendar Reunião** | `RegistrarReuniao()` | Guardar o agendamento e horário de reuniões | `IReuniao` | Reunião |
| **Agendar Reunião** | `EnviarNotificacao()` | Enviar notificações sobre reuniões agendadas | `INotificacao` | Notificação |
| **Aplicar Feedback** | `ListarTCCsOrientados()` | Listar os TCCs orientados pelo orientador | `ITCC` | TCC |
| **Aplicar Feedback** | `MostrarTarefas()` | Mostrar quadro de tarefas do TCC orientado para escolher em qual o feedback será aplicado | `ITarefa` | Tarefa |
| **Aplicar Feedback** | `ValidarDadosFeedback()` | Validar os dados do feedback antes do registro | `IFeedback` | Feedback |
| **Aplicar Feedback** | `RegistrarFeedback()` | Registrar e disponibilizar feedbacks dos orientadores para alunos | `IFeedback` | Feedback |
| **Aplicar Feedback** | `EnviarNotificacao()` | Enviar notificações sobre feedbacks registrados | `INotificacao` | Notificação |
| **Criar Tarefa** | `VerTCC()` | Consultar informações do TCC | `ITCC` | TCC |
| **Criar Tarefa** | `MostrarTarefas()` | Mostrar o quadro de tarefas do TCC | `ITarefa` | Tarefa |
| **Criar Tarefa** | `ValidarDadosTarefa()` | Validar dados da tarefa a ser criada | `ITarefa` | Tarefa |
| **Criar Tarefa** | `CriarTarefa()` | Criar e registrar a nova tarefa no quadro | `ITarefa` | Tarefa |
| **Cadastrar TCC** | `ListarOrientadores()` | Listar os orientadores que estão cadastrados | `IOrientador` | Orientador |
| **Cadastrar TCC** | `VerificarVagas()` | Verificar a disponibilidade do orientador selecionado | `IOrientador` | Orientador |
| **Cadastrar TCC** | `ValidarDadosTCC()` | Validar os dados do TCC a ser cadastrado | `ITCC` | TCC |
| **Cadastrar TCC** | `EnviarNotificacao()` | Enviar notificação solicitando ao professor a aprovação do cadastro do TCC com ele como orientador | `INotificacao` | Notificação |
| **Cadastrar TCC** | `CadastrarTCC()` | Cadastrar o novo TCC vinculado ao aluno e orientador | `ITCC` | TCC |
