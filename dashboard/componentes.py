import streamlit as st
import streamlit.components.v1 as components


def cabecalho():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #002B5C, #001A38);
        padding: 26px;
        border-radius: 14px;
        margin-bottom: 24px;
        border-bottom: 3px solid #FFD100;
    ">
        <h1 style="color:white; margin:0;">📦 Dashboard de Pedidos</h1>
        <p style="color:#d9e6f2; margin-top:8px;">Tennant Operations Center</p>
    </div>
    """, unsafe_allow_html=True)


def card_kpi(titulo, subtitulo, valor):
    html = f"""
    <div style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #002B5C, #001A38);
        padding: 22px;
        border-radius: 14px;
        border-top: 4px solid #FFD100;
        text-align: center;
        height: 175px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: white;
    ">
        <div style="
            color:white;
            font-size:16px;
            font-weight:700;
        ">
            {titulo}
        </div>

        <div style="
            color:#b8c7d9;
            font-size:13px;
            margin-top:8px;
            min-height:22px;
        ">
            {subtitulo}
        </div>

        <div style="
            color:white;
            font-size:42px;
            font-weight:800;
            margin-top:14px;
        ">
            {valor}
        </div>
    </div>
    """

    components.html(
        html,
        height=190,
        scrolling=False
    )

def cards_principais(kpi):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        card_kpi(
           "Em Aberto",
           "1-IMP",
           kpi["em_aberto"]
        )

    with col2:
        card_kpi(
            "Aguardando Faturamento",
            "2-LIBT e 5-FIM",
            kpi["faturamento"]
        )

    with col3:
        card_kpi(
            "Aguardando Peças",
            "3-LIBP, 4-REIM e 7-PEND",
            kpi["aguardando_pecas"]
        )

    with col4:
        card_kpi(
            "Aguardando Impressão",
            "",
            kpi["aguardando_impressao"]
        )

    with col5:
        card_kpi(
            "Pedidos Ativos",
            "Todos os pedidos",
            kpi["pedidos"]
        )
def etiqueta_status(status):
    status = str(status).strip()

    if status in ["", "None", "nan"]:
        return "⚪ OUTROS", "#6c757d"

    if "1-IMPR" in status:
        return "🔴 EM ABERTO", "#dc3545"

    if "3-LIBP" in status or "4-REIM" in status or "7-PEND" in status:
        return "🟡 AGUARDANDO PEÇAS", "#ffc107"

    if "2-LIBT" in status or "5-FIM" in status:
        return "🔵 FATURAMENTO", "#0d6efd"

    return "⚪ OUTROS", "#6c757d"

def cards_pedidos(df, quantidade=12):
    st.subheader("📦 Pedidos em aberto")

    colunas = st.columns(3)

    for i, (_, pedido) in enumerate(df.head(quantidade).iterrows()):
        coluna = colunas[i % 3]

        numero = pedido.get("Numero", "")
        cliente = pedido.get("Nome Reduzid", "")
        status = pedido.get("TP Liberacao", "")
        peso = pedido.get("Peso Bruto", "")
        incluido = pedido.get("Incluido por", "")
        nota = pedido.get("Nota Fiscal", "")

        etiqueta, cor = etiqueta_status(status)

        if str(status).strip() in ["", "None", "nan"]:
            status = "OUTROS"

        html = f"""
        <div style="
            font-family: Arial, sans-serif;
            background: rgba(0, 43, 92, 0.95);
            border: 1px solid rgba(255,255,255,0.28);
            border-left: 6px solid {cor};
            border-radius: 14px;
            padding: 18px;
            min-height: 220px;
            box-sizing: border-box;
            box-shadow: 0 4px 12px rgba(0,0,0,0.30);
            color: white;
        ">

            <div style="
                background:{cor};
                color:white;
                display:inline-block;
                padding:5px 12px;
                border-radius:20px;
                font-size:12px;
                font-weight:700;
                margin-bottom:12px;
            ">
                {etiqueta}
            </div>

            <h3 style="margin:0 0 10px 0; color:white;">
                Pedido #{numero}
            </h3>

            <hr style="border: 0.5px solid rgba(255,255,255,0.18);">

            <p><b>Empresa:</b> {cliente}</p>
            <p><b>Status:</b> {status}</p>
            <p><b>Peso:</b> {peso} kg</p>
            <p><b>Nota Fiscal:</b> {nota}</p>
            <p><b>Incluído por:</b> {incluido}</p>

        </div>
        """

        with coluna:
            components.html(
                html,
                height=330,
                scrolling=False
            )