import lib601.poly as poly
import lib601.sig
from lib601.sig import *

## You can evaluate expressions that use any of the classes or
## functions from the sig module (Signals class, etc.).  You do not
## need to prefix them with "sig."


# s = CosineSignal()
# a = CosineSignal(omega = .25, phase = 0.5)
# s.plot(-5,5)
# a.plot(-5,5)

# Problem Wk.4.1.1: Constructing Signals
# Use any: ConstantSignal, UnitSampleSignal, CosineSignal, StepSignal,
# SummedSignal, ScaledSignal, R, Rn and polyR (all defined in handout).
# They are all defined for you already

# = 3.0 for t>= 3 and 0 otherwise
step1 = Rn(ScaledSignal(StepSignal(),3),3)
step1.plot(-5,5)