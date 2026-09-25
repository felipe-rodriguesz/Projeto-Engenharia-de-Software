import math
from typing import Dict

class SimuladorProjecao:
    """
    Componente matemático encarregado de simular a evolução patrimonial por meio
    de juros compostos mensais sobre o portfólio de investimentos alocado.
    """
    def __init__(self) -> None:
        self._taxas_mensais: Dict[str, float] = {
            "Renda Fixa Curto Prazo": 0.008, 
            "Renda Fixa Longo Prazo": 0.009,
            "Ativos de Risco": 0.012
        }

    def calcular_patrimonio_futuro(self, alocacao_mensal: Dict[str, float], anos: int) -> float:
        if not isinstance(anos, (int, float)) or not math.isfinite(anos) or anos <= 0:
            raise ValueError("O período para projeção deve ser de pelo menos 1 ano.")
        
        meses_totais = anos * 12
        patrimonio_total = 0.0

        for ativo, aporte_mensal in alocacao_mensal.items():
            if not math.isfinite(aporte_mensal):
                raise ValueError("Os aportes mensais devem ser valores finitos.")
            if aporte_mensal <= 0:
                continue
                
            taxa = self._taxas_mensais.get(ativo, 0.005)
            saldo_ativo = 0.0
            
            for _ in range(meses_totais):
                # Cada aporte mensal recebe rendimento no mesmo ciclo, conforme a fórmula do protótipo.
                saldo_ativo = (saldo_ativo + aporte_mensal) * (1 + taxa)
                
            patrimonio_total += saldo_ativo

        return round(patrimonio_total, 2)
