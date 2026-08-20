import pandas as pd

from prophet import Prophet


def forecast_price(
    df: pd.DataFrame,
    periods: int = 30,
) -> pd.DataFrame:

    # Copiar os dados para não alterar o DataFrame original
    data = df.copy()

    # Garantir que o índice seja datetime
    data.index = pd.to_datetime(data.index)

    # Criar DataFrame no formato exigido pelo Prophet
    data = data.reset_index()

    # Renomear as colunas
    data = data.rename(
        columns={
            data.columns[0]: "ds",
            "close": "y",
        }
    )

    # Manter somente as colunas necessárias
    data = data[
        ["ds", "y"]
    ]

    # Garantir tipos corretos
    data["ds"] = pd.to_datetime(
        data["ds"]
    )

    data["y"] = pd.to_numeric(
        data["y"],
        errors="coerce"
    )

    # Remover valores inválidos
    data = data.dropna(
        subset=["ds", "y"]
    )

    # Ordenar por data
    data = data.sort_values("ds")

    # Precisamos de dados suficientes
    if len(data) < 10:

        raise ValueError(
            "Não existem dados históricos suficientes "
            "para gerar uma previsão."
        )

    # Criar modelo
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
    )

    # Treinar
    model.fit(data)

    # Criar datas futuras
    future = model.make_future_dataframe(
        periods=periods,
        freq="D",
    )

    # Gerar previsão
    forecast = model.predict(future)

    return forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper",
        ]
    ]