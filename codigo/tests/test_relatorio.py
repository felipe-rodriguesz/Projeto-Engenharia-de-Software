import os
import sys
import tempfile
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codigo.relatorio import GeradorRelatorio


class TestGeradorRelatorio(unittest.TestCase):

    def test_valores_da_alocacao_usam_formato_brasileiro(self):
        resultado = SimpleNamespace(
            renda_bruta=5000.0,
            total_despesas=1000.0,
            sobra_mensal=4000.0,
            perfil="moderado",
            alocacao={"Renda Fixa Curto Prazo": 1234.56},
            anos_projecao=1,
            patrimonio_projetado=15000.0,
        )
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "relatorio.txt")
            GeradorRelatorio(caminho).gerar_txt(resultado)
            with open(caminho, encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

        self.assertIn("Renda Fixa Curto Prazo: R$ 1.234,56", conteudo)


if __name__ == "__main__":
    unittest.main()
