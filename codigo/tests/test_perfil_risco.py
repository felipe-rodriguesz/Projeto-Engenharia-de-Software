import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from codigo.perfil_risco import AvaliadorPerfilRisco

class TestAvaliadorPerfilRisco(unittest.TestCase):
    """Conjunto de testes unitários para a classe AvaliadorPerfilRisco."""

    def setUp(self):
        """Prepara a instância da classe antes de cada teste."""
        self.avaliador = AvaliadorPerfilRisco()

    def test_calcular_perfil_conservador_sucesso(self):
        """Testa o caminho feliz retornando perfil conservador via Fail-Fast na Q1."""
        resultado = self.avaliador.calcular_perfil(['a', 'b', 'c'])
        self.assertEqual(resultado, "conservador")

    def test_calcular_perfil_moderado_sucesso(self):
        """Testa o caminho feliz retornando perfil moderado com soma exata de 6 pontos."""
        resultado = self.avaliador.calcular_perfil(['b', 'b', 'b'])
        self.assertEqual(resultado, "moderado")

    def test_calcular_perfil_arrojado_sucesso(self):
        """Testa o caminho feliz retornando perfil arrojado com pontuação máxima."""
        resultado = self.avaliador.calcular_perfil(['c', 'c', 'c'])
        self.assertEqual(resultado, "arrojado")

    def test_calcular_perfil_borda_fail_fast_q2(self):
        """Testa limite de borda verificando o acionamento do Fail-Fast na segunda pergunta."""
        resultado = self.avaliador.calcular_perfil(['b', 'a', 'c'])
        self.assertEqual(resultado, "conservador")

    def test_calcular_perfil_borda_limite_score_exato(self):
        """Testa o limite matemático exato da transição entre os perfis moderado e arrojado."""
        self.assertEqual(self.avaliador.calcular_perfil(['b', 'c', 'a']), "moderado")
        self.assertEqual(self.avaliador.calcular_perfil(['b', 'c', 'b']), "arrojado")

    def test_calcular_perfil_borda_letras_maiusculas_espacos(self):
        """Testa a resiliência do método contra formatação incorreta, como letras maiúsculas e espaços."""
        resultado = self.avaliador.calcular_perfil([' B ', 'C', ' c '])
        self.assertEqual(resultado, "arrojado")

    def test_calcular_perfil_falha_lista_vazia(self):
        """Testa a falha forçada ao enviar uma lista vazia, aguardando um ValueError."""
        with self.assertRaises(ValueError):
            self.avaliador.calcular_perfil([])

    def test_calcular_perfil_falha_tamanho_invalido(self):
        """Testa a falha forçada ao enviar quantidade incorreta de respostas, aguardando um ValueError."""
        with self.assertRaises(ValueError):
            self.avaliador.calcular_perfil(['a', 'b'])
        with self.assertRaises(ValueError):
            self.avaliador.calcular_perfil(['a', 'b', 'c', 'd'])

    def test_calcular_perfil_falha_tipo_errado(self):
        """Rejeita opções e tipos que não pertencem ao questionário."""
        for respostas in (["a", "x", "c"], ["a", "b", "1"], [1, 2, 3]):
            with self.subTest(respostas=respostas):
                with self.assertRaises(ValueError):
                    self.avaliador.calcular_perfil(respostas)

if __name__ == '__main__':
    unittest.main()
