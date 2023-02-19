from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens
from F0FGrammar import Terminal, NonTerminal, Production, Sentential_Form, Symbol, EOF, Epsilon
from AST_nodes import *
from F0FParser import PT_node,Parse_Tree

# types_dict = {'int':INT(), 'double':DOUBLE(), 'void':VOID(), 'bool':BOOL(), 
#          'string':STRING(), 'mfun':MFUN(), 'point':POINT() }

class AST():
    def __init__(self, root:Node = None):
        self.root = root
        if root:
            self.initialized = True
        else: 
            self.initialized = False

    def ast_from_parse_tree(parse_tree:Parse_Tree):
        # Build the AST        
        if parse_tree.root.symbol.token_type == NonTerminalsTokens.Program:
            declarations = AST._declaration_list(parse_tree.root.children[0])
            forge = AST._forge(parse_tree.root.children[1])
            root = Program(declarations,forge)
            ast = AST(root)
            return ast

    def __remove_epsilon(node:PT_node):
        if node.is_leaf(): return
        i = 0
        while i < len(node.children):
            n:PT_node = node.children[i]
            if n.symbol.IsEpsilon:
                node.children.remove(n)
            else:
                AST.__remove_epsilon(n)
                i+=1
    def __remove_NT_leaves(node:PT_node):
        if node.is_leaf(): return
        i = 0
        while i < len(node.children):
            n:PT_node = node.children[i]
            if n.is_leaf() and type(n.symbol) is NonTerminal:
                node.children.remove(n)
            else:
                AST.__remove_NT_leaves(n)
                i+=1
    def __remove_grouping(node:PT_node):
        if node.is_leaf(): return

        grouping = ['(',')','{','}']
        i = 0
        while i < len(node.children):
            n:PT_node = node.children[i]
            if n.symbol.lex in grouping:
                node.children.remove(n)
            else:
                AST.__remove_grouping(n)
                i+=1
    def __group_lineal(node:PT_node,parent:PT_node):
        if node.is_leaf(): return
        i = 0
        while i < len(node.children):
            n:PT_node = node.children[i]
            if len(node.children) == 1 and type(n.symbol) is NonTerminal:
                if parent is None:
                    return 
                # n is the only child and it's a non-terminal
                index = parent.children.index(node)
                parent.children[index] = n
                AST.__group_lineal(n,parent)
                return
            else:
                AST.__group_lineal(n,node)
                i+=1
    def __operations_up(node:PT_node,parent:PT_node):
        if node.is_leaf(): return
        operations = ['+','-','*','/','%','^','||','&&']
        i = 0
        while i < len(node.children):
            n:PT_node = node.children[i]
            if n.symbol.lex in operations:
                if not n.is_leaf():
                    raise Exception('Unexpected operation with children')
                # node.children.remove(n)
                left = node.children[0:i]
                try:
                    right = node.children[i+1:]
                except: 
                    right = []
                n.children = left + right
                index = parent.children.index(node)
                parent.children[index] = n
                AST.__operations_up(n,parent)
                return
            else:
                AST.__operations_up(n,node)
                i+=1
    

    def _declaration_list(node:PT_node) -> list:
        # declaration_list -> declaration declaration_list
        declarations = []
        dec_list = node
        while True:
            if dec_list.children[0].symbol.IsEpsilon:
                break
            declarations.append(AST._declaration(dec_list.children[0]))
            dec_list = dec_list.children[1]
        return declarations
    def _declaration(node:PT_node) -> Node:
        # declaration -> funct_decl | var_decl | statement
        if node.children[0].symbol.token_type == NonTerminalsTokens.FunctDecl:
            return AST._function_dec(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.VarDecl:
            return AST._variable_dec(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.Statement:
            return AST._statement(node.children[0])
        pass
    def _forge(node:PT_node) -> Forge:
        # F0F -> Forge ( parameters ) { statement_list }
        parameters_list= AST._parameter_list(node.children[2])
        body = AST._statement_list(node.children[5])
        return Forge(node.children[0].symbol,parameters_list,body)
    def _function_dec(node:PT_node) -> Function:
        # funct_decl -> fun type id ( parameters ) { statement_list }
        # Function(type:Type, id:Identifier, parameters_list:list, body:list)
        id = AST._identifier(node.children[1])
        parameters_list= AST._parameter_list(node.children[3])
        body = AST._statement_list(node.children[6])
        return Function(id,parameters_list,body)
    def _variable_dec(node:PT_node) -> VariableDecl:
        # var_decl -> var id var_value
        # var_value -> = expression ; | ;   
        var = AST._identifier(node.children[1])
        value = node.children[2]
        if len(value.children) >= 3:
            init = AST._expression(value.children[1])
        else: init = None
        
        return VariableDecl(var,init)
    # def _variable(type_node:PT_node,id_node:PT_node) -> Variable:
    #     # type id 
    #     vtype = AST._type(type_node)
    #     id = AST._identifier(id_node)
    #     return Variable(vtype,id)
    # def _type(node:PT_node) -> Type:
    #     types_dict = {'int':INT(), 'double':DOUBLE(), 'void':VOID(), 'bool':BOOL(), 
    #              'string':STRING(), 'mfun':MFUN(), 'point':POINT() }
    #     if node.symbol.lex == 'int':
    #         return INT(node.symbol)
    #     elif node.symbol.lex == 'double':
    #         return DOUBLE(node.symbol)
    #     elif node.symbol.lex == 'void':
    #         return VOID(node.symbol)
    #     elif node.symbol.lex == 'bool':
    #         return BOOL(node.symbol)
    #     elif node.symbol.lex == 'string':
    #         return STRING(node.symbol)
    #     elif node.symbol.lex == 'mfun':
    #         return MFUN(node.symbol)
    #     elif node.symbol.lex == 'point':
    #         return POINT(node.symbol)
    def _identifier(node:PT_node) -> Identifier:
        return Identifier(node.symbol)
    def _statement_list(node:PT_node) -> list:
        # statement_list -> var_decl statement_list | statement statement_list
        stmts = []
        stmt_list = node
        while True:
            if stmt_list.children[0].symbol.IsEpsilon:
                break
            if stmt_list.children[0].symbol.token_type == NonTerminalsTokens.VarDecl:
                stmts.append(AST._variable_dec(stmt_list.children[0]))
            elif stmt_list.children[0].symbol.token_type == NonTerminalsTokens.Statement:
                stmts.append(AST._statement(stmt_list.children[0]))
            stmt_list = stmt_list.children[1]
        return stmts
    def _statement(node:PT_node) -> Node:
        # statement ->  expression ; | assign ; | for_stmt | while_stmt | if_stmt | return_stmt | print_stmt
        if node.children[0].symbol.token_type == NonTerminalsTokens.Expression:
            return AST._expression(node.children[0])
        if node.children[0].symbol.token_type == NonTerminalsTokens.Assignment:
            return AST._assign(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.ForStmt:
            return AST._for(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.WhileStmt:
            return AST._while(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.IfStmt:
            return AST._if(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.ReturnStmt:
            return AST._return(node.children[0])
        elif node.children[0].symbol.token_type == NonTerminalsTokens.PrintStmt:
            return AST._print(node.children[0])
    def _parameter_list(node:PT_node) -> list:
        # parameters -> type id parm | epsilon
        # parm -> , type id parm | epsilon
        parameters = []
        if not node.children[0].symbol.IsEpsilon:
            pname = node.children[0]
            pname = AST._identifier(pname)
            parameters.append(pname)
            parm:PT_node = node.children[1]
        else: return parameters
        while not parm.children[0].symbol.IsEpsilon:
            pname = parm.children[1]
            pname = AST._identifier(pname)
            parameters.append(pname)
            parm:PT_node = parm.children[2]
        return parameters
    def _argument_list(node:PT_node) -> list:
        # arguments -> expression args | epsilon
        # args -> , expression args | epsilon
        arguments = []
        if not node.children[0].symbol.IsEpsilon:
            expr = AST._expression(node.children[0])
            arguments.append(expr)
            args:PT_node = node.children[1]
        else: return arguments
        while not args.children[0].symbol.IsEpsilon:
            expr = AST._expression(args.children[1])
            arguments.append(expr)
            args:PT_node = args.children[2]
        return arguments
    def _for(node:PT_node) -> For:
        # for_statement -> for ( var_decl expression ; expression ) { statement_list }
        initializer = AST._variable_dec(node.children[2])
        condition = AST._expression(node.children[3])
        increment = AST._expression(node.children[5])
        body = AST._statement_list(node.children[8])
        body.append(increment)
        return For(initializer,While(condition,body))
    def _while(node:PT_node) -> While:
        # while_statement -> while ( expression ) { statement_list }
        condition = AST._expression(node.children[2])
        body = AST._statement_list(node.children[5])
        return While(condition,body)
    def _if(node:PT_node) -> If:
        # if_statement -> if ( expression ) { statement_list } else_stmt
        condition = AST._expression(node.children[2])
        body = AST._statement_list(node.children[5])
        if node.children[7].children[0].symbol.IsEpsilon:
            else_stmt = None
        else:
            else_stmt = AST._else(node.children[7])
        return If(condition,body,else_stmt)
    def _else(node:PT_node) -> Else:
        # else_stmt -> else { statement_list } | epsilon
        if node.children[0].symbol.IsEpsilon:
            return Else([])
        body = AST._statement_list(node.children[2])
        return Else(body)
    def _return(node:PT_node) -> Node:
        # return_statement -> return ret
        # ret -> expression ; | ;
        ret = node.children[1]
        if len(ret.children) > 1:
            expr = AST._expression(ret.children[0])
        else: 
            expr = None
        return Return(expr)
    def _print(node:PT_node) -> Node:
        # print_statement -> print ( expression ) ;
        expr = AST._expression(node.children[2])
        return Print(expr)
    def _expression(node:PT_node) -> Node:
        # expression -> operation
        if len(node.children) == 1:
            return AST._or(node.children[0])
        # else:
        #     # Assignment(call:Call, expression:Node)
        #     call = AST._call(node.children[0])
        #     value = AST._or(node.children[2])
        #     return Assignment(call, value)
    def _assign(node:PT_node) -> Assignment:
        # assign -> id = expression
        id = AST._identifier(node.children[0])
        value = AST._expression(node.children[2])
        return Assignment(id, value)
    def _or(node:PT_node) -> Node:
        # operation -> logic_and OR
        # OR -> || operation | epsilon
        left = AST._and(node.children[0])
        OR:PT_node = node.children[1]
        while not OR.children[0].symbol.IsEpsilon:
            n:PT_node = OR.children[1]
            OR = n.children[1]
            right = AST._and(n.children[0])
            left = Logic_OR(left,right)
        return left
    def _and(node:PT_node) -> Node:
        # logic_and -> equality AND
        # AND -> && logic_and | epsilon
        left = AST._equality(node.children[0])
        AND:PT_node = node.children[1]
        while not AND.children[0].symbol.IsEpsilon:
            n:PT_node = AND.children[1]
            AND = n.children[1]
            right = AST._equality(n.children[0])
            left = Logic_AND(left,right)
        return left
    def _equality(node:PT_node) -> Node:
        # equality -> comparison eql
        # eql -> == equality | != equality | epsilon
        left = AST._comparison(node.children[0])
        eql:PT_node = node.children[1]
        while not eql.children[0].symbol.IsEpsilon:
            n:PT_node = eql.children[1]
            right = AST._comparison(n.children[0])
            if eql.children[0].symbol.token_type == TerminalsTokens.equal_equal:
                left = Equality(left,right)
            elif eql.children[0].symbol.token_type == TerminalsTokens.excl_equal:
                left = Unequality(left,right)
            eql = n.children[1]
        return left
    def _comparison(node:PT_node) -> Node:
        # comparison -> term LGEq
        # LGEq -> < comparison | <= comparison | > comparison | >= comparison | epsilon
        left = AST._term(node.children[0])
        lgeq:PT_node = node.children[1]
        while not lgeq.children[0].symbol.IsEpsilon:
            n:PT_node = lgeq.children[1]
            right = AST._term(n.children[0])
            if lgeq.children[0].symbol.token_type == TerminalsTokens.less:
                left = Less(left,right)
            elif lgeq.children[0].symbol.token_type == TerminalsTokens.less_equal:
                left = Less_Equal(left,right)
            elif lgeq.children[0].symbol.token_type == TerminalsTokens.greater:
                left = Greater(left,right)
            elif lgeq.children[0].symbol.token_type == TerminalsTokens.greater_equal:
                left = Greater_Equal(left,right)
            lgeq = n.children[1]
        return left
    def _term(node:PT_node) -> Node:
        # term -> factor FX
        # FX -> + term | - term | epsilon
        left = AST._factor(node.children[0])
        fx:PT_node = node.children[1]
        while not fx.children[0].symbol.IsEpsilon:
            n:PT_node = fx.children[1]
            right = AST._factor(n.children[0])
            if fx.children[0].symbol.token_type == TerminalsTokens.plus:
                left = Sum(left,right)
            elif fx.children[0].symbol.token_type == TerminalsTokens.minus:
                left = Minus(left,right)
            fx = n.children[1]
        return left
    def _factor(node:PT_node) -> Node:
        # factor -> pow PowX
        # PowX -> * factor | / factor | % factor | epsilon
        left = AST._pow(node.children[0])
        px:PT_node = node.children[1]
        while not px.children[0].symbol.IsEpsilon:
            n:PT_node = px.children[1]
            right = AST._pow(n.children[0])
            if px.children[0].symbol.token_type == TerminalsTokens.star:
                left = Mult(left,right)
            elif px.children[0].symbol.token_type == TerminalsTokens.slash:
                left = Div(left,right)
            elif px.children[0].symbol.token_type == TerminalsTokens.percent:
                left = Module(left,right)
            px = n.children[1]
        return left
    def _pow(node:PT_node) -> Node:
        # pow -> unary UX
        # UX -> ^ pow | epsilon
        left = AST._unary(node.children[0])
        ux:PT_node = node.children[1]
        if not ux.children[0].symbol.IsEpsilon:
            right = AST._pow(ux.children[1])
            return Pow(left,right)
        return left
    def _unary(node:PT_node) -> Node:
        # unary -> ! unary | - unary | call
        if len(node.children) == 1:
            return AST._call(node.children[0])
        unary = AST._unary(node.children[1])
        if node.children[0].symbol.token_type == TerminalsTokens.excl:
            return Logic_NOT(unary)
        elif node.children[0].symbol.token_type == TerminalsTokens.minus:
            return Negate(unary)
    def _call(node:PT_node) -> Node:
        # call -> primary call_type 
        # call_type -> . id call_type | ( arguments ) call_type | epsilon
        prim = AST._primary(node.children[0])
        ctype:PT_node = node.children[1]
        while not ctype.children[0].symbol.IsEpsilon:
            if ctype.children[0].symbol.token_type == TerminalsTokens.dot:
                # id = AST._identifier(node.children[1])
                # prim = DotCall(prim,id)
                # ctype = ctype.children[2]
                pass
            elif ctype.children[0].symbol.token_type == TerminalsTokens.opar:
                args = AST._argument_list(ctype.children[1])
                prim = ParenCall(prim,args)
                ctype = ctype.children[3]
        return prim
    def _primary(node:PT_node) -> Node:
        # primary -> true | false | null | integer | decimal | string_chain | id | ( expression )
        if len(node.children) == 1:
            if node.children[0].symbol.token_type == TerminalsTokens.true:
                return TRUE(node.children[0].symbol)
            elif node.children[0].symbol.token_type == TerminalsTokens.false:
                return FALSE(node.children[0].symbol)
            elif node.children[0].symbol.token_type == TerminalsTokens.null:
                return NULL(node.children[0].symbol)
            elif node.children[0].symbol.token_type == TerminalsTokens.integer:
                return Integer(node.children[0].symbol)
            elif node.children[0].symbol.token_type == TerminalsTokens.decimal:
                return Decimal(node.children[0].symbol)    
            elif node.children[0].symbol.token_type == TerminalsTokens.string_chain:
                return String_chain(node.children[0].symbol)
            elif node.children[0].symbol.token_type == TerminalsTokens.identifier:
                return AST._identifier(node.children[0])
        else:
            return AST._expression(node.children[1])

