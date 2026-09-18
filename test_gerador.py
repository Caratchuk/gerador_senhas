import string
import unittest

from src.gerador import ESPECIAIS, OpcoesGeracao, gerar_senha
from src.validador import validar_senha


class TestGerarSenha(unittest.TestCase):
    def test_tamanho_respeitado(self):
        senha = gerar_senha(OpcoesGeracao(tamanho=24))
        self.assertEqual(len(senha), 24)

    def test_senha_padrao_e_muito_forte(self):
        senha = gerar_senha()
        resultado = validar_senha(senha)
        self.assertEqual(resultado.classificacao, "Muito forte")

    def test_senha_gerada_nao_se_repete(self):
        senhas = {gerar_senha() for _ in range(50)}
        self.assertEqual(len(senhas), 50)  # nenhuma colisão em 50 gerações

    def test_apenas_numeros_quando_outras_categorias_desativadas(self):
        opcoes = OpcoesGeracao(
            tamanho=10,
            incluir_maiusculas=False,
            incluir_minusculas=False,
            incluir_numeros=True,
            incluir_especiais=False,
        )
        senha = gerar_senha(opcoes)
        self.assertTrue(all(c in string.digits for c in senha))

    def test_contem_ao_menos_um_caractere_de_cada_categoria_ativada(self):
        senha = gerar_senha(OpcoesGeracao(tamanho=12))
        self.assertTrue(any(c.isupper() for c in senha))
        self.assertTrue(any(c.islower() for c in senha))
        self.assertTrue(any(c.isdigit() for c in senha))
        self.assertTrue(any(c in ESPECIAIS for c in senha))

    def test_nenhuma_categoria_selecionada_gera_erro(self):
        opcoes = OpcoesGeracao(
            incluir_maiusculas=False,
            incluir_minusculas=False,
            incluir_numeros=False,
            incluir_especiais=False,
        )
        with self.assertRaises(ValueError):
            gerar_senha(opcoes)

    def test_tamanho_menor_que_categorias_gera_erro(self):
        with self.assertRaises(ValueError):
            gerar_senha(OpcoesGeracao(tamanho=2))  # 4 categorias ativas por padrão


if __name__ == "__main__":
    unittest.main()
