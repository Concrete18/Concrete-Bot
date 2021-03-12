from discord.ext import commands
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import discord as ds
from functions import *
import difflib
import random
import json
import sys


class AI(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()
        self.stemmer = LancasterStemmer()
        self.valid_channels = [self.bot.bot_commands_test_chan, self.bot.bot_commands_chan]

        # settings
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.similarity_req = self.phrase_data['settings']['similarity_req']
        self.debug = self.phrase_data['settings']['debug']

        # load stop words
        with open("stopwords.txt", "r") as f:
            self.stopwords = set(f.read())


    def simpilify_phrase(self, sentence):
        '''
        Uses NLTK and a stopwords list to stem and shorten
        the inputted sentence to remove unneeded information.

        Arguments:

        sentence -- sentence is simplified
        '''
        sentence = self.stemmer.stem(sentence.lower())
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w in self.stopwords]
        filtered_sentence = []
        for w in word_tokens:
            if w not in self.stopwords:
                filtered_sentence.append(w)
        if self.debug:
            print(f'filtered sentence: {filtered_sentence}')
        return filtered_sentence


    def phrase_matcher(self, phrase):
        '''Matches phrases to patterns in intent.json

        Arguments:

        phrase -- phrase that is checked for best match
        '''
        intents = self.phrase_data['intents']
        # switch to giving max_similarity self.similarity_req
        max_similarity = 0
        matched_pattern = ''
        tag = ''
        responses = ''
        prepped_phrase = self.simpilify_phrase(phrase)
        for item in intents:
            for pattern in item['patterns']:
                prepped_pattern = self.simpilify_phrase(pattern)
                similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
                if similarity > max_similarity and similarity > self.similarity_req:
                    responses = item['responses']
                    max_similarity = similarity
                    tag = item['tag']
                    matched_pattern = pattern.lower()
        if responses == '':
            return None, None, None
        if self.debug:
            print(f'Final pick is: {tag} with similarity: {max_similarity}\n{matched_pattern}\n')
        return tag, responses, matched_pattern


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        On message reaction.
        '''
        print(self.bot.user.id)
        print(message.content)
        if message.author == self.bot.user:  # Ignore messages made by the bot
            return
        if message.channel.id in self.valid_channels or str(812257484734988299) in message.content:
            tag, responses, pattern = self.phrase_matcher(message.content)
            if tag == None:
                return
            if len(responses) > 1:
                response = random.choice(responses)
            elif len(responses) == 1:
                response = responses[0]
            else:
                print('No responses.')
                return
            # sends message
            if '@' in response:
                response = response.replace('@', str(message.author.display_name))
            await message.channel.send(response)


def setup(bot):
    bot.add_cog(AI(bot))
