from abc import ABC, ABCMeta, abstractmethod

import re

command_classes = []

# A metaclass that populates `command_classes`.
class SubclassWatcher(ABCMeta):
    def __init__(cls, name, bases, clsdict):
        super(SubclassWatcher, cls).__init__(name, bases, clsdict)

        if len(cls.mro()) > 3: # inherited `Command`
            command_classes.append(cls)

class Command(ABC, metaclass=SubclassWatcher):
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
        # Takes exactly one parameter: the user ID or mention.
        if len(self.args) != 1:
            return "the fuck do i do, you little shit"

        try:
            user_id = int(self.args[0])
        except: # not a user ID; parse the mention
            pattern = "<@!?([0-9]+)>"

            try:
                match = re.fullmatch(pattern, self.args[0])
                user_id = int(match.group(1))
            except: # not a mention either; die
                return "pass a mention or a user id"

        user = self.client.get_user(user_id)

        if user:
            return str(user.avatar_url)
        else: # None because the user has to share the bot's server
            return "i don't personally know this user"
