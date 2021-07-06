from discord.ext import commands
import discord

import datetime

from settings import MODERATOR_ROLE_NAME


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        """A command which unload cogs module.
        Parameters
        ------------
        !unload cogs.module 
        """
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")
    
    
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        """A command which load cogs module.
        Parameters
        ------------
        !unload cogs.module 
        """
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            return
        await ctx.send("Cog loaded")
    
    
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """A command which reload cogs module.
        Parameters
        ------------
        !unload cogs.module 
        """
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, *args):
        """Server status.
        Parameters
        ------------
        !status
        """
        guild = ctx.guild

        no_voice_channels = len(guild.voice_channels)
        no_text_channels = len(guild.text_channels)
        #set local variable for img
        file = discord.File("data/img/homie_bot_profil.jpg", filename = "homie_bot_profil.jpg")

        embed = discord.Embed(description="Server Status",
                              colour=discord.Colour.dark_purple())

        embed.set_thumbnail(url="attachment://homie_bot_profil.jpg")
        
        #add a bottom image to investigate I want it to be a local image aswell
        # embed.set_image(
        #     url="attachment://ineedahomie_discord_image.jpeg")

        emoji_string = ""
        for e in guild.emojis:
            if e.is_usable():
                emoji_string += str(e)
        embed.add_field(name="Custom Emojies",
                        value=emoji_string or "No emojis available", inline=False)

        embed.add_field(name="Server Name", value=guild.name, inline=False)

        embed.add_field(name="# Voice Channels", value=no_voice_channels)

        embed.add_field(name="# Text Channels", value=no_text_channels)

        embed.add_field(name="AFK Channel:", value=guild.afk_channel)
        embed.set_author(name=self.bot.user.name)
        embed.set_footer(text=datetime.datetime.now())
        await ctx.send(file=file , embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))