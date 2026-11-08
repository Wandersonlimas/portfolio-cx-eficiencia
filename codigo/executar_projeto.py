"""Execute na raiz do projeto: python3 codigo/executar_projeto.py"""
from pathlib import Path
from gerar_dados import gerar
from processar_etl import executar
from construir_dashboard import construir
from gerar_relatorio import relatorio

if __name__=='__main__':
    base=Path(__file__).resolve().parent.parent
    gerar(base/'dados')
    s=executar(base)
    construir(base)
    relatorio(base)
    print(f'OK: {s["linhas"]} registros sintéticos. Dashboard e relatório construídos em {base/"entregaveis"}')
