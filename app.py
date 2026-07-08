import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from dashboard.leitura import carregar_planilha
from dashboard.indicadores import calcular_indicadores
from dashboard.componentes import cabecalho, cards_principais, cards_pedidos
from dashboard.graficos import grafico_distribuicao_grupos, grafico_status_detalhado, grafico_incluido_por

st.set_page_config(
    page_title="Tennant Operations Center",
    page_icon="📦",
    layout="wide"
)

st_autorefresh(
    interval=60000,
    key="atualizacao_dashboard"
)

st.sidebar.title("📦 Tennant")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Painel de controle",
        "📦 Estoque",
        "📋 Pedidos",
        "🚚 Expedição",
        "📈 Indicadores",
        "⚙ Configurações"
    ]
)

st.sidebar.divider()

atualizacao_auto = st.sidebar.checkbox(
    "🔄 Atualizar automaticamente",
    value=False
)

intervalo = st.sidebar.selectbox(
    "Intervalo",
    [30, 60, 120, 300],
    index=0
)
st.sidebar.divider()

quantidade_cards = st.sidebar.slider(
    "Pedidos na Tela",
    min_value=6,
    max_value=60,
    value=12,
    step=3
)

st.sidebar.divider()

arquivo_enviado = st.sidebar.file_uploader(
    "📂 Carregar planilha do Protheus",
    type=["xlsx"]
)

try:
    url_onedrive = st.secrets["ONEDRIVE_EXCEL_URL"]
except Exception:
    url_onedrive = ""

try:
    df = carregar_planilha(
        arquivo_enviado=arquivo_enviado,
        url_onedrive=url_onedrive
    )
except Exception as erro:
    st.error("Não foi possível carregar a planilha do OneDrive.")
    st.info("Verifique se o link permite download sem login, ou carregue a planilha manualmente pelo botão Upload.")
    st.stop()
if df is None:
    st.warning("Carregue uma planilha do Protheus ou configure o link do OneDrive.")
    st.stop()

kpi = calcular_indicadores(df)

cabecalho()
cards_principais(kpi)

st.divider()

st.subheader("🔎 Pesquisa de Pedido")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    busca = st.text_input("🔎 Buscar pedido, cliente ou cidade")

with col_f2:
    status_opcoes = ["Todos"] + sorted(df["TP Liberacao"].dropna().astype(str).unique().tolist())
    status_selecionado = st.selectbox("Status", status_opcoes)

with col_f3:
    usuario_opcoes = ["Todos"] + sorted(df["Incluido por"].dropna().astype(str).unique().tolist())
    usuario_selecionado = st.selectbox("Incluído por", usuario_opcoes)

df_filtrado = df.copy()

if busca:
    df_filtrado = df_filtrado[
        df_filtrado.astype(str).apply(
            lambda linha: linha.str.contains(busca, case=False, na=False).any(),
            axis=1
        )
    ]

if status_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["TP Liberacao"].astype(str) == status_selecionado
    ]

if usuario_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Incluido por"].astype(str) == usuario_selecionado
    ]

def prioridade_status(status):
    status = str(status).strip()

    if status in ["", "None", "nan"]:
        return 1

    if "1-IMPR" in status:
        return 2

    if "3-LIBP" in status or "4-REIM" in status or "7-PEND" in status:
        return 3

    if "2-LIBT" in status or "5-FIM" in status:
        return 4

    return 5


df_filtrado["Prioridade"] = df_filtrado["TP Liberacao"].apply(prioridade_status)

df_filtrado = df_filtrado.sort_values(
    by="Prioridade",
    ascending=True
)

st.info(f"🔎 Resultado do filtro: {len(df_filtrado)} pedidos encontrados")

st.divider()

cards_pedidos(df_filtrado, quantidade_cards)

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    grafico_distribuicao_grupos(kpi)

with col_g2:
    grafico_status_detalhado(df_filtrado)

with col_g3:
    grafico_incluido_por(df_filtrado)

st.subheader("📋 Pedidos")

arquivo_exportado = df_filtrado.to_csv(
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 Exportar pedidos filtrados",
    data=arquivo_exportado,
    file_name="pedidos_filtrados.csv",
    mime="text/csv"
)

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=420
)