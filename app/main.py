import discord, os
from discord.ext import commands
from settings import *



description = str("Homie-bot allow theses prefix  !   $  . to use his/her commands. \n\nExample : !help    $help    .help \n \nFor more details on commands itself you can type : !help yourcommands") 

bot = commands.Bot(command_prefix = ['!','$','.'], description = description)

#add dynamicly new extension from dir.cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(DISCORD_TOKEN)