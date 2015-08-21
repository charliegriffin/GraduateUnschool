import lib601.le as le
import lib601.circ as circ

ce = le.EquationSet()
#	one equation for each of the 6 components
ce.addEquation(le.Equation([1.,-1.],['e3','e0'],10.))
ce.addEquation(le.Equation([1.,-1.,-100.],['e3','e2','i3'],0.))
ce.addEquation(le.Equation([1.,-1.,-100.],['e3','e1','i2'],0.))
ce.addEquation(le.Equation([1.,-1.,-100.],['e1','e2','i6'],0.))
ce.addEquation(le.Equation([1.,-1.,-10.],['e1','e0','i4'],0.))
ce.addEquation(le.Equation([1.,-1.,-100.],['e2','e0','i5'],0.))
# Set the ground node to be zero
ce.addEquation(le.Equation([1.],['e0'],0.0))
# Specify the KCL equations for all of the nodes except e0
ce.addEquation(le.Equation([-1.,1.,-1.],['i6','i2','i4'],0.))
ce.addEquation(le.Equation([1.,1.,-1.],['i3','i6','i5'],0.))
ce.addEquation(le.Equation([1.,-1.,-1.],['i1','i2','i3'],0.))
print ce.solve()

ce1 = circ.Circuit([
    # Enter your circuit components here
    ])
print ce1.solve('e0')
