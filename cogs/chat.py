from discord.ext import commands
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import difflib, random, json
from functions import *
import datetime as dt


class Chat(commands.Cog):


    def __init__(self, bot):
        '''
        Chat Cog
        '''
        self.bot = bot
        self.bot_func = bot_functions()
        self.stemmer = LancasterStemmer()
        self.valid_channels = [
            self.bot.bot_commands_test_chan,
            self.bot.bot_commands_chan,
            self.bot.bot_test_chan_main
            ]
        self.valid_bot = [
            'Concrete Test',
            'Concrete Bot'
            ]
        # special actions
        self.actions = {
            'taco':self.taco,
            }
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
        # skip if it is a command
        if message.clean_content[0] == '/':
            return False
        # Ignore messages made by the bot
        elif message.author == self.bot.user:
            return False
        # checks if channel id is in valid_channels
        elif message.channel.id in self.valid_channels:
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


    def simplify(self, sentence):
        '''
        Uses NLTK and a stopwords list to stem and shorten
        the inputted sentence to remove unneeded information.

        Arguments:

        sentence -- sentence is simplified
        '''
        sentence = self.stemmer.stem(sentence.lower())
        word_tokens = word_tokenize(sentence)
        # return [word for word in word_tokens if not word in self.stop_words]
        # WIP new method.
        return_string = ''
        for word in word_tokens:
            if word not in self.stop_words:
                for letter in word:
                    return_string += letter + ' '
        return return_string.strip()


    async def taco(self, channel):
        '''
        Taco: Made for PathieZ.
        Requires info on the `channel` that the message will send to.
        '''
        if dt.datetime.today().weekday() == 1:
            rand_small = "{:,}".format(random.randrange(1, 8))
            rand_big = "{:,}".format(random.randrange(20000, 50000))
            is_tuesday = [
                'Fine, I will get you a taco.... What is your address. I am finding the number for delivery.',
                f'It is actually Taco Tuesday, give me {rand_small} to {rand_big} business days to find you a taco.',
                'Busy this Tuesday, ask next Tuesday',
                'Sorry, out of taco\'s. Would Nachos suffice?... Nevermind, out of those too.']
            msg = random.choice(is_tuesday)
        else:
            not_tuesday = [
                'It is not even Taco Tuesday.... Are you addicted to taco\'s or something?',
                'Taco, hahahaha',
                'Yo quiero Taco Bell!',
                'Can you make me a Taco instead?',
                'Who will give me some taco bell though?']
            msg = random.choice(not_tuesday)
        await channel.send(msg)

    
    # TODO update whats up phrase to rememeber something that happened recently


    def phrase_matcher(self, phrase):
        '''
        Matches the enterted `phrase` to patterns in intent.json.
        '''
        # switch to giving max_similarity self.similarity_req
        max_similarity = 0
        matched_pattern = ''
        best_response = False
        prepped_phrase = self.simplify(phrase)
        # check loop
        for intent in self.phrase_data['intents']:
            for pattern in intent['patterns']:
                prepped_pattern = self.simplify(pattern)
                similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
                if similarity > max_similarity and similarity > self.similarity_req:
                    max_similarity = similarity
                    matched_pattern = pattern.lower()
                    best_response = intent
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
            intent = self.phrase_matcher(message_string)
            if intent == False:
                return
            # allows responses to happen only if the last message goes with the context_set
            if 'context_set' in intent.keys():
                if intent['context_set'] != self.last_response_tags:
                    return
            if 'tag' in intent.keys():
                self.last_response_tags = intent['tag']
            # function based responses
            if intent["tag"] in self.actions.keys():
                await self.actions[intent["tag"]](message.channel)
                return
            # normal responses
            if len(intent['responses']) > 1:
                if 'weighted' in intent.keys():
                    response = random.choices(intent['responses'], weights=(intent['weighted']))[0]
                else:
                    response = random.choice(intent['responses'])
            elif len(intent['responses']) == 1:
                response = intent['responses'][0]
            else:
                print('No responses.')
                return
            # replaces some text with variable
            if '{' in response:
                replacements = {
                    '{display_name}':str(message.author.display_name),
                    '{years_old}':str(self.bot_func.readable_time_since(dt.datetime(2020,2,18,0,0,0,0)))
                }
                for placeholder, replacement in replacements.items():
                    response = response.replace(placeholder, replacement)
            # sends message if not blank
            if response != '':
                await message.channel.send(response)


def setup(bot):
    bot.add_cog(Chat(bot))
