#!/usr/bin/env python3

import discord

from .parser import Parser

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
        if not expressions or expressions[0] != ["bot"]:
            return

        # Just the initial "bot;" expression.
        if len(expressions) == 1:
            response = "wtf, you mf"
        else:
            response = "you told me to:"

            for tokens in expressions[1:]:
                response += "\n" + " ".join(tokens)

        await message.channel.send(response)

def main():
    Hmmbot().run(open("token.secret").readline())

if __name__ == "__main__":
    main()
