import json
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP


# Dados fornecidos no desafio.
DADOS_VENDAS = {
    "vendas": [
        {"vendedor": "João Silva", "valor": 1200.50},
        {"vendedor": "João Silva", "valor": 950.75},
        {"vendedor": "João Silva", "valor": 1800.00},
        {"vendedor": "João Silva", "valor": 1400.30},
        {"vendedor": "João Silva", "valor": 1100.90},
        {"vendedor": "João Silva", "valor": 1550.00},
        {"vendedor": "João Silva", "valor": 1700.80},
        {"vendedor": "João Silva", "valor": 250.30},
        {"vendedor": "João Silva", "valor": 480.75},
        {"vendedor": "João Silva", "valor": 320.40},
        {"vendedor": "Maria Souza", "valor": 2100.40},
        {"vendedor": "Maria Souza", "valor": 1350.60},
        {"vendedor": "Maria Souza", "valor": 950.20},
        {"vendedor": "Maria Souza", "valor": 1600.75},
        {"vendedor": "Maria Souza", "valor": 1750.00},
        {"vendedor": "Maria Souza", "valor": 1450.90},
        {"vendedor": "Maria Souza", "valor": 400.50},
        {"vendedor": "Maria Souza", "valor": 180.20},
        {"vendedor": "Maria Souza", "valor": 90.75},
        {"vendedor": "Carlos Oliveira", "valor": 800.50},
        {"vendedor": "Carlos Oliveira", "valor": 1200.00},
        {"vendedor": "Carlos Oliveira", "valor": 1950.30},
        {"vendedor": "Carlos Oliveira", "valor": 1750.80},
        {"vendedor": "Carlos Oliveira", "valor": 1300.60},
        {"vendedor": "Carlos Oliveira", "valor": 300.40},
        {"vendedor": "Carlos Oliveira", "valor": 500.00},
        {"vendedor": "Carlos Oliveira", "valor": 125.75},
        {"vendedor": "Ana Lima", "valor": 1000.00},
        {"vendedor": "Ana Lima", "valor": 1100.50},
        {"vendedor": "Ana Lima", "valor": 1250.75},
        {"vendedor": "Ana Lima", "valor": 1400.20},
        {"vendedor": "Ana Lima", "valor": 1550.90},
        {"vendedor": "Ana Lima", "valor": 1650.00},
        {"vendedor": "Ana Lima", "valor": 75.30},
        {"vendedor": "Ana Lima", "valor": 420.90},
        {"vendedor": "Ana Lima", "valor": 315.40},
    ]
}

DADOS_ESTOQUE = {
    "estoque": [
        {"codigoProduto": 101, "descricaoProduto": "Caneta Azul", "estoque": 150},
        {"codigoProduto": 102, "descricaoProduto": "Caderno Universitário", "estoque": 75},
        {"codigoProduto": 103, "descricaoProduto": "Borracha Branca", "estoque": 200},
        {"codigoProduto": 104, "descricaoProduto": "Lápis Preto HB", "estoque": 320},
        {"codigoProduto": 105, "descricaoProduto": "Marcador de Texto Amarelo", "estoque": 90},
    ]
}

IDS_MOVIMENTACOES = set()


def dinheiro(valor):
    """Formata um número como moeda brasileira."""
    valor = Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"R$ {valor:.2f}".replace(".", ",")


def percentual_comissao(valor):
    if valor < 100:
        return Decimal("0")
    if valor < 500:
        return Decimal("0.01")
    return Decimal("0.05")


def calcular_comissoes():
    totais = {}

    for venda in DADOS_VENDAS["vendas"]:
        vendedor = venda["vendedor"]
        valor = Decimal(str(venda["valor"]))
        taxa = percentual_comissao(valor)
        comissao = valor * taxa

        if vendedor not in totais:
            totais[vendedor] = Decimal("0")
        totais[vendedor] += comissao

    print("\n--- COMISSÕES POR VENDEDOR ---")
    for vendedor, total in totais.items():
        print(f"{vendedor}: {dinheiro(total)}")


def encontrar_produto(codigo):
    for produto in DADOS_ESTOQUE["estoque"]:
        if produto["codigoProduto"] == codigo:
            return produto
    return None


def movimentar_estoque():
    print("\n--- MOVIMENTAÇÃO DE ESTOQUE ---")
    print("Produtos cadastrados:")
    for produto in DADOS_ESTOQUE["estoque"]:
        print(
            f"{produto['codigoProduto']} - {produto['descricaoProduto']} "
            f"(estoque atual: {produto['estoque']})"
        )

    try:
        numero = int(input("Número identificador da movimentação: "))
        codigo = int(input("Código do produto: "))
        tipo = input("Descrição da movimentação (entrada ou saída): ").strip().lower()
        quantidade = int(input("Quantidade movimentada: "))
    except ValueError:
        print("Os campos numéricos precisam ser informados corretamente.")
        return

    if numero in IDS_MOVIMENTACOES:
        print("Esse identificador já foi utilizado. Informe outro número.")
        return

    if quantidade <= 0:
        print("A quantidade deve ser maior que zero.")
        return

    produto = encontrar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    if tipo not in ("entrada", "saida", "saída"):
        print("A descrição deve ser 'entrada' ou 'saída'.")
        return

    eh_saida = tipo in ("saida", "saída")
    novo_estoque = produto["estoque"] - quantidade if eh_saida else produto["estoque"] + quantidade

    if novo_estoque < 0:
        print("Não é possível realizar a saída: estoque insuficiente.")
        return

    IDS_MOVIMENTACOES.add(numero)
    produto["estoque"] = novo_estoque
    print(f"Movimentação {numero} registrada com sucesso.")
    print(f"Produto: {produto['descricaoProduto']}")
    print(f"Estoque final: {produto['estoque']} unidade(s)")


def calcular_juros():
    print("\n--- CÁLCULO DE JUROS ---")
    try:
        valor = Decimal(input("Valor original da dívida: ").replace(",", "."))
        vencimento_texto = input("Data de vencimento (dd/mm/aaaa): ").strip()
        vencimento = datetime.strptime(vencimento_texto, "%d/%m/%Y").date()
    except (ValueError, TypeError):
        print("Informe um valor e uma data válidos.")
        return

    if valor < 0:
        print("O valor não pode ser negativo.")
        return

    hoje = date.today()
    dias_atraso = max((hoje - vencimento).days, 0)
    juros = valor * Decimal("0.025") * dias_atraso
    total = valor + juros

    print(f"Dias de atraso: {dias_atraso}")
    print(f"Juros: {dinheiro(juros)}")
    print(f"Valor atualizado: {dinheiro(total)}")


def menu():
    while True:
        print("\n========== DESAFIO DEV ==========")
        print("1 - Calcular comissões")
        print("2 - Registrar movimentação de estoque")
        print("3 - Calcular juros por atraso")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            calcular_comissoes()
        elif opcao == "2":
            movimentar_estoque()
        elif opcao == "3":
            calcular_juros()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()