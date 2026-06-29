class ASTNode:
    pass


class VarAssign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VarAssign({self.name}, {self.value})"


class Number(ASTNode):
    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return f"Number({self.value})"


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class MemberAccess(ASTNode):
    def __init__(self, object_, member):
        self.object = object_
        self.member = member

    def __repr__(self):
        return f"MemberAccess({self.object}, {self.member})"


class BinaryOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.op}, {self.left}, {self.right})"


class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"


class String(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"


class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"


class Null(ASTNode):
    def __repr__(self):
        return "Null()"


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"


class If(ASTNode):
    def __init__(self, condition, then_branch, elif_branches=None, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches or []
        self.else_branch = else_branch

    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.elif_branches}, {self.else_branch})"


class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {self.params}, {self.body})"


class Call(ASTNode):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def __repr__(self):
        return f"Call({self.callee}, {self.args})"


class Return(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"


class ImportStmt(ASTNode):
    def __init__(self, module):
        self.module = module

    def __repr__(self):
        return f"Import({self.module})"


class SimpleStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Stmt({self.expr})"


class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assign({self.name}, {self.value})"


class SetStmt(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"SetStmt({self.name}, {self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def expect(self, token_type):
        token = self.advance()
        if token is None:
            raise SyntaxError(f"Expected {token_type}, got EOF")
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type}")
        return token

    # ----------------------------
    # ENTRY POINT
    # ----------------------------
    def parse(self):
        statements = []

        while self.peek() is not None:
            statements.append(self.statement())

        return statements

    # ----------------------------
    # STATEMENTS
    # ----------------------------
    def statement(self):
        token = self.peek()
        if token is None:
            return None
        if token.type == "VAR":
            return self.var_declaration()

        if token.type == "FUNCTION":
            return self.function_declaration()

        if token.type == "IF":
            return self.if_statement()

        if token.type == "WHILE":
            return self.while_statement()

        if token.type == "RETURN":
            return self.return_statement()

        if token.type == "IMPORT":
            return self.import_statement()

        if token.type == "RUN":
            return self.run_statement()

        if token.type == "SET":
            return self.set_statement()

        if token.type == "CHANGE":
            return self.change_statement()

        if token.type == "WRITE":
            return self.write_statement()

        if token.type == "LBRACE":
            return self.parse_block()

        # assignment or expression statement
        if token.type == "IDENTIFIER":
            # lookahead to see if it's assignment
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == "ASSIGN":
                name = self.expect("IDENTIFIER").value
                self.expect("ASSIGN")
                value = self.expression()
                # optional semicolon
                if self.peek() and self.peek().type == "SEMICOLON":
                    self.advance()
                return Assign(name, value)

        # default: expression statement
        expr = self.expression()
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return SimpleStmt(expr)

    def var_declaration(self):
        self.expect("VAR")

        name = self.expect("IDENTIFIER").value
        self.expect("ASSIGN")

        value = self.expression()

        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()

        return VarAssign(name, value)

    def parse_block(self):
        self.expect("LBRACE")
        stmts = []
        while self.peek() and self.peek().type != "RBRACE":
            stmts.append(self.statement())
        if self.peek() is None:
            raise SyntaxError("Missing '}' - block not closed")
        self.expect("RBRACE")
        return Block(stmts)

    def function_declaration(self):
        self.expect("FUNCTION")
        name = self.expect("IDENTIFIER").value
        self.expect("LPAREN")
        params = []
        if self.peek() and self.peek().type != "RPAREN":
            params.append(self.expect("IDENTIFIER").value)
            while self.peek() and self.peek().type == "COMMA":
                self.advance()
                params.append(self.expect("IDENTIFIER").value)
        self.expect("RPAREN")
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def if_statement(self):
        self.expect("IF")
        condition = self.expression()
        then_branch = self.parse_block() if self.peek() and self.peek().type == "LBRACE" else self.statement()
        elif_branches = []
        else_branch = None
        while self.peek() and self.peek().type == "ELIF":
            self.advance()
            cond = self.expression()
            branch = self.parse_block() if self.peek() and self.peek().type == "LBRACE" else self.statement()
            elif_branches.append((cond, branch))
        if self.peek() and self.peek().type == "ELSE":
            self.advance()
            else_branch = self.parse_block() if self.peek() and self.peek().type == "LBRACE" else self.statement()
        return If(condition, then_branch, elif_branches, else_branch)

    def while_statement(self):
        self.expect("WHILE")
        condition = self.expression()
        body = self.parse_block() if self.peek() and self.peek().type == "LBRACE" else self.statement()
        return While(condition, body)

    def return_statement(self):
        self.expect("RETURN")
        value = None
        if self.peek() and self.peek().type != "SEMICOLON":
            value = self.expression()
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return Return(value)

    def import_statement(self):
        self.expect("IMPORT")
        module = None
        if self.peek() and self.peek().type in ("STRING", "IDENTIFIER"):
            token = self.advance()
            module = token.value
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return ImportStmt(module)

    def run_statement(self):
        self.expect("RUN")
        if self.peek() and self.peek().type == "LPAREN":
            args = []
            self.expect("LPAREN")
            if self.peek() and self.peek().type != "RPAREN":
                args.append(self.expression())
                while self.peek() and self.peek().type == "COMMA":
                    self.advance()
                    args.append(self.expression())
            self.expect("RPAREN")
            if self.peek() and self.peek().type == "SEMICOLON":
                self.advance()
            return SimpleStmt(Call(Identifier("run"), args))

        expr = self.expression()
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return SimpleStmt(Call(Identifier("run"), [expr]))

    def call(self, callee):
        self.expect("LPAREN")
        args = []
        if self.peek() and self.peek().type != "RPAREN":
            args.append(self.expression())
            while self.peek() and self.peek().type == "COMMA":
                self.advance()
                args.append(self.expression())
        self.expect("RPAREN")
        return Call(callee, args)

    def set_statement(self):
        self.expect("SET")
        name = self.expect("IDENTIFIER").value
        self.expect("ASSIGN")
        value = self.expression()
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return SetStmt(name, value)

    def change_statement(self):
        self.expect("CHANGE")
        name = self.expect("IDENTIFIER").value
        self.expect("ASSIGN")
        value = self.expression()
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return SetStmt(name, value)

    def write_statement(self):
        self.expect("WRITE")
        expr = self.expression()
        if self.peek() and self.peek().type == "SEMICOLON":
            self.advance()
        return SimpleStmt(Call(Identifier("write"), [expr]))

    # ----------------------------
    # EXPRESSIONS
    # ----------------------------
    def expression(self):
        return self.equality()

    # precedence climbing
    def equality(self):
        node = self.comparison()
        while self.peek() and self.peek().type in ("EQ", "NE"):
            op = self.advance().type
            right = self.comparison()
            node = BinaryOp(op, node, right)
        return node

    def comparison(self):
        node = self.term()
        while self.peek() and self.peek().type in ("GT", "GE", "LT", "LE"):
            op = self.advance().type
            right = self.term()
            node = BinaryOp(op, node, right)
        return node

    def term(self):
        left = self.factor()

        while self.peek() and self.peek().type in ("PLUS", "MINUS"):
            op = self.advance().type
            right = self.factor()
            left = BinaryOp(op, left, right)

        return left

    def factor(self):
        node = self.unary()

        while self.peek() and self.peek().type in ("STAR", "SLASH", "PERCENT"):
            op = self.advance().type
            right = self.unary()
            node = BinaryOp(op, node, right)

        return node

    def unary(self):
        if self.peek() and self.peek().type in ("PLUS", "MINUS"):
            op = self.advance().type
            operand = self.unary()
            return UnaryOp(op, operand)
        return self.primary()

    def primary(self):
        token = self.advance()
        if token is None:
            raise SyntaxError("Unexpected EOF in expression")
        if token.type == "NUMBER":
            return Number(token.value)
        if token.type == "STRING":
            return String(token.value)
        if token.type == "IDENTIFIER":
            expr = Identifier(token.value)

            while self.peek() and self.peek().type == "DOT":
                self.advance()
                member = self.expect("IDENTIFIER").value
                expr = MemberAccess(expr, Identifier(member))

            if self.peek() and self.peek().type == "LPAREN":
                return self.call(expr)
            return expr
        if token.type == "TRUE":
            return Boolean(True)
        if token.type == "FALSE":
            return Boolean(False)
        if token.type == "NULL":
            return Null()
        if token.type == "LPAREN":
            expr = self.expression()
            self.expect("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token: {token}")
