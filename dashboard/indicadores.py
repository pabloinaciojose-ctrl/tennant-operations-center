import pandas as pd


def coluna_texto(df, coluna):
    return (
        df[coluna]
        .fillna("")
        .astype(str)
        .str.strip()
    )


def calcular_indicadores(df):

    status = coluna_texto(df, "TP Liberacao")
    tem_op = coluna_texto(df, "Tem OP ?").str.lower()
    codcli_final = coluna_texto(df, "CodCli Final")

    peso_bruto = pd.to_numeric(
        df["Peso Bruto"],
        errors="coerce"
    ).fillna(0)

    # ==============================
    # CONDIÇÃO BASE
    # Tem OP ? = Não
    # CodCli Final = vazio
    # ==============================

    tem_op_nao = tem_op.isin(["nao", "não"])

    codcli_vazio = (
        (codcli_final == "") |
        (codcli_final.str.lower() == "none") |
        (codcli_final.str.lower() == "nan")
    )

    condicao_base = tem_op_nao & codcli_vazio

    # ==============================
    # CARD 1 - EM ABERTO
    # TP Liberação = 1-IMPR
    # + Tem OP ? = Não
    # + CodCli Final vazio
    # ==============================

    grupo_em_aberto = (
        condicao_base &
        status.str.contains("1-IMPR", na=False)
    )

    # ==============================
    # CARD 2 - AGUARDANDO FATURAMENTO
    # TP Liberação = 2-LIBT ou 5-FIM
    # + Tem OP ? = Não
    # + CodCli Final vazio
    # ==============================

    grupo_faturamento = (
        condicao_base &
        (
            status.str.contains("2-LIBT", na=False) |
            status.str.contains("5-FIM", na=False)
        )
    )

    # ==============================
    # CARD 3 - AGUARDANDO PEÇAS
    # TP Liberação = 3-LIBP, 4-REIM ou 7-PEND
    # + Tem OP ? = Não
    # + CodCli Final vazio
    # ==============================

    grupo_aguardando_pecas = (
        condicao_base &
        (
            status.str.contains("3-LIBP", na=False) |
            status.str.contains("4-REIM", na=False) |
            status.str.contains("7-PEND", na=False)
        )
    )

    # ==============================
    # CARD 4 - AGUARDANDO IMPRESSÃO
    # TP Liberação em branco
    # ==============================

    status_vazio = (
        (status == "") |
        (status.str.lower() == "none") |
        (status.str.lower() == "nan")
    )

    grupo_aguardando_impressao = status_vazio

    total_pedidos_ativos = (
    grupo_em_aberto.sum()
    + grupo_faturamento.sum()
    + grupo_aguardando_pecas.sum()
    + grupo_aguardando_impressao.sum()
)

    return {
        "pedidos": total_pedidos_ativos,

        "em_aberto": grupo_em_aberto.sum(),
        "impr": grupo_em_aberto.sum(),

        "faturamento": grupo_faturamento.sum(),

        "aguardando_pecas": grupo_aguardando_pecas.sum(),

        "aguardando_impressao": grupo_aguardando_impressao.sum(),

        "peso": peso_bruto.sum(),
        "clientes": df["Cliente"].nunique()
    }