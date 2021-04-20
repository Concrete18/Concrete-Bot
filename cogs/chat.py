from discord.ext import commands
import discord as ds
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import difflib, random, json
from functions import *


class Chat(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()
        self.stemmer = LancasterStemmer()
        self.valid_channels = [self.bot.bot_commands_test_chan, self.bot.bot_commands_chan, self.bot.bot_test_chan_main]
        self.valid_bot = ['Concrete Test', 'Concrete Bot']
        self.last_response_tag = ''

        # settings
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.similarity_req = self.phrase_data['settings']['similarity_req']
        self.debug = self.phrase_data['settings']['debug']

        # load stop words
        with open("stopwords.txt", "r") as f:
            self.stop_words = set(f.read())


    def respond_if(self, message):
        '''
        Returns True only if the bot should respond.
        '''
        if message.author == self.bot.user:  # Ignore messages made by the bot
            return False
        if message.channel.id in self.valid_channels:
            if self.debug:
                print('Valid Channel')
            return True
        else:
            # TODO make this less problematic and automatic
            for bot_name in self.valid_bot:
                if bot_name in message.clean_content:
                    if self.debug:
                        print('Valid Mention')
                    return True
            if self.debug:
                print('invalid Channel')
            return False


    def simpilify_phrase(self, sentence):
        '''
        Uses NLTK and a stopwords list to stem and shorten
        the inputted sentence to remove unneeded information.

        Arguments:

        sentence -- sentence is simplified
        '''
        sentence = self.stemmer.stem(sentence.lower())
        word_tokens = word_tokenize(sentence)
        return [word for word in word_tokens if not word in self.stop_words]


    def phrase_matcher(self, phrase):
        '''Matches phrases to patterns in intent.json

        Arguments:

        phrase -- phrase that is checked for best match
        '''
        intents = self.phrase_data['intents']
        # switch to giving max_similarity self.similarity_req
        max_similarity = 0
        matched_pattern = ''
        best_response = ''
        prepped_phrase = self.simpilify_phrase(phrase)
        for item in intents:
            for pattern in item['patterns']:
                prepped_pattern = self.simpilify_phrase(pattern)
                similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
                if similarity > max_similarity and similarity > self.similarity_req:
                    max_similarity = similarity
                    matched_pattern = pattern.lower()
                    best_response = item
        if best_response == '':
            return
        if self.debug:
            print(phrase)
            print(f'Final pick is: {best_response["tag"]} with similarity: {max_similarity}\n{matched_pattern}\n')
        return best_response


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        On message reaction.
        '''
        if self.respond_if(message):
            # TODO fix mentions in other channels so it is less of a dumb fix
            message_string = message.clean_content.replace('@Concrete Test ', '')
            message_string = message_string.replace('@Concrete Bot ', '')
            data_dict = self.phrase_matcher(message_string)
            if data_dict == None:
                return
            if 'context_set' in data_dict.keys():
                if data_dict['context_set'] != self.last_response_tags:
                    return
            if 'tag' in data_dict.keys():
                self.last_response_tags = data_dict['tag']
            if len(data_dict['responses']) > 1:
                if 'weighted' in data_dict.keys():
                    response = random.choices(data_dict['responses'], weights=(data_dict['weighted']))[0]
                else:
                    response = random.choice(data_dict['responses'])
            elif len(data_dict['responses']) == 1:
                response = data_dict['responses'][0]
            else:
                print('No responses.')
                return
            # replaces some text with variable
            if '{' in response:
                replacements = {
                    '{display_name}':str(message.author.display_name)
                }
                for placeholder, replacement in replacements.items():
                    response = response.replace(placeholder, replacement)
            # sends message if not blank
            if response != '':
                await message.channel.send(response)


def setup(bot):
    bot.add_cog(Chat(bot))
