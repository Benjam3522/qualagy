import re

# Define token patterns
TOKEN_SPEC = [
    ("LBRACE", re.compile(r"\{")),
    ("RBRACE", re.compile(r"\}")),
    ("LPAREN", re.compile(r"\(")),
    ("RPAREN", re.compile(r"\)")),
    ("LBRACKET", re.compile(r"\[")),
    ("RBRACKET", re.compile(r"\]")),

    ("COMMENT", re.compile(r"//.*")),
    
    ("COMMA", re.compile(r",")),
    ("DOT", re.compile(r"\.")),
    ("COLON", re.compile(r":")),
    ("SEMICOLON", re.compile(r";")),

    ("PLUS", re.compile(r"\+")),
    ("MINUS", re.compile(r"-")),
    ("STAR", re.compile(r"\*")),
    ("SLASH", re.compile(r"/")),
    ("PERCENT", re.compile(r"%")),

    ("EQ", re.compile(r"==")),
    ("GT", re.compile(r">")),
    ("LT", re.compile(r"<")),
    ("GE", re.compile(r">=")),
    ("LE", re.compile(r"<=")),
    ("NE", re.compile(r"!=")),
    ("ASSIGN", re.compile(r"=")),

    ("NUMBER", re.compile(r"\d+(\.\d+)?")),
    ("STRING", re.compile(r'"[^"]*"')),
    ("IDENTIFIER", re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")),

    ("SKIP", re.compile(r"[ \t\n]+")),
]

KEYWORDS = {
    "run": "RUN",
    "visibility": "VISIBILITY",
    "import": "IMPORT",
    "button": "BUTTON",
    "text": "TEXT",
    "change": "CHANGE",
    "get": "GET",
    "function": "FUNCTION",
    "if": "IF",
    "set": "SET",
    "write": "WRITE",
}

VALUE_TOKENS = {
    "IDENTIFIER",
    "NUMBER",
    "STRING",
}


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return (
            f"{self.type}({self.value})"
            if self.value is not None
            else self.type
        )


def lex(code):
    tokens = []
    i = 0

    while i < len(code):
        match = None

        for token_type, pattern in TOKEN_SPEC:
            match = pattern.match(code, i)

            if match:
                value = match.group(0)

                # Convert identifiers that are keywords
                if token_type == "IDENTIFIER":
                    token_type = KEYWORDS.get(value, "IDENTIFIER")

                if token_type not in ("SKIP", "COMMENT"):
                    token_value = (
                        value
                        if token_type in VALUE_TOKENS
                        else None
                    )
                    tokens.append(Token(token_type, token_value))

                i = match.end()
                break

        if not match:
            raise SyntaxError(f"Unexpected character: {code[i]}")

    return tokens


if __name__ == "__main__":
    code = """
    language MyLang {
        keywords {
            write 
            set 
        }
    }
    """

    tokens = lex(code)

    for token in tokens:
        print(token)