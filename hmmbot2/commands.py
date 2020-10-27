from abc import ABC, abstractmethod

class Command(ABC):
    # Return a command on `client` in response to `message`.
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.args = None

    # Return the command's identifier as string.
    @abstractmethod
    def identifier(self):
        pass

    # "Probe" the command to see if it can be executed in the given expression.
    def probe(self, expression):
        # Empty expression yields nothing.
        if not expression:
            return False

        # First token is the command name.
        if expression.pop(0) != self.identifier():
            return False

        # The rest is the arguments.
        self.args = expression
        return True

    # Execute the command with previously probed arguments.
    def execute(self):
        if self.args is None:
            raise RuntimeError("Command hasn't been probed")

        return self.run()

    # Run the command. Never call this manually; use `execute` instead!
    @abstractmethod
    def run(self):
        pass

class Avatar(Command):
    def identifier(self):
        return "avatar"

    def run(self):
        if self.args:
            return "stop saying shit about my avatar"
        else:
            return "yeah, my avatar is good"
