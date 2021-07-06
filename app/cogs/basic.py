import discord
from discord.ext import commands
from discord.utils import find
from discord.ext.commands import CommandNotFound
from ftools import notify_user
import random

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        # for guild in self.bot.guilds:
        #     for channel in guild.text_channels:
        #         if channel.name == "text-testing":
        #             await channel.send("🐶 Hi I'm Barker and I'm ready to bark 🐶")
        
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == "role-testing":
                    role_msg = await channel.send("Please react with theses emotes to get access at features")
                    role_msg
                    await role_msg.add_reaction("🏃")
    
    
    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):
    #     chans = guild.text_channels
    #     for channel in chans:
    #         if channel.name == 'general':
    #             await channel.send('hi')
                
    @commands.command()
    async def poke(self, ctx, member: discord.Member = None):
        """Send a poke to mention user.
        Parameters
        ------------
        !poke @user
        """
        if member is not None:
            message = "%s Require your presence" % ctx.author.name
            await notify_user(member, message)
        else:
            await ctx.send("Please use @mention to poke someone.")
    
    @commands.command()
    async def dm(self, ctx, member: discord.Member = None , message: str=""):
        """Send a dm to mention user.
        Parameters
        ------------
        !dm @user "direct message"
        """
        if member is not None : 
            dm = f'{ctx.author.name} say : {message}'
            await notify_user(member, message = dm)
        elif message == "":
            await ctx.send("Please fill your message to dm someone")
        else :
            await ctx.send("Please use @mention to message someone.")


    @commands.command(name='repeat', aliases=['mimic', 'copy','say'])
    async def say(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        Parameters
        ------------
        inp: str
            The input you wish to repeat.
        """
        await ctx.send(inp)
        
    @say.error
    async def say_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")

    @commands.command()
    async def invite(self, ctx):
        '''Create an server invite.
        Parameters
        ------------
        !invite
        '''
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)

    @commands.Cog.listener("on_message")
    async def detect(self, message):
        if message.author.bot:
            pass
        else :
            x = message.content.split()
            print(x)
            #Possible greetings from user
            Cheers = ["Hi", "hi", "Hello", "hello","bonjour","salut","coucou","ciao","Hey","Yo","Sup","sup","yo","hey"]
            unCheers= ["bye", "Bye", "cya", "cu","ciao","aurevoir","Aurevoir","a+","A+","++",]
            #Possible greetings from bot
            happy_emoji = [":grinning:",":smiley:",":smile:",":grin:",":laughing:",":slight_smile:",":sunglasses:"]
            RCheers = ["Hi", "Hello","Bonjour","Salut","Coucou","It’s good to see you.","Hey","Hey there","What’s up?","Yo!","Sup?","Waddap"]
            RunCheers= ["Bye", "cya", "cu","ciao","Aurevoir","a+","Goodbye","Bye bye!","Take it easy","Take care","Later","See you soon","I hope to see you soon"]
            if any(word in x for word in Cheers):
                    msg = f'{random.choice(RCheers)} {message.author.mention} {random.choice(happy_emoji)}'
                    await message.channel.send(msg)
            elif any(word in x for word in unCheers):
                    msg = f'{random.choice(RunCheers)} {message.author.mention} {random.choice(happy_emoji)}'
                    await message.channel.send(msg)

def setup(bot):
    bot.add_cog(Basic(bot))