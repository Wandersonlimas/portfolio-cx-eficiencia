"""ETL demonstrativo: validação de origem CSV, SQL (SQLite), agregação e métricas ponderadas."""
import csv, json, sqlite3
from collections import defaultdict
from pathlib import Path

NUMERICOS=['contatos','contatos_repetidos','nps_promotores','nps_neutros','nps_detratores','csat_positivas','csat_negativas','custo_variavel_centavos','custo_fixo_alocado_centavos']
DIM=['mes','canal','motivo','parceiro']

def ler_validar(caminho):
    with open(caminho, newline='', encoding='utf-8') as f: bruto=list(csv.DictReader(f))
    assert len(bruto)==22*3*6*2, 'Granularidade mensal incompleta'
    assert len(set(tuple(x[k] for k in DIM) for x in bruto))==len(bruto), 'Chave duplicada'
    for x in bruto:
        assert all(k in x for k in DIM+NUMERICOS)
        for n in NUMERICOS:
            x[n]=int(x[n]); assert x[n]>=0, f'Valor negativo em {n}'
        assert x['contatos_repetidos'] <= x['contatos']
        assert x['nps_promotores']+x['nps_neutros']+x['nps_detratores'] <= x['contatos']
        assert x['csat_positivas']+x['csat_negativas'] <= x['contatos']
        assert len(x['mes'])==7 and x['mes'][4]=='-'
    return bruto

def sql_agregar(rows):
    con=sqlite3.connect(':memory:')
    colunas=', '.join(f'{n} INTEGER NOT NULL' for n in NUMERICOS)
    con.execute('CREATE TABLE contatos (mes TEXT, canal TEXT, motivo TEXT, parceiro TEXT, '+colunas+', PRIMARY KEY(mes,canal,motivo,parceiro))')
    names=DIM+NUMERICOS
    con.executemany('INSERT INTO contatos VALUES ('+','.join('?' for _ in names)+')', [tuple(r[n] for n in names) for r in rows])
    consulta='SELECT mes, '+', '.join(f'SUM({n}) AS {n}' for n in NUMERICOS)+' FROM contatos GROUP BY mes ORDER BY mes'
    con.row_factory=sqlite3.Row
    mensais=[dict(row) for row in con.execute(consulta)]
    anual=[dict(row) for row in con.execute('SELECT substr(mes,1,4) AS ano, SUM(contatos) AS contatos FROM contatos GROUP BY substr(mes,1,4) ORDER BY ano')]
    con.close()
    return mensais, anual

def agrupar(rows):
    resultado={n:sum(int(r[n]) for r in rows) for n in NUMERICOS}
    nps_res=resultado['nps_promotores']+resultado['nps_neutros']+resultado['nps_detratores']
    csat_res=resultado['csat_positivas']+resultado['csat_negativas']
    c=resultado['contatos']
    resultado.update({
        'nps':100*(resultado['nps_promotores']-resultado['nps_detratores'])/nps_res if nps_res else None,
        'csat':100*resultado['csat_positivas']/csat_res if csat_res else None,
        'recontato':100*resultado['contatos_repetidos']/c if c else None,
        'cts':(resultado['custo_variavel_centavos']+resultado['custo_fixo_alocado_centavos'])/100/c if c else None,
        'custo_variavel_unitario':resultado['custo_variavel_centavos']/100/c if c else None,
        'respostas_nps':nps_res,'respostas_csat':csat_res,
    })
    return resultado

def agregar_dim(rows, dim):
    grouped=defaultdict(list)
    for r in rows: grouped[r[dim]].append(r)
    return {k:agrupar(v) for k,v in grouped.items()}

def executar(base):
    base=Path(base)
    raw=ler_validar(base/'dados'/'contatos_sinteticos.csv')
    mensais_sql,anos=sql_agregar(raw)
    for m in mensais_sql:
        p=agrupar([r for r in raw if r['mes']==m['mes']])
        assert all(p[n]==m[n] for n in NUMERICOS), 'Divergência SQL vs Python'
        m.update(p)
    summary={'dados_sinteticos':True,'gerador_semente':20261108,'linhas':len(raw),'periodo':{'inicio':'2025-01','fim':'2026-10'},
         'meses':mensais_sql,'anos':anos,'geral':agrupar(raw),
         'por_canal':agregar_dim(raw,'canal'),'por_motivo':agregar_dim(raw,'motivo'),
         'por_parceiro':agregar_dim(raw,'parceiro'),
         'eventos_modelados':[{'mes':'2025-07','motivo':'Pix e transferências','hipotese':'Aumento fictício de atrito no Pix'},
                              {'mes':'2026-03','motivo':'Acesso e autenticação','hipotese':'Instabilidade fictícia no processo de autenticação'},
                              {'mes':'2026-08','motivo':'Cartões e limites','hipotese':'Alteração fictícia em jornada de cartões'},
                              {'mes':'2026-09','motivo':'Cartões e limites','hipotese':'Efeito residual fictício em cartões'}]}
    with (base/'dados'/'indicadores_processados.json').open('w',encoding='utf-8') as f: json.dump(summary,f,ensure_ascii=False,indent=2)
    return summary

if __name__=='__main__': executar(Path(__file__).resolve().parent.parent)
