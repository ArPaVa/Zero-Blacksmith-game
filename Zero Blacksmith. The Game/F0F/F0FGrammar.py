from F0FTokens import Token, TokenType, TerminalsTokens, NonTerminalsTokens

class Symbol(Token):

    def __init__(self, lex: str='', token_type:TokenType=None,token:Token = None):
        if token != None:
            super().__init__(token.lex, token.token_type,token.line,token.length)
        else:
            super().__init__(lex, token_type)

    def __str__(self):
        return self.lex
    def __repr__(self):
        return repr(self.lex)

    @property
    def IsEpsilon(self):
        return False

    def __len__(self):
        return 1

class NonTerminal(Symbol):
    def __init__(self, lex: str, token_type: NonTerminalsTokens):
        super().__init__(lex, token_type)
        self.productions = []

    @property
    def IsTerminal(self):
        return False

    @property
    def IsNonTerminal(self):
        return True

    @property
    def IsEpsilon(self):
        return False

class Terminal(Symbol):
    def __init__(self, lex: str, token_type:TerminalsTokens):
        super().__init__(lex, token_type)

    @property
    def IsTerminal(self):
        return True

    @property
    def IsNonTerminal(self):
        return False

    @property
    def IsEpsilon(self):
        return 

class EOF(Terminal):
    def __init__(self):
        super().__init__('$', TerminalsTokens.EOF)

class Sentential_Form:
    def __init__(self, *args):
        self._symbols = tuple(s for s in args if not s.IsEpsilon)

    def __len__(self):
        return len(self._symbols)

    def __repr__(self):
        return  self.__str__()#str(self._symbols)
    def __str__(self):
        sentString = ''
        for s in self._symbols:
            s:Symbol
            sentString += str(s.lex) + ' '
        return sentString

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    @property
    def IsEpsilon(self):
        return False

class Epsilon(Terminal, Sentential_Form):

    def __init__(self):
        super().__init__('epsilon', TerminalsTokens.epsilon)

    def __str__(self):
        return "e"

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))
    
    def __hash__(self):
        return hash("")

    def __iter__(self):
        yield self

    @property
    def IsEpsilon(self):
        return True

class Production:
    def __init__(self, nonTerminal:NonTerminal, sentential:Sentential_Form):
        self.Head = nonTerminal
        self.Body = sentential
    
    def __str__(self):
        return '%s --> %s' % (self.Head.lex, self.Body)
    def __repr__(self):
        return self.__str__()
    
    @property
    def IsEpsilon(self):
        return self.Body.IsEpsilon

class AttributedProduction(Production):
    def __init__(self, nonTerminal: NonTerminal, sentential: Sentential_Form, attributes):
        super().__init__(nonTerminal, sentential)
        self.attributes = attributes
    def syntetice(self):
        pass

class Grammar():
    
    def __init__(self):

        self.Productions = []
        self.nonTerminals = []
        self.terminals = []
        self.mainSymbol = None
        self.Epsilon = Epsilon()
        self.EOF = EOF()

        self.symbDict = { '$': self.EOF }
    
    def New_NonTerminal(self, lex:str, token_type:NonTerminalsTokens, main_symbol = False):
        
        if not lex: raise Exception("Empty lex")

        nt = NonTerminal(lex, token_type)
        if main_symbol:
            if self.mainSymbol is None:
                self.mainSymbol = nt
            else: raise Exception(" ".join(["This grammar already has a main symbol: ", self.mainSymbol]))
        
        self.nonTerminals.append(nt)
        self.symbDict[nt.lex] = nt
        return nt
    
    def New_Terminal(self, lex:str, token_type:TerminalsTokens):

        if not lex: raise Exception("Empty lex")

        t = Terminal(lex, token_type)
        self.terminals.append(t)
        self.symbDict[t.lex] = t
        return t

    def Add_Production(self, production:Production):
        production.Head.productions.append(production)
        self.Productions.append(production)

    def __str__(self):

        ans = 'Non-Terminals:\n\t'
        for nt in self.nonTerminals:
            ans+= str(nt.lex) + " , "
        ans = ans[:len(ans) - 2]
        ans+='\n\n'

        ans += 'Terminals:\n\t'
        for t in self.terminals:
            ans+= str(t.lex) + " , "
        ans = ans[:len(ans) - 2]
        ans+='\n\n'

        ans += 'Productions:'
        for pr in self.Productions:
            ans += "\n\t" + str(pr) 
        ans = ans[:len(ans) - 1]

        return ans

    def __getitem__(self, lex:str):
        try:
            return self.symbDict[lex]
        except KeyError:
            return None
    
class F0F(Grammar):
    def __init__(self):
        self.Epsilon = Epsilon()
        self.EOF = EOF()
        terminals = [
            # 0
            Terminal('+', TerminalsTokens.plus),
            Terminal('-', TerminalsTokens.minus),
            Terminal('*', TerminalsTokens.star),
            Terminal('/', TerminalsTokens.slash),
            Terminal('(', TerminalsTokens.opar),
            # 5
            Terminal(')',TerminalsTokens.cpar),
            Terminal(',', TerminalsTokens.comma),
            Terminal('.', TerminalsTokens.dot),
            Terminal('[', TerminalsTokens.obracket),            
            Terminal(']', TerminalsTokens.cbracket),
            # 10
            Terminal('{', TerminalsTokens.obrace),
            Terminal('}', TerminalsTokens.cbrace),
            Terminal(';', TerminalsTokens.semicolon),
            Terminal('%', TerminalsTokens.percent),
            Terminal('^', TerminalsTokens.caret),
            # 15
            Terminal('\'', TerminalsTokens.quoat),
            Terminal('\"', TerminalsTokens.double_quoat),
            Terminal('=', TerminalsTokens.equal),
            Terminal('==', TerminalsTokens.equal_equal),
            Terminal('!', TerminalsTokens.excl),
            # 20
            Terminal('!=', TerminalsTokens.excl_equal),
            Terminal('<', TerminalsTokens.less),
            Terminal('<=', TerminalsTokens.less_equal),
            Terminal('>', TerminalsTokens.greater),
            Terminal('>=', TerminalsTokens.greater_equal),
            # 25
            Terminal('&&', TerminalsTokens.And),
            Terminal('||', TerminalsTokens.Or),
            Terminal('if', TerminalsTokens.If),
            Terminal('else', TerminalsTokens.Else),
            Terminal('for', TerminalsTokens.For),
            # 30
            Terminal('while', TerminalsTokens.While),
            Terminal('return', TerminalsTokens.Return),
            Terminal('fun', TerminalsTokens.function),
            Terminal('null',  TerminalsTokens.null),
            Terminal('var', TerminalsTokens.var),
            # 35
            Terminal('true', TerminalsTokens.true),
            Terminal('false', TerminalsTokens.false),
            Terminal('integer', TerminalsTokens.integer),
            Terminal('decimal', TerminalsTokens.decimal),
            Terminal('string_chain', TerminalsTokens.string_chain),
            #40
            Terminal('id', TerminalsTokens.identifier),
            Terminal('Forge', TerminalsTokens.Forge),
            Terminal('print',TerminalsTokens.Print)
        ]
        nonTerminals = [
            # 0 
            NonTerminal('program'         , NonTerminalsTokens.Program),
            NonTerminal('declaration_list', NonTerminalsTokens.Declaration_list),
            NonTerminal('declaration'     , NonTerminalsTokens.Declaration),
            NonTerminal('funct_decl'      , NonTerminalsTokens.FunctDecl),
            NonTerminal('var_decl'        , NonTerminalsTokens.VarDecl),
            # 5
            NonTerminal('statement'       , NonTerminalsTokens.Statement),
            NonTerminal('statement_list'  , NonTerminalsTokens.Statement_List),
            NonTerminal('F0F'             , NonTerminalsTokens.F0F),
            NonTerminal('for_statement'   , NonTerminalsTokens.ForStmt),
            NonTerminal('while_statement' , NonTerminalsTokens.WhileStmt),
            # 10
            NonTerminal('if_statement'    , NonTerminalsTokens.IfStmt),
            NonTerminal('return_statement', NonTerminalsTokens.ReturnStmt),
            NonTerminal('expression'      , NonTerminalsTokens.Expression),
            NonTerminal('parameters'      , NonTerminalsTokens.Parameters),
            NonTerminal('parm'            , NonTerminalsTokens.Parm),
            # 15
            NonTerminal('arguments'       , NonTerminalsTokens.Arguments),
            NonTerminal('args'            , NonTerminalsTokens.Arg),
            NonTerminal('else_stmt'       , NonTerminalsTokens.elseStmt),
            NonTerminal('ret'             , NonTerminalsTokens.ret),
            NonTerminal('var_value'       , NonTerminalsTokens.VarValue),
            # 20
            NonTerminal('call'            , NonTerminalsTokens.Call),
            NonTerminal('operation'       , NonTerminalsTokens.Operation),
            NonTerminal('OR'              , NonTerminalsTokens.OR),
            NonTerminal('logic_and'       , NonTerminalsTokens.Logic_And),
            NonTerminal('AND'             , NonTerminalsTokens.AND),
            # 25 
            NonTerminal('equality'        , NonTerminalsTokens.Equality),
            NonTerminal('eql'             , NonTerminalsTokens.Eq),
            NonTerminal('comparison'      , NonTerminalsTokens.Comparison),
            NonTerminal('LGEq'            , NonTerminalsTokens.LGEq),
            NonTerminal('term'            , NonTerminalsTokens.Term),
            # 30
            NonTerminal('factor'          , NonTerminalsTokens.Factor),
            NonTerminal('FX'              , NonTerminalsTokens.FX),
            NonTerminal('pow'             , NonTerminalsTokens.Pow),
            NonTerminal('PowX'            , NonTerminalsTokens.PowX),
            NonTerminal('unary'           , NonTerminalsTokens.Unary),
            # 35
            NonTerminal('UX'              , NonTerminalsTokens.UX),
            NonTerminal('primary'         , NonTerminalsTokens.Primary),
            NonTerminal('call_type'       , NonTerminalsTokens.call_type),
            NonTerminal('print_statement' , NonTerminalsTokens.PrintStmt),
            NonTerminal('assign'          , NonTerminalsTokens.Assignment)
            # 40
        ]

        self.mainSymbol = nonTerminals[0]
        symbDict = { '$': self.EOF,
                    'epsilon' : self.Epsilon }
        for nt in nonTerminals:
            symbDict[nt.lex] = nt
        for t in terminals:
            symbDict[t.lex] = t

        Productions = [
            # program -> declaration_list F0F EOF
            Production(nonTerminals[0], Sentential_Form(nonTerminals[1], nonTerminals[7])),  
            # declaration_list -> declaration declaration_list
            # declaration_list -> epsilon
            Production(nonTerminals[1], Sentential_Form(nonTerminals[2], nonTerminals[1])),
            Production(nonTerminals[1], self.Epsilon),
            # declaration -> funct_decl
            # declaration -> var_decl
            # declaration -> statement
            Production(nonTerminals[2], Sentential_Form(nonTerminals[3])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[4])),
            Production(nonTerminals[2], Sentential_Form(nonTerminals[5])),
            # statement_list -> var_decl statement_list
            # statement_list -> statement statement_list
            # statement_list -> epsilon
            Production(nonTerminals[6], Sentential_Form(nonTerminals[4], nonTerminals[6])),
            Production(nonTerminals[6], Sentential_Form(nonTerminals[5], nonTerminals[6])),
            Production(nonTerminals[6], self.Epsilon),
            # F0F -> Forge ( parameters ) { statement_list }
            Production(nonTerminals[7], Sentential_Form(terminals[41],terminals[4], nonTerminals[13],terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # funct_decl -> fun type id ( parameters ) { statement_list }
            Production(nonTerminals[3], Sentential_Form(terminals[32],terminals[40],terminals[4], nonTerminals[13],terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # var_decl -> var id var_value
            # var_value -> = expression ;
            # var_value -> ;   
            Production(nonTerminals[4], Sentential_Form(terminals[34],terminals[40],nonTerminals[19])),
            Production(nonTerminals[19],Sentential_Form(terminals[17],nonTerminals[12],terminals[12])),    
            Production(nonTerminals[19],Sentential_Form(terminals[12])), 
            # statement -> expression ;
            # statement -> assign ;
            # statement -> for_statement
            # statement -> while_statement
            # statement -> if_statement
            # statement -> return_statement
            # statement -> print_statement
            Production(nonTerminals[5], Sentential_Form(nonTerminals[12],terminals[12])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[39],terminals[12])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[8])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[9])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[10])),
            Production(nonTerminals[5], Sentential_Form(nonTerminals[11])),
            # Production(nonTerminals[5], Sentential_Form(nonTerminals[38])),
            # for_statement -> for ( var_decl expression ; expression ) { statement_list }
            Production(nonTerminals[8], Sentential_Form(terminals[29],terminals[4], nonTerminals[4], nonTerminals[12],terminals[12],nonTerminals[12],terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # while_statement -> while ( expression ) { statement_list }
            Production(nonTerminals[9], Sentential_Form(terminals[30],terminals[4], nonTerminals[12], terminals[5], terminals[10],nonTerminals[6], terminals[11])),
            # if_statement -> if ( expression ) { statement_list } else_stmt
            # else_stmt -> else { statement_list }
            # else_stmt -> epsilon
            Production(nonTerminals[10],Sentential_Form(terminals[27],terminals[4], nonTerminals[12],terminals[5], terminals[10],nonTerminals[6], terminals[11],nonTerminals[17])),
            Production(nonTerminals[17],Sentential_Form(terminals[28],terminals[10],nonTerminals[6], terminals[11])),
            Production(nonTerminals[17],self.Epsilon),
            # return_statement -> return ret
            # ret -> expression ;
            # ret -> ;
            Production(nonTerminals[11],Sentential_Form(terminals[31],nonTerminals[18])),
            Production(nonTerminals[18],Sentential_Form(nonTerminals[12],terminals[12])),
            Production(nonTerminals[18],Sentential_Form(terminals[12])),
            # print_statement -> print ( expression ) ;
            Production(nonTerminals[38],Sentential_Form(terminals[42],terminals[4], nonTerminals[12],terminals[5], terminals[12])),
            # parameters -> type id parm
            # parameters -> epsilon
            # parm -> , type id parm
            # parm -> epsilon
            Production(nonTerminals[13],Sentential_Form(terminals[40],nonTerminals[14])),
            Production(nonTerminals[13],self.Epsilon),
            Production(nonTerminals[14],Sentential_Form(terminals[6],terminals[40],nonTerminals[14])),
            Production(nonTerminals[14],self.Epsilon),
            # arguments -> expression args
            # arguments -> epsilon
            # args -> , expression args
            # args -> epsilon
            Production(nonTerminals[15],Sentential_Form(nonTerminals[12],nonTerminals[16])),
            Production(nonTerminals[15],self.Epsilon),
            Production(nonTerminals[16],Sentential_Form(terminals[6], nonTerminals[12],nonTerminals[16])),
            Production(nonTerminals[16],self.Epsilon),
            # assign -> id = expression
            Production(nonTerminals[39],Sentential_Form(terminals[40],terminals[17],nonTerminals[12])),
            # expression -> operation
            Production(nonTerminals[12],Sentential_Form(nonTerminals[21])),
            # operation -> logic_and OR
            # OR -> || operation
            # OR -> epsilon
            Production(nonTerminals[21],Sentential_Form(nonTerminals[23],nonTerminals[22])),
            Production(nonTerminals[22],Sentential_Form(terminals[26],nonTerminals[21])),
            Production(nonTerminals[22],self.Epsilon),
            # logic_and -> equality AND
            # AND -> && logic_and
            # AND -> epsilon
            Production(nonTerminals[23],Sentential_Form(nonTerminals[25],nonTerminals[24])),
            Production(nonTerminals[24],Sentential_Form(terminals[25],nonTerminals[23])),
            Production(nonTerminals[24],self.Epsilon),
            # equality -> comparison eql
            # eql -> == equality
            # eql -> != equality
            # eql -> epsilon
            Production(nonTerminals[25],Sentential_Form(nonTerminals[27],nonTerminals[26])),
            Production(nonTerminals[26],Sentential_Form(terminals[18],nonTerminals[25])),
            Production(nonTerminals[26],Sentential_Form(terminals[20],nonTerminals[25])),
            Production(nonTerminals[26],self.Epsilon),
            # comparison -> term LGEq
            # LGEq -> < comparison
            # LGEq -> <= comparison
            # LGEq -> > comparison
            # LGEq -> >= comparison
            # LGEq -> epsilon
            Production(nonTerminals[27],Sentential_Form(nonTerminals[29],nonTerminals[28])),
            Production(nonTerminals[28],Sentential_Form(terminals[21],nonTerminals[27])),
            Production(nonTerminals[28],Sentential_Form(terminals[22],nonTerminals[27])),
            Production(nonTerminals[28],Sentential_Form(terminals[23],nonTerminals[27])),
            Production(nonTerminals[28],Sentential_Form(terminals[24],nonTerminals[27])),
            Production(nonTerminals[28],self.Epsilon),
            # term -> factor FX
            # FX -> + term
            # FX -> - term
            # FX -> epsilon
            Production(nonTerminals[29],Sentential_Form(nonTerminals[30],nonTerminals[31])),
            Production(nonTerminals[31],Sentential_Form(terminals[0], nonTerminals[29])),
            Production(nonTerminals[31],Sentential_Form(terminals[1], nonTerminals[29])),
            Production(nonTerminals[31],self.Epsilon),
            # factor -> pow PowX
            # PowX -> * factor
            # PowX -> / factor
            # PowX -> % factor
            # PowX -> epsilon
            Production(nonTerminals[30],Sentential_Form(nonTerminals[32],nonTerminals[33])),
            Production(nonTerminals[33],Sentential_Form(terminals[2], nonTerminals[30])),
            Production(nonTerminals[33],Sentential_Form(terminals[3], nonTerminals[30])),
            Production(nonTerminals[33],Sentential_Form(terminals[13],nonTerminals[30])),
            Production(nonTerminals[33],self.Epsilon),
            # pow -> unary UX
            # UX -> ^ pow
            # UX -> epsilon
            Production(nonTerminals[32],Sentential_Form(nonTerminals[34],nonTerminals[35])),
            Production(nonTerminals[35],Sentential_Form(terminals[14],nonTerminals[32])),
            Production(nonTerminals[35],self.Epsilon),
            # unary -> ! unary
            # unary -> - unary
            # unary -> call
            Production(nonTerminals[34],Sentential_Form(terminals[19],nonTerminals[34])),
            Production(nonTerminals[34],Sentential_Form(terminals[1], nonTerminals[34])),
            Production(nonTerminals[34],Sentential_Form(nonTerminals[20])),
            # call -> primary call_type 
            Production(nonTerminals[20],Sentential_Form(nonTerminals[36],nonTerminals[37])),
            # call_type -> . id call_type
            # call_type -> [ expression ] call_type
            # call_type -> ( arguments ) call_type
            # call_type -> epsilon
            # Production(nonTerminals[37],Sentential_Form(terminals[7], terminals[40],nonTerminals[37])),
            # Production(nonTerminals[37],Sentential_Form(terminals[8], nonTerminals[12],terminals[9], nonTerminals[37])),
            Production(nonTerminals[37],Sentential_Form(terminals[4], nonTerminals[15],terminals[5], nonTerminals[37])),
            Production(nonTerminals[37],self.Epsilon),
            # primary -> true 
            # primary -> false
            # primary -> null
            # primary -> integer 
            # primary -> decimal
            # primary -> string_chain 
            # primary -> id
            # primary -> ( expression )
            Production(nonTerminals[36],Sentential_Form(terminals[35])),
            Production(nonTerminals[36],Sentential_Form(terminals[36])),
            Production(nonTerminals[36],Sentential_Form(terminals[33])),
            Production(nonTerminals[36],Sentential_Form(terminals[37])),
            Production(nonTerminals[36],Sentential_Form(terminals[38])),
            Production(nonTerminals[36],Sentential_Form(terminals[39])),
            Production(nonTerminals[36],Sentential_Form(terminals[40])),
            Production(nonTerminals[36],Sentential_Form(terminals[4], nonTerminals[12],terminals[5]))                        
        ]

        for pr in Productions:
            pr.Head.productions.append(pr)

        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.symbDict = symbDict
        self.Productions = Productions
