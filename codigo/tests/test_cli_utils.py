import contextlib
import io
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codigo import cli_utils


class TestCliUtils(unittest.TestCase):

    def test_float_invalido_retorna_ao_prompt(self):
        with patch("builtins.input", side_effect=["texto", "nan", "inf", "-1", "0", "125,50"]):
            with contextlib.redirect_stdout(io.StringIO()):
                valor = cli_utils.ler_float_obrigatorio("Valor: ")

        self.assertEqual(valor, 125.5)

    def test_inteiro_positivo_invalido_retorna_ao_prompt(self):
        with patch("builtins.input", side_effect=["abc", "0", "3"]):
            with contextlib.redirect_stdout(io.StringIO()):
                valor = cli_utils.ler_int_positivo("Anos: ")

        self.assertEqual(valor, 3)

    def test_opcao_invalida_retorna_ao_prompt(self):
        with patch("builtins.input", side_effect=["x", "b"]):
            with contextlib.redirect_stdout(io.StringIO()):
                valor = cli_utils.ler_opcao("Resposta: ", ["a", "b", "c"])

        self.assertEqual(valor, "b")


if __name__ == "__main__":
    unittest.main()
