import itertools, json, math, sys, tempfile, threading, unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coding_bank import TASKS
from judge import run
import server

class JudgeTests(unittest.TestCase):
    def test_all_reference_solutions(self):
        for task in TASKS:
            with self.subTest(task=task['id']):
                result=run(task['id'],task['solution'])
                self.assertNotIn('error',result)
                self.assertEqual(result['passed'],result['total'],result)
    def test_samples_do_not_count_as_full_submission(self):
        sample=run('c01','def solve(values, target):\n    return 2','run')
        full=run('c01','def solve(values, target):\n    return 2','submit')
        self.assertEqual(sample['passed'],sample['total'])
        self.assertLess(full['passed'],full['total'])
    def test_common_boundary_mistakes_are_rejected(self):
        for id,code in [
            ('c01','def solve(values,target):\n    return len(set(values))'),
            ('c05','def solve(values,window):\n    return [sum(values[max(0,i-window+1):i+1])/window for i in range(len(values))]'),
            ('c09','def solve(intervals,validation):\n    return [i for i,(a,b) in enumerate(intervals) if b < validation[0] or a > validation[1]]'),
            ('c11','def solve(positions,returns,cost):\n    p=[a*b for a,b in zip(positions,returns)]\n    return [p,sum(p)]')]:
            result=run(id,code)
            self.assertLess(result.get('passed',0),result.get('total',1),id)
    def test_error_stdout_and_import_handling(self):
        self.assertIn('error',run('c01','import os\ndef solve(a,b): return 0'))
        self.assertIn('error',run('c01','def solve(a,b): return open("secret")'))
        self.assertIn('error',run('c01','def solve(a,b): return a.__class__'))
        self.assertIn('error',run('c01','not valid python !'))
        result=run('c01','def solve(a,b):\n    print("debug")\n    return 0','run')
        self.assertIn('debug',result['stdout'])
        self.assertFalse(result['results'][0]['passed'])
    def test_infinite_loop_is_bounded(self):
        self.assertIn('error',run('c01','def solve(a,b):\n    while True: pass'))
    def test_error_lines_and_failed_case_arguments(self):
        syntax=run('c01','def solve(values,target):\n    return (')
        self.assertEqual(syntax['errorLine'],2)
        runtime=run('c01','def solve(values,target):\n    print("before failure")\n    return 1/0','run')
        self.assertEqual(runtime['results'][0]['errorLine'],3)
        self.assertIn('ZeroDivisionError',runtime['results'][0]['error'])
        self.assertIn('arguments',runtime['results'][0])
        self.assertIn('before failure',runtime['stdout'])
        top=run('c01','print("before failure")\n1/0\ndef solve(values,target): return 0','run')
        self.assertEqual(top['errorLine'],2)
        self.assertIn('before failure',top['stdout'])
        wrong=run('c01','def solve(values,target): return -100','run')
        self.assertIn('arguments',wrong['results'][0])

class ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank=json.loads((server.ROOT/'static/content.json').read_text())
    def test_link_integrity_and_quiz_contract(self):
        qids={q['id'] for q in self.bank['questions']}; lids={l['id'] for l in self.bank['lessons']}; cids={t['id'] for t in TASKS}
        self.assertEqual(len(qids),48);self.assertEqual(len(lids),24);self.assertEqual(len(cids),14)
        for q in self.bank['questions']:
            self.assertIn(q['lesson'],lids)
            self.assertIn(q['difficulty'],['Easy','Medium','Hard'])
            self.assertGreaterEqual(len(q['hints']),2)
            self.assertTrue(q['solution'] and q['followSolution'])
            if q['type']=='numeric':self.assertTrue(math.isfinite(q['answer']))
        for l in self.bank['lessons']:
            self.assertTrue(set(l['questions'])<=qids)
            self.assertTrue(set(l['coding'])<=cids)
            self.assertTrue(0<=l['correct']<len(l['options']))
    def test_independent_exact_checks(self):
        q={item['id']:item for item in self.bank['questions']}
        dice=list(itertools.product(range(1,7),repeat=2))
        self.assertAlmostEqual(q['q01']['answer'],sum(6 in d for d in dice)/36)
        subset=[d for d in dice if sum(d)==8]
        self.assertAlmostEqual(q['q02']['answer'],sum(a==b for a,b in subset)/len(subset))
        self.assertAlmostEqual(q['q07']['answer'],sum(max(d) for d in dice)/36)
        # Exact enumeration of overlapping indicators independently checks the variance follow-up.
        n=7;counts=[sum(a==b==1 for a,b in zip(bits,bits[1:])) for bits in itertools.product([0,1],repeat=n)]
        mean=sum(counts)/len(counts);var=sum((x-mean)**2 for x in counts)/len(counts)
        self.assertAlmostEqual(mean,(n-1)/4);self.assertAlmostEqual(var,(5*n-7)/16)
        self.assertAlmostEqual(q['q04']['answer'],.02*.9/(.02*.9+.98*.1))
        self.assertAlmostEqual(q['q13']['answer'],sum(max(i,3.5) for i in range(1,7))/6)
        self.assertAlmostEqual(q['q20']['answer'],.8*.8-math.sqrt((1-.8**2)**2))
        self.assertAlmostEqual(q['q36']['answer'],100*(.5*.5+.5*.5)/(.5*.5+.5))
        self.assertAlmostEqual(q['q46']['answer'],(2+3)/(2+2+4))

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.old=server.DATA;server.DATA=Path(cls.tmp.name)/'data/progress.json'
        cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        threading.Thread(target=cls.http.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{cls.http.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown();cls.http.server_close();server.DATA=cls.old;cls.tmp.cleanup()
    def request(self,path,obj=None,headers=None):
        return urlopen(Request(self.base+path,data=json.dumps(obj).encode() if obj is not None else None,headers={'Content-Type':'application/json',**(headers or {})}))
    def test_progress_roundtrip_and_static_separation(self):
        progress={'version':1,'updatedAt':123,'questions':{},'coding':{},'lessons':{},'drafts':{},'trainers':[]}
        self.assertEqual(json.load(self.request('/api/progress'))['state'],None)
        self.assertTrue(json.load(self.request('/api/progress',progress))['saved'])
        self.assertEqual(json.load(self.request('/api/progress'))['state'],progress)
        with self.assertRaises(HTTPError) as error:self.request('/data/progress.json')
        self.assertEqual(error.exception.code,404)
    def test_revision_conflicts_and_preview_filename(self):
        original=server.DATA
        try:
            server.DATA=Path(self.tmp.name)/'cas/progress.json'
            a={'version':1,'updatedAt':1,'questions':{},'coding':{},'lessons':{},'drafts':{'c01':'A'},'trainers':[]}
            b={**a,'updatedAt':2,'drafts':{'c01':'B'}}
            first=json.load(self.request('/api/progress',{'state':a,'revision':None}))
            self.assertTrue(first['saved'])
            for payload in [{'state':b,'revision':None},b]:
                with self.assertRaises(HTTPError) as failure:self.request('/api/progress',payload)
                self.assertEqual(failure.exception.code,409)
                conflict=json.load(failure.exception)
                self.assertEqual(conflict['state'],a)
                self.assertEqual(conflict['revision'],first['revision'])
            self.assertEqual(json.load(self.request('/api/progress'))['state'],a)
            second=json.load(self.request('/api/progress',{'state':b,'revision':first['revision']}))
            self.assertNotEqual(first['revision'],second['revision'])
            self.assertTrue(json.load(self.request('/api/progress',{'state':b,'revision':first['revision']}))['saved'])
            preview={**a,'workspace':'preview'}
            url=json.load(self.request('/api/export',preview))['url']
            response=self.request(url)
            self.assertIn('quant-atelier-test-preview-',response.headers['Content-Disposition'])
            self.assertEqual(json.load(response),preview)
            self.assertEqual(json.load(self.request('/api/progress'))['state'],b)
        finally:server.DATA=original
    def test_cross_site_and_invalid_host_rejected(self):
        for headers in [{'Origin':'https://unrelated.example'},{'Host':'unrelated.example'}]:
            with self.assertRaises(HTTPError) as error:self.request('/api/judge',{'id':'c01','code':'def solve(a,b): return 0'},headers)
            self.assertEqual(error.exception.code,403)
    def test_editor_style_nonce_and_bundle(self):
        for path in ['/', '/index.html']:
            response=self.request(path)
            html=response.read().decode()
            csp=response.headers['Content-Security-Policy']
            self.assertIn(f'content="{server.STYLE_NONCE}"',html)
            self.assertNotIn('__EDITOR_STYLE_NONCE__',html)
            self.assertIn(f"style-src 'self' 'nonce-{server.STYLE_NONCE}'",csp)
            self.assertIn("script-src 'self';",csp)
            self.assertNotIn("script-src 'self' 'unsafe-inline'",csp)
            self.assertIn('/vendor/codemirror/python-editor.js',html)
        with self.request('/vendor/codemirror/python-editor.js') as response:
            self.assertEqual(response.status,200)
            self.assertTrue(response.read())
    def test_judge_http_and_save_schema(self):
        result=json.load(self.request('/api/judge',{'id':'c01','code':TASKS[0]['solution'],'mode':'submit'}))
        self.assertEqual(result['passed'],result['total'])
        with self.assertRaises(HTTPError) as error:self.request('/api/progress',{'version':0})
        self.assertEqual(error.exception.code,400)
    def test_portable_download_snapshot_does_not_write_progress(self):
        snapshot={'version':1,'updatedAt':456,'questions':{'q01':{'solved':True}},'coding':{},'lessons':{},'drafts':{'q01':'11/36'},'trainers':[]}
        export=json.load(self.request('/api/export',snapshot))
        response=self.request(export['url'])
        self.assertIn('attachment',response.headers['Content-Disposition'])
        self.assertEqual(json.load(response),snapshot)
        self.assertFalse(server.DATA.exists())

if __name__=='__main__': unittest.main(verbosity=2)
