# importing sys
import sys
import os
 
# adding F0F to the system path
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'F0F'))

import F0Fmain 
from F0FDefinitions import MFUN
# import F0FErrors
import random as rnd
import time
import numpy as np
import matplotlib.pyplot as plt
import Functions

def compile(code:str,forge_args):
    return F0Fmain.main(code=code,forge_args=forge_args)

class FunctDetails:
    def __init__(self, funct_list: list, funct_dist: list = None):
        self.funct_list = funct_list
        self.funct_dist = funct_dist
        if type(self.funct_list) == list and self.funct_dist == None:
            # set uniform distribution
            prob = 1 / len(self.funct_list)
            self.funct_dist = [prob] * len(self.funct_list)
        
    @staticmethod
    def check_zero(funct:MFUN, point:tuple, tolerance = 1e-5) -> bool:
        value = funct(tuple(point))
        # print(funct, value, tolerance)
        return abs(value) <= tolerance
          
    @staticmethod  
    def graph(funct:MFUN, center_at:int,name:str) -> str:
        llim = center_at - 5
        rlim = center_at + 5
        X = np.linspace(llim, rlim, 60)    
        Y = []      
        for i in range(len(X)):
            Y.append(funct(tuple([X[i]])))
        path = os.path.join("resources", "curr_funct", name+".png")
        plt.ylim(-5,5)
        plt.plot(X,Y)
        plt.plot([center_at],[funct(center_at)])
        plt.title(str(funct))
        plt.savefig(path, format='png')
        plt.close()
        return path
    
    def get_funct(self) -> MFUN:
        if type(self.funct_list) == list and self.funct_dist == None:
            # set uniform distribution
            prob = 1 / len(self.funct_list)
            self.funct_dist = [prob] * len(self.funct_list)
        if type(self.funct_list) != list or type(self.funct_dist) != list:
            return None
        rnd.seed = time.time()
        return rnd.choices(self.funct_list, self.funct_dist,k=1)[0]
