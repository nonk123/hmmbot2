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

        tokens = Parser(message.content).parse()

        # Check for tokens that initiate the command.
        for initiator in ["bot", "do"]:
            try:
                if tokens.pop(0) != initiator:
                    return
            except: # pop failed; not enough tokens
                return

        if tokens: # not empty
            # Enclose everything in fancy code tags.
            response = "tokens:\n```\n"
            response += "\n".join(tokens)
            response += "\n```"
        else:
            response = "wtf did you just do"

        await message.channel.send(response)

def main():
    Hmmbot().run(open("token.secret").readline())

if __name__ == "__main__":
    main()
