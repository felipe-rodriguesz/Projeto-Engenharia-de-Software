# Requisitos — InvestPlan

> **Responsabilidades de preenchimento:**
> - **Elder** → Seção 1 (Elicitação)
> - **Felipe** → Seção 2 (Histórias de Usuário)
> - **Guilherme** → Seção 3 (Validação)

> **Nota sobre o escopo implementado:** Este arquivo preserva os requisitos, hipóteses e protótipos levantados durante o trabalho acadêmico; nem todos foram implementados. A versão atual recebe renda bruta, despesas em categorias livres, três respostas de risco e um prazo de projeção. Não calcula descontos CLT/PJ, não exige oito categorias e não aplica os limites de renda descritos nas RN-01 a RN-04. O fluxo de CLI e o exemplo da seção 3.4 são propostas de requisito, não uma transcrição da interface atual. A RN-08 também diverge: a implementação usa taxas mensais fixas por classe de ativo, não uma taxa anual por perfil. Consulte o README para o comportamento atual.

---

## 1. Síntese da Elicitação
**Responsável:** Elder

### 1.1 Técnicas de Elicitação Utilizadas

- Pesquisa de Similares (análise de 6 sistemas no mercado)
- Análise de Documentos Técnicos (ANBIMA, CVM)
- Consulta a Comunidades (Reddit r/investimentos)
- Análise de Padrões de Domínio (regras de educação financeira)

---

### 1.2 Análise de Similares

| Sistema Analisado | O que faz | Limitação identificada | O que o InvestPlan resolve |
|---|---|---|---|
| Nubank App | Rastreia gastos por categoria, relatórios mensais | Não oferece recomendação de investimento | Integra controle de gastos + alocação de investimentos |
| Minhas Economias | Agregador de contas + análise de orçamento | Recomendações genéricas sem personalização | Alocação personalizada por perfil de risco |
| Calculadoras Online | Simulam crescimento com taxa fixa | Não calculam capacidade de poupança | Integra orçamento → poupança → simulação em um fluxo |
| Apps de Renda Fixa | Interface para compra de títulos | Não ajudam a estruturar orçamento | Recomenda tipo de ativo (Tesouro vs CDB vs ETF) |
| Planilhas Excel/Sheets | Controle manual com fórmulas | Requer conhecimento técnico; manual | Automatiza em Python; saída consistente |
| Micro-Investimento | Aportes automáticos pequenos | Não diagnosticam orçamento | Diagnóstico completo antes de investir |

---

### 1.3 Regras de Negócio Identificadas

**RN-01:** A renda mensal bruta deve ser >= R$ 1.000,00 e <= R$ 1.000.000,00. Se abaixo do mínimo, o sistema exibe aviso.

**RN-02:** Os gastos devem ser categorizados em 8 categorias obrigatórias: Moradia, Alimentação, Transporte, Saúde, Educação, Lazer e Cultura, Contas Fixas e Outros.

**RN-03:** A soma total de gastos não pode exceder a renda líquida. Se exceder, o sistema alerta e solicita revisão.

**RN-04:** Renda Líquida = Renda Bruta - Desconto Tributário. CLT: 11,5% | PJ/Autônomo: 20%.

**RN-05:** Poupança Mensal = Renda Líquida - Soma de Gastos. Se <= 0, o sistema marca "Déficit Orçamentário" e bloqueia investimentos.

**RN-06:** O questionário de perfil terá peso por resposta. Pontuação baixa define perfil Conservador, média Moderado e alta Arrojado. Se o usuário informar necessidade de resgate em menos de 1 ano, o perfil é forçado para Conservador, anulando a pontuação.

**RN-07:** A alocação da poupança seguirá proporções fixas baseadas no perfil do usuário. Para o perfil Conservador: 100% em Renda Fixa (sendo 70% Curto Prazo e 30% Longo Prazo).

**RN-08 (requisito original):** O cálculo de projeção de patrimônio utilizará a fórmula de juros compostos com aportes mensais constantes, assumindo uma taxa de retorno anual simulada atrelada ao perfil de risco. A implementação atual usa taxas mensais fixas por classe de ativo, conforme descrito no README.

---

### 1.4 Fontes Consultadas na Elicitação

1. **ANBIMA - Raio X do Investidor Brasileiro (9ª Edição)**
   - Aproximadamente 31% da população não possui nenhum tipo de reserva financeira.
   - Forte dependência de canais digitais e influenciadores para tomada de decisão em novos investidores, justificando a necessidade de uma ferramenta técnica e isenta.

2. **CVM - Perfil e Comportamento dos Investidores 2024**
   - Crescimento de 42% no interesse por educação financeira
   - Objetivo principal: formação de reserva de emergência e aposentadoria

3. **Comunidade r/investimentos (Reddit)**
   - "Paralisia por análise" é barreira central para iniciantes
   - Usuários buscam "regras matemáticas" e "calculadoras estruturadas"

---

## 2. Histórias de Usuário

> _Responsável: **Felipe**_
>
> **Legenda de prioridade:** Alta = essencial para o fluxo principal / Média = importante mas não bloqueante / Baixa = desejável
>
> **Legenda de sprint:** Sprint 3 = desenvolvimento principal / Sprint 4 = refinamento

---

### HU-01 — Otimização Orçamentária e Cálculo de Sobra

**Como** um adulto em fase de organização financeira,
**Quero** inserir minha renda mensal e despesas básicas no terminal,
**Para** descobrir minha capacidade real de poupança mensal.

**Regras de negócio relacionadas:** RN-01, RN-02, RN-03, RN-04, RN-05

**Critérios de Aceite:**
- [ ] CA-01: O sistema deve solicitar a entrada do valor da renda mensal líquida.
- [ ] CA-02: O sistema deve permitir que o usuário insira o valor total estimado de gastos.
- [ ] CA-03: O sistema deve calcular a diferença (Renda - Gastos) e exibir a sobra disponível.
- [ ] CA-04: Se a sobra calculada for menor ou igual a zero, o sistema deve emitir um aviso de "Orçamento Estourado", bloquear o avanço para a etapa de investimentos e orientar o corte de gastos.

**Prioridade:** Alta | **Sprint prevista:** Sprint 3

---

### HU-02 — Definição do Perfil de Risco

**Como** um iniciante em investimentos,
**Quero** responder a um questionário rápido sobre prazos e tolerância a perdas,
**Para** que o sistema identifique adequadamente o meu perfil de investidor.

**Regras de negócio relacionadas:** RN-06

**Critérios de Aceite:**
- [ ] CA-01: O sistema deve exibir perguntas de múltipla escolha diretamente no terminal.
- [ ] CA-02: Se o usuário selecionar opções que indicam aversão total à perda de capital ou prazo menor que 1 ano, o perfil deve ser forçado para "Conservador".
- [ ] CA-03: O sistema deve registrar e exibir o perfil final (Conservador, Moderado ou Arrojado).

**Prioridade:** Alta | **Sprint prevista:** Sprint 3

---

### HU-03 — Recomendação de Alocação de Recursos (Strategy)

**Como** um usuário com capacidade de poupança positiva,
**Quero** receber uma sugestão detalhada de onde investir meu dinheiro,
**Para** começar a investir com segurança de acordo com o meu perfil.

**Regras de negócio relacionadas:** RN-07

**Critérios de Aceite:**
- [ ] CA-01: O sistema deve processar a "sobra mensal" (HU-01) e o perfil (HU-02) para injetar na estratégia correta de cálculo.
- [ ] CA-02: Para o perfil Conservador, a sobra deve ser dividida em Renda Fixa Curta (70%) e Renda Fixa Longo Prazo (30%), exibindo os valores em R$ no terminal.
- [ ] CA-03: A saída no terminal deve exibir os valores recomendados em Reais (R$), mostrando a divisão exata baseada na sobra do usuário.

**Prioridade:** Alta | **Sprint prevista:** Sprint 3

---

### HU-04 — Geração de Relatório Financeiro

**Como** um usuário que concluiu a análise,
**Quero** que o sistema consolide todas as informações em um relatório,
**Para** que eu tenha um registro claro do meu plano de ação financeiro.

**Regras de negócio relacionadas:** RN-08

**Critérios de Aceite:**
- [ ] CA-01: O sistema deve gerar um resumo contendo: Renda, Gastos, Sobra, Perfil de Risco e a Estratégia de Alocação recomendada, além da projeção de patrimônio.
- [ ] CA-02: O sistema deve oferecer a opção de salvar esse relatório em um arquivo de texto estruturado (ex: `.txt` ou `.csv`) no diretório local.

**Prioridade:** Média | **Sprint prevista:** Sprint 3

---

### HU-05 — Tratamento de Entradas Inválidas no Terminal

**Como** um usuário interagindo com uma interface de texto,
**Quero** ser alertado caso eu digite um formato de dado incorreto,
**Para** que o sistema não trave inesperadamente (crash) e eu possa corrigir a informação.

