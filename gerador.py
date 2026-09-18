"""
Geração de senhas seguras aleatórias.

Usa `secrets` (não `random`) porque `random` não é seguro para fins
criptográficos — detalhe importante para quem quer mostrar atenção a
boas práticas de segurança num projeto de portfólio.
"""

import secrets
import string
from dataclasses import dataclass

LETRAS_MAIUSCULAS = string.ascii_uppercase
LETRAS_MINUSCULAS = string.ascii_lowercase
NUMEROS = string.digits
ESPECIAIS = "!@#$%^&*()-_=+[]{};:,.<>?"


@dataclass
class OpcoesGeracao:
    tamanho: int = 16
    incluir_maiusculas: bool = True
    incluir_minusculas: bool = True
    incluir_numeros: bool = True
    incluir_especiais: bool = True

    def alfabeto(self) -> str:
        alfabeto = ""
        if self.incluir_maiusculas:
            alfabeto += LETRAS_MAIUSCULAS
        if self.incluir_minusculas:
            alfabeto += LETRAS_MINUSCULAS
        if self.incluir_numeros:
            alfabeto += NUMEROS
        if self.incluir_especiais:
            alfabeto += ESPECIAIS
        return alfabeto

    def grupos_obrigatorios(self) -> list[str]:
        """Um grupo por categoria ativada, para garantir que a senha
        gerada sempre contenha pelo menos um caractere de cada tipo
        pedido (gerar puramente ao acaso poderia, por azar, não sortear
        nenhum número, por exemplo)."""
        grupos = []
        if self.incluir_maiusculas:
            grupos.append(LETRAS_MAIUSCULAS)
        if self.incluir_minusculas:
            grupos.append(LETRAS_MINUSCULAS)
        if self.incluir_numeros:
            grupos.append(NUMEROS)
        if self.incluir_especiais:
            grupos.append(ESPECIAIS)
        return grupos


def gerar_senha(opcoes: OpcoesGeracao = OpcoesGeracao()) -> str:
    alfabeto = opcoes.alfabeto()
    if not alfabeto:
        raise ValueError("Selecione ao menos uma categoria de caractere")

    grupos = opcoes.grupos_obrigatorios()
    if opcoes.tamanho < len(grupos):
        raise ValueError(
            f"Tamanho ({opcoes.tamanho}) menor que o número de categorias exigidas ({len(grupos)})"
        )

    # Garante um caractere de cada categoria ativada...
    senha_chars = [secrets.choice(grupo) for grupo in grupos]
    # ...e completa o restante sorteando do alfabeto completo.
    senha_chars += [secrets.choice(alfabeto) for _ in range(opcoes.tamanho - len(grupos))]

    # Embaralha para que os caracteres "obrigatórios" não fiquem sempre no início.
    for i in range(len(senha_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        senha_chars[i], senha_chars[j] = senha_chars[j], senha_chars[i]

    return "".join(senha_chars)
