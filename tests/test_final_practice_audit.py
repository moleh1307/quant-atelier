"""Whole-bank compatibility, authoring gates and semantic notation regressions.

The public baseline contains pre-expansion assessment contracts, never user data.
"""
import copy
import json
import math
import re
import unittest
from fractions import Fraction as F
from pathlib import Path

from coding_bank import TASKS
from math_markup import math_text
from test_distribution_stopping_practice import pattern_mean_from_states, exact_linear_solve
from test_topic_practice import BANK, QUESTIONS
from topic_practice import attach_and_validate, validate_coding

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT/'tests/fixtures/original-practice-contract.json').read_text())


class FinalPracticeAuditTests(unittest.TestCase):
    def test_every_original_assessment_and_journey_is_preserved(self):
        self.assertEqual(len(BASELINE['questions']),51)
        for old in BASELINE['questions']:
            self.assertEqual({key:QUESTIONS[old['id']][key] for key in old},old)
        current={l['id']:l for l in BANK['lessons']}
        for old in BASELINE['lessons']:
            l=current[old['id']]
            self.assertEqual(l['path'],old['path'])
            self.assertLessEqual(set(old['questions']),set(l['questions']))
            self.assertLessEqual(set(old['coding']),set(l['coding'])|set(l.get('legacyCoding',[])))
        # Classification changes do not change the permanent exercise contract.
        task=next(t for t in TASKS if t['id']=='c14')
        self.assertEqual(task['path'],'trader')
        self.assertIn('c14',current['l24']['coding'])
        self.assertIn('c14',current['l18']['legacyCoding'])

    def test_future_counts_do_not_permit_placeholder_authoring(self):
        for field in ('prompt','solution','followup','followSolution'):
            questions=copy.deepcopy(BANK['questions']);questions[0][field]=' '
            with self.assertRaisesRegex(ValueError,'authored prompt, solution and follow-up'):
                attach_and_validate(copy.deepcopy(BANK['lessons']),questions,TASKS)
        for field,value,message in (
            ('hints',['help'],'meaningful hints'),
            ('rubric',['State the assumptions and the object you are computing.','generic'], 'generic assessment placeholder'),
            ('lesson','unknown','registered topic owner')):
            questions=copy.deepcopy(BANK['questions']);questions[0][field]=value
            with self.assertRaisesRegex(ValueError,message):
                attach_and_validate(copy.deepcopy(BANK['lessons']),questions,TASKS)
        for q in BANK['questions']:
            self.assertNotIn('State the assumptions and the object you are computing.',q['rubric'])
            self.assertGreaterEqual(len(q['rubric']),2)
        for key,value,message in (
            ('solution',' ','authored solution'),
            ('explanation',None,'authored explanation'),
            ('tests',[],'visible and hidden cases'),
            ('samples',[{'args':[]}],'complete case arguments and expectations')):
            tasks=copy.deepcopy(TASKS);tasks[0][key]=value
            with self.assertRaisesRegex(ValueError,message):validate_coding(tasks)

    def test_complete_numerals_and_fraction_parameters_survive_markup(self):
        for numeral in ('10','40','400','1000','100000','100.1'):
            for variable in ('T','n','p'):
                value=math_text(f'Use {variable}={numeral} now.')
                self.assertNotRegex(value,r'\\\)\d')
                self.assertIn(f'{variable}={numeral}',value)
        self.assertEqual(math_text('Use p=1/4 and p=1/2.'),r'Use p=\(\frac{1}{4}\) and p=\(\frac{1}{2}\).')
        self.assertEqual(math_text('Use p=1, then n=4.'),r'Use \(p=1\), then \(n=4\).')
        self.assertEqual(math_text('Use p=0.031.'),'Use p=0.031.')
        for item in BANK['questions']:
            for field in ('prompt','solution','followup','followSolution','hints','rubric'):
                value=item[field];value=' '.join(value) if isinstance(value,list) else value
                self.assertNotRegex(value,r'\\\)(?:\d|/\d)',(item['id'],field))
        # Summation and covariance retain distinct meanings.
        for id,field in [('q_l13_m1','prompt'),('q_l13_m2','prompt'),
                         ('q_l13_h1','prompt'),('q_l18_m1','prompt'),('q_l22_m1','solution')]:
            self.assertIn(r'\sum',QUESTIONS[id][field])
            self.assertNotIn(r'\(\Sigma\)',QUESTIONS[id][field])
        self.assertIn(r'\Sigma',QUESTIONS['q_l10_h2']['prompt'])
        self.assertIn('Define',QUESTIONS['q_l13_m1']['prompt'])
        self.assertIn(r'Y_t=X_t^2',QUESTIONS['q_l13_m1']['prompt'])

    def test_retained_stopping_and_changed_cutting_proofs(self):
        for k in range(1,7):
            for p in (F(1,4),F(1,2),F(2,3)):
                direct=pattern_mean_from_states('H'*k,p)
                self.assertEqual(direct,(1-p**k)/((1-p)*p**k))
        # Solve every interior-state expectation, without the displayed quadratic.
        matrix=[[F(int(i==j)) for j in range(11)] for i in range(11)]
        for i in range(11):
            for j in (i-1,i+1):
                if 0<=j<11:matrix[i][j]-=F(1,2)
        waits=exact_linear_solve(matrix,[1]*11)
        self.assertEqual(waits,[F(i*(12-i)) for i in range(1,12)])
        self.assertEqual(QUESTIONS['q12']['answer'],waits[4])
        # Independent midpoint integration of the conditional length probabilities.
        n=20000
        probability=sum(((u/(1-u)) if u<.5 else ((1-u)/u))/2
                        for u in ((i+.5)/n for i in range(n)))/n
        self.assertAlmostEqual(probability,math.log(2)-.5,places=8)
        self.assertLess(probability,QUESTIONS['q14']['answer'])
        self.assertIn(r'\log 2',QUESTIONS['q14']['followSolution'])


if __name__=='__main__':unittest.main()
