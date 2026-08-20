import pandas as pd
import streamlit as st

from database.connection import engine
from database.models import Base
from database.ingestion import update_symbol
from database.repository import (
    get_active_assets,
    get_stock_data,
)

from analysis.forecast import forecast_price


# CONFIGURAÇÃO

st.set_page_config(
    page_title="Financial Market Dashboard",
    page_icon="📈",
    layout="wide",
)


# BANCO DE DADOS

Base.metadata.create_all(engine)


# TÍTULO

st.title("📈 Financial Market Dashboard")

st.markdown(
    "Análise histórica e previsão de preços de ativos financeiros."
)


# ATIVOS CADASTRADOS

assets = get_active_assets()


if not assets:

    st.warning(
        "Nenhum ativo cadastrado no banco de dados."
    )

    st.info(
        "Execute o arquivo seed_assets.py para cadastrar os ativos."
    )

    st.stop()


# DICIONÁRIO PARA O SELECTBOX

asset_options = {
    f"{asset.name} ({asset.symbol})": asset.symbol
    for asset in assets
}


st.sidebar.header("Filtros")


selected_asset = st.sidebar.selectbox(
    "Selecione o ativo",
    options=list(asset_options.keys()),
)


symbol = asset_options[selected_asset]


# ATUALIZAÇÃO DOS DADOS

if st.sidebar.button(
    "🔄 Atualizar dados",
    use_container_width=True,
):

    with st.spinner(
        f"Atualizando dados de {symbol}..."
    ):

        try:

            inserted_count = update_symbol(
                symbol
            )

            if inserted_count == 0:

                st.sidebar.success(
                    "Os dados mais recentes "
                    "já estão atualizados."
                )

            else:

                st.sidebar.success(
                    f"{inserted_count} novos "
                    f"registros adicionados."
                )

                st.rerun()

        except Exception as error:

            st.sidebar.error(
                f"Erro ao atualizar {symbol}: {error}"
            )


# BUSCAR DADOS DO BANCO

df = get_stock_data(symbol)


if df.empty:

    st.info(
        f"Ainda não existem dados históricos "
        f"para {symbol}."
    )

    st.info(
        "Clique em '🔄 Atualizar dados' "
        "para buscar os dados desse ativo."
    )

    st.stop()


# DATAS DISPONÍVEIS

min_date = df.index.min().date()
max_date = df.index.max().date()


start_date = st.sidebar.date_input(
    "Data inicial",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
)


end_date = st.sidebar.date_input(
    "Data final",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
)


if start_date > end_date:

    st.error(
        "A data inicial não pode ser maior "
        "que a data final."
    )

    st.stop()


# FILTRO DE DATAS

df_filtered = df.loc[
    (df.index >= pd.Timestamp(start_date))
    &
    (df.index <= pd.Timestamp(end_date))
].copy()


if df_filtered.empty:

    st.warning(
        "Não existem dados para o período selecionado."
    )

    st.stop()


# PERÍODO DA PREVISÃO

forecast_periods = st.sidebar.selectbox(
    "Períodos para previsão",
    options=[7, 15, 30, 60, 90],
    index=2,
)


# INDICADORES

first_price = df_filtered["close"].iloc[0]

last_price = df_filtered["close"].iloc[-1]

period_return = (
    (last_price / first_price) - 1
) * 100

max_price = df_filtered["high"].max()

min_price = df_filtered["low"].min()


# CARDS

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Preço de fechamento",
    f"${last_price:,.2f}",
)


col2.metric(
    "Retorno no período",
    f"{period_return:.2f}%",
)


col3.metric(
    "Máxima",
    f"${max_price:,.2f}",
)


col4.metric(
    "Mínima",
    f"${min_price:,.2f}",
)


# GRÁFICO DE PREÇO

st.subheader(
    f"Preço de fechamento — {selected_asset}"
)


st.line_chart(
    df_filtered["close"],
)


# PREVISÃO

st.subheader(
    f"Tendência dos próximos "
    f"{forecast_periods} períodos"
)


with st.spinner(
    "Calculando previsão..."
):

    try:

        forecast = forecast_price(
            df_filtered,
            periods=forecast_periods,
        )

    except Exception as error:

        st.error(
            f"Não foi possível gerar a previsão: {error}"
        )

        st.stop()


# DADOS HISTÓRICOS

historical = df_filtered[
    ["close"]
].copy()

historical.columns = [
    "Preço real"
]


# DADOS FUTUROS

future = forecast[
    forecast["ds"] > df_filtered.index.max()
].copy()


future["ds"] = pd.to_datetime(
    future["ds"]
)

future = future.set_index("ds")


future = future[
    ["yhat"]
]

future.columns = [
    "Previsão"
]


# COMBINAR HISTÓRICO + PREVISÃO

forecast_chart = pd.concat(
    [
        historical,
        future,
    ],
    axis=1,
)


# GRÁFICO DE PREVISÃO

st.line_chart(
    forecast_chart,
)


st.caption(
    "A previsão é uma estimativa estatística baseada "
    "no histórico do ativo e não representa recomendação "
    "de investimento."
)


# VISUALIZAR DADOS

with st.expander("Visualizar dados"):

    display_df = df_filtered.reset_index()

    display_df = display_df[
        [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
    )