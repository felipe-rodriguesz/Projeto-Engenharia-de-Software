import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codigo.facade import InvestPlanFacade


class TestInvestPlanFacade(unittest.TestCase):

    def test_falha_de_persistencia_interrompe_fluxo(self):
        facade = InvestPlanFacade()
        with patch("codigo.facade.GerenciadorDados.salvar_sessao_completa", return_value=False):
            with patch.object(facade.gerador_relatorio, "gerar_txt") as gerar_relatorio:
                with self.assertRaisesRegex(RuntimeError, "Não foi possível salvar"):
                    facade.processar_simulacao_completa(
                        renda=5000.0,
                        despesas={"aluguel": 1000.0},
                        respostas_risco=["b", "b", "b"],
                        anos_projecao=1,
                    )

        gerar_relatorio.assert_not_called()


if __name__ == "__main__":
    unittest.main()
