class Parser:
    def __init__(self, code):
        self.__code = code
        self.__position = 0

    # Return True if current position + offset is past the end of code.
    def eobp(self, offset=0):
        return self.__position + offset >= len(self.__code)

    # Return the Nth character after the current position, without moving it.
    def peek(self, n=1):
        if not self.eobp(n):
            return self.__code[self.__position + n]

    # Idiomatically peek backwards.
    def last(self, n=1):
        return self.peek(-n)

    # Return the character at point.
    def char(self):
        return self.peek(0)

    # Move position by N characters.
    def next(self, n=1):
        self.__position += n

    # Parse the next token and return it.
    def next_token(self):
        # Characters that separate tokens.
        separators = (" ", "\t", "\n", "\r")

        token = ""

        while True:
            # End abruptly on expression separator or end of buffer.
            if self.char() == ";" or self.eobp():
                return token

            if self.char() in separators:
                # Ignore leading separators or multiple in a row.
                if token and self.last() not in separators:
                    self.next()
                    return token
            else:
                token += self.char()

            self.next()

    # Parse the given code and return a list of expressions from it.
    # Each expression is, in turn, a list of tokens.
    def parse(self):
        expressions = []

        while not self.eobp():
            tokens = []

            # ';' is the expression separator.
            while self.char() != ";" and not self.eobp():
                tokens.append(self.next_token())

            self.next()

            expressions.append(tokens)

        return expressions
