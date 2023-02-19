from AST_nodes import *
from F0FDefinitions import *
from F0FErrors import SemanticError, RuntimeF0FError

class Visitor:
    def visitLiteralExpr(self,expr:Literal):
        pass
    def visitIdentifierExpr(self,expr:Identifier):
        pass
    def visitUnaryExpr(self,expr:UnaryNode):
        pass 
    def visitBinaryExpr(self,expr:BinaryNode):
        pass
    def visitCallExpr(self,expr:Call):
        pass    
    def visitAssignExpr(self,expr:Assignment):
        pass


    def visitVarDeclStmt(self,stmt:VariableDecl):
        pass    
    def visitFunctionStmt(self,stmt:Function):
        pass    
    def visitWhileStmt(self,stmt:While):
        pass   
    def visitForStmt(self,stmt:For):
        pass     
    def visitStmtList(self,stmt:list):
        pass     
    def visitIfStmt(self,stmt:If):
        pass    
    def visitReturnStmt(self,stmt:Return):
        pass    
    def visitPrintStmt(self,stmt:Print):
        pass

def dumb_fun(x:tuple):
    return x[0]

class Interpreter(Visitor):
    def __init__(self):
        super().__init__()
        self.had_semantic_error = False
        self.had_runtime_error = False
        self.errors = []
        self.locals  = {} # [Node] = depth
        self.globals = Enviroment()
        self.enviroment = self.globals
        self.globals.define('clock',globals_clock())
        self.globals.define('derivative',Derivate())
        self.globals.define('abs',Absolute())

    def interpret(self, program:Program, forge_args:list=None):
        zero = None
        eq_count = None
        try:
            for stmt in program.declarations:
                # execute it
                stmt.visit(self)
            if forge_args == None:
                forge_args = [MFUN(dumb_fun,1),-1000,1000]
            program.forge.visit(self)
            forge = self.enviroment.get(program.forge.main_token)
            zero = forge.call(self,forge_args)
            if not( (type(zero) is float) or (type(zero) is int) ):
                self.had_runtime_error = True
                raise RuntimeF0FError(program.forge.main_token, "Forge must return a numeric value.")
            
            eq = Equal_Sin(self)
            eq_count = eq.Equal_count(program)
        except Exception as error:
            self.errors.append(error)
            self.had_runtime_error = True
            print(error)
            return None, None
        if isinstance(zero,float):
            strn = str(zero)
            if strn.endswith('.0'):
                strn = strn[:len(strn)-2]
                zero = int(strn)
        return zero, eq_count

    def evaluate(self,expr:Node):
        return expr.visit(self)
    def executeBlock(self,statements:list,enviroment):
        previous = self.enviroment
        try: 
            self.enviroment = enviroment
            for stmt in statements:
                # execute it
                stmt.visit(self)
        finally:
            self.enviroment = previous

    def visitLiteralExpr(self,expr:Literal):
        expr.node_value = expr.value
        return expr.node_value
    def visitIdentifierExpr(self,expr:Identifier):
        # distance = self.locals.get(expr)
        # try:
        return self.enviroment.get(expr.main_token)
        # except:
        #     return self.globals.get(expr.main_token)
    def visitUnaryExpr(self,expr:UnaryNode):
        value = self.evaluate(expr.node)
        if type(expr) is Logic_NOT:
            if type(value) != bool:
                error = SemanticError(expr.main_token,'Invalid ! operation with a non boolean value.')
                expr.semantic_errors.append(error)
                self.had_semantic_error = True
                raise error
        elif type(expr) is Negate:
            try: 
                value = float(value)
            except:
                error = SemanticError(expr.main_token,'Invalid negate operation with a non numeric value.')
                expr.semantic_errors.append(error) 
                self.had_semantic_error = True
                raise error
        expr.node_value = expr.operate(value)
        return expr.node_value
    def visitBinaryExpr(self,expr:BinaryNode):
        lvalue = self.evaluate(expr.left)
        rvalue = self.evaluate(expr.right)
        if type(expr) is Equality or type(expr) is Unequality:
            expr.node_value = expr.operate(lvalue, rvalue)
            return expr.node_value
        if type(expr) is Logic_AND or type(expr) is Logic_OR:
            try:
                lvalue = bool(lvalue)
                rvalue = bool(rvalue)
                expr.node_value = expr.operate(lvalue, rvalue)
                return expr.node_value
            except:
                error = SemanticError(expr.main_token,'Operands must be boolean expressions.')
                expr.semantic_errors.append(error) 
                self.had_semantic_error = True
                raise error
        else:
            try:
                lvalue = float(lvalue)
                rvalue = float(rvalue)
            except:
                error = SemanticError(expr.main_token,'Operands must be numbers.')
                expr.semantic_errors.append(error) 
                self.had_semantic_error = True
                raise error

            if type(expr) is Div or type(expr) is Module:
                if rvalue == 0:
                    error = RuntimeF0FError(expr.main_token,'Zero division error.')
                    # expr.semantic_errors.append(error) 
                    self.had_runtime_error = True
                    raise error
        expr.node_value = expr.operate(lvalue, rvalue)
        return expr.node_value
    def visitCallExpr(self,expr:Call):
        caller = self.evaluate(expr.caller)
        if isinstance(expr.caller,Identifier):
            caller = self.enviroment.get(expr.caller.main_token)
        else: print(type(expr.caller))
        
        evaluated_args = []
        for arg in expr.arguments:
            evaluated_args.append(self.evaluate(arg))
        if isinstance(caller,Callable):
            caller:Callable
            if len(evaluated_args)!=caller.arity():
                error = RuntimeF0FError(expr.main_token, "Expected " + str(caller.arity()) + " arguments, but got " + str(len(evaluated_args)) + ".")
                self.had_runtime_error = True
                raise error
            else:
                return caller.call(self, evaluated_args)
        else:            
            print(type(caller))
            error = RuntimeF0FError(expr.main_token,"This object it\'s not callable.")
            self.had_runtime_error = True
            raise error

    def visitAssignExpr(self,expr:Assignment):
        value = self.evaluate(expr.right)
        # distance = self.locals.get(expr)
        # if distance is None:
        #     self.globals.assign(expr.left.main_token,value)
        # else:
        self.enviroment.assign(expr.left.main_token,value)
        return value

    def visitVarDeclStmt(self,stmt:VariableDecl):
        value = Unasigned()
        if stmt.initialized():
            value = self.evaluate(stmt.initializer)
        self.enviroment.define(stmt.name.lex, value)
    def visitFunctionStmt(self,stmt:Function):
        funct = F0FFunctions(stmt,self.enviroment)
        self.enviroment.define(stmt.name.lex, funct)
    def visitWhileStmt(self,stmt:While):
        cond = self.evaluate(stmt.condition)
        while cond:
            self.visitStmtList(stmt.body)
            cond = self.evaluate(stmt.condition)
    def visitForStmt(self,stmt:For):
        self.visitVarDeclStmt(stmt.initializer)
        cond = self.evaluate(stmt.loop.condition)
        while cond:
            self.visitStmtList(stmt.loop.body)
            cond = self.evaluate(stmt.loop.condition)
    def visitStmtList(self,stmts:list):
        self.executeBlock(stmts,Enviroment(self.enviroment))
    def visitIfStmt(self,stmt:If):
        cond = self.evaluate(stmt.condition)
        if cond:
            self.visitStmtList(stmt.body)
        else:
            if stmt.else_branch == None:
                return
            stmt.else_branch.visit(self)
    def visitReturnStmt(self,stmt:Return):
        if stmt.expression != None:
            value = self.evaluate(stmt.expression)
        raise Return_asExc(value)