**Regras de negócio relacionadas:** N/A (Requisito Não-Funcional / Engenharia)

**Critérios de Aceite:**
- [ ] CA-01: Se o sistema pedir um número (ex: Renda) e o usuário digitar letras ou símbolos, o sistema deve exibir a mensagem de erro "Entrada inválida. Por favor, digite apenas números."
- [ ] CA-02: Após o erro, o sistema deve repetir a pergunta original sem encerrar a execução do programa.

**Prioridade:** Alta | **Sprint prevista:** Sprint 4

---

### 2.1 Backlog Priorizado

| # | História | Prioridade | Sprint |
|---|---|---|---|
| HU-01 | Otimização Orçamentária e Cálculo de Sobra | Alta | Sprint 3 |
| HU-02 | Definição do Perfil de Risco | Alta | Sprint 3 |
| HU-03 | Recomendação de Alocação de Recursos | Alta | Sprint 3 |
| HU-05 | Tratamento de Entradas Inválidas no Terminal | Alta | Sprint 4 |
| HU-04 | Geração de Relatório Financeiro | Média | Sprint 3 |

---

## 3. Validação dos Requisitos

> _Responsável: **Guilherme**_

### 3.1 Ambiguidades Encontradas

| ID | HU(s) afetada(s) | Descrição da ambiguidade | Resolução adotada |
|---|---|---|---|
| AMB-01 | HU-01 | O termo "Gastos Básicos/Estimados" na descrição da HU não deixa claro se o usuário digita um valor único consolidado ou se deve detalhar por categorias. | Ficou definido que a interface CLI solicitará obrigatoriamente os gastos divididos nas 8 categorias descritas na RN-02, realizando a soma de forma automática para o cálculo da sobra. |
| AMB-02 | HU-02 | O critério de aceite CA-02 fala em "opções que indicam aversão total à perda". Quais opções ou pesos exatos no questionário definem isso de forma matemática? | O questionário terá 5 perguntas com pontuações de 1 a 3. Se a pergunta específica de tolerância a quedas receber a resposta de peso mínimo (aversão total), o perfil será forçado para Conservador, independente da soma das outras respostas. |
| AMB-03 | HU-04 | O CA-02 menciona "salvar em arquivo de texto estruturado (ex: `.txt` ou `.csv`)", deixando o formato definitivo em aberto. | Para manter o alinhamento com os requisitos de persistência e escopo do projeto, o sistema exportará um arquivo legível `.txt` para o usuário e salvará o estado interno em um arquivo estruturado `.json`. |

### 3.2 Conflitos Identificados

| ID | HUs em conflito | Descrição do conflito | Resolução adotada |
|---|---|---|---|
| CONF-01 | HU-03 vs Lógica de Alocação | A HU-03 (CA-02) prevê uma saída simplificada no terminal exibindo apenas o valor global de 100% em Renda Fixa. No entanto, o plano do algoritmo de negócios prevê uma granularidade maior, subdividindo esse montante em Renda Fixa Curta e Longa. Embora ambos sejam Renda Fixa, há uma divergência no nível de detalhamento da exibição. | Foi definido que o critério de aceite CA-02 da HU-03 será refinado para que a interface de texto detalhe as subcategorias de prazo em Reais (R$), garantindo que a exibição no terminal reflita fielmente o algoritmo matemático completo de alocação de carteira. |
| CONF-02 | HU-01 vs RN-05 | A HU-01 (CA-01) estipula que o sistema deve solicitar diretamente a renda líquida. Contudo, a RN-04 determina que o usuário insere a renda bruta e o sistema calcula a líquida com base nos descontos fiscais. Além disso, a HU-01 (CA-04) bloqueia o avanço se a sobra for <= 0$, enquanto a RN-05 apenas classifica como "Déficit Orçamentário". | Ficou adotado o fluxo do protótipo (Seção 3.4): a CLI solicitará a renda bruta (conforme RN-04) e aplicará o cálculo automático. O bloqueio total de avanço só ocorrerá se a sobra final calculada for >= 0$ (em estrito cumprimento da RN-05). Se a sobra for positiva, mas abaixo de 10% da renda líquida, o sistema emitirá um alerta preventivo de baixa poupança, mas permitirá prosseguir.|

### 3.3 Questões em Aberto

As questões abaixo foram registradas durante a elicitação. QA-02 foi decidida na implementação com taxas mensais fixas em `projecao.py`; QA-01 e QA-03 permanecem fora do fluxo implementado.

| ID | Descrição da questão | Impacto | Responsável | Prazo |
|---|---|---|---|---|
| QA-01 | Como o sistema deve se comportar caso o arquivo de persistência local (`dados_usuario.json`) esteja corrompido ou com formato inválido na inicialização? | Pode causar um *crash* no sistema logo na inicialização, violando o princípio de robustez do terminal. | Guilherme | 02/06 (Sprint 2) |
| QA-02 | As taxas de retorno assumidas para as projeções de patrimônio (ex: 10% a.a. para Renda Fixa) serão estáticas no código (hardcoded) ou carregadas de um arquivo de configuração parametrizável? | Impacta a facilidade de manutenção e escrita de testes automatizados na Sprint 4. | Elder | 09/06 (Sprint 3) |
| QA-03 | Caso o usuário cadastre múltiplos objetivos de investimento cujas metas financeiras somadas ultrapassem drasticamente a projeção de sua capacidade real de poupança, o sistema deve sugerir o reajuste de todos ou priorizar por ordem de cadastro? | Afeta a lógica algorítmica do Módulo de Recomendação/Relatório (HU-04). | Felipe | 09/06 (Sprint 3) |

### 3.4 Protótipo de Fluxo no Terminal

```text
======================================================================
                     INVESTPLAN - SIMULADOR FINANCEIRO                
======================================================================

[1] Identificação do Regime de Trabalho:
Selecione seu regime:
(1) CLT (Desconto estimado de 11.5%)
(2) PJ / Autônomo (Desconto estimado de 20.0%)
Escolha: 1

[2] Coleta de Dados Financeiros:
Digite sua renda mensal bruta (R$): 5000.00
--- Carga tributária aplicada. Renda Líquida estimada: R$ 4425.00 ---

Informe seus gastos mensais por categoria:
1. Moradia (Aluguel, IPTU, Condomínio): R$ 1200.00
2. Alimentação (Supermercado, Restaurantes): R$ 600.00
3. Transporte (Combustível, Transporte Público): R$ 300.00
4. Saúde (Plano de Saúde, Farmácia): R$ 200.00
5. Educação (Faculdade, Cursos): R$ 400.00
6. Lazer e Cultura (Streaming, Viagens): R$ 300.00
7. Contas Fixas (Água, Luz, Internet): R$ 250.00
8. Outros Gastos: R$ 150.00

======================================================================
                        DIAGNÓSTICO FINANCEIRO                        
======================================================================
Soma Total de Gastos: R$ 3400.00
Sobra Mensal Disponível (Poupança Real): R$ 1025.00
Taxa de Poupança: 23.16% da renda líquida.

[ALERTA] Gasto com Moradia compromete 27.12% da renda líquida (Limite: 30%).
[OK] Gasto com Essenciais compromete 53.11% da renda líquida (Limite: 60%).
[OK] Capacidade de poupança adequada para iniciar investimentos (> 10%).

Deseja responder ao questionário de Perfil de Risco? (S/N): S

======================================================================
                         QUESTIONÁRIO DE PERFIL                       
======================================================================
Pergunta 1: Se seu investimento caísse 20% em um mês, o que você faria?
(1) Venderia imediatamente para evitar mais perdas.
(2) Manteria o investimento aguardando a recuperação.
(3) Compraria mais unidades aproveitando o preço baixo.
Escolha: 1

[... demais perguntas ...]

Seu Perfil de Investidor é: CONSERVADOR

======================================================================
                       ESTRATÉGIA DE ALOCAÇÃO                         
======================================================================
Com base na sua sobra de R$ 1025.00 e perfil CONSERVADOR, aloque:

- Renda Fixa Curta (70%): R$ 717.50 / mês
  -> Sugestão: Tesouro SELIC ou CDB 100% CDI com liquidez diária.
  
- Renda Fixa Longo Prazo (30%): R$ 307.50 / mês
  -> Sugestão: Tesouro IPCA+ ou CDB Pós-fixado.

- Ativos de Risco / Ações (0%): R$ 0.00 / mês

======================================================================
                  PROJEÇÃO DE PATRIMÔNIO (CENÁRIO BASE)               
======================================================================
Mantendo o aporte constante de R$ 1025.00/mês:
- Em 1 ano:  R$ 12.981,25
- Em 5 anos: R$ 81.110,43
- Em 10 anos: R$ 221.750,18

Deseja exportar o relatório detalhado (.txt)? (S/N): S
[Sucesso] Relatório salvo como 'plano_investplan.txt' no diretório local.

Obrigado por utilizar o InvestPlan! Finalizando o sistema...
======================================================================
