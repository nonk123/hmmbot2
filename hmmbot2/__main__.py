#!/usr/bin/env python3

import discord

from .parser import Parser

class Hmmbot(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game("hmm?"))
        print("Ready")

    async def on_message(self, message):
        if message.author == self.user:
            return

        tokens = Parser(message.content).parse()

        # Tokens that initiate the command.
        initiator = ["bot", "do"]

        for word in initiator:
            if tokens.pop(0) != word:
                return

        response = "Tokens:\n```\n"
        response += "\n".join(tokens)
        response += "\n```"

        await message.channel.send(response)

def main():
    Hmmbot().run(open("token.secret").readline())

if __name__ == "__main__":
    main()
