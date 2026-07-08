import streamlit as st
import plotly.express as px
import pandas as pd


def grafico_distribuicao_grupos(kpi):

    st.subheader("📊 Distribuição de Pedidos Ativos")

    dados = pd.DataFrame({
        "Grupo": [
            "Em Aberto",
            "Faturamento",
            "Aguardando Peças",
            "Impressão"
        ],
        "Quantidade": [
            kpi["impr"],
            kpi["faturamento"],
            kpi["aguardando_pecas"],
            kpi["aguardando_impressao"]
        ]
    })

    fig = px.pie(
        dados,
        names="Grupo",
        values="Quantidade",
        hole=0.45
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_status_detalhado(df):

    st.subheader("📈 Status Detalhado")

    dados = df["TP Liberacao"].value_counts().reset_index()
    dados.columns = ["Status", "Quantidade"]

    fig = px.bar(
        dados,
        x="Status",
        y="Quantidade",
        text="Quantidade"
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_incluido_por(df):

    st.subheader("👤 Pedidos por Usuário")

    dados = df["Incluido por"].value_counts().head(10).reset_index()
    dados.columns = ["Usuário", "Quantidade"]

    fig = px.bar(
        dados,
        x="Usuário",
        y="Quantidade",
        text="Quantidade"
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)