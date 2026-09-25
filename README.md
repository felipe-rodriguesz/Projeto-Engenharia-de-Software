# InvestPlan

Planejador financeiro em Python para organizar um orçamento mensal e simular uma estratégia de alocação de aportes. O projeto é uma aplicação de linha de comando desenvolvida como protótipo acadêmico de Engenharia de Software.

## Problema

Quem está começando a organizar as finanças pode ter dificuldade para entender quanto sobra da renda depois das despesas e como distribuir esse valor. O InvestPlan reúne esses cálculos em um fluxo simples no terminal.

## Como funciona

O usuário informa a renda mensal, cadastra despesas com categorias livres, responde a três perguntas de perfil de risco e escolhe o prazo da projeção. O sistema calcula a sobra, interrompe a simulação se as despesas forem iguais ou superiores à renda, estima um perfil, distribui a sobra entre classes genéricas de ativos e calcula um patrimônio projetado. Ao final, grava os dados da sessão em JSON e gera um relatório em texto.

Também é possível importar vários cenários de um arquivo CSV. O arquivo [clientes_teste.csv](codigo/clientes_teste.csv) contém exemplos de entrada para essa opção.

## Funcionalidades implementadas

- Menu interativo com opção para iniciar uma simulação, importar CSV ou sair.
- Cálculo de despesas totais e sobra mensal, com bloqueio quando não há sobra positiva.
- Questionário de três perguntas e classificação conservadora, moderada ou arrojada. Respostas de aversão/necessidade de resgate imediato nas duas primeiras perguntas forçam o perfil conservador.
- Distribuição fixa da sobra: conservador (70% renda fixa de curto prazo, 30% de longo prazo), moderado (50%, 30% e 20% em ativos de risco) e arrojado (30%, 20% e 50%).
- Projeção composta mensal por prazo informado pelo usuário.
- Persistência local em `codigo/dados_usuario.json` e relatório em `codigo/plano_investplan.txt`.
- Importação em lote com colunas `Renda`, `Despesas`, `Resposta1`, `Resposta2`, `Resposta3` e `AnosProjecao`. Despesas no CSV usam pares `Categoria:Valor` separados por ponto e vírgula.

## Organização

| Caminho | Responsabilidade |
|---|---|
| `codigo/main.py` | Interface de terminal e fluxo principal, incluindo importação CSV |
| `codigo/facade.py` | Orquestra orçamento, perfil, alocação, projeção, persistência e relatório |
| `codigo/orcamento.py` | Validação e cálculo de despesas e sobra |
| `codigo/perfil_risco.py` | Perguntas e classificação do perfil |
| `codigo/motor_investimento.py` | Estratégias de alocação (Strategy) |
| `codigo/projecao.py` | Cálculo da projeção patrimonial |
| `codigo/persistencia.py` | Leitura e gravação do estado em JSON |
| `codigo/relatorio.py` | Geração do relatório `.txt` |
| `codigo/cli_utils.py` | Formatação de mensagens e validação do menu |
| `codigo/tests/` | Testes unitários com `unittest` |
| `docs/` | Requisitos acadêmicos, decisões de arquitetura e estratégia de testes |

## Requisitos

- Python 3.9 ou superior.
- Nenhuma dependência externa. A aplicação e os testes usam a biblioteca padrão do Python.

## Executar

Na raiz do repositório:

```bash
cd codigo
python3 main.py
```

Para usar outro CSV, coloque o arquivo em `codigo/` e informe seu nome ao selecionar a opção de importação.

## Testes

Na raiz do repositório:

```bash
python3 -m unittest discover -s codigo/tests -v
```

Os testes cobrem regras selecionadas de orçamento, perfil de risco, alocação e projeção. Não há testes automatizados para a interface CLI, fachada, persistência ou geração do relatório.

## Limitações e premissas

- A classificação e os percentuais de alocação são regras fixas do protótipo, não uma avaliação financeira individual.
- As taxas mensais usadas na projeção são fixas no código: 0,8% para renda fixa de curto prazo, 0,9% para renda fixa de longo prazo e 1,2% para ativos de risco. A simulação não consulta dados de mercado, não considera impostos, inflação, taxas ou variação real dos ativos e não representa promessa de rentabilidade.
- O cálculo aplica o rendimento mensal depois de adicionar cada aporte mensal ao saldo; essa é a convenção usada pela implementação.
- As despesas são categorias livres; cadastrar novamente uma categoria substitui o valor anterior. A interface aceita entradas numéricas diretamente e pode encerrar a simulação corrente se o formato for inválido.
- A persistência é local e não criptografada. O arquivo `dados_usuario.json` na raiz é um exemplo versionado; a execução grava em `codigo/dados_usuario.json`.
- A importação CSV espera o cabeçalho e o formato descritos acima. Não há integração com corretoras, cotações, autenticação ou banco de dados.

## Equipe

- Elder Nunes Gonçalves
- Felipe dos Santos Rodrigues
- Guilherme Giuliangeli Monteiro

## Documentação

- [Arquitetura](docs/arquitetura.md)
- [Requisitos e elicitação](docs/requisitos.md)
- [Estratégia e cobertura de testes](docs/testes.md)
