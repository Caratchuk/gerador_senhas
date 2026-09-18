import unittest

from src.validador import validar_senha


class TestValidarSenha(unittest.TestCase):
    def test_senha_forte_atende_tudo(self):
        resultado = validar_senha("Senha!Forte123")
        self.assertTrue(resultado.valida)
        self.assertEqual(resultado.classificacao, "Muito forte")
        self.assertEqual(resultado.regras_faltando, [])

    def test_senha_curta_reprova_tamanho(self):
        resultado = validar_senha("Ab1!")
        self.assertFalse(resultado.valida)
        self.assertIn("Ter pelo menos 8 caracteres", resultado.regras_faltando)

    def test_senha_sem_numero(self):
        resultado = validar_senha("SenhaForte!")
        self.assertIn("Ter ao menos um número", resultado.regras_faltando)

    def test_senha_sem_maiuscula(self):
        resultado = validar_senha("senha123!")
        self.assertIn("Ter ao menos uma letra maiúscula", resultado.regras_faltando)

    def test_senha_sem_especial(self):
        resultado = validar_senha("SenhaForte123")
        self.assertIn("Ter ao menos um caractere especial", resultado.regras_faltando)

    def test_senha_totalmente_fraca(self):
        resultado = validar_senha("abc")
        self.assertEqual(resultado.classificacao, "Muito fraca")


if __name__ == "__main__":
    unittest.main()
