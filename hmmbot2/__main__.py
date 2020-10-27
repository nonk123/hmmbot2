#!/usr/bin/env python3

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

        output = []

        for expression in expressions:
            # Skip empty expressions.
            if not expression:
                continue

            for clazz in command_classes:
                command = clazz(self, expressions)

                if command.probe(expression):  # a valid avatar command
                    result = command.execute() # execute with "probed" args
                    output.append(result)
                    break
            else: # none of the commands worked
                output = ["?"]

        output = "\n".join(output)

        if output: # avoid sending an empty message
            await message.channel.send(output)

def main():
    Hmmbot().run(open("token.secret").readline())

if __name__ == "__main__":
    main()
