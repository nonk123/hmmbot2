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

    def parse(self):
        tokens = []

        # Discord doesn't allow empty messages, so this will be filled
        # in, one way or another.
        current_token = ""

        # Characters that separate tokens.
        separators = (" ", "\t", "\n", "\r")

        while not self.eobp():
            if self.char() in separators:
                # Ignore multiple separators in a row.
                if self.last() not in separators:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += self.char()

            self.next()

        # Trailing newlines are trimmed, so terminate the sequence.
        tokens.append(current_token)

        return tokens
