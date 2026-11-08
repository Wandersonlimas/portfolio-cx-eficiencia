import sys, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'codigo'))
from processar_etl import ler_validar,agrupar,sql_agregar

class TesteIndicadores(unittest.TestCase):
    def test_contagens_e_consistencia(self):
        rows=ler_validar(P/'dados'/'contatos_sinteticos.csv')
        self.assertEqual(len(rows),792)
        s=agrupar(rows)
        self.assertGreater(s['contatos'],1000000)
        self.assertLess(s['recontato'],40)
        self.assertGreater(s['csat'],60)
        self.assertGreater(s['cts'],0)
        meses,_=sql_agregar(rows)
        self.assertEqual(sum(m['contatos'] for m in meses),s['contatos'])
        self.assertEqual(sum(m['contatos_repetidos'] for m in meses),s['contatos_repetidos'])
    def test_ponderacao_respostas(self):
        rows=ler_validar(P/'dados'/'contatos_sinteticos.csv')
        sel=[r for r in rows if r['mes']=='2026-08']
        s=agrupar(sel)
        n=s['nps_promotores']+s['nps_neutros']+s['nps_detratores']
        self.assertAlmostEqual(s['nps'],100*(s['nps_promotores']-s['nps_detratores'])/n)
        self.assertAlmostEqual(s['cts'],(s['custo_variavel_centavos']+s['custo_fixo_alocado_centavos'])/100/s['contatos'])
    def test_dados_sao_agregados_sem_pii(self):
        rows=ler_validar(P/'dados'/'contatos_sinteticos.csv')
        self.assertNotIn('cliente',rows[0]);self.assertNotIn('cpf',rows[0]);self.assertNotIn('id_contato',rows[0])

if __name__=='__main__': unittest.main()
