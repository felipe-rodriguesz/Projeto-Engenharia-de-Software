import math
from typing import Dict

class GerenciadorOrcamento:
    """
    Entidade do Core responsável por estruturar, validar e processar
    o balanço orçamentário e a capacidade de poupança do usuário.
    """
    def __init__(self, renda_bruta: float) -> None:
        if not math.isfinite(renda_bruta) or renda_bruta <= 0:
            raise ValueError("A renda bruta inicial deve ser finita e maior que zero.")
        self._renda_bruta: float = renda_bruta
        self._despesas: Dict[str, float] = {}

    def adicionar_despesa(self, categoria: str, valor: float) -> None:
        categoria_limpa = categoria.strip().lower()
        if not categoria_limpa:
            raise ValueError("A categoria da despesa não pode estar vazia.")
        if not math.isfinite(valor) or valor <= 0:
            raise ValueError("O valor da despesa deve ser finito e maior que zero.")
        total_categoria = self._despesas.get(categoria_limpa, 0.0) + valor
        if not math.isfinite(total_categoria):
            raise ValueError("O total da categoria deve ser finito.")
        self._despesas[categoria_limpa] = total_categoria

    def obter_despesas(self) -> Dict[str, float]:
        return self._despesas.copy()

    def calcular_total_despesas(self) -> float:
        return sum(self._despesas.values())

    def verificar_orcamento_estourado(self) -> bool:
        """Retorna True se as despesas superarem ou igualarem a renda bruta."""
        return self.calcular_total_despesas() >= self._renda_bruta

    def calcular_sobra_liquida(self) -> float:
        """Calcula a margem financeira real disponível."""
        sobra = self._renda_bruta - self.calcular_total_despesas()
        return round(sobra, 2)
