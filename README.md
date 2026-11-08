# Case 01 | Customer Experience & Eficiência Operacional · V5.1

[**Abrir dashboard interativo**](https://wandersonlimas.github.io/portfolio-cx-eficiencia/) · [**Código-fonte no GitHub**](https://github.com/Wandersonlimas/portfolio-cx-eficiencia)

**Autor do portfólio:** Wanderson Limas  
**Natureza:** projeto demonstrativo gerado com apoio de IA, para estudo, revisão e apresentação de competências analíticas.  
**Dados:** 100% sintéticos, sem qualquer ligação com informações reais de empresas, clientes, contratos ou pessoas.

## Dashboard V5.1: layout lateral claro e responsivo

A versão pública apresenta identidade visual clara em marfim, ameixa, lilás e coral, menu lateral fixo nas telas grandes e navegação horizontal no celular, com cinco áreas, filtros globais, gráficos SVG com interação e distribuição por canal. Mantém os mesmos 792 registros sintéticos, indicadores ponderados e simulação de eficiência. O site foi recompilado a partir dos módulos HTML/CSS/JavaScript e passou por verificações estáticas de integridade dos scripts.

- **Visão executiva:** cinco KPIs ponderados, minigráficos, série temporal selecionável, composição dos canais, ranking de recontatos e insights determinísticos.
- **Performance:** quatro séries temporais selecionáveis com tooltip e tabela mensal auditável.
- **Diagnóstico:** motivos de recontato, comparação por canais e operadores e hipóteses de investigação.
- **Cenários:** simulador de redução hipotética de recontato, sem atribuir economias realizadas.
- **Engenharia:** fluxo CSV → validação → SQLite/Python → métricas → dashboard/relatório.

Os dados são sempre 100% sintéticos. A página é autocontida e roda offline. O painel foi reconstruído mantendo o algoritmo das métricas e as dimensões de filtro. O frontend é modular em `src/web/`, e `codigo/construir_dashboard.py` compila CSS, JavaScript e registros sintéticos em um único `index.html`.

## O que está incluído

| Local | Conteúdo |
|---|---|
| `entregaveis/Relatorio_Executivo_CX_V2.pdf` | Relatório executivo de 8 páginas para a seção Em destaque do LinkedIn |
| `entregaveis/Dashboard_CX_Case_Tecnico_V4.html` | Dashboard V5.1 offline autocontido, idêntico à versão pública |
| `entregaveis/Dashboard_CX_Case_Tecnico_V2.html` | Versão V2 anterior, preservada para histórico |
| `index.html` | Dashboard V5.1 público, publicado pelo GitHub Pages na raiz `/` |
| `dados/contatos_sinteticos.csv` | Fonte agregada com 792 observações |
| `dados/indicadores_processados.json` | Resultados agregados via SQL e Python |
| `codigo/gerar_dados.py` | Gerador sintético com semente fixa `20261108` |
| `codigo/processar_etl.py` | Valida dados, agrega SQLite, calcula métricas ponderadas e exporta JSON |
| `codigo/consultas.sql` | Exemplos de queries reexecutáveis no SQLite após criação da tabela |
| `codigo/construir_dashboard.py` | Compila a interface V4 a partir do frontend modular e do CSV validado |
| `codigo/gerar_relatorio.py` | Gera o PDF a partir do CSV processado |
| `src/web/templates/dashboard.html` | Estrutura HTML editável e documentada do dashboard V4 |
| `src/web/css/dashboard.css` | Design system responsivo em CSS puro |
| `src/web/js/dashboard.js` | Filtros, séries, KPIs, exportação, análises e simulador |
| `codigo/executar_projeto.py` | Pipeline completo |
| `testes/test_pipeline.py` | Testes automáticos de integridade e fórmulas |
| `METODOLOGIA.md` | Dicionário de dados, indicadores e limitações |

## Executar no Mac

**Para apenas visualizar**, acesse o [dashboard online](https://wandersonlimas.github.io/portfolio-cx-eficiencia/) ou abra `entregaveis/Dashboard_CX_Case_Tecnico_V4.html` no Chrome. Ele funciona offline, sem acesso à rede. Use os filtros de período, canal, motivo e operador e o simulador de redução de recontatos.

**Para reproduzir os dados, dashboard e PDF**, é necessário Python 3 e ReportLab:

```bash
python3 -m pip install reportlab
python3 codigo/executar_projeto.py
python3 -m unittest discover -s testes -v
```

Se seu Mac impedir instalação no Python global, crie um ambiente virtual antes:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab
python codigo/executar_projeto.py
python -m unittest discover -s testes -v
```

O gerador usa semente determinística, de modo que os valores serão os mesmos na mesma versão do Python. O gerador atualiza `index.html` e o HTML offline. O PDF continua sendo o relatório executivo V2, identificado como documento histórico, não uma nova edição visual. O dashboard V4 possui arquivo offline independente.

## Como interpretar o dashboard

- Os cartões representam o período **inteiro** atualmente filtrado.
- A variação mostrada em cada cartão compara **segunda metade versus primeira metade** da seleção, com pesos corretos. Ex.: em um recorte de 6 meses, meses 4–6 versus meses 1–3. A variação **não** é mês contra mês.
- NPS utiliza respondentes NPS; CSAT utiliza respondentes CSAT; taxa de recontato utiliza volume de contatos; CTS utiliza despesa total dividida pelo volume de contatos.
- O simulador **não prevê economia**. Ele calcula: `retornos × percentual hipotético evitável × custo variável médio por contato`.
- Os eventos modelados em jul/2025, mar/2026 e ago–set/2026 foram **inventados** para apresentar rupturas, tendências conflitantes e hipóteses de investigação. Nenhuma causa é comprovada em operação real.

## Publicar no LinkedIn

1. Revise o PDF, confirme que domina os cálculos e adapte a redação à sua experiência.
2. No LinkedIn, entre em **Em destaque** e atualize o link do dashboard para a versão V4; mantenha o PDF V2 identificado como relatório complementar, para evitar duplicação.
3. Título recomendado: **CX e Eficiência Operacional | Case técnico demonstrativo (dados sintéticos)**.
4. Descrição recomendada: **Estudo de BI e análise operacional com dados sintéticos. Inclui modelo de dados, ETL reproduzível em Python/SQLite, análise de NPS, CSAT, recontato e CTS, segmentações e simulações ilustrativas. Desenvolvido com apoio de ferramentas de IA. Não representa resultados reais de empresas.**
5. Para exibir o dashboard **interativo** nos Destaques, adicione o link público do GitHub Pages. Não é possível rodar código HTML diretamente como documento no LinkedIn.

### Publicação no GitHub Pages

Este repositório publica o arquivo `index.html` da **raiz** pela configuração **Settings → Pages → Deploy from a branch → main / (root)**. Endereço público: https://wandersonlimas.github.io/portfolio-cx-eficiencia/ . O HTML em `entregaveis/` é uma cópia offline e não deve substituir o `index.html` da raiz. Os dados e os códigos ficam disponíveis para inspeção e reprodução. Todos os dados são sintéticos; revise o conteúdo antes de compartilhar o repositório.

## Boas práticas de apresentação

Esse material foi criado como demonstração com apoio de IA. Ele não comprova por si só execução anterior do projeto em uma operação real, nem deve ser citado como conquista profissional real. Antes de apresentá-lo como parte do seu portfólio pessoal, revise a lógica, adapte a análise e esteja pronto para explicar os scripts e as limitações.
