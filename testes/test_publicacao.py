"""Testes de publicação do dashboard e PDF V5.1."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'codigo'))

class HTMLInfo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.scripts=[]
        self._capture=False
        self._type=''
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if 'id' in data: self.ids.append(data['id'])
        if tag=='script':
            self._capture=True
            self._type=data.get('type','')
    def handle_data(self,data):
        if self._capture:self.scripts.append((self._type,data))
    def handle_endtag(self,tag):
        if tag=='script':self._capture=False

class TestPublicacao(unittest.TestCase):
    def setUp(self):
        self.html=(ROOT/'index.html').read_text(encoding='utf-8')
    def test_html_offline_identico_ao_publico(self):
        offline=ROOT/'entregaveis'/'Dashboard_CX_Case_Tecnico_V5_1.html'
        self.assertTrue(offline.exists())
        self.assertEqual(offline.read_bytes(),(ROOT/'index.html').read_bytes())
        self.assertFalse((ROOT/'entregaveis'/'Dashboard_CX_Case_Tecnico_V2.html').exists())
        self.assertFalse((ROOT/'entregaveis'/'Dashboard_CX_Case_Tecnico_V4.html').exists())
    def test_scripts_ids_e_dados(self):
        parser=HTMLInfo();parser.feed(self.html)
        self.assertEqual(len(parser.ids),len(set(parser.ids)))
        scripts=[m.group(2) for m in re.finditer(r'<script([^>]*)>([\s\S]*?)</script>',self.html,re.I)]
        self.assertEqual(len(scripts),2)
        self.assertIn('window.DATA_ROWS=',scripts[0])
        rows=json.loads(scripts[0].split('window.DATA_ROWS=',1)[1].rstrip().removesuffix(';'))
        self.assertEqual(len(rows),792)
        self.assertTrue(all(r['contatos']>=r['contatos_repetidos']>=0 for r in rows))
        if shutil.which('node'):
            for js in scripts:
                with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8') as f:
                    f.write(js);f.flush()
                    subprocess.run(['node','--check',f.name],check=True,capture_output=True,text=True)
    def test_pdf_v51_reproduzivel(self):
        try:
            import reportlab
            from pypdf import PdfReader
        except ImportError:
            self.skipTest('reportlab e pypdf necessários para validar PDF')
        from gerar_relatorio import relatorio
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            (base/'dados').mkdir()
            shutil.copy2(ROOT/'dados'/'contatos_sinteticos.csv',base/'dados'/'contatos_sinteticos.csv')
            path=relatorio(base)
            self.assertEqual(path.name,'Relatorio_Executivo_CX_V5_1.pdf')
            self.assertTrue(path.exists())
            reader=PdfReader(str(path))
            self.assertEqual(len(reader.pages),8)
            self.assertIn('V5.1',reader.pages[0].extract_text())
            self.assertIn('NPS',reader.pages[1].extract_text())
            annotations=reader.pages[-1].get('/Annots',[])
            urls=[]
            for ref in annotations:
                d=ref.get_object()
                action=d.get('/A')
                if action and action.get('/URI'): urls.append(str(action['/URI']))
            self.assertIn('https://wandersonlimas.github.io/portfolio-cx-eficiencia/',urls)
            self.assertIn('https://github.com/Wandersonlimas/portfolio-cx-eficiencia',urls)

if __name__=='__main__':
    unittest.main()
