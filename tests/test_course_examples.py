"""Independent arithmetic checks for the expanded lessons' delicate examples."""
import itertools
import math
import unittest
from fractions import Fraction as F

class ExpandedExampleTests(unittest.TestCase):
    def test_fill_selection_by_enumeration(self):
        fills=[value for value,informed in itertools.product((0,100),(False,True)) if not informed or value==100]
        self.assertEqual(F(sum(fills),len(fills)),F(200,3))
        self.assertEqual(F(sum(55-v for v in fills),4),F(-35,4))

    def test_continuation_values(self):
        continuation=F(7,2)
        self.assertEqual(sum(max(F(x),continuation) for x in range(1,7))/6,F(17,4))
        self.assertEqual(sum(max(F(x),continuation-1) for x in range(1,7))/6,F(23,6))
        self.assertEqual(sum(max(F(x),F(17,4)) for x in range(1,7))/6,F(14,3))
        self.assertAlmostEqual(.6*math.log(1.2)+.4*math.log(.8),.0201355135506888)
        self.assertLess(.6*math.log(1.5)+.4*math.log(.5),0)

    def test_variance_reduction_by_polynomial_integrals(self):
        def integral(poly):return sum((coef/F(i+1) for i,coef in enumerate(poly)),F(0))
        def multiply(a,b):
            out=[F(0)]*(len(a)+len(b)-1)
            for i,x in enumerate(a):
                for j,y in enumerate(b):out[i+j]+=x*y
            return out
        square=[F(0),F(0),F(1)];reflected=[F(1),F(-2),F(1)]
        var=integral(multiply(square,square))-integral(square)**2
        cov=integral(multiply(square,reflected))-integral(square)*integral(reflected)
        self.assertEqual(var,F(4,45));self.assertEqual(cov,F(-7,90))
        self.assertEqual((var+cov)/2,F(1,180))
        controlled=[F(1,2),F(-1),F(1)]
        self.assertEqual(integral(controlled),F(1,3))
        self.assertEqual(integral(multiply(controlled,controlled))-integral(controlled)**2,F(1,180))

    def test_finite_dependence_and_selection(self):
        n=100;rho=.8
        factor=1+2*sum((1-h/n)*rho**h for h in range(1,n))
        self.assertAlmostEqual(factor,8.6,places=8)
        self.assertAlmostEqual(n/factor,11.6279069767)
        posterior=.02*.9**2/(.02*.9**2+.98*.1**2)
        self.assertAlmostEqual(posterior,81/130)
        self.assertEqual((7*F(9,100)+3*F(49,100))/10,F(21,100))
