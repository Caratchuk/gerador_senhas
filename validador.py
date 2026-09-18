"""
Validação de força de senha.

Cada regra é uma função independente que recebe a senha e devolve
True/False 

import re
from dataclasses import dataclass, field

TAMANHO_MINIMO = 8


def tem_tamanho_minimo(senha: str) -> bool:
    return len(senha) >= TAMANHO_MINIMO


def tem_letra_maiuscula(senha: str) -> bool:
    return bool(re.search(r"[A-Z]", senha))


def tem_letra_minuscula(senha: str) -> bool:
    return bool(re.search(r"[a-z]", senha))


def tem_numero(senha: str) -> bool:
    return bool(re.search(r"\d", senha))


def tem_caractere_especial(senha: str) -> bool:
    return bool(re.search(r"[!@#$%^&*()\-_=+\[\]{};:,.<>?/\\|~]", senha))


REGRAS = {
    f"Ter pelo menos {TAMANHO_MINIMO} caracteres": tem_tamanho_minimo,
    "Ter ao menos uma letra maiúscula": tem_letra_maiuscula,
    "Ter ao menos uma letra minúscula": tem_letra_minuscula,
    "Ter ao menos um número": tem_numero,
    "Ter ao menos um caractere especial": tem_caractere_especial,
}


@dataclass
class ResultadoValidacao:
    pontuacao: int  # 0 a len(REGRAS): quantas regras foram atendidas
    total_regras: int
    regras_atendidas: list[str] = field(default_factory=list)
    regras_faltando: list[str] = field(default_factory=list)

    @property
    def classificacao(self) -> str:
        proporcao = self.pontuacao / self.total_regras
        if proporcao == 1:
            return "Muito forte"
        if proporcao >= 0.8:
            return "Forte"
        if proporcao >= 0.6:
            return "Média"
        if proporcao >= 0.4:
            return "Fraca"
        return "Muito fraca"

    @property
    def valida(self) -> bool:
        """Considerada aceitável se atender a todas as regras."""
        return self.pontuacao == self.total_regras


def validar_senha(senha: str) -> ResultadoValidacao:
    atendidas = [descricao for descricao, regra in REGRAS.items() if regra(senha)]
    faltando = [descricao for descricao in REGRAS if descricao not in atendidas]
    return ResultadoValidacao(
        pontuacao=len(atendidas),
        total_regras=len(REGRAS),
        regras_atendidas=atendidas,
        regras_faltando=faltando,
    )
