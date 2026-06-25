import re

# Define token patterns
TOKEN_SPEC = [
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("SKIP", r"[ \t\n]+"),
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.type == "IDENTIFIER" else self.type


def lex(code):
    tokens = []
    i = 0

    while i < len(code):
        match = None

        for token_type, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(code, i)

            if match:
                value = match.group(0)

                if token_type != "SKIP":
                    token_value = value if token_type == "IDENTIFIER" else None
                    tokens.append(Token(token_type, token_value))

                i = match.end()
                break

        if not match:
            raise SyntaxError(f"Unexpected character: {code[i]}")

    return tokens

if __name__ == "__main__":
    code = """
    language MyLang {
        keywords { say let }
    }
    """

    tokens = lex(code)

    for t in tokens:
        print(t)