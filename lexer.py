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
    ("GE", re.compile(r">=")),
    ("LE", re.compile(r"<=")),
    ("GT", re.compile(r">")),
    ("LT", re.compile(r"<")),
    ("NE", re.compile(r"!=")),
    ("ASSIGN", re.compile(r"=")),

    ("NUMBER", re.compile(r"\d+(\.\d+)?")),
    ("STRING", re.compile(r'"(?:\\.|[^"\\])*"')),
    ("IDENTIFIER", re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")),

    ("SKIP", re.compile(r"[ \t\n]+")),
]

KEYWORDS = {
    "var": "VAR",
    "run": "RUN",
    "visibility": "VISIBILITY",
    "import": "IMPORT",
    "change": "CHANGE",
    "function": "FUNCTION",
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "while": "WHILE",
    "return": "RETURN",
    "set": "SET",
    "log.write": "WRITE",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",
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
        chunk = code[i:]

        for token_type, pattern in TOKEN_SPEC:
            match = pattern.match(chunk)

            if match:
                value = match.group(0)

                if token_type == "IDENTIFIER":
                    token_type = KEYWORDS.get(value, "IDENTIFIER")

                if token_type not in ("SKIP", "COMMENT"):
                    token_value = value if token_type in VALUE_TOKENS else None
                    tokens.append(Token(token_type, token_value))

                i += len(value)
                break

        if not match:
            raise SyntaxError(f"Unexpected character: {code[i]}")

    return tokens