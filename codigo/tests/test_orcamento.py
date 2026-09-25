import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from codigo.orcamento import GerenciadorOrcamento

class TestGerenciadorOrcamento(unittest.TestCase):

    def test_criacao_e_adicao_despesa_sucesso(self):
        """Cenário de Sucesso: Garante que o fluxo padrão de criação e inserção funciona."""
        orcamento = GerenciadorOrcamento(renda_bruta=5000.0)
        orcamento.adicionar_despesa("Aluguel", 1500.0)
        orcamento.adicionar_despesa(" Mercado ", 800.0) 

        despesas = orcamento.obter_despesas()
        self.assertEqual(despesas["aluguel"], 1500.0)
        self.assertEqual(despesas["mercado"], 800.0)
        self.assertEqual(orcamento.calcular_total_despesas(), 2300.0)
        self.assertEqual(orcamento.calcular_sobra_liquida(), 2700.0)

    def test_inicializacao_com_renda_invalida(self):
        """Cenário de Falha: Renda inicial menor ou igual a zero deve lançar ValueError."""
        with self.assertRaises(ValueError):
            GerenciadorOrcamento(renda_bruta=0)
        with self.assertRaises(ValueError):
            GerenciadorOrcamento(renda_bruta=-100.0)

    def test_adicionar_despesa_com_valores_invalidos(self):
        """Cenário de Falha: Categoria vazia ou valores negativos/zero devem lançar ValueError."""
        orcamento = GerenciadorOrcamento(renda_bruta=3000.0)
        
        with self.assertRaises(ValueError):
            orcamento.adicionar_despesa("", 500.0)
        with self.assertRaises(ValueError):
            orcamento.adicionar_despesa("Luz", 0.0)
        with self.assertRaises(ValueError):
            orcamento.adicionar_despesa("Internet", -50.0)

    def test_orcamento_exatamente_estourado_limite(self):
        """Cenário de Borda: Despesas EXATAMENTE iguais à renda bruta."""
        orcamento = GerenciadorOrcamento(renda_bruta=2000.0)
        orcamento.adicionar_despesa("Contas", 2000.0)
        
        self.assertTrue(orcamento.verificar_orcamento_estourado())
        
        self.assertEqual(orcamento.calcular_sobra_liquida(), 0.0)

    def test_valores_centas_e_pequenos(self):
        """Cenário de Borda: Valores com centavos e limites de precisão flutuante."""
        orcamento = GerenciadorOrcamento(renda_bruta=1000.05)
        orcamento.adicionar_despesa("Bala", 0.01)
        
        self.assertAlmostEqual(orcamento.calcular_sobra_liquida(), 1000.04, places=2)

    def test_categoria_repetida_soma_valores(self):
        orcamento = GerenciadorOrcamento(renda_bruta=5000.0)
        orcamento.adicionar_despesa(" Mercado ", 100.0)
        orcamento.adicionar_despesa("mercado", 50.0)

        self.assertEqual(orcamento.obter_despesas()["mercado"], 150.0)

    def test_rejeita_renda_e_despesas_nao_finitas(self):
        for valor in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    GerenciadorOrcamento(renda_bruta=valor)

                orcamento = GerenciadorOrcamento(renda_bruta=1000.0)
                with self.assertRaises(ValueError):
                    orcamento.adicionar_despesa("Contas", valor)

if __name__ == "__main__":
    unittest.main()
