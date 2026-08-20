from api.client import AlphaVantageClient
from data.transform import transform_data

from database.repository import (
    get_active_symbols,
    get_latest_date,
    save_stock_data,
)


def ingest_symbol(symbol: str) -> int:

    symbol = symbol.upper().strip()

    client = AlphaVantageClient()

    print(f"\nBuscando dados de {symbol}...")

    dados = client.get_daily_data(symbol)

    df = transform_data(dados)

    if df.empty:
        print(f"Nenhum dado encontrado para {symbol}.")
        return 0

    inserted_count = save_stock_data(
        df,
        symbol,
    )

    print(
        f"{symbol}: "
        f"{inserted_count} registros adicionados."
    )

    return inserted_count


def update_symbol(symbol: str) -> int:

    symbol = symbol.upper().strip()

    latest_date = get_latest_date(symbol)

    client = AlphaVantageClient()

    print(f"\nAtualizando {symbol}...")

    dados = client.get_daily_data(symbol)

    df = transform_data(dados)

    if df.empty:
        print(f"Nenhum dado encontrado para {symbol}.")
        return 0

    if latest_date is not None:

        df = df[
            df.index.date > latest_date
        ]

    if df.empty:

        print(
            f"{symbol}: "
            "os dados já estão atualizados."
        )

        return 0

    inserted_count = save_stock_data(
        df,
        symbol,
    )

    print(
        f"{symbol}: "
        f"{inserted_count} novos registros."
    )

    return inserted_count


def run_ingestion():

    symbols = get_active_symbols()

    if not symbols:

        print(
            "Nenhum ativo ativo encontrado "
            "no cadastro."
        )

        return

    print(
        f"Iniciando ingestão de "
        f"{len(symbols)} ativos..."
    )

    total_inserted = 0

    for symbol in symbols:

        try:

            inserted = update_symbol(symbol)

            total_inserted += inserted

        except Exception as error:

            print(
                f"Erro ao processar "
                f"{symbol}: {error}"
            )

    print("\n================================")
    print("Ingestão finalizada")
    print("================================")
    print(
        f"Total de novos registros: "
        f"{total_inserted}"
    )