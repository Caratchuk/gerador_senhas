# Gerador e Validador de Senhas Seguras

Ferramenta de linha de comando em Python para gerar senhas
criptograficamente seguras e avaliar a força de senhas existentes
contra um conjunto de critérios configurável.

## Por que este projeto

Portfólio pequeno e focado, mostrando fundamentos de Python bem
aplicados: uso do módulo `secrets` (em vez de `random`, que não é
seguro para senhas), regras de validação desacopladas e testáveis
individualmente, e uma CLI com `argparse`.

## Como rodar

```bash
# gerar uma senha de 20 caracteres e já avaliar a força dela
python -m src.cli gerar --tamanho 20 --avaliar

# gerar só com letras e números (sem símbolos)
python -m src.cli gerar --sem-especiais

# validar uma senha (via argumento)
python -m src.cli validar "MinhaSenha123!"

# validar sem deixar a senha visível no terminal (prompt oculto)
python -m src.cli validar
```

## Testes

```bash
python -m unittest discover -s tests -v
```

13 testes cobrindo geração (tamanho, categorias ativas/inativas,
ausência de colisão em 50 gerações) e validação (cada regra
individualmente, classificação final).

## Estrutura

```
src/
  gerador.py    # geração de senha aleatória segura (secrets)
  validador.py  # regras de força de senha, cada uma testável isoladamente
  cli.py        # interface de linha de comando (argparse)
tests/
```

## Critérios de validação

- Pelo menos 8 caracteres
- Ao menos uma letra maiúscula
- Ao menos uma letra minúscula
- Ao menos um número
- Ao menos um caractere especial

Classificação final: Muito fraca / Fraca / Média / Forte / Muito forte,
proporcional a quantos critérios foram atendidos.
