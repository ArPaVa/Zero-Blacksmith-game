# importing sys
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
 
# adding F0F to the system path
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'F0F'))

import F0Fmain 
from F0FDefinitions import MFUN
import numpy as np

def Pol1(x):
    x = x[0]
    return x**3 + x - 1
pol1 = MFUN(Pol1,1,-5,5,'')
def Pol2(x):
    x = x[0]
    return 2*(x**3) - x - 7
pol2 = MFUN(Pol2,1,-5,5,'')
def Pol3(x):
    x = x[0]
    return x**4 - 3*x**3 - 10
pol3 = MFUN(Pol3,1,-5,5,'')
def Pol4(x):
    x = x[0]
    return x**3 + 6*(x**2) + 11*x - 6
pol4 = MFUN(Pol4,1,-5,5,'')
def Pol5(x):
    x = x[0]
    return x**3 - 2*(x**2) + (3/2)*x
pol5 = MFUN(Pol5,1,-5,5,'')
def Pol6(x):
    x = x[0]
    return 3*(x+1) * (x-0.5) * (x-1)
pol6 = MFUN(Pol6,1,-5,5,'')
def Pol7(x):
    x = x[0]
    return 4*(x**4) - 6*(x**2) - 11/4
pol7 = MFUN(Pol7,1,-5,5,'')

def Trig1(x):
    x = x[0]
    return (np.cos(x))**2 + 6 - x
trig1 = MFUN(Trig1,1,-5,20,'cos(x)^2 + 6 - x')
def Trig2(x):
    x = x[0]
    return np.sin(x) - 6*x - 5
trig2 = MFUN(Trig2,1,-5,5,'sin(x) - 6*x - 5')
def Trig3(x):
    x = x[0]
    return 2*x * np.cos(2*x) - (x + 1)**2
trig3 = MFUN(Trig3,1,-10,-2,'2*x * cos(2*x) - (x + 1)^2')
def Trig4(x):
    x = x[0]
    return x**2 - 4*np.sin(x)
trig4 = MFUN(Trig4,1,-5,5,'x^2 - 4*sin(x)')
def Trig5(x):
    x = x[0]
    return np.sqrt(x) - np.cos(x)
trig5 = MFUN(Trig5,1,0.1,15,'sqrt(x)-cos(x)')
def Trig6(x):
    x = x[0]
    return x*np.cos(x) - 2*x**2 + 3*x - 1
trig6 = MFUN(Trig6,1,-5,5,'x*cos(x) - 2*x^2 + 3*x - 1')

def Inv1(x):
    x = x[0]
    return x**2 + 1/(x + 1) - 3*x
inv1 = MFUN(Inv1,1,-3,-1.15,'x^2 + 1/(x + 1) - 3*x')
def Inv2(x):
    x = x[0]
    return 7/(x**5) + 13*np.sin(x)
inv2 = MFUN(Inv2,1,-25,-20,'7/(x**5) + 13*sin(x)')
def Inv3(x):
    x = x[0]
    return 1/(x + x**2) + 3.2 * np.log(x) 
inv3 = MFUN(Inv3,1,0.15,5,'1/(x + x^2) + 3.2 * ln(x) ')

def Log1(x):
    x = x[0]
    return np.log(x) + x**2 - 3
log1 = MFUN(Log1,1,0.1,5,'ln(x) + x^2 - 3')
def Log2(x):
    x = x[0]
    return np.log(x-1) + np.cos(x-1)
log2 = MFUN(Log2,1,1.0001,6,'ln(x-1) + cos(x-1)')

def Exp1(x):
    x = x[0]
    return 3*x - np.e**x
exp1 = MFUN(Exp1,1,-5,5,'3*x - e^x')
def Exp2(x):
    x = x[0]
    return np.e**x - 3
exp2 = MFUN(Exp2,1,-5,5,'')
def Exp3(x):
    x = x[0]
    return x - 2**(-x)
exp3 = MFUN(Exp3,1,-5,5,'')
def Exp4(x):
    x = x[0]
    return np.e**(-x) - x
exp4 = MFUN(Exp4,1,-5,5,'')
def Exp5(x):
    x = x[0]
    return np.e**(1 - x**2) - x**2 + 1
exp5 = MFUN(Exp5,1,-5,5,'')
def Exp6(x):
    x = x[0]
    return np.e**x + x - 7
exp6 = MFUN(Exp6,1,-5,5,'')
def Exp7(x):
    x = x[0]
    return 4*x**2 - np.e**x - np.e**(-x)
exp7 = MFUN(Exp7,1,-15,15,'')

def TrEx1(x):
    x = x[0]
    return np.sin(x) - np.e**(-x)
trex1 = MFUN(TrEx1,1,-1,15,'sin(x) - e^(-x)')
def TrEx2(x):
    x = x[0]
    return np.e**(x) + 2**(-x) + 2*np.cos(x) - 6
trex2 = MFUN(TrEx2,1,-10,10,'')
def TrEx3(x):
    x = x[0]
    return np.e**(x) + np.sin(x) - 4
trex3 = MFUN(TrEx3,1,-20,2,'')
def TrEx4(x):
    x = x[0]
    return np.cos(np.e**(x) - 2) - np.e**(x) + 2
trex4 = MFUN(TrEx4,1,-5,5,'')

def Pol8(x):
    x = x[0]
    return 2*(x**2) - x**3 - 2
pol8 = MFUN(Pol8,1,-5,5,'2x^2 - x^3 - 2')
def Exp8(x):
    x = x[0]
    return np.log(np.e**x + np.e**(-x)) - 54
exp8 = MFUN(Exp8,1,-70,60,'ln(e^x + e^(-x)) - 54')
def Trig7(x):
    x = x[0]
    return (np.sin(x**2))**2 - np.e / 7
trig7 = MFUN(Trig7,1,-2.5,0,'sin^2(x^2) - e/7')
def Trig8(x):
    x = x[0]
    return 4*(np.sin(x)**3) - 1
trig8 = MFUN(Trig8,1,-10,40,'4 * sin(x^3) - 1')
def Trig9(x):
    x = x[0]
    return x**2 * np.arctan(x**3) - 732
trig9 = MFUN(Trig9,1,-60,40,'x^2 * arctan(x^3) - 732')
def Log3(x):
    x = x[0]
    return - np.log(8 * x**7)
log3 = MFUN(Log3,1,0.1,5,'- ln(8 * x^7)')
def Other1(x):
    x = x[0]
    if x < 0:
        sgn = -1
    elif x > 0:
        sgn = 1
    else: sgn = 0
    return sgn * np.sqrt(abs(x)) - 14.7
other1 = MFUN(Other1,1,100,300,'sgn(x) * sqrt(|x|) - 14.7')
def Other2(x):
    x = x[0]
    return np.sqrt(abs(x**3 + 312)) - x -19
other2 = MFUN(Other2,1,-10,5,'sqrt(|x**3 + 312|) - x -19')
def Other3(x):
    x = x[0]
    return abs(3*x - 12)
other3 = MFUN(Other3,1,-10,10,'|3*x - 12|')
def Other4(x):
    x = x[0]
    return (x + 7.7777777)**5
other4 = MFUN(Other4,1,-10,10,'(x + 7.7777777) ^ 5')
def Other5(x):
    x = x[0]
    return np.sqrt((x-5)**2) - np.cos(x)
other5 = MFUN(Other5,1,0,10,'sqrt((x - 5)^2) - cos(x)')

def Snk1(x):
    x = x[0]
    return np.cos(x)
snk1 = MFUN(Snk1,1,0,4.5,'cos(x)')
def Snk2(x):
    x = x[0]
    return np.sin(x + 1)
snk2 = MFUN(Snk2,1,0,4.5,'sin(x + 1)')


###### Functions Information, like graphs, extremes to give and time to compute. 
###### Later they'll be grouped by time, indicating the difficulty

mfuns = [pol1, pol2, pol3, pol4, pol5, pol6, pol7, 
         trig1, trig2, trig3, trig4, trig5, trig6, 
         exp1, exp2, exp3, exp4, exp5, exp6, exp7,
         trex1, trex2, trex3, trex4,
         inv1, log1, log2, snk1, snk2,
         pol8, exp8, trig7, trig8, trig9, log3,
         other1, other2, other3, other4,
         snk1, snk2]

def time_info(solver_name:str):
    file = os.path.join(os.path.dirname(__file__), 'functions', solver_name+'_time_data.txt')
    data = ""
    for mf in mfuns:
        start = time.time()
        result = F0Fmain.main(solver_name + '.txt', [mf,mf.llim,mf.rlim])
        end = time.time()
        zeroEval = abs(mf(result[0]))
        data += str((result, round(end-start, 3), zeroEval <= 1e-5 )) + '\n'
    save = open(file,'w+')
    save.write(data)
    save.close()
    
def graph():
    j = 1
    for mf in mfuns:
        mf:MFUN
        X = np.linspace(mf.llim, mf.rlim, int(mf.rlim-mf.llim)*60)    
        Y = []      
        for i in range(len(X)):
            Y.append(mf(tuple([X[i]])))

        path = os.path.join(os.path.dirname(__file__), 'functions', '0'+str(j)+'.png')
        
        plt.figure(j)
        plt.ylim(-5,5)
        plt.plot(X,Y)
        plt.title(str(mf))
        plt.savefig(path, format='png')
        # plt.show()
        plt.close()
        j+=1