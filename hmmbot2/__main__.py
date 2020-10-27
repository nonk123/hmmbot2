#!/usr/bin/env python3

from io import BytesIO

import discord

from .parser import Parser
from .commands import command_classes

class Hmmbot(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game("hmm?"))
        print("Ready")

    async def on_message(self, message):
        # Ignore messages from self.
        if message.author == self.user:
            return

        expressions = Parser(message.content).parse()

        # Commands start with a "bot;" expression.
        if not expressions or expressions.pop(0) != ["bot"]:
            return

        # Enter "processing" state.
        await message.channel.trigger_typing()

        output = []

        for expression in expressions:
            # Skip empty expressions.
            if not expression:
                continue

            # Try to match command names with the first token.
            for command_name, clazz in command_classes.items():
                command = clazz(self)

                if command.probe(expression): # a valid avatar command
                    result = command.execute() # execute with "probed" args
                    output.append(result)
                    break
            else: # none of the commands worked; try the built-ins
                try:
                    # Pipe the output of the previous command.
                    if expression[0] == "into":
                        # Syntax: "into" command_name
                        assert len(expression) == 2
                        command_name = expression[1]

                        command = command_classes[command_name](self)

                        # Consume the last piece of output and add the result.
                        command.pipe(output.pop())
                        output.append(command.execute())
                    else:
                        raise
                except:
                    # A very meaningful, ed-style error message.
                    output = ["?"]

        files = []

        for index, line in enumerate(output):
            if isinstance(line, BytesIO): # probably an image; attach it
                files.append(discord.File(line, filename="image.png"))
                del output[index]

        if len(files) > 10: # 10 files per message max
            await message.channel.send("ungh, too many images to send. fuck you")
            return

        output = "\n".join(output)

        if output or files: # avoid sending an empty message
            await message.channel.send(output, files=files)

def main():
    Hmmbot().run(open("token.secret").readline())

if __name__ == "__main__":
    main()
