
import json
import os
import random

import discord
from discord.ext import commands
import time 


from settings import *


async def get_momma_jokes():
    with open(os.path.join(DATA_DIR,"jokes.json")) as joke_file:
        jokes = json.load(joke_file)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult

def mods_or_owner():
    """
    Check that the user has the correct role to execute a command
    """
    def predicate(ctx):
        return commands.check_any(commands.is_owner(), commands.has_role(MODERATOR_ROLE_NAME))
    return commands.check(predicate)

def chill():
    """
    Check that the user has the correct role to execute a command
    """
    def predicate(ctx):
        return commands.check_any(commands.has_role(CHILL_ROLE_NAME))
    return commands.check(predicate)

def student():
    """
    Check that the user has the correct role to execute a command
    """
    def predicate(ctx):
        return commands.check_any(commands.has_role(STUDENT_ROLE_NAME))
    return commands.check(predicate)


async def notify_user(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)

  
# define the countdown func. 
def countdown(t): 
    
    in_time = True

    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
    return in_time is False
      
    print('Fire in the hole!!') 
  
  
# input time in seconds 
# t = input("Enter the time in seconds: ") 
  
# function call 
# countdown(int(t)) 
