from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PerguntaRisco:
    """DTO (Data Transfer Object) para trafegar as perguntas sem usar dicionários soltos."""
    id: int
    enunciado: str
    opcoes: Dict[str, str]

class AvaliadorPerfilRisco:
    """
    Classe responsável pela regra de negócio que define o perfil do investidor.
    Não contém interação com o usuário (sem prints ou inputs).
    """

    def obter_questionario(self) -> List[PerguntaRisco]:
        """Retorna a lista de perguntas oficiais do sistema."""
        return [
            PerguntaRisco(
                id=1,
                enunciado="Quando você imagina que vai precisar resgatar a maior parte desse dinheiro investido?",
                opcoes={
                    "a": "Em menos de 1 ano ou a qualquer emergência.",
                    "b": "Entre 1 e 5 anos.",
                    "c": "Só daqui a muitos anos (mais de 5 anos)."
                }
            ),
            PerguntaRisco(
                id=2,
                enunciado="Os investimentos de maior retorno oscilam. Como você reagiria se seu patrimônio caísse 15% em um mês?",
                opcoes={
                    "a": "Entraria em pânico e tiraria tudo. Não aceito perder dinheiro.",
                    "b": "Ficaria desconfortável, mas esperaria para ver se recupera.",
                    "c": "Aproveitaria a queda para comprar mais barato (foco no longo prazo)."
                }
            ),
            PerguntaRisco(
                id=3,
                enunciado="Qual é o seu principal objetivo ao começar a investir esse dinheiro?",
                opcoes={
                    "a": "Proteger o meu dinheiro. A segurança vem em primeiro lugar.",
                    "b": "Crescimento constante, misturando segurança com um pouco de risco.",
                    "c": "Fazer o dinheiro render o máximo possível, aceitando os riscos."
                }
            )
        ]

    def calcular_perfil(self, respostas: List[str]) -> str:
        """
        Recebe uma lista de opções ['a', 'b', 'c'] e calcula o perfil.
        Aplica a regra de Fail-Fast para aversão a risco ou liquidez imediata.
        """
        if not respostas or len(respostas) != 3:
            raise ValueError("O questionário exige exatamente 3 respostas para calcular o perfil.")

        if any(not isinstance(resp, str) or resp.strip().lower() not in {"a", "b", "c"} for resp in respostas):
            raise ValueError("As respostas do questionário devem ser a, b ou c.")

        r1, r2, r3 = [resp.lower().strip() for resp in respostas]

        if r1 == 'a' or r2 == 'a':
            return "conservador"

        tabela_pontos = {
            1: {'b': 2, 'c': 3},
            2: {'b': 2, 'c': 3},
            3: {'a': 1, 'b': 2, 'c': 3}
        }

        score = 0
        score += tabela_pontos[1].get(r1, 0)
        score += tabela_pontos[2].get(r2, 0)
        score += tabela_pontos[3].get(r3, 0)

        if score <= 6:
            return "moderado"
        else:
            return "arrojado"
