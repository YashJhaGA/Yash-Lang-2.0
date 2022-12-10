class Token:
    def __init__(self, _type, value=None) -> None:
        self.type = _type
        self.value = value

    # representation method to return a string with the token's value and type
    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"


class Variable:
    def __init__(self, dataType, variable):
        self.type = dataType
        self.variable = variable

    def __repr__(self) -> str:
        return f"{self.type}:{self.variable}"

class parser:

    def __init__(self, listOfTokens):
        self.listOfTokens = listOfTokens
        self.index = 0
        self.symbols = []
        self.declareFlag = True


    def printTokens(self):
        print(self.listOfTokens)


    def isThereANextToken(self):
        try:
            self.listOfTokens[self.index+1]
            return True
        except:
            return False

    def getCurrentToken(self):
        return self.listOfTokens[self.index]

    def getNextToken(self):
        if(self.isThereANextToken()):
            self.index += 1
            return self.listOfTokens[self.index]
        else:
            return "NONE"

    def startParse(self):

        if(len(self.listOfTokens) <  2):
            print("Error: Program must be at least 2 Tokens Long (Start,End) pair")

        currentToken = self.listOfTokens[self.index]
        if(currentToken.type == "STRUCT"):
            if(currentToken.value == 'START'):
                pass
            else:
                print("Error: Expected [STRUCT: START] token")
        self.index += 1
        while(self.index < len(self.listOfTokens)):
            currentToken = self.listOfTokens[self.index]
            if(currentToken.type == 'DATATYPE'):
                self.declaration(currentToken)
            elif(currentToken.type == 'KEYWORD'):
                if(currentToken.value == 'IF_STMT'):
                    self.startIfStmt()
                elif(currentToken.value == 'WHILE'):
                    self.startWhileLoop()
                else:
                    print("Cannot start with keyword: "+currentToken.value)
                    exit(1)
            elif (currentToken.type == 'STRUCT'):
                if (currentToken.value == "END"):
                    self.endProgram()
                else:
                    print("Can't have two start tokens in program")
                    exit(1)
            elif(currentToken.type == 'IDENTIFIER'):
                self.startInitialize()
            else:
                print("Can't start line with Token: "+currentToken)
            self.index += 1



        print("Finished Parse")
        print(self.symbols)


    def endProgram(self):
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            return
        else:
            print("Error: END TOKEN should be LAST TOKEN IN PROGRAM")
            exit(1)


    def validateIdentifier(self,currentToken):
        for i in currentToken.value:
            if(i.isalpha()):
                pass
            else:
                return False
        return True


    def declaration(self,currentToken):

        declareType = currentToken.value

        currentToken = self.getNextToken()
        if (currentToken == 'NONE'):
            print("Missing tokens necessary for declaration")
            exit(1)
        elif (currentToken.type != 'IDENTIFIER'):
            print("Expected Token Type of IDENTIFIER and instead received " + currentToken.type)
            exit(1)
        else:
            if(self.validateIdentifier(currentToken)):
                pass
            else:
                print("Variable Identifier has wrong naming convention")
                exit(1)

        varIdentifer = currentToken.value
        if (any(y.variable == varIdentifer for y in self.symbols)):
            print("Variable '"+varIdentifer+"' already exists.")
            exit(1)
        currentToken = self.getNextToken()

        if(currentToken == 'NONE'):
            exit(1)
        elif(currentToken.type == 'SEMICOLON'):
            self.declareFlag = True
            self.symbols.append(Variable(declareType, varIdentifer))
            return
        elif(currentToken.type == 'ASSIGN'):
            self.initializePicker(declareType,varIdentifer)
        else:
            print("Expected Token of Semicolon or Assign. Instead received "+currentToken.type)

    def startInitialize(self):
        currentToken = self.getCurrentToken()
        if (any(y.variable == currentToken.value for y in self.symbols)):
            varName = currentToken.value
            dataType = ""
            for i in self.symbols:
                if i.variable == varName:
                    dataType = i.type
                    break
            currentToken = self.getNextToken()
            if(currentToken == 'NONE'):
                print("Missing tokens to initialize. Expected ASSIGN")
                exit(1)
            elif(currentToken.type == 'ASSIGN'):
                 self.declareFlag = False
                 self.initializePicker(dataType,varName)
            else:
                print("Expected Token of Assign. Instead received "+currentToken.type)
        else:
            print("Cannot initialize undeclared variable")

    def initializePicker(self,declareType, varIdentifier):
        if(declareType == 'INT'):
            self.makeInt(varIdentifier)
        elif(declareType == 'STRING'):
            self.makeString(varIdentifier)
        elif(declareType == 'REAL'):
            self.makeReal(varIdentifier)
        else:
            self.makeBoolean(varIdentifier)


    def makeInt(self,varIdentifer):
        currentToken = self.getNextToken()

        # If Token is a 'INTEGER', increment.
        # If Token is a 'OPERATOR', decrement.
        # If this value is something other than 0 or 1, throw error.
        expresionBalance = 0

        if(currentToken == 'NONE'):
            print("Missing necessary tokens")
        elif(currentToken.type == 'INTEGER' or currentToken.type == 'REAL' or currentToken.type == 'BOOLRESULT'):
            expresionBalance += 1
            pass
        elif(currentToken.type == 'IDENTIFIER'):
            if(any(y.variable == currentToken.value for y in self.symbols)):
                expresionBalance += 1
            else:
                print("Unidentifiable Identifier used")
                exit(1)
        else:
            print("Expected token of INTEGER. Instead received "+currentToken.type)
            exit(1)


        currentToken = self.getNextToken()

        if(currentToken == 'NONE'):
            print("Missing Semicolon")
            exit(1)
        elif(currentToken.type == 'SEMICOLON'):
            pass
        elif(currentToken.type != 'OPERATOR'):
            print("Expected Operator. Instead received "+currentToken.type)
            exit(1)
        else:
            while(currentToken.type != 'SEMICOLON'):

                if(currentToken.type == 'INTEGER' or currentToken.type == 'REAL' or currentToken.type == 'BOOLRESULT'):
                    expresionBalance += 1
                elif(currentToken.type == 'OPERATOR'):
                    expresionBalance -= 1
                elif (currentToken.type == 'IDENTIFIER'):
                    if (any(y.variable == currentToken.value for y in self.symbols)):
                        expresionBalance += 1
                    else:
                        print("Unidentifiable Identifier used")
                        exit(1)
                else:
                    print(currentToken.type)
                    print('Invalid Token for initializing Integer')
                    exit(1)

                if(expresionBalance < 0 or expresionBalance > 1):
                    print("Expression is unbalanced. You can't have 2 consecutive numbers or operators")
                    exit(1)

                currentToken = self.getNextToken()
                if (currentToken == 'NONE'):
                    print('Missing tokens to initialize')
                    exit(1)


        if(expresionBalance != 1):
            print("Invalid Syntax for Integer Initialization.")

        if(self.declareFlag):
            self.symbols.append(Variable("INTEGER", varIdentifer))


    def makeReal(self,varIdentifer):
        currentToken = self.getNextToken()

        # If Token is a 'INTEGER', increment.
        # If Token is a 'OPERATOR', decrement.
        # If this value is something other than 0 or 1, throw error.
        expresionBalance = 0

        if(currentToken == 'NONE'):
            print("Missing necessary tokens")
        elif(currentToken.type == 'REAL' or currentToken.type == 'INTEGER' or currentToken.type == 'BOOLRESULT'):
            expresionBalance += 1
            pass
        elif(currentToken.type == 'IDENTIFIER'):
            if(any(y.variable == currentToken.value for y in self.symbols)):
                expresionBalance += 1
            else:
                print("Unidentifiable Identifier used")
                exit(1)
        else:
            print("Expected token of REAL. Instead received "+currentToken.type)
            exit(1)


        currentToken = self.getNextToken()

        if(currentToken == 'NONE'):
            print("Missing Semicolon")
            exit(1)
        elif(currentToken.type == 'SEMICOLON'):
            pass
        elif(currentToken.type != 'OPERATOR'):
            print("Expected Operator. Instead received "+currentToken.type)
            exit(1)
        else:
            while(currentToken.type != 'SEMICOLON'):

                if(currentToken.type == 'INTEGER' or currentToken.type == 'REAL' or currentToken.type == 'BOOLRESULT'):
                    expresionBalance += 1
                elif(currentToken.type == 'OPERATOR'):
                    expresionBalance -= 1
                elif (currentToken.type == 'IDENTIFIER'):
                    if (any(y.variable == currentToken.value for y in self.symbols)):
                        expresionBalance += 1
                    else:
                        print("Unidentifiable Identifier used")
                        exit(1)
                else:
                    print(currentToken.type)
                    print('Invalid Token for initializing Integer')
                    exit(1)

                if(expresionBalance < 0 or expresionBalance > 1):
                    print("Expression is unbalanced. You can't have 2 consecutive numbers or operators")
                    exit(1)

                currentToken = self.getNextToken()
                if (currentToken == 'NONE'):
                    print('Missing tokens to initialize')
                    exit(1)


        if(expresionBalance != 1):
            print("Invalid Syntax for Integer Initialization.")

        if (self.declareFlag):
            self.symbols.append(Variable("REAL", varIdentifer))

    def makeString(self, varIdentifer):

        currentToken = self.getNextToken()
        quoteBalance = 0

        if(currentToken == 'NONE'):
            print("Missing Tokens to initialize String")
            exit(1)
        elif(currentToken.type == 'QUOTE'):
            quoteBalance += 1
            pass
        else:
            print("Expected Quote Token. Instead received: "+currentToken.type)


        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Missing Tokens to initialize String")
            exit(1)
        else:
            concatFlag = 0
            inQuote = True
            while(currentToken.type != 'SEMICOLON'):
                if(currentToken.type == 'QUOTE'):
                    if(quoteBalance % 2 == 1):
                        quoteBalance += 1
                        inQuote = False
                    else:
                        if(concatFlag == 1):
                            quoteBalance += 1
                            inQuote = True
                            concatFlag = 0
                        else:
                            print("Unbalanced amount of quotations")
                            exit(1)

                elif(currentToken.value == 'ADD'):
                    if(quoteBalance % 2 != 0):
                        print("Unbalanced amount of quotations")
                        exit(1)
                    else:
                        concatFlag = 1
                elif(not inQuote):
                    if(concatFlag == 1 and currentToken.type == 'IDENTIFIER'):
                        if (any(y.variable == currentToken.value for y in self.symbols)):
                            concatFlag = 0
                        else:
                            print("Unidentifiable Identifier Used")

                currentToken = self.getNextToken()

                if(currentToken == 'NONE'):
                    print("Missing necessary tokens to initialize String")
                    exit(1)



            if(quoteBalance % 2 == 0):
                if (self.declareFlag):
                    self.symbols.append(Variable("STRING", varIdentifer))
            else:
                print("Error in Syntax of initializing String")


    def makeBoolean(self, varIdentifer):
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Missing necessary tokens to initialize boolean")
            exit(1)
        elif(currentToken.type == 'BOOLRESULT'):
            currentToken = self.getNextToken()
            if(currentToken == 'NONE'):
                print("Expected Semicolon when there was nothing.")
                exit(1)
            elif(currentToken.type == 'SEMICOLON'):
                return
            else:
                print("Expected Semicolon. Instead received "+currentToken.type)
                exit(1)
        elif(currentToken.type == 'INTEGER' or currentToken.type == 'REAL' or currentToken.type == 'IDENTIFIER'):
            result = self.isBooleanExpression()
            if(result):
                if (self.declareFlag):
                    self.symbols.append(Variable("BOOLEAN", varIdentifer))
            else:
                print("Invalid Syntax for initalizing boolean expression ")
                exit(1)
        else:
            print("Expected a numerical value or variable identifer. Instead received "+currentToken.type)
            exit(1)


    def isBooleanExpression(self):
        currentToken = self.getCurrentToken()
        expressionBalance = 0
        while(currentToken.type != 'COMPARISON'):
            if(currentToken.type == 'INTEGER' or currentToken.type == 'REAL'):
                expressionBalance += 1
            elif(currentToken.type == 'IDENTIFIER'):
                if (any(y.variable == currentToken.value for y in self.symbols)):
                    expressionBalance +=1
                else:
                    print("Undefined Variable used: "+currentToken.value)
            elif(currentToken.type == 'OPERATOR'):
                expressionBalance -= 1

            else:
                print("Invalid Token used for boolean syntax")
                exit(1)

            if(expressionBalance < 0 or expressionBalance > 1):
                print("Cannot have 2+ consecutive numbers or operator tokens")
                exit(1)

            currentToken = self.getNextToken()
            if(currentToken == 'NONE'):
                print('Missing Tokens necessary for boolean expression initialization')
                exit(1)

        if(expressionBalance == 1):
            pass
        else:
            print("There must always be one more number than number of operators")
            exit(1)

        expressionBalance = 0
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Expected expression and instead received nothing")
            exit(1)
        elif(currentToken.type == 'SEMICOLON'):
            print("Expected expression and instead received "+currentToken.type)
            exit(1)

        while(currentToken.type != 'SEMICOLON'):
            if (currentToken.type == 'INTEGER' or currentToken.type == 'REAL'):
                expressionBalance += 1
            elif (currentToken.type == 'IDENTIFIER'):
                if (any(y.variable == currentToken.value for y in self.symbols)):
                    expressionBalance += 1
                else:
                    print("Undefined Variable used: " + currentToken.value)
            elif (currentToken.type == 'OPERATOR'):
                expressionBalance -= 1

            else:
                print("Invalid Token used for boolean syntax")
                exit(1)

            if (expressionBalance < 0 or expressionBalance > 1):
                print("Cannot have 2+ consecutive numbers or operator tokens")
                exit(1)

            currentToken = self.getNextToken()
            if (currentToken == 'NONE'):
                print('Missing Tokens necessary for boolean expression initialization')
                exit(1)


        if(expressionBalance == 1):
            return True
        else:
            return False


    def startIfStmt(self):
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Missing tokens necessary to complete if statement")
            exit(1)
        elif(currentToken.value == 'START_PARAM'):
            pass
        else:
            print("Expected symbol of '('. Instead received: "+currentToken.type+": "+currentToken.value)
            exit(1)

        currentToken = self.getNextToken()

        # Validates an if statement. For example ' if ( 10 + 4 < 5 ) ; ' is correct syntax.
        if(currentToken == 'NONE'):
            print("Missing Tokens. Expected boolean expression")
            exit(1)
        elif(currentToken.type == 'INTEGER' or currentToken.type == 'REAL' or currentToken.type == 'IDENTIFIER'):
            result = self.isIfBooleanExpression()
            if(result):
                currentToken = self.getNextToken()
                if(currentToken == 'NONE'):
                    print("Missing semicolon to complete initialization of if statement")
                    exit(1)
                elif(currentToken.type == 'SEMICOLON'):
                    pass
                else:
                    print("Expected Token of 'Semicolon'. Instead received: "+currentToken.type)
                    exit(1)
            else:
                print("Invalid Boolean Expression")
                exit(1)
        else:
            print("Expected Token of Numerical Value or Identifer. Instead received: "+currentToken.type)


        self.ifStmtBody()

        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Missing Token. Expected Semicolon")
            exit(1)
        elif(currentToken.type == 'SEMICOLON'):
            return
        else:
            print("Expected Semicolon. Instead received: "+currentToken.value)

    def startWhileLoop(self):
        currentToken = self.getNextToken()
        if (currentToken == 'NONE'):
            print("Missing tokens necessary to complete if statement")
            exit(1)
        elif (currentToken.value == 'START_PARAM'):
            pass
        else:
            print("Expected symbol of '('. Instead received: " + currentToken.type + ": " + currentToken.value)
            exit(1)

        currentToken = self.getNextToken()

        if (currentToken == 'NONE'):
            print("Missing Tokens. Expected boolean expression")
            exit(1)
        elif (currentToken.type == 'INTEGER' or currentToken.type == 'REAL' or currentToken.type == 'IDENTIFIER'):
            result = self.isIfBooleanExpression()
            if (result):
                currentToken = self.getNextToken()
                if (currentToken == 'NONE'):
                    print("Missing semicolon to complete initialization of if statement")
                    exit(1)
                elif (currentToken.type == 'SEMICOLON'):
                    pass
                else:
                    print("Expected Token of 'Semicolon'. Instead received: " + currentToken.type)
                    exit(1)
            else:
                print("Invalid Boolean Expression")
                exit(1)
        else:
            print("Expected Token of Numerical Value or Identifer. Instead received: " + currentToken.type)

        self.whileStmtBody()

        currentToken = self.getNextToken()
        if (currentToken == 'NONE'):
            print("Missing Token. Expected Semicolon")
            exit(1)
        elif (currentToken.type == 'SEMICOLON'):
            return
        else:
            print("Expected Semicolon. Instead received: " + currentToken.value)

    def whileStmtBody(self):
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Missing tokens for if statement")
            exit(1)
        while(currentToken.value != 'END_WHILE'):
            if (currentToken.type == 'DATATYPE'):
                self.declaration(currentToken)
            elif (currentToken.type == 'KEYWORD'):
                if (currentToken.value == 'IF_STMT'):
                    self.startIfStmt()
                elif (currentToken.value == 'WHILE'):
                    self.startWhileLoop()
                else:
                    print("Cannot start with keyword: " + currentToken.value)
                    exit(1)
            elif(currentToken.type == 'IDENTIFIER'):
                self.startInitialize()
            else:
                print("Invalid Initial Token for Line")
                exit(1)

            currentToken = self.getNextToken()
            if(currentToken == 'NONE'):
                print("Missing tokens for if statement")
                exit(1)




    def ifStmtBody(self):
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Missing tokens for if statement")
            exit(1)
        while(currentToken.value != 'END_IF_STMT'):
            if (currentToken.type == 'DATATYPE'):
                self.declaration(currentToken)
            elif (currentToken.type == 'KEYWORD'):
                if (currentToken.value == 'IF_STMT'):
                    self.startIfStmt()
                elif (currentToken.value == 'WHILE'):
                    self.startWhileLoop()
                else:
                    print("Cannot start with keyword: " + currentToken.value)
                    exit(1)
            elif(currentToken.type == 'IDENTIFIER'):
                self.startInitialize()
            else:
                print("Invalid Initial Token for Line")
                exit(1)

            currentToken = self.getNextToken()
            if(currentToken == 'NONE'):
                print("Missing tokens for if statement")
                exit(1)



    def isIfBooleanExpression(self):
        currentToken = self.getCurrentToken()
        expressionBalance = 0
        while(currentToken.type != 'COMPARISON'):
            if(currentToken.type == 'INTEGER' or currentToken.type == 'REAL'):
                expressionBalance += 1
            elif(currentToken.type == 'IDENTIFIER'):
                if (any(y.variable == currentToken.value for y in self.symbols)):
                    expressionBalance +=1
                else:
                    print("Undefined Variable used: "+currentToken.value)
            elif(currentToken.type == 'OPERATOR'):
                expressionBalance -= 1
            else:
                print("Invalid Token used for boolean syntax")
                exit(1)

            if(expressionBalance < 0 or expressionBalance > 1):
                print("Cannot have 2+ consecutive numbers or operator tokens")
                exit(1)

            currentToken = self.getNextToken()
            if(currentToken == 'NONE'):
                print('Missing Tokens necessary for boolean expression initialization')
                exit(1)

        if(expressionBalance == 1):
            pass
        else:
            print("There must always be one more number than number of operators")
            exit(1)


        expressionBalance = 0
        currentToken = self.getNextToken()
        if(currentToken == 'NONE'):
            print("Expected expression and instead received nothing")
            exit(1)
        elif(currentToken.value == 'END_PARAM'):
            print("Expected expression and instead received "+currentToken.type)
            exit(1)

        while(currentToken.value != 'END_PARAM'):
            if (currentToken.type == 'INTEGER' or currentToken.type == 'REAL'):
                expressionBalance += 1
            elif (currentToken.type == 'IDENTIFIER'):
                if (any(y.variable == currentToken.value for y in self.symbols)):
                    expressionBalance += 1
                else:
                    print("Undefined Variable used: " + currentToken.value)
            elif (currentToken.type == 'OPERATOR'):
                expressionBalance -= 1

            else:
                print("Invalid Token used for boolean syntax")
                exit(1)

            if (expressionBalance < 0 or expressionBalance > 1):
                print("Cannot have 2+ consecutive numbers or operator tokens")
                exit(1)

            currentToken = self.getNextToken()
            if (currentToken == 'NONE'):
                print('Missing Tokens necessary for boolean expression initialization')
                exit(1)


        if(expressionBalance == 1):
            return True
        else:
            return False



