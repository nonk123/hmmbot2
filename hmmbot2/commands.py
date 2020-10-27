from abc import ABC, ABCMeta, abstractmethod, abstractclassmethod
from io import BytesIO

import re

from wand.image import Image
import requests

command_classes = {}

# A metaclass that populates `command_classes`.
class SubclassWatcher(ABCMeta):
    def __init__(cls, name, bases, clsdict):
        super(SubclassWatcher, cls).__init__(name, bases, clsdict)

        if len(cls.mro()) > 3: # if inherited `Command`
            command_classes[cls.identifier(cls)] = cls

class Command(ABC, metaclass=SubclassWatcher):
    # Return a command on `client`.
    def __init__(self, client):
        self.client = client
        self.args = None

    # Return the command's identifier as string.
    @abstractclassmethod
    def identifier(cls):
        pass

    # "Probe" the command to see if it can be executed in the given expression.
    def probe(self, expression):
        # Empty expression yields nothing.
        if not expression:
            return False

        # First token is the command name.
        if expression[0] != self.identifier():
            return False

        # The rest is the arguments.
        self.args = expression[1:]
        return True

    # Pipe the last command's output into the current.
    def pipe(self, last_output):
        self.args = [last_output]

    # Execute the command with previously probed arguments.
    def execute(self):
        if self.args is None:
            raise RuntimeError("Command hasn't been probed")

        try:
            return self.run()
        except Exception as err:
            return "`" + str(err) + "`"

    # Run the command. Never call this manually; use `execute` instead!
    @abstractmethod
    def run(self):
        pass

    # Read an image from the first argument.
    def read_image(self):
        if len(self.args) != 1:
            raise ValueError("Argument count != 1")

        # Already an image.
        if isinstance(self.args[0], BytesIO):
            return Image(file=self.args[0])

        # Otherwise, it's a URL we have to download.
        response = requests.get(self.args[0])
        return Image(file=BytesIO(response.content))

class Avatar(Command):
    def identifier(cls):
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

class Magik(Command):
    def identifier(cls):
        return "magik"

    def run(self):
        magik = BytesIO()

        try:
            image = self.read_image()
        except:
            return "that's not one fucking image, you moron"

        image.convert("png")

        image.liquid_rescale(int(image.width * 0.5), int(image.height * 0.5),
                             delta_x=1, rigidity=0)
        image.liquid_rescale(int(image.width * 1.5), int(image.height * 1.5),
                             delta_x=2, rigidity=0)

        image.save(file=magik)

        magik.seek(0)

        return magik
