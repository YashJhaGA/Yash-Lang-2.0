from CodeParser import parser

operators = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "/": "DIV"
}

dataTypes = {
    "int": "INT",
    "String": "STRING",
    "real": "REAL",
    "boolean": "BOOLEAN"
}

comparisons = {
    "<": "LESS",
    ">": "GREATER",
    "<=": "LESSEQ",
    ">=": "GREATEREQ",
    "!=": "NOTEQ"
    "==" "ISEQ"
}

keywords = {
    "if": "IF_STMT",
    "fi": "END_IF_STMT",
    "while": "WHILE",
    "elihw": "END_WHILE"
}

parameters = {
    "(": "START_PARAM",
    ")": "END_PARAM"
}

boolResult = {
    "True": "TRUE",
    "False": "FALSE"
}


SYMBOLS = '+-*/()<>=!;"'
DIGITS = '0123456789.'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


class Token:
    def __init__(self, _type, value=None) -> None:
        self.type = _type
        self.value = value

    # representation method to return a string with the token's value and type
    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"



def lex(line):
    tok = []
    lineSplit = line.split(" ")
    print(lineSplit)
    for i in lineSplit:
        if(i in operators):
            tok.append(Token("OPERATOR",operators[i]))
        elif(i in dataTypes):
            tok.append(Token("DATATYPE",dataTypes[i]))
        elif(i in comparisons):
            tok.append(Token("COMPARISON",comparisons[i]))
        elif(i in boolResult):
            tok.append(Token("BOOLRESULT",boolResult[i]))
        elif(i in keywords):
            tok.append(Token("KEYWORD",keywords[i]))
        elif(i in parameters):
            tok.append(Token("PARAMETER",parameters[i]))
        elif(i == ";"):
            tok.append(Token("SEMICOLON",i))
        elif(i == "="):
            tok.append(Token("ASSIGN",i))
        elif(i == "\""):
            tok.append(Token("QUOTE",i))
        elif(i.isdigit()):
            tok.append(Token("INTEGER", i))
        elif(i == " "):
            pass
        elif(i[0].isdigit()):
            dot = i.count(".")
            num = True
            for j in i:
                if(j in DIGITS):
                    continue
                elif(j in LETTERS or j in SYMBOLS):
                    num = False
                else:
                    print(j + " is an invalid token")
                    exit(1)

            if(dot > 0 and num == True):
                tok.append(Token("REAL", i))
            else:
                tok.append(Token("IDENTIFIER",i))
        else:
            for j in i:
                if j not in DIGITS and j not in LETTERS and j not in SYMBOLS:
                    print(j + " is an invalid token")
                    exit(1)

            tok.append(Token("IDENTIFIER",i))


    return tok




# line = 'int y = 10 * 4 ; boolean x = 10 / y < 5 - 2 ;'
#line = 'int x = 10 ; if ( 10 < 5 ) ; int g = 4 ; fi ;'

line = 'int x ; if ( 5 < 10 ) ; x = 5 ; fi ;'

tokenList = lex(line)
print(tokenList)
p = parser(tokenList)
p.startParse()