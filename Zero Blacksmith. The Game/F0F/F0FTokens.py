from enum import Enum
class TokenType(Enum):
    pass
class TerminalsTokens(TokenType):
    """single character tokens"""
    opar = '('
    cpar = ')'
    obracket = '['
    cbracket = ']'
    obrace = '{'
    cbrace = '}'
    comma = ','
    dot = '.'
    semicolon = ';'
    minus = '-'
    plus = '+'
    star = '*'
    slash = '/'
    percent = '%'
    caret = '^'
    quoat = '\''
    double_quoat = '\"'
    """ comparisson """
    equal = '=' 
    equal_equal = '==' 
    excl = '!'
    excl_equal = '!='
    greater = '>' 
    greater_equal = '>=' 
    less = '<' 
    less_equal = '<='
    """ keywords """
    _class = 'class' 
    Forge = 'Forge'
    function = 'fun'
    null = 'null'
    this = 'this'
    And = '&&'
    Or = '||'
    Return = 'return'
    While = 'while'
    For = 'for'
    If = 'if'
    Else = 'else'
    Print = 'print'
    """ literals """
    true = 'true'
    false = 'false'
    integer = 'integer'
    decimal = 'decimal'
    string_chain = 'string_chain'
    identifier = 'id'
    """ end of file"""
    EOF = '$'
    """ types """
    _type = ['int', 'double', 'void', 'bool', 'string', 'mfun' ]
    var = 'var'
    # _int = 'int'
    # _double = 'double'
    # _void = 'void'
    # _bool = 'bool' 
    # _string = 'string' 
    # _math_function = 'mfun' 
    # _point = 'point' 
    # Floor, Ceil, Round, Random

    epsilon = 'epsilon'
    pass

class NonTerminalsTokens(TokenType):
    Program = 0
    Declaration_list = 1
    Declaration = 2
    ClassDecl = 3
    FunctDecl = 4
    FunctList = 5
    VarDecl = 6
    VarValue = 7
    Statement = 8
    Expression = 9
    ForStmt = 10
    ForFirst = 11
    WhileStmt = 12
    IfStmt = 13
    elseStmt = 14
    PrintStmt = 15
    ReturnStmt = 16
    ret = 17
    Block = 18
    block_body = 19
    Assignment = 20
    Call = 21
    Logic_Or = 22
    OR = 23
    Logic_And = 24
    AND = 25
    Equality = 26
    Eq = 27
    Comparison = 28
    LGEq = 29
    Term = 30
    Factor = 31
    FX = 32
    Pow = 33 # Pow -> Unary ^ Unary
    UX = 34
    PowX = 35
    Unary = 36
    call_type = 37
    call_right = 38
    Primary = 39
    Parameters = 40
    Parm = 41
    Arguments = 42
    Arg = 43
    F0F = 44
    Statement_List = 45
    Operation = 46


class Token:
    """
    Basic token class.

    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    line: int
        Token's line
    length: int
        Token's length
    """

    def __init__(self, lex:str, token_type:TokenType, line:int = -1, length:int = -1):
        self.lex = lex
        self.token_type = token_type
        self.line = line
        self.length = length

    def __str__(self):
        return f'{self.token_type.name}: {self.lex}, line:{self.line}'

    def __repr__(self):
        return str(self)

symbols_tokens = {
    '+'   : TerminalsTokens.plus,
    '-'   : TerminalsTokens.minus,
    '*'   : TerminalsTokens.star,
    '/'   : TerminalsTokens.slash,
    '('   : TerminalsTokens.opar,
    ')'   : TerminalsTokens.cpar,
    ','   : TerminalsTokens.comma,
    '.'   : TerminalsTokens.dot,
    '$'   : TerminalsTokens.EOF,
    '['   : TerminalsTokens.obracket,
    ']'   : TerminalsTokens.cbracket,
    '{'   : TerminalsTokens.obrace,
    '}'   : TerminalsTokens.cbrace,
    ';'   : TerminalsTokens.semicolon,
    '%'   : TerminalsTokens.percent,
    '^'   : TerminalsTokens.caret,
    '\''  : TerminalsTokens.quoat,
    '\"'  : TerminalsTokens.double_quoat,
    '='   : TerminalsTokens.equal,
    '=='  : TerminalsTokens.equal_equal,
    '!'   : TerminalsTokens.excl,
    '!='  : TerminalsTokens.excl_equal,
    '<'   : TerminalsTokens.less,
    '<='  : TerminalsTokens.less_equal,
    '>'   : TerminalsTokens.greater,
    '>='  : TerminalsTokens.greater_equal,
    '&&'  : TerminalsTokens.And,
    '||'  : TerminalsTokens.Or,
}
keywords_tokens = {
    # 'class'  : TerminalsTokens._class,
    'fun'    : TerminalsTokens.function,
    'null'   : TerminalsTokens.null,
    # 'this'   : TerminalsTokens.this,
    'return' : TerminalsTokens.Return,
    'while'  : TerminalsTokens.While,
    'for'    : TerminalsTokens.For,
    'if'     : TerminalsTokens.If,
    'else'   : TerminalsTokens.Else,
    # 'print'  : TerminalsTokens.Print,
    'true'   : TerminalsTokens.true,
    'false'  : TerminalsTokens.false,
    'var'    : TerminalsTokens.var,
    # 'type'   : TerminalsTokens._type,
    # 'void'   : TerminalsTokens._type,
    # 'int'    : TerminalsTokens._type,
    # 'double' : TerminalsTokens._type,
    # 'char'   : TerminalsTokens._type,
    # 'bool'   : TerminalsTokens._type,
    # 'string' : TerminalsTokens._type,
    # 'mfun'   : TerminalsTokens._type,
    # 'point'  : TerminalsTokens._type,
    'Forge'  : TerminalsTokens.Forge
}
