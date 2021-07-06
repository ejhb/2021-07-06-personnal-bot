import discord
from discord.ext import commands
import random
import time
import pandas as pd
from ftools import notify_user, mods_or_owner 
import pymongo
from datetime import datetime



class Feedback(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def feedback(self , ctx):
        """
        This command allow you to send us a feedback. You will be redicted into a temp chan to gather your suggestions.
        Parameters
        ----------
        !feedback 
        """
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d (%H:%M)")
        ################################################################################################
        #                                   MOGO DB CONN                                               #
        ################################################################################################
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["homie"]
        question_feedback = {}
        quest = mydb.question.find_one(question_feedback)
        #Load question form db mongo
        list_q = []
        for question in quest:
            list_q.append(question)
        list_question = list_q[1:]

        new_user = str(ctx.author)    
        print(ctx.author)   
        guild = ctx.message.guild
        happy_emoji = [":grinning:",":smiley:",":smile:",":grin:",":laughing:",":slight_smile:",":sunglasses:"]
        temp_chan = await guild.create_text_channel("feedback")
        temp_chan
        await ctx.send(f'We are ready to hear you about that in {temp_chan.mention}')
        await temp_chan.send(f'Welcome to you {ctx.author.mention} {random.choice(happy_emoji)}')
        await temp_chan.send(f'Are your ready to answers at my questions? (yes/no)')
        list_answers = [] 
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content.lower() == "yes":
            print("on est ici")
            # while len(self.list_question) >= 0:
            for question in list_question :
                await temp_chan.send(question)
                # self.list_question.remove(question)
                answers = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                list_answers.append(answers.content)
            await temp_chan.send("Thanks you for your feedback, we are about to close this channel")
            time.sleep(1)
            await notify_user(ctx.author, f'Thanks you for your feedback, we closed the channel.')
            await temp_chan.delete()
            print("L'utilisateur :",ctx.author,"voici ma liste de réponse :",list_answers)
        elif msg.content.lower() == "no":
            await temp_chan.send("Tu as dis no or n")
            await notify_user(ctx.author, f'You close the request')
            await temp_chan.delete()
        ################################################################################################
        #                                   IMPORT MONGO                                               #
        ################################################################################################
        user_feedback = {
            "user":new_user,
            "answer1":list_answers[0],
            "answer2":list_answers[1],
            "answer3":list_answers[2],
            "answer4":list_answers[3], 
            "date-feedback":timestampStr
        }
        mydb.user.insert_one(user_feedback)
    
    
    @commands.command()
    @commands.has_role('Moderator')
    async def download(self, ctx, option: str = ""):
        """
        This command allow you to download question or answer feedback from our database.
        Parameters
        ----------
        !download answer/question 
        """
    ################################################################################################
    #                                   MOGO DB CONN                                               #
    ################################################################################################
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["homie"]
        if option == "question" : 
            df_question = pd.DataFrame(list(mydb.question.find()))
            df_question = df_question.drop(columns=["_id"])
            csv_question = df_question.to_csv()
            with open("./data/framer.csv", "w") as file:
                file.write(csv_question)
                file.close()
            with open("./data/framer.csv", "rb") as file:
                await ctx.send("Your file is:", file=discord.File(file, "question.csv"))
                file.close()
        elif option == "answer" : 
            df_user = pd.DataFrame(list(mydb.user.find()))
            df_user = df_user.drop(columns=["_id"])
            csv_answer = df_user.to_csv()
            with open("./data/framer.csv", "w") as file:
                file.write(csv_answer)
                file.close()
            with open("./data/framer.csv", "rb") as file:
                await ctx.send("Your file is:", file=discord.File(file, "answer.csv"))
                file.close()
        else :
            await ctx.send("Your must specify the option with : answer or question.")
        # # file = discord.File(csv_question, filename = "question.csv")
        # # with open("./data/framer.csv", "w") as file:
        # #     file.write(csv_question)
        # with open("./data/framer.csv", "rb") as file:
        #     await ctx.send("Your file is:", file=discord.File(file, "question.csv"))
        

   

def setup(bot):
    bot.add_cog(Feedback(bot))