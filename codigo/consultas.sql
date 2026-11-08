-- Consultas demonstrativas: todos os dados são sintéticos.
-- Códigos de evento NÃO estão disponíveis; esta base é agregada por mês, canal, motivo, operador.
-- Exemplo A: indicador de recontato e CTS por motivo, sem médias indevidas.
SELECT motivo,
       SUM(contatos) AS contatos,
       ROUND(100.0 * SUM(contatos_repetidos) / NULLIF(SUM(contatos),0), 2) AS recontato_pct,
       ROUND((SUM(custo_variavel_centavos) + SUM(custo_fixo_alocado_centavos)) / 100.0
           / NULLIF(SUM(contatos),0), 2) AS cts_brl
FROM contatos
WHERE mes BETWEEN '2026-05' AND '2026-10'
GROUP BY motivo
ORDER BY SUM(contatos_repetidos) DESC;

-- Exemplo B: NPS ponderado pelos respondentes, não média de NPS por canal.
SELECT mes,
       ROUND(100.0 * (SUM(nps_promotores)-SUM(nps_detratores)) /
           NULLIF(SUM(nps_promotores+nps_neutros+nps_detratores),0), 1) AS nps_pontos
FROM contatos
GROUP BY mes
ORDER BY mes;

-- Exemplo C: custo variável por canal para construção de cenários.
SELECT canal, SUM(contatos) AS volume,
       ROUND(SUM(custo_variavel_centavos)/100.0/NULLIF(SUM(contatos),0),2) AS custo_variavel_unitario
FROM contatos
GROUP BY canal;
