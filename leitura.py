import pandas as pd
import os
import requests
from io import BytesIO


def preparar_link_download(url):
    if url is None or url == "":
        return None

    url = str(url).strip()

    if "download=1" in url:
        return url

    if "?" in url:
        return url + "&download=1"

    return url + "?download=1"


def ler_excel_de_url(url):
    url_download = preparar_link_download(url)

    resposta = requests.get(url_download, timeout=30)

    if resposta.status_code != 200:
        raise Exception("Não foi possível baixar a planilha do OneDrive/SharePoint.")

    conteudo = resposta.content

    df = pd.read_excel(
        BytesIO(conteudo),
        engine="openpyxl",
        header=6
    )

    return df


def carregar_planilha(arquivo_enviado=None, url_onedrive=None):

    if arquivo_enviado is not None:
        df = pd.read_excel(
            arquivo_enviado,
            engine="openpyxl",
            header=6
        )

    elif url_onedrive:
        df = ler_excel_de_url(url_onedrive)

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