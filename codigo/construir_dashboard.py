"""Compila o Case 01 V4 com frontend modular e dados sintéticos do ETL.
Uso: python codigo/construir_dashboard.py
"""
import json
from pathlib import Path
from processar_etl import ler_validar

ROOT=Path(__file__).resolve().parents[1]

def construir(base=ROOT):
    base=Path(base)
    rows=ler_validar(base/'dados'/'contatos_sinteticos.csv')
    if len(rows)!=792:
        raise ValueError('Esperados 792 grupos sintéticos')
    template=(base/'src'/'web'/'templates'/'dashboard.html').read_text(encoding='utf-8')
    css=(base/'src'/'web'/'css'/'dashboard.css').read_text(encoding='utf-8')
    js=(base/'src'/'web'/'js'/'dashboard.js').read_text(encoding='utf-8')
    data=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    for token in ('{{CSS}}','{{JS}}','{{DATA}}'):
        if template.count(token)!=1:
            raise ValueError('Token ausente/duplicado: '+token)
    html=template.replace('{{CSS}}',css).replace('{{JS}}',js).replace('{{DATA}}',data)
    if 'window.DATA_ROWS=' not in html:
        raise ValueError('Dados não foram incorporados')
    (base/'index.html').write_text(html,encoding='utf-8')
    (base/'entregaveis'/'Dashboard_CX_Case_Tecnico_V4.html').write_text(html,encoding='utf-8')
    return html

if __name__=='__main__':
    print('Dashboard V4 gerado:',len(construir()),'caracteres')
