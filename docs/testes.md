# Estratégia de Testes Automatizados — InvestPlan

> Este documento registra a estratégia acadêmica de testes e a cobertura existente no repositório. As tabelas abaixo descrevem os casos atualmente implementados, não uma cobertura planejada.

---

## 1. Estratégia e Ferramental Escolhido

Para a suíte de testes do InvestPlan, optamos pela biblioteca nativa do Python **`unittest`**. A escolha arquitetural se baseou em dois fatores principais:

- **Integração direta com a linguagem**, sem exigir dependências externas;
- **Forte adequação ao padrão de testes orientados a objetos** (xUnit).

Os testes são testes unitários de caixa branca para partes do núcleo de negócio. Eles validam os casos enumerados abaixo; não cobrem o fluxo completo nem garantem por si só a confiabilidade financeira do sistema.

---

## 2. Cobertura atual

Os casos existentes incluem cenários de sucesso, borda e falha em diferentes proporções por módulo.

### `motor_investimento.py` — Felipe

| Tipo | Descrição |
|------|-----------|
| ✅ Sucesso | Distribuição da estratégia arrojada para aporte de R$ 1.000,00. |
| ⚠️ Borda | Rejeição de sobra igual a zero. |
| ❌ Falha | Tipo de entrada incompatível (texto). |

### `orcamento.py` e `projecao.py` — Guilherme

| Tipo | Descrição |
|------|-----------|
| ✅ Sucesso | Soma de despesas e cálculo da sobra; projeção por um ano. |
| ⚠️ Borda | Despesas iguais à renda, valores com centavos, aportes zerados/negativos e prazo de 50 anos. |
| ❌ Falha | Renda ou despesa inválida e prazo de projeção menor ou igual a zero. |

### `perfil_risco.py` — Elder

| Tipo | Descrição |
|------|-----------|
| ✅ Sucesso | Classificação conservadora, moderada e arrojada. |
| ⚠️ Borda | Regra *fail-fast* nas duas primeiras respostas, limite entre perfis e normalização de maiúsculas/espaços. |
| ❌ Falha | Lista vazia, quantidade incorreta de respostas e tipos incompatíveis. |

---

## 3. Lacunas Não Cobertas e Tratamento de Exceções

Não há testes automatizados para a interface CLI, fachada, persistência de dados ou geração de relatório.

### Camada CLI — `main.py`

Não foram implementados testes que simulam o input do teclado (`input()`) ou capturam os prints no console. A interface é volátil e testes de UI neste momento gerariam alto custo de manutenção.

### Camada de Arquivos — `relatorio.py`

A geração de arquivos `.txt` (como o `plano_investplan.txt`) não é coberta pelo `unittest`.

### Justificativa e Mitigação

O relatório usa gravação por arquivo temporário seguido de `os.replace()`. Essa implementação não substitui testes de I/O e não se aplica à persistência JSON, que grava diretamente no arquivo.
