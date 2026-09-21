# Modelagem de Componentes

## 1. Análise dos Fluxos dos Casos de Uso

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


## 2. Identificação dos Componentes

| Componente | Responsabilidade | Operações realizadas |
|---|---|---|
| **Orientador** | Consultar orientadores e verificar sua disponibilidade | `+ListarOrientadores()`<br>`+VerificarVagas()` |
| **Reunião** | Controlar o agendamento e horário de reuniões entre aluno e orientador | `+RegistrarReuniao()`<br>`+MostrarAgenda()` |
| **TCC** | Cadastrar e consultar TCCs | `+CadastrarTCC()`<br>`+VerTCC()`<br>`+ListarTCCsOrientados()`<br>`+ValidarDadosTCC()` |
| **Tarefa** | Criar e acompanhar as tarefas relacionadas ao TCC | `+MostrarTarefas()`<br>`+ValidarDadosTarefa()`<br>`+CriarTarefa()` |
| **Feedback** | Registrar e disponibilizar feedbacks dos orientadores para alunos | `+ValidarDadosFeedback()`<br>`+RegistrarFeedback()` |
| **Notificações** | Enviar notificações sobre eventos importantes aos usuários | `+EnviarNotificacao()` |


## 3. Interfaces

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


## 4. Diagrama de Componentes

![componentes](Componentes_artemis.png)
