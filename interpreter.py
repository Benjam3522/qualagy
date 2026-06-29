import random


class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, statements):
        for stmt in statements:
            self.visit(stmt)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            raise RuntimeError(
            f"No visitor for {type(node).__name__}"
         )

        return method(node)
        
    def visit_Number(self, node):
        return node.value
    
    def visit_String(self, node):
        return node.value.strip('"')
    
    def visit_Boolean(self, node):
        return node.value
    
    def visit_Null(self, node):
        return None

    def visit_Identifier(self, node):
        if node.name not in self.variables:
            raise RuntimeError(
                f"Undefined variable: {node.name}"
            )

        return self.variables[node.name]

    def visit_VarAssign(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value

    def visit_Assign(self, node):
        if node.name not in self.variables:
            raise RuntimeError(
                f"Variable '{node.name}' does not exist."
            )

        value = self.visit(node.value)
        self.variables[node.name] = value

    def visit_SetStmt(self, node):
        if node.name not in self.variables:
            raise RuntimeError(
                f"Variable '{node.name}' does not exist."
            )

        value = self.visit(node.value)
        self.variables[node.name] = value

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == "PLUS":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right

        if node.op == "MINUS":
            return left - right

        if node.op == "STAR":
            return left * right

        if node.op == "SLASH":
            return left / right

        if node.op == "PERCENT":
            return left % right

        if node.op == "EQ":
            return left == right

        if node.op == "NE":
            return left != right

        if node.op == "GT":
            return left > right

        if node.op == "GE":
            return left >= right

        if node.op == "LT":
            return left < right

        if node.op == "LE":
            return left <= right
        
    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)

        if node.op == "PLUS":
            return +value

        if node.op == "MINUS":
            return -value
        
    def visit_SimpleStmt(self, node):
        return self.visit(node.expr)

    def visit_Block(self, node):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result

    def visit_If(self, node):
        if self.visit(node.condition):
            return self.visit(node.then_branch)

        for cond, branch in node.elif_branches:
            if self.visit(cond):
                return self.visit(branch)

        if node.else_branch:
            return self.visit(node.else_branch)
        
    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_MemberAccess(self, node):
        object_name = getattr(getattr(node, "object", None), "name", None)
        member_name = getattr(getattr(node, "member", None), "name", None)

        if object_name == "log" and member_name == "write":
            return "log.write"

        raise RuntimeError(
            f"Unknown member access: {object_name}.{member_name}"
        )

    def visit_Call(self, node):
        callee_name = getattr(getattr(node, "callee", None), "name", None)
        callee_type = type(getattr(node, "callee", None)).__name__

        if callee_name == "write" or callee_name == "log.write" or callee_type == "MemberAccess":
            values = []

            for arg in node.args:
                values.append(str(self.visit(arg)))

            print("".join(values))
            return None

        if callee_name == "random":
            if len(node.args) != 2:
                raise RuntimeError("random expects exactly two arguments")

            low = int(self.visit(node.args[0]))
            high = int(self.visit(node.args[1]))
            return random.randint(low, high)

        raise RuntimeError(
            f"Unknown function: {node.callee.name}"
        )
        