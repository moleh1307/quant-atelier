"""Editable cases must help debugging without weakening official grading."""
import copy, json, sys, threading, unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coding_bank import TASKS
from judge import run, submission_cases
import server

class DebugTests(unittest.TestCase):
    def debug(self, code, args, expected='', task='c01'):
        return run(task,code,'debug',[{'argumentsJSON':args,'expectedJSON':expected}])
    def test_optional_expected_is_not_a_pass_and_null_is_explicit(self):
        code='def solve(a,b): return None'
        output=self.debug(code,'[[],0]')
        self.assertEqual(output['mode'],'debug');self.assertIsNone(output['results'][0]['passed']);self.assertEqual(output['passed'],0)
        self.assertNotIn('expectedJSON',output['results'][0])
        checked=self.debug(code,'[[],0]','null')
        self.assertTrue(checked['results'][0]['passed']);self.assertEqual(checked['results'][0]['expectedJSON'],'null')
    def test_nested_and_large_numeric_values_survive_copy_exactly(self):
        args='[[[9007199254740993, null, {"a": [true, 0.125]}]], 0]'
        expected='[[9007199254740993, null, {"a": [true, 0.125]}]]'
        result=self.debug('def solve(a,b): return a',args,expected)
        self.assertEqual(result['passed'],1,result)
        case=result['results'][0]
        self.assertEqual(json.loads(case['argumentsJSON']),json.loads(args))
        self.assertEqual(json.loads(case['expectedJSON']),json.loads(expected))
        self.assertEqual(run('c01','def solve(a,b): return a','debug',[case])['passed'],1)
        # Integer cases are exact, even beyond JavaScript's safe integer range.
        self.assertEqual(self.debug('def solve(a,b): return 9007199254740992','[[],0]','9007199254740993')['passed'],0)
        self.assertEqual(self.debug('def solve(a,b): return 9007199254740993.0','[[],0]','9007199254740993')['passed'],0)
        self.assertEqual(self.debug('def solve(a,b): return 0','[[],0]','false')['passed'],0)
        # Preserve the existing numerical tolerance for ordinary float results.
        self.assertEqual(self.debug('def solve(a,b): return 2.000000001','[[],0]','2')['passed'],1)
    def test_invalid_cases_have_actionable_errors(self):
        for args,expected,message in [('oops','','Debug case 1'),('{}','','JSON array'),('[1]','','expects 2 arguments'),('[1,2]','oops','Debug case 1'),('[NaN,0]','','finite'),('[1e999,0]','','finite')]:
            with self.subTest(args=args,expected=expected):self.assertIn(message,self.debug('def solve(a,b): return a',args,expected)['error'])
        for cases in [None,[],[{}]*21]:self.assertIn('1 and 20',run('c01','def solve(a,b): return a','debug',cases)['error'])
        self.assertIn('Unknown check mode',run('c01','def solve(a,b): return a',[])['error'])
    def test_runtime_failure_retains_complete_copy(self):
        args=json.dumps([list(range(1000)),0])
        result=self.debug('def solve(a,b): return 1/0',args,'null')['results'][0]
        self.assertFalse(result['passed']);self.assertIn('ZeroDivisionError',result['error']);self.assertEqual(result['errorLine'],1)
        self.assertEqual(json.loads(result['argumentsJSON']),json.loads(args));self.assertEqual(result['expectedJSON'],'null')
        self.assertGreater(len(result['argumentsJSON']),450)
    def test_submission_cases_are_exact_copies_and_cannot_replace_suite(self):
        original=copy.deepcopy(TASKS)
        for task in TASKS:
            cases=submission_cases(task['id'])['cases']
            bank=task['samples']+task['tests']
            self.assertEqual(len(cases),len(bank))
            for index,(copied,official) in enumerate(zip(cases,bank)):
                self.assertEqual(copied['caseNumber'],index+1)
                self.assertEqual(json.loads(copied['argumentsJSON']),official['args'])
                self.assertEqual(json.loads(copied['expectedJSON']),official['expected'])
        fake=[{'argumentsJSON':'[[],0]','expectedJSON':'2'}]
        result=run('c01','def solve(a,b): return 2','submit',fake)
        self.assertGreater(result['total'],len(fake));self.assertLess(result['passed'],result['total'])
        failed=next(case for case in result['results'] if not case['passed'])
        self.assertEqual(run('c01','def solve(a,b): return 2','debug',[failed])['passed'],0)
        failed['argumentsJSON']='[[],0]';failed['expectedJSON']='2'
        self.assertEqual(run('c01','def solve(a,b): return 2','debug',[failed])['passed'],1)
        self.assertEqual(TASKS,original)

class DebugHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        threading.Thread(target=cls.http.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{cls.http.server_port}'
    @classmethod
    def tearDownClass(cls):cls.http.shutdown();cls.http.server_close()
    def post(self,path,body,origin=None):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        return urlopen(Request(self.base+path,data=json.dumps(body).encode(),headers=headers))
    def test_cases_endpoint_and_custom_judge(self):
        self.assertEqual(json.load(self.post('/api/coding-cases',{'id':'c01'})),submission_cases('c01'))
        result=json.load(self.post('/api/judge',{'id':'c01','mode':'debug','code':'def solve(a,b): return a','cases':[{'argumentsJSON':'[[1,2],0]','expectedJSON':'[1,2]'}]}))
        self.assertEqual(result['passed'],1);self.assertEqual(result['mode'],'debug')
        with self.assertRaises(HTTPError) as err:self.post('/api/coding-cases',{'id':'missing'})
        self.assertEqual(err.exception.code,404)
        with self.assertRaises(HTTPError) as err:self.post('/api/coding-cases',{'id':'c01'},'https://evil.example')
        self.assertEqual(err.exception.code,403)

if __name__=='__main__':unittest.main()
