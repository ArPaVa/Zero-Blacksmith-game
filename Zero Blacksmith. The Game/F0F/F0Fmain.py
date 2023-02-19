import sys
import os
from Visitor import Interpreter
from F0FGrammar import F0F
import F0FLexer
from F0FParser import LL1_Parser, Parse_Tree
from AST import AST
code_path = os.path.join(os.path.dirname(__file__),'code_examples')

def runFile(file_path:str,forge_args:list=None):
    file_path = os.path.join(code_path, file_path)
    file = open(file_path,'r')
    source_code = file.read()
    file.close()
    Forge_eval, had_error, error_list = run(source_code,forge_args)
    if had_error:
        for er in error_list:
            print(er)
        return None
    else: return Forge_eval

def run(code:str,forge_args:list=None):
    lexer = F0FLexer.F0FLexer(code)
    had_error = lexer.had_error 
    error_list = lexer.lexer_errors
    G = F0F()
    # parse
    parser = LL1_Parser(G)
    parser.begin(lexer.tokens)
    had_error = had_error or parser.had_error 
    error_list = error_list + parser.parser_errors
    if had_error:
        return None, had_error, error_list
    # AST
    tree = Parse_Tree()
    tree.parse_tree_from_prod_list(parser.left_parse,lexer.tokens)
    ast = AST.ast_from_parse_tree(tree)
    # interpret
    interpreter = Interpreter()
    Forge_eval = interpreter.interpret(ast.root,forge_args)
    had_error = had_error or interpreter.had_runtime_error or interpreter.had_semantic_error
    error_list = error_list + interpreter.errors
    if had_error:
        return None, had_error, error_list
    return Forge_eval, had_error, error_list

def main(file_path:str=None,code:str=None, forge_args:list=None):
    if file_path != None:
        file_path = os.path.join(code_path, file_path)
        file = open(file_path,'r')
        source_code = file.read()
        file.close()
        return run(source_code, forge_args) 
    elif code != None:
        return run(code, forge_args) 
    else:
        print("Usage error: you must pass a file path")
        return None

if __name__ == "__main__":
    main(sys.argv[1])