import discord
from discord.ext import commands
import random


class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast(self, ctx, member: discord.Member = None):
        '''Roast someone
         Parameters
        ------------
        !roast @user (if none user selected will post a random joke)
        '''
        insult = await get_momma_jokes()
        if member is not None:
            await ctx.send("%s  %s" %(member.name, insult))
        else : 
            await ctx.send(insult)


def setup(bot):
    bot.add_cog(Insult(bot))
