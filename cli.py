"""
Interface de linha de comando.

    python -m src.cli gerar --tamanho 20
    python -m src.cli validar "MinhaSenha123!"
"""

import argparse
import getpass

from src.gerador import OpcoesGeracao, gerar_senha
from src.validador import validar_senha


def _comando_gerar(args: argparse.Namespace) -> None:
    opcoes = OpcoesGeracao(
        tamanho=args.tamanho,
        incluir_maiusculas=not args.sem_maiusculas,
        incluir_minusculas=not args.sem_minusculas,
        incluir_numeros=not args.sem_numeros,
        incluir_especiais=not args.sem_especiais,
    )
    senha = gerar_senha(opcoes)
    print(senha)

    if args.avaliar:
        resultado = validar_senha(senha)
        print(f"Classificação: {resultado.classificacao}")


def _comando_validar(args: argparse.Namespace) -> None:
    senha = args.senha or getpass.getpass("Digite a senha a validar (não será exibida): ")
    resultado = validar_senha(senha)

    print(f"Classificação: {resultado.classificacao} ({resultado.pontuacao}/{resultado.total_regras})")
    if resultado.regras_faltando:
        print("Ainda falta:")
        for regra in resultado.regras_faltando:
            print(f"  - {regra}")
    else:
        print("Atende a todos os critérios.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerador e validador de senhas seguras")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    p_gerar = subparsers.add_parser("gerar", help="Gera uma senha segura aleatória")
    p_gerar.add_argument("--tamanho", type=int, default=16)
    p_gerar.add_argument("--sem-maiusculas", action="store_true")
    p_gerar.add_argument("--sem-minusculas", action="store_true")
    p_gerar.add_argument("--sem-numeros", action="store_true")
    p_gerar.add_argument("--sem-especiais", action="store_true")
    p_gerar.add_argument(
        "--avaliar", action="store_true", help="Também mostra a classificação da senha gerada"
    )
    p_gerar.set_defaults(func=_comando_gerar)

    p_validar = subparsers.add_parser("validar", help="Avalia a força de uma senha")
    p_validar.add_argument("senha", nargs="?", help="Se omitido, é pedida via prompt oculto")
    p_validar.set_defaults(func=_comando_validar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
