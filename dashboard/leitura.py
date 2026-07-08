import pandas as pd
import os


def carregar_planilha(arquivo_enviado=None):

    if arquivo_enviado is not None:
        df = pd.read_excel(
            arquivo_enviado,
            engine="openpyxl",
            header=6
        )

    else:
        arquivo = "data/pedidos.xlsx"

        if not os.path.exists(arquivo):
            return None

        df = pd.read_excel(
            arquivo,
            engine="openpyxl",
            header=6
        )

    df = df.dropna(how="all")

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df