# Metodologia e dicionário de dados

## 1. Escopo

**Base sintética agregada** por `mês × canal × motivo × operador`: 22 meses (jan/2025 a out/2026), 3 canais (Chat, Telefone, E-mail), 6 motivos, 2 operadores fictícios = 792 registros. Todas as variáveis e os eventos são simulados; nenhum registro contém indivíduo, protocolo, empresa real ou dado pessoal. O simulador serve para demonstrar raciocínio analítico e não substitui dados observados em campo.

## 2. Campos de entrada

| Campo CSV | Definição |
|---|---|
| `mes` | Mês de referência YYYY-MM |
| `canal` | Chat, Telefone ou E-mail (categorias fictícias) |
| `motivo` | Acesso e autenticação, Cartões e limites, Pix e transferências, Contestação, Crédito ou Cadastro |
| `parceiro` | Operador A ou Operador B, genéricos |
| `contatos` | Total de interações no grupo |
| `contatos_repetidos` | Interações marcadas sinteticamente como recontato; subconjunto de `contatos` |
| `nps_promotores`, `nps_neutros`, `nps_detratores` | Respostas NPS por categoria, todas sintéticas |
| `csat_positivas`, `csat_negativas` | Respostas CSAT binárias (satisfeito / não satisfeito), ambas sintéticas |
| `custo_variavel_centavos` | Custos variáveis modelados, valor inteiro em centavos |
| `custo_fixo_alocado_centavos` | Despesa fixa total simulada do mês rateada proporcionalmente ao volume |

Os custos mensais fixos são integralmente rateados, com ajuste de centavos na última linha do mês. Os volumes e taxas têm variabilidade sazonal e um crescimento operacional. As pesquisas NPS e CSAT são amostras independentes, aproximadas por canais; **não representam pesquisas reais nem a mesma base de respondentes**.

## 3. Cálculo dos indicadores

As medidas são sempre recalculadas depois do filtro. **Nunca se calcula NPS, CSAT, recontato ou CTS pela média simples dos percentuais de linhas.**

- **NPS em pontos** = `100 × (Σ promotores − Σ detratores) / (Σ promotores + Σ neutros + Σ detratores)`.
- **CSAT (%)** = `100 × Σ csat_positivas / (Σ csat_positivas + Σ csat_negativas)`.
- **Taxa de recontato (%)** = `100 × Σ contatos_repetidos / Σ contatos`.
- **CTS (R$/contato)** = `(Σ custo_variavel_centavos + Σ custo_fixo_alocado_centavos) / 100 / Σ contatos`.
- **Custo variável unitário (R$/contato)** = `Σ custo_variavel_centavos / 100 / Σ contatos`.
- **Contribuição dos motivos (%)** = `100 × retornos do motivo / retornos totais no filtro`.
- **Comparação do cartão** = métrica ponderada da segunda metade dos meses menos a métrica ponderada da primeira metade (quantidade de meses dividida ao meio).

### Cenário hipotético de eficiência

`Retornos marcados × percentual evitável suposto × custo variável médio unitário`.

O cálculo representa **proxy de custo variável associado a contatos que hipoteticamente deixariam de ocorrer**. Não é savings efetivo; requer validar se o retorno é realmente evitável, se o custo variável pode ser desmobilizado, custos de implementação, impacto em qualidade, tempo de resolução, unidades econômicas e efeitos indiretos.

## 4. Quebras de padrão simuladas

- Jul/2025: atrito fictício no Pix.
- Mar/2026: fricção fictícia de autenticação.
- Ago/2026: alteração fictícia em cartões, com degradação de satisfação e recontato.
- Set/2026 e out/2026: efeito residual fictício em cartões.

Esses eventos são **premissas do gerador de dados**. Usá-los para ilustrar hipóteses é válido; apresentá-los como causa descoberta a partir dos dados seria incorreto.

## 5. Limitações

1. Não há microdados por contato nem identificador individual para validar janela de recontato, reabertura de protocolo, migração de canal ou motivo resolvido.
2. O modelo de pesquisa é sintético, com probabilidades estabelecidas manualmente; não há análise de viés amostral, intervalos de confiança ou representatividade.
3. Custos fixos são rateados pelo volume, o que distorce comparações de custo quando o objetivo é alocação econômica causal.
4. Para avaliar melhorias seriam necessários logs de processo, amostras de atendimento, controle de sazonalidade, capacidade, mudança de mix e testes controlados.
5. O relatório e dashboard foram construídos com apoio de IA e exigem revisão humana antes de apresentação como trabalho autoral do usuário.

## 6. Integridade e rastreabilidade

O ETL confirma unicidade da chave (`mes`, `canal`, `motivo`, `parceiro`), ausência de contagens negativas, limites das amostras em relação aos contatos, resultados SQL consistentes com agregações em Python e soma dos custos. Testes automatizados verificam fórmulas com denominadores adequados e fechamento de volumes.

**Uso recomendado:** portfólio demonstrativo explicitamente fictício, para testar habilidade de análise, comunicação e julgamento, sem simular conquistas profissionais reais.
