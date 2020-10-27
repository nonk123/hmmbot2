#!/usr/bin/env python3

import discord

from .parser import Parser
from .commands import Avatar

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

            command = Avatar(self, message)

            if command.probe(expression):  # a valid avatar command
                result = command.execute() # execute with "probed" args
                output.append(result)
            else: # can't find command; print ed-style error message
                output = ["?"]
                break

        output = "\n".join(output)

        if output: # avoid sending an empty message
            await message.channel.send(output)

def main():
    Hmmbot().run(open("token.secret").readline())

if __name__ == "__main__":
    main()
