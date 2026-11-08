"""Gera dados SINTETICOS agregados para o portfólio CX. Nenhuma fonte real.
Reprodução: python3 codigo/executar_projeto.py --base <pasta>
"""
import csv, calendar, math, random
from pathlib import Path

SEED = 20261108
CANAIS = {'Chat': (27000, 6.6, 0.070, 0.115), 'Telefone': (19000, 12.1, 0.090, 0.110), 'E-mail': (9000, 8.5, 0.060, 0.130)}
MOTIVOS = {
    'Acesso e autenticação': (0.225, 0.145, 0.845, 0.690),
    'Cartões e limites': (0.215, 0.168, 0.830, 0.665),
    'Pix e transferências': (0.185, 0.120, 0.887, 0.727),
    'Contestação': (0.155, 0.267, 0.706, 0.545),
    'Crédito': (0.135, 0.189, 0.805, 0.640),
    'Cadastro': (0.085, 0.202, 0.828, 0.668),
}
PARCEIROS = {'Operador A': 0.54, 'Operador B': 0.46}
CAMPOS = ['mes','canal','motivo','parceiro','contatos','contatos_repetidos',
          'nps_promotores','nps_neutros','nps_detratores','csat_positivas','csat_negativas',
          'custo_variavel_centavos','custo_fixo_alocado_centavos']


def limitar(x, lo, hi):
    return max(lo, min(hi, x))


def gerar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True,exist_ok=True)
    rng=random.Random(SEED)
    linhas=[]
    meses=[f'{a}-{m:02d}' for a in (2025, 2026) for m in range(1,13) if (a,m)<=(2026,10)]
    for i, mes in enumerate(meses):
        ano, mm = map(int, mes.split('-'))
        sazonal = 1 + .065*math.sin((mm-2)*2*math.pi/12) + (.105 if mm==1 else 0) + (.045 if mm==11 else 0)
        crescimento = 1 + .0048*i
        mes_linhas=[]
        for canal, (base, custo_unit, amostra_nps, amostra_csat) in CANAIS.items():
            for motivo,(share,repeat_base,csat_base,promo_base) in MOTIVOS.items():
                incidente = 0
                if mes == '2025-07' and motivo == 'Pix e transferências': incidente=1.0
                if mes == '2026-03' and motivo == 'Acesso e autenticação': incidente=1.35
                if mes == '2026-08' and motivo == 'Cartões e limites': incidente=1.55
                if mes == '2026-09' and motivo == 'Cartões e limites': incidente=.55
                if mes == '2026-10' and motivo == 'Cartões e limites': incidente=.16
                for parceiro,pshare in PARCEIROS.items():
                    vol = base * share * pshare * sazonal * crescimento * (1+0.43*incidente)
                    vol *= rng.uniform(.948, 1.052)
                    contatos=round(vol)
                    penalidade = (.013 if canal=='Telefone' else .038 if canal=='E-mail' else 0) + (.012 if parceiro=='Operador B' else 0)
                    taxa_retorno=limitar(repeat_base + penalidade - .00055*i + .074*incidente+rng.gauss(0,.006),.03,.47)
                    repetidos=round(contatos*taxa_retorno)
                    nps_total=round(contatos*amostra_nps*rng.uniform(.91,1.09))
                    csat_total=round(contatos*amostra_csat*rng.uniform(.91,1.09))
                    promo=limitar(promo_base+(.025 if canal=='Chat' else -.045 if canal=='Telefone' else -.02)-.075*incidente + .00035*i + rng.gauss(0,.012),.20,.85)
                    det=limitar(.175 + (0.025 if canal=='Telefone' else .01 if canal=='E-mail' else 0) +(.18 if motivo=='Contestação' else .02 if motivo=='Crédito' else 0)+.075*incidente +rng.gauss(0,.011),.05,.60)
                    if promo+det>.96: det=.96-promo
                    promotores=round(nps_total*promo)
                    detratores=round(nps_total*det)
                    neutros=nps_total-promotores-detratores
                    csat=limitar(csat_base+(.012 if canal=='Chat' else -.02 if canal=='Telefone' else -.012)+(.015 if parceiro=='Operador A' else -.012)-.082*incidente + rng.gauss(0,.010),.3,.98)
                    csat_positivas=round(csat_total*csat)
                    fator_motivo=1.28 if motivo=='Contestação' else 1.17 if motivo=='Crédito' else 1.08 if motivo=='Cadastro' else 1
                    # Mais custos variáveis em meses com incidente por necessidade de tratamento de exceções.
                    custo_var=round(contatos*custo_unit*fator_motivo*(1.04 if parceiro=='Operador B' else 1)* (1+.075*incidente) * (1+.0035*i) *100)
                    mes_linhas.append({'mes':mes,'canal':canal,'motivo':motivo,'parceiro':parceiro,
                        'contatos':contatos,'contatos_repetidos':repetidos,
                        'nps_promotores':promotores,'nps_neutros':neutros,'nps_detratores':detratores,
                        'csat_positivas':csat_positivas,'csat_negativas':csat_total-csat_positivas,
                        'custo_variavel_centavos':custo_var,'custo_fixo_alocado_centavos':0})
        # Custos fixos rateados proporcionalmente à volumetria, com ajuste centesimal.
        custo_fixo_total=round((88000 + i*720)*100)
        contatos_mes=sum(l['contatos'] for l in mes_linhas)
        alocado=0
        for l in mes_linhas[:-1]:
            l['custo_fixo_alocado_centavos']=round(custo_fixo_total*l['contatos']/contatos_mes)
            alocado+=l['custo_fixo_alocado_centavos']
        mes_linhas[-1]['custo_fixo_alocado_centavos']=custo_fixo_total-alocado
        linhas.extend(mes_linhas)
    destino_arquivo=destino/'contatos_sinteticos.csv'
    with destino_arquivo.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=CAMPOS);w.writeheader();w.writerows(linhas)
    return linhas

if __name__=='__main__':
    gerar(Path(__file__).resolve().parent.parent/'dados')
