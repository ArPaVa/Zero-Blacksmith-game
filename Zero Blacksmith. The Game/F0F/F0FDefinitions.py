import AST_nodes
import time
from F0FErrors import *

class Return_asExc(RuntimeError):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
class Callable:
    def arity(self) -> int:
        pass
    def call(self,interpreter, arguments:list):
        pass
class globals_clock(Callable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter, arguments: list):
        return time.time()

class F0FFunctions(Callable):
    def __init__(self,declaration:AST_nodes.Function,closure):
        self.declaration = declaration
        self.closure = closure
    def arity(self) -> int:
        return len(self.declaration.parameters)
    def call(self, interpreter, arguments: list):
        env = Enviroment(self.closure)
        for i in range(self.arity()):
            env.define(self.declaration.parameters[i].name,arguments[i])
        try: 
            interpreter.executeBlock(self.declaration.body,env)
        except Return_asExc as ret:
            return ret.value

class Derivate(Callable):
    def arity(self) -> int:
        # function and degree
        return 2
    def call(self, interpreter, arguments: list):
        mfun:MFUN = arguments[0]
        if not isinstance(mfun,MFUN):
            raise TypeError('The derivative first argument must be a mathematical function.')
        point = arguments[1]
        # if len(arguments) > 2:
        #     degree = int(arguments[2])
        #     if degree < 0: 
        #         raise TypeError('The derivative degree must be positive.')
        # else: degree = 1
        # add the degree part
        return Derivate.d2(mfun,point)    

    # Rigorous definition
    def d1(fun,x):
        h = 1e-5
        return (fun((x+h,)) - fun((x,)))  /  h
    # Symmetric derivative
    def d2(fun,x):
        
        h = 1e-5
        return (fun((x+h,)) - fun((x-h,)))  /  (2*h)
   
class Absolute(Callable):
    def arity(self) -> int:
        # function and degree
        return 1
    def call(self, interpreter, arguments: list):
        number = arguments[0]
        try:
            number = float(number)
        except:
            raise TypeError('The absolute function is only applied to numbers.')
        return abs(number)    

 
class MFUN(Callable):
    def __init__(self,fun, arity:int,llim = -100,rlim = 100,fun_des:str=None):
        self.function = fun
        self.f_arity = int(arity)
        self.llim = llim
        self.rlim = rlim
        self.fun_des = fun_des
    def __call__(self, point:tuple = None, *args, **kwds):
        if point == None:
            return super().__call__(*args, **kwds)
        if isinstance(point,(int,float)):
            point = tuple([point])
        else:
            point = tuple(point)
        return self.function(point)
    def __str__(self) -> str:
        if self.fun_des != None:
            return str(self.fun_des)
        return ''
    def __repr__(self) -> str:
        return self.__str__()
    def arity(self) -> int:
        return self.f_arity
    def call(self, interpreter, arguments: list):
        args = []
        try:
            for i in range(self.arity()):
                args.append(arguments[i])
        except: 
            msg = 'The Mfun should receive '+ str(self.arity()) + ' arguments. ' + len(arguments)+ ' were given.'
            raise IndexError(msg)
        args = tuple(args)
        return self.function(args)
        
class Unasigned:
    pass

class Enviroment:
    def __init__(self,enclosing=None):
        self.enclosing = enclosing
        self.values = {} # [string] = object

    def get(self,name):
        val = self.values.get(name.lex)
        if val != None:
            if isinstance(val,Unasigned):
                raise RuntimeF0FError(name,"Unasigned identifier '" + name.lex + "'.")
            return self.values[name.lex]
        if self.enclosing != None:
            return self.enclosing.get(name)
        raise RuntimeF0FError(name,"Undefined identifier '" + name.lex + "'.")
    
    def assign(self,name,value):
        val = self.values.get(name.lex)
        if val != None:
            self.values[name.lex] = value
            return
        if self.enclosing != None:
            self.enclosing.assign(name,value)
            return
        raise RuntimeF0FError(name,"Undefined identifier '" + name.lex + "'.")
    
    def define(self,name:str,value):
        self.values[name] = value
    
    def ancestor(self,distance:int):
        env = self
        for i in range(distance):
            env = env.enclosing
        return env
    
    def getAt(self,distance:int,name:str):
        return self.ancestor(distance).values.get(name)
    
    def assignAt(self,distance:int,name,value):
        self.ancestor(distance).values[name.lex] = value
