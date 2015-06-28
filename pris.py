import parse_pris
import grako
import sys
import collections

TRUEVALUES = ('true', 'True', 'TRUE', 't', 'yes')
FALSEVALUES = ('false', 'False', 'FALSE', 'f', 'no')


class PrisSemantics(object):
    """These mostly convert typed values into python-native values and fix
       oddities in the AST."""

    def atom(self, ast):
        myast = grako.ast.AST()
        string = ast['atom'][0]
        string += u''.join(ast['atom'][1])
        myast[u'rawvalue'] = string
        return myast

    def eolstring(self, ast):
        myast = grako.ast.AST()
        unescaped = u''
        for i in ast['string']:
            if len(i) and i[0] == '\\':
                unescaped = unescaped + i.decode('unicode_escape')
            else:
                unescaped += i

        myast[u'rawvalue'] = unescaped
        return myast


    def string(self, ast):
        myast = grako.ast.AST()
        unescaped = u''
        for i in ast['string']:
            if len(i) and i[0] == '\\':
                unescaped = unescaped + i.decode('unicode_escape')
            else:
                unescaped += i

        myast[u'rawvalue'] = unescaped
        return myast

    def simplenumber(self, ast):
        myast = grako.ast.AST()
        myast[u'rawvalue'] = int(ast['simplenumber'])
        return myast

    def hexnumber(self, ast):
        myast = grako.ast.AST()
        myast[u'rawvalue'] = int(ast['hexnumber'], 16)
        return myast

    def decnumber(self, ast):
        myast = grako.ast.AST()
        myast[u'rawvalue'] = float(ast['decnumber'])
        return myast

    def bool(self, ast):
        myast = grako.ast.AST()
        if ast['bool'] in TRUEVALUES:
            myast[u'rawvalue'] = True
        else:
            myast[u'rawvalue'] = False
        return myast

    def null(self, ast):
        myast = grako.ast.AST()
        myast[u'rawvalue'] = None
        return myast


def process_ast_value(ast):
    """Accept an AST object (assumed to be a value) and return
       a key (or None), and a value."""
    if 'nulliter' in ast:
        return None, collections.OrderedDict()
    elif 'kvp' in ast:
        key = ast['kvp'][0][ast['kvp'][0].keys()[0]]
        k, value = process_ast_value(ast['kvp'][1])
        return key, value
    elif 'rawvalue' in ast:
        return None, ast['rawvalue']
    elif 'iter' in ast:
        if isinstance(ast['iter'], grako.ast.AST):
            key, value = process_ast_value(ast['iter'])
            if key:
                value = collections.OrderedDict(((key, value), ))
        else:
            value = process_ast_iteratable(ast['iter'])
        return None, value


def process_ast_iteratable(asts):
    """Process a list of AST values while respecting the top level structure
       imposed by PRIS.."""
    outp = collections.OrderedDict()
    idx = 0
    for item in asts:
        k, v = process_ast_value(item)
        if not k:
            k = idx
        outp[k] = v
        idx += 1

    return outp


def process_ast(ast, flags=None):
    """Entry point for input processing. Takes a list of ASTs from the parser
       and processes them into an OrderedDict."""
    if flags:
        flags = flags
    else:
        flags = []
    outp = collections.OrderedDict()
    idx = 0
    if isinstance(ast, grako.ast.AST):
        k, v = process_ast_value(ast)
        if not k:
            k = 0
        if 'nofold' in flags or k != 0:
            outp[k] = v
        else:
            outp = v
    else:
        for item in ast:
            if 'directive' in item:
                if item['directive'] in ('reset', 'nofold'):
                    if item['directive'] == 'reset':
                        idx = 0
                    else:
                        flags.append('nofold')
                else:
                    directive = item['directive'][0]
                    directiveparam = item['directive'][1]['rawvalue']
                    flags.append((directive, directiveparam))
                continue  # directives don't increment index
            else:
                k, v = process_ast_value(item)
                if not k:
                    k = idx
                outp[k] = v
            idx += 1

    return outp, flags


def loads(data):
    """Load a string as a PRIS file."""
    parser = parse_pris.prisParser()

    ast = parser.parse(data, rule_name='start', semantics=PrisSemantics())
    flags = []
    result, flags = process_ast(ast, flags)
    return result


def load(f):
    """Load a file-like object (which exposes read) as a PRIS file."""
    data = f.read()
    return loads(data)

if __name__ == '__main__':
    result = load(open(sys.argv[1]))
    for item in result:
        print item, '=', result[item]
