class Parser:
    def __init__(self, code):
        self.code = code
        self.position = 0

    # Return True if current position + offset is past the end of code.
    def eobp(self, offset=0):
        return self.position + offset >= len(self.code)

    # Return the Nth character after the current position, without moving it.
    def peek(self, n=1):
        if not self.eobp(n):
            return self.code[self.position + n]

    # Return the character at point.
    def char(self):
        return self.peek(0)

    # Move position by N characters.
    def next(self, n=1):
        self.position += n

    def parse(self):
        tokens = []

        # Discord doesn't allow empty messages, so this will be filled
        # in, one way or another.
        current_token = ""

        while not self.eobp():
            if self.char() in (" ", "\t", "\n", "\r"):
                tokens.append(current_token)
                current_token = ""
            else:
                current_token += self.char()

            self.next()

        # Trailing newlines are trimmed, so terminate the sequence.
        tokens.append(current_token)

        return tokens