class Equal_Sin(Visitor):
    
    def __init__(self,interpreter:Interpreter):
        self.interpreter = interpreter
        self.counter = 0
    
    def goto(self,node:Node):
        node.visit(self)
        
    def Equal_count(self,ast:Program):
        for stmt in ast.declarations:
            self.goto(stmt)
        self.goto(ast.forge)
        
        return self.counter
    
    def visitLiteralExpr(self,expr:Literal):
        return expr.node_value
    def visitIdentifierExpr(self,expr:Identifier):
        try:
            self.interpreter.enviroment.get(expr.main_token)
        except:
            return None
    def visitUnaryExpr(self,expr:UnaryNode):
        return expr.node_value
    def visitBinaryExpr(self,expr:BinaryNode):
        if type(expr) is Equality:
            lv = expr.left.node_value
            rv = expr.right.node_value
            if lv != None and rv != None:
                if ((type(lv) is float) or (type(lv) is int)) or ((type(rv) is float) or (type(rv) is int)):
                    self.counter +=1
            elif lv != None and ((type(lv) is float) or (type(lv) is int)):
                self.counter +=1
            elif rv != None and ((type(rv) is float) or (type(rv) is int)):
                self.counter +=1
            else: #both None
                lv = self.interpreter.evaluate(expr.left)
                rv = self.interpreter.evaluate(expr.right)
                if ((type(lv) is float) or (type(lv) is int)) or ((type(rv) is float) or (type(rv) is int)):
                    self.counter +=1    
        return expr.node_value
    def visitCallExpr(self,expr:Call):
        return expr.node_value
    def visitAssignExpr(self,expr:Assignment):
        self.goto(expr.right)
        return expr.node_value


    def visitVarDeclStmt(self,stmt:VariableDecl):
        if stmt.initialized():
            self.goto(stmt.initializer)
        return stmt.node_value
    def visitFunctionStmt(self,stmt:Function):
        self.visitStmtList(stmt.body)
        return stmt.node_value
    def visitWhileStmt(self,stmt:While):
        self.goto(stmt.condition)
        self.visitStmtList(stmt.body)
        return stmt.node_value
    def visitForStmt(self,stmt:For):
        self.goto(stmt.loop.condition)
        self.visitStmtList(stmt.loop.body)
        return stmt.node_value
    def visitStmtList(self,stmt:list):
        for st in stmt:
            self.goto(st)
    def visitIfStmt(self,stmt:If):
        self.goto(stmt.condition)
        self.visitStmtList(stmt.body)
        if stmt.else_branch != None:
            self.goto(stmt.else_branch)
        return stmt.node_value
    def visitReturnStmt(self,stmt:Return):
        if stmt.expression != None:
            self.goto(stmt.expression)
        return stmt.node_value
    