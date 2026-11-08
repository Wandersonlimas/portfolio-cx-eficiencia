"""Relatório executivo vetorial; os indicadores são derivados da base sintética validada."""
from pathlib import Path
from collections import defaultdict
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from processar_etl import ler_validar,agrupar

W,H=960,540
NAVY='#13273A';DEEP='#102132';TEAL='#00A58B';PALE='#E3F4ED';WHITE='#FFFFFF';INK='#172A3B';MUTED='#6D8291';BG='#F4F7F8';LINE='#DEE7E9';ORANGE='#D98B3E';BLUE='#477BCB';RED='#BD5D57'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DV',REG));pdfmetrics.registerFont(TTFont('DV-Bold',BOLD))

def cor(hex):return HexColor(hex)
def string(s):return str(s)
def fmt(v,d=1):return f'{v:,.{d}f}'.replace(',','~').replace('.',',').replace('~','.')
def num(v):return f'{v:,.0f}'.replace(',','.')
def money(v):return 'R$ '+fmt(v,2)

def t(c,x,y,s,size=12,color=INK,bold=False):
    c.setFont('DV-Bold' if bold else 'DV',size);c.setFillColor(cor(color));c.drawString(x,y,str(s))
def right(c,x,y,s,size=12,color=INK,bold=False):
    c.setFont('DV-Bold' if bold else 'DV',size);c.setFillColor(cor(color));c.drawRightString(x,y,str(s))
def rect(c,x,y,w,h,fill,r=0,stroke=None):
    c.setFillColor(cor(fill));c.setStrokeColor(cor(stroke or fill))
    c.roundRect(x,y,w,h,r,fill=1,stroke=1 if stroke else 0)
def wrap(text,width,size=11,bold=False):
    font='DV-Bold' if bold else 'DV'
    lines=[]
    for para in str(text).split('\n'):
        words=para.split();line=''
        for word in words:
            test=(line+' '+word).strip()
            if pdfmetrics.stringWidth(test,font,size)>width and line:
                lines.append(line);line=word
            else:line=test
        lines.append(line)
    return lines

def p(c,x,y,text,width,size=11,leading=18,color=INK,max_lines=99,bold=False):
    lines=wrap(text,width,size,bold)
    for line in lines[:max_lines]:
        t(c,x,y,line,size,color,bold);y-=leading
    return y

def base(c,n,tag='CASE TECNICO / PORTFOLIO'):
    rect(c,0,0,W,H,BG)
    rect(c,0,H-51,W,51,WHITE)
    t(c,40,H-33,'WANDERSON LIMAS',11,NAVY,True)
    t(c,255,H-33,tag,9,TEAL,True)
    c.setStrokeColor(cor(LINE));c.line(40,46,W-40,46)
    t(c,40,27,'CX & EFICIENCIA OPERACIONAL  |  DADOS 100% SINTETICOS',9,MUTED)
    right(c,W-40,27,f'{n:02d} / 08',9,MUTED,True)

def title(c,over,heading,sub=None):
    t(c,40,452,over.upper(),10,TEAL,True)
    t(c,40,402,heading,30,NAVY,True)
    if sub: p(c,40,374,sub,870,12,18,MUTED,max_lines=2)

def metric(c,x,y,w,h,label,value,detail,delta=None,negative=False):
    rect(c,x,y,w,h,WHITE,14,LINE)
    t(c,x+18,y+h-30,label.upper(),9,MUTED,True)
    t(c,x+18,y+h-76,value,27,NAVY,True)
    p(c,x+18,y+25,detail,w-36,9,13,MUTED,max_lines=2)
    if delta is not None:
        right(c,x+w-16,y+h-28,delta,9,RED if negative else TEAL,True)

def graph(c,x,y,w,h,values,labels,color,fmtf):
    ymin=min(values);ymax=max(values);padding=max((ymax-ymin)*.28,.4 if max(values)<30 else 2)
    ymin=max(0,ymin-padding);ymax+=padding
    for k in range(4):
        yy=y+(h-32)*k/3
        c.setStrokeColor(cor(LINE));c.setLineWidth(.8);c.line(x+41,yy,x+w-10,yy)
        t(c,x,yy-3,fmtf(ymin+(ymax-ymin)*k/3),8,MUTED)
    coords=[]
    for i,v in enumerate(values):
        px=x+45+(w-57)*i/max(1,len(values)-1)
        py=y+(h-32)*(v-ymin)/(ymax-ymin)
        coords.append((px,py))
    c.setStrokeColor(cor(color));c.setLineWidth(2.5)
    for (ax,ay),(bx,by) in zip(coords,coords[1:]):c.line(ax,ay,bx,by)
    c.setFillColor(cor(color))
    for i,(px,py) in enumerate(coords):
        c.circle(px,py,3 if i==len(coords)-1 else 2,stroke=0,fill=1)
        if i%max(1,math.ceil(len(coords)/5))==0 or i==len(coords)-1:
            t(c,px-9,y-17,labels[i].split('-')[1]+'/'+labels[i][2:4],8,MUTED)

def section_box(c,x,y,w,h,label,body,shade=WHITE):
    rect(c,x,y,w,h,shade,12,LINE)
    t(c,x+17,y+h-28,label,12,NAVY,True)
    p(c,x+17,y+h-53,body,w-32,10,17,MUTED,max_lines=max(1,int((h-58)/17)))

def relatorio(basepath):
    basepath=Path(basepath);rows=ler_validar(basepath/'dados'/'contatos_sinteticos.csv')
    months=sorted(set(r['mes'] for r in rows));last=months[-6:];prev=months[-12:-6]
    cur_rows=[r for r in rows if r['mes'] in last]; prev_rows=[r for r in rows if r['mes'] in prev]
    cur=agrupar(cur_rows);pre=agrupar(prev_rows)
    metrics_month=[{'mes':m,**agrupar([r for r in rows if r['mes']==m])} for m in months if m.startswith('2026-')]
    channels={ch:agrupar([r for r in cur_rows if r['canal']==ch]) for ch in sorted(set(r['canal'] for r in cur_rows))}
    motivos={mo:agrupar([r for r in cur_rows if r['motivo']==mo]) for mo in sorted(set(r['motivo'] for r in cur_rows))}
    motivos=dict(sorted(motivos.items(),key=lambda a:a[1]['contatos_repetidos'],reverse=True))
    costo=cur['custo_variavel_unitario'];hypo=cur['contatos_repetidos']*.20*costo
    dest=basepath/'entregaveis'/'Relatorio_Executivo_CX_V2.pdf'
    c=canvas.Canvas(str(dest),pagesize=(W,H),pageCompression=1)
    c.setTitle('CX em números - case técnico V2 - dados sintéticos');c.setAuthor('Portfólio demonstrativo | Wanderson Limas')
    # page 1
    rect(c,0,0,W,H,NAVY)
    rect(c,40,427,220,31,'#1D514D',12)
    t(c,54,438,'CASE DEMONSTRATIVO • V2',10,'#8BF0CB',True)
    t(c,40,327,'CX EM NUMEROS.',39,WHITE,True)
    t(c,40,266,'DECISOES',44,WHITE,True)
    t(c,40,205,'RASTREAVEIS.',44,'#53E2BC',True)
    p(c,42,152,'Um estudo de CX, eficiência e custo com dados sintéticos, métricas auditáveis e leitura crítica de hipóteses.',650,14,23,'#B6CBD4',3)
    t(c,40,49,'WANDERSON LIMAS   •   ANALISE DE DADOS & INTELIGENCIA OPERACIONAL',10,WHITE,True)
    right(c,920,49,'MAI - OUT / 2026',10,'#A7C3C9')
    c.showPage()
    # page 2
    base(c,2);title(c,'01 | RESUMO EXECUTIVO','Resultados mistos. Sem narrativa pronta.','Comparação justa entre dois intervalos de seis meses: Nov/25-Abr/26 versus Mai-Out/26.')
    def tendencia(d,unit,dig=1):return ('+' if d>=0 else '-')+fmt(abs(d),dig)+unit
    items=[('NPS',fmt(cur['nps'])+' pts',tendencia(cur['nps']-pre['nps'],' pts'),cur['nps']<pre['nps'],'Métrica ponderada por pesquisas'),
           ('CSAT',fmt(cur['csat'])+'%',tendencia(cur['csat']-pre['csat'],' p.p.'),cur['csat']<pre['csat'],'Respostas positivas / respondentes'),
           ('RECONTATO',fmt(cur['recontato'])+'%',tendencia(cur['recontato']-pre['recontato'],' p.p.',2),cur['recontato']>pre['recontato'],'Contato marcado como retorno'),
           ('CTS',money(cur['cts']),tendencia(cur['cts']-pre['cts'],' R$/contato',2),cur['cts']>pre['cts'],'Custo total / volume de contatos')]
    for i,(label,val,delta,down,detail) in enumerate(items):
        metric(c,40+(i%2)*444,212-(i//2)*136,420,128,label,val,detail,delta,down)
    t(c,40,350,f'Volume: {num(cur["contatos"])} contatos | {num(cur["respostas_nps"])} respostas NPS | {num(cur["respostas_csat"])} respostas CSAT',10,MUTED)
    c.showPage()
    # page3
    base(c,3);title(c,'02 | TENDENCIAS','O agregado esconde meses críticos.','Séries Jan-Out/26 geradas do CSV. Quedas e deteriorações fazem parte da simulação.')
    months26=[m['mes'] for m in metrics_month]
    for i,(label,key,color,fn) in enumerate([('NPS (pontos)','nps',TEAL,lambda z:fmt(z,0)),('Recontato (%)','recontato',ORANGE,lambda z:fmt(z,0))]):
        x=40+i*446;rect(c,x,120,426,226,WHITE,12,LINE);t(c,x+20,318,label,13,NAVY,True)
        graph(c,x+18,157,384,132,[m[key] for m in metrics_month],months26,color,fn)
    rect(c,40,61,872,51,PALE,11)
    t(c,58,91,'SINAL A INVESTIGAR',10,TEAL,True)
    p(c,58,73,'Ago/26 concentra um pico sintético de recontato e queda de NPS. O cenário gerado não comprova a causa no mundo real.',820,9,13,MUTED,max_lines=1)
    c.showPage()
    # page4
    base(c,4);title(c,'03 | PARETO','De onde vem o volume de recontatos?','Seis motivos de contato, ordenados pelo número absoluto de retornos no período Mai-Out/26.')
    x0=40; ytop=341
    for label,x in [('MOTIVO',54),('CONTATOS',514),('RETORNOS',652),('TAXA',775),('% RETORNOS',870)]:right(c,x+10,ytop,label,9,MUTED,True) if x>70 else t(c,x,ytop,label,9,MUTED,True)
    for idx,(mo,v) in enumerate(motivos.items()):
        y=ytop-36-43*idx
        if idx%2==0:rect(c,40,y-14,875,40,WHITE,5)
        t(c,54,y+1,mo,11,NAVY,True)
        right(c,524,y+1,num(v['contatos']),10,NAVY)
        right(c,662,y+1,num(v['contatos_repetidos']),10,NAVY)
        right(c,785,y+1,fmt(v['recontato'])+'%',10,NAVY)
        right(c,900,y+1,fmt(100*v['contatos_repetidos']/cur['contatos_repetidos'])+'%',10,TEAL,True)
        rect(c,54,y-9,272*(v['contatos_repetidos']/max(a['contatos_repetidos'] for a in motivos.values())),3,TEAL,1)
    t(c,44,60,'Um motivo com taxa alta pode não ter o maior impacto absoluto. Priorizar exige volume, taxa e custo.',10,MUTED)
    c.showPage()
    # page5
    base(c,5);title(c,'04 | CANAIS','O mesmo problema tem custos diferentes.','Separar canais reduz o risco de comparar operações com intensidade e mix distintos.')
    for i,(ch,v) in enumerate(channels.items()):
        x=40+299*i;rect(c,x,195,280,164,WHITE,13,LINE)
        t(c,x+19,328,ch.upper(),12,TEAL,True)
        t(c,x+19,283,num(v['contatos'])+' contatos',17,NAVY,True)
        t(c,x+19,244,'Recontato  '+fmt(v['recontato'])+'%',11,INK)
        t(c,x+19,222,'NPS  '+fmt(v['nps'])+' pts',11,INK)
        t(c,x+19,203,'CTS  '+money(v['cts']),11,INK)
    section_box(c,40,81,876,94,'Perguntas para uma análise de causa raiz','Há diferença de mix de motivos por canal? A operação transfere casos entre canais? O aumento de custo coincide com escalonamento ou retrabalho? Os dados sintéticos não contêm logs de eventos para responder a essas perguntas.',PALE)
    c.showPage()
    #page6
    base(c,6);title(c,'05 | DIAGNOSTICO','Hipóteses que podem ser testadas.','Os eventos abaixo foram programados pelo gerador de dados. No mundo real, precisariam de evidência independente.')
    hypotheses=[('01  Entrada / jornada','Mar/26: aumento sintético de contatos e retorno em acesso e autenticação.','Conferir versões, falhas de login, tentativas repetidas e reclassificação de motivos.'),('02  Fluxo de cartões','Ago-Set/26: choque sintético em cartões com piora de NPS e taxa de recontato.','Comparar históricos de processo, reclamações, repasses e amostras de resoluções.'),('03  Redução de custo','CTS pode subir mesmo quando satisfação melhora, por mudança no mix e custo unitário.','Separar volume, custo variável, custo fixo e eficiência por canal.')]
    for i,(head,body,action) in enumerate(hypotheses):
        y=259-i*99;rect(c,40,y,877,88,WHITE,12,LINE)
        t(c,58,y+63,head,13,NAVY,True)
        p(c,58,y+40,body,839,10,16,INK,max_lines=1)
        p(c,58,y+19,'TESTE: '+action,839,10,15,MUTED,max_lines=1)
    c.showPage()
    # page7
    base(c,7);title(c,'06 | CENARIO','Uma conta, não uma promessa.','Exercício de redução hipotética de 20% dos contatos classificados como retornos no período Mai-Out/26.')
    metric(c,40,211,275,133,'CONTATOS REPETIDOS',num(cur['contatos_repetidos']),'Base do exercício, já incluida no volume total')
    metric(c,342,211,275,133,'REDUCAO HIPOTETICA',num(cur['contatos_repetidos']*.2),'20% dos retornos no recorte')
    metric(c,644,211,272,133,'CUSTO VAR. MEDIO',money(costo),'Somente a parcela variável do custo')
    rect(c,40,89,877,95,PALE,13)
    t(c,60,143,'PROXY DE CUSTO VARIAVEL EVITAVEL',12,TEAL,True)
    t(c,60,103,money(hypo),30,NAVY,True)
    p(c,477,132,'Exclui despesas de intervenção, efeito sobre qualidade, custos fixos e limites operacionais. Não representa economia realizada ou projeção de receita.',405,10,16,MUTED,max_lines=3)
    c.showPage()
    # page8
    base(c,8);title(c,'07 | METODO','Da fonte sintética à decisão.','O projeto é intencionalmente reproduzível, inclusive quando o resultado não confirma uma narrativa positiva.')
    steps=[('01. Gerar','Python com semente fixa cria 792 linhas mensais agregadas, sem dados pessoais.'),('02. Validar','Chaves únicas, volumes não negativos, pesquisas limitadas, custos fechados.'),('03. Consultar','SQLite consolida séries e permite conferir agregações e denominadores.'),('04. Visualizar','HTML offline recalcula todas as métricas para filtros de período, canal, motivo e operador.')]
    for idx,(lab,desc) in enumerate(steps):
        x=40+(idx%2)*443;y=260-(idx//2)*107
        section_box(c,x,y,421,94,lab,desc)
    rect(c,40,71,875,79,DEEP,10)
    t(c,56,121,'LIMITES E TRANSPARENCIA',11,'#6DE8C6',True)
    p(c,56,100,'Base fictícia, produzida com apoio de IA. Sem clientes reais, dados proprietários ou resultados de empresas. Relações e eventos são construídos; não representam causalidade comprovada.',826,10,16,WHITE,max_lines=2)
    c.showPage();c.save()
    return dest

if __name__=='__main__':relatorio(Path(__file__).resolve().parent.parent)
