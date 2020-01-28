import random
import discord
import pathlib
from . import constants
from .solvertools.anagram import anagrams
from .solvertools.wordlist import cromulence
from .utils import ciphers, external_api
from .utils.registrar import WORD_SET_TESTS

from redbot.core import commands



COMMAND_KEYWORDS = {}

def random_nature_emoji():
    return random.choice(constants.NATURE_EMOJIS)

class HypeBot(commands.Cog):
    def __init__(self):
        self.path = pathlib.Path(__file__).parent.resolve() / "images"
    
    def images_path(self, ext):
        return self.path / ext

    @commands.command()
    async def pingu(self,ctx):
        await ctx.send("pongu")


    @commands.command()
    async def helper(self, ctx, *tokens):
        # TODO: refactor this into a more sophisticated help system

        if len(tokens) == 0:
            available_codes = '`' + ' '.join(constants.AVAILABLE_CODE_SHEETS) + '`'
            help_str = '\n'.join(constants.HELP_STR)
            await ctx.send(help_str)
            return

        help_type = tokens[0]

        if help_type == 'trivia' or help_type == 'ranked':
            help_str = '\n'.join(constants.TRIVIA_HELP_STR)
            await ctx.send(help_str)
            return

        if help_type == 'dropquote':
            help_str = '\n'.join(constants.DROPQUOTE_HELP_STR)
            await ctx.send(help_str)
            await ctx.send(file=discord.File(self.images_path('dropquote.png')))
            return

        if help_type == 'regex':
            help_str = '\n'.join(constants.REGEX_HELP_STR)
            await ctx.send(help_str)
            return

        if help_type.startswith('spiral'):
            help_str = '\n'.join(constants.SPIRAL_GALAXIES_HELP_STR)
            await ctx.send(help_str)
            await ctx.send(file=discord.File(self.images_path('spiralgalaxies.png')))


    @commands.command(aliases=['hugs'])
    async def hug(self, ctx):
        await ctx.send(f'(hugs {ctx.author.mention})')
        return

    @commands.command()
    async def emoji(self, ctx):
        await ctx.send(random_nature_emoji())
        return


    @commands.command()
    async def quote(self, ctx):
        response_str = random.choice(constants.QUOTES)
        await ctx.send(
            response_str.format(mention=ctx.author.mention))
        return


    ###############
    # Code sheets #
    ###############


    @commands.command()
    async def braille(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('braille.png')))


    @commands.command(aliases=['morsecode'])
    async def morse(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('morse_code.png')))


    @commands.command(aliases=['resist','resistors'])
    async def resistor(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('resistor_color_codes.jpg')))


    @commands.command()
    async def pigpen(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('pigpen.png')))


    @commands.command(aliases=['ipa'])
    async def ipachart(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('ipa.png')))


    @commands.command()
    async def binary(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('binary.webp')))


    @commands.command()
    async def ascii(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('ascii.png')))


    @commands.command(aliases=['aminoacid', 'aminoacids'])
    async def amino(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('amino.png')))


    @commands.command(aliases=['natoalphabet', 'radio', 'phonetic'])
    async def nato(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('nato.jpg')))


    @commands.command(aliases=['nautical', 'flags', 'maritime', \
                    'signal', 'signalflag', 'signalflags'])
    async def nauticalflags(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('flags.png')))


    @commands.command(aliases=['sem', 'semaphor', 'flagsemaphore'])
    async def semaphore(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('semaphore.png')))


    @commands.command(aliases=['element', 'elements', 'periodictable', \
                    'atomic', 'atomicnumbers'])
    async def periodic(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('periodic_table.png')))


    @commands.command(aliases=['pokerhands'])
    async def poker(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('poker.jpg')))


    @commands.command()
    async def greek(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('greek.png')))


    @commands.command()
    async def hebrew(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('hebrew.png')))


    @commands.command(aliases=['hiragana', 'katakana'])
    async def japanese(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('japanese.png')))


    @commands.command()
    async def scrabble(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('scrabble.png')))


    @commands.command()
    async def dvorak(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('dvorak.png')))


    @commands.command(aliases=['sign', 'asl'])
    async def signlanguage(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('sign_language.webp')))


    @commands.command(aliases=['roman', 'romannumeral', 'romannumerals'])
    async def send_sign_language(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('roman.png')))


    @commands.command(aliases=['mooncode'])
    async def moon(self, ctx):
        channel = ctx
        await channel.send(file=discord.File(self.images_path('moon.png')))


    @commands.command(aliases=['airportcodes'])
    async def airport(self, ctx):
        channel = ctx
        await channel.send('http://www.airportcodes.org/')


    @commands.command(aliases=['ceasar', 'cesar', 'caesarshift', 'shift'])
    async def caesar(self, ctx, *tokens):
        channel = ctx
        if len(tokens) <= 0:
            return

        msg = ' '.join(tokens) if tokens[0] != 'shift' else ' '.join(tokens[1:])

        shifts = [ciphers.caesar_shift(msg, i) for i in range(26)]
        best_cromulence = max(enumerate(shifts), key=lambda k: cromulence(k[1])[0])
        cromulence_idx = best_cromulence[0] if cromulence(best_cromulence[1])[0] > 0 else -1

        await channel.send('```\n' +
            '\n'.join([f'{shifts[i]} (+{i})' + (' *' if i == cromulence_idx else '') for i in range(26)]) +
        '\n```')


    @commands.command(aliases=['ana'])
    async def anagram(self, ctx, *tokens):
        channel = ctx
        if len(tokens) <= 0:
            return

        msg = ''.join(tokens)

        results = anagrams(msg)

        await channel.send('Anagrams for ' + msg + ':\n```\n' +
            '\n'.join([f'{r[1]} ({r[0]})' for r in results[:15]]) +
        '\n```')


    #################
    # External APIs #
    #################


    @commands.command(aliases=['crom'])
    async def cromulence(self, ctx,*args):
        content = ''.join(args)

        response = cromulence(content)
        await ctx.send(response)


    @commands.command(aliases=['o', 'ol'])
    async def onelook(self, ctx, *tokens):
        content = ' '.join(tokens)

        url, results = external_api.onelook(content)
        if len(results) == 0:
            await ctx.send('<' + url + '>\nNothing found')
            return

        await ctx.send('<' + url +
                                '>\n```\n' +
                                '\n'.join(results) + '```')
        return


    @commands.command(aliases=['r'])
    async def regex(self, ctx, *tokens):

        if len(tokens) <= 0 or tokens[0].lower() == 'help':
            help_str = '\n'.join(constants.REGEX_HELP_STR)
            await ctx.send(help_str)
            return


        dictionary = 'ukacd'
        dictionary_mappings = {
            'standard': 'standard',
            'small': 'standard',
            'ukacd': 'ukcryptic',
            'cryptic': 'ukcryptic',
            'medium': 'ukcryptic',
            'scrabble': 'ospdlong',
            'oed': 'oed',
            'onelook': 'onelook',
            'large': 'onelook',
            'huge': 'onelook',
            'wikipedia': 'wikititles',
            'cities': 'cities',
            'movies': 'movies',
            'bible': 'bible',
        }
        if tokens[0].lower() in dictionary_mappings.keys():
            dictionary = dictionary_mappings[tokens[0]]
            content = ' '.join(tokens[1:])
        else:
            content = ' '.join(tokens[0:])

        if dictionary == 'onelook':
            content = content.replace(' ', '_').replace('$', ' ')

        url, results = external_api.regex(content, dictionary)
        if len(results) == 0:
            await ctx.send('(via <' + url + '>)\nNothing found')
            return

        results = [r.replace('_', ' ') for r in results]
        results = '\n'.join(results)[:1900]

        await ctx.send('(via <' + url +
                                '>)\n```\n' +
                                results + '```')
        return


    @commands.command(aliases=['c'])
    async def crossword(self, ctx, *tokens):
        def _print_row(row, max_answer_length):
            print(row)
            return ('*' * row[0] + ' ' * (5 - row[0]) + ' ' +
                    row[1].ljust(max_answer_length) + ' ' +
                    row[2])

        content = ' '.join(tokens)

        url, response = external_api.crossword(content)

        max_answer_length = max([len(row[1]) for row in response])
        response_str = '\n'.join(_print_row(row, max_answer_length) for row in response)
        response_str = '<' + url + '>\n```\n' + response_str + '\n```'
        await ctx.send(response_str)


    @commands.command(aliases=['syn', 'syns', 'synonyms'])
    async def synonym(self, ctx, *tokens):
        content = ' '.join(tokens)

        response = external_api.synonyms(content)
        response = '`' + ' '.join(response)[:1350] + '`'
        await ctx.send(response)


    @commands.command(aliases=['ant', 'ants', 'antonyms', 'opps', \
                    'opposite', 'opposites'])
    async def antonym(self, ctx, *tokens):
        content = ' '.join(tokens)

        response = external_api.antonyms(content)
        response = '`' + ' '.join(response)[:1350] + '`'
        await ctx.send(response)


    @commands.command(aliases=['n', 'nm', 'nutri'])
    async def nutrimatic(self, ctx, *tokens):
        content = ''.join(tokens)

        url, results = external_api.nutrimatic(content)
        await ctx.send('<' + url +
                                '>\n```\n' +
                                '\n'.join(results) + '```')
        return


    @commands.command(aliases=['v', 'vignere'])
    async def vigenere(self, ctx, *args):
        tokens = ' '.join(args)
        key, decoded = external_api.solve_vigenere(tokens)
        response = f'{decoded}\n(key: {key})'
        await ctx.send(response)


    @commands.command(aliases=['qq', 'quip', 'quipquip', 'qiupqiup', 'quipqiup', \
                    'crypto'])
    async def cryptogram(self, ctx, *args):
        tokens = ' '.join(args)

        responses = external_api.solve_cryptogram(tokens)
        response = '```\n' + '\n'.join(
                [f'({k["logp"]:.2f}) {k["plaintext"]}  | KEY: {k["key"]}'
                for k in responses[:8]]) + '\n```'
        await ctx.send(response)


    @commands.command(aliases=['q'])
    async def qat(self, ctx, *args):
        content = ''.join(args)

        url, results = external_api.qat(content)
        url_r = '<' + url + '>\n'
        response = ''
        joiner = ' ' if ';' not in content else '\n'

        for key in results.keys():
            if len(results[key]) == 0:
                continue

            intermed = joiner.join(results[key])
            length_prefix = f'**Length {key}**\n' if key > 0 else ''
            response = response + f'{length_prefix}```\n{intermed}\n```'
        if len(response):
            response = response[:1350]
            backticks = response[-3:].count('`')
            response += '`' * (3 - backticks)
        else:
            response = f'No results {random_nature_emoji()}'
        await ctx.send(url_r + response)


    @commands.command(aliases=['t', 'common'])
    async def commonalities(self, ctx, *args):
        words = [w.lower() for w in args]

        if len(words) < 3:
            await ctx.send('I need at least 3 words')
            return

        msg = []
        for test_name, test in WORD_SET_TESTS.items():
            passed_tests = test(words)
            if not passed_tests:
                continue
            
            for return_str in passed_tests:
                msg.append(return_str)

        msg = '\n'.join(msg) if len(msg) else 'Sorry, couldn\'t find anything :('
        await ctx.send(msg)


    @commands.command(aliases=['wolfram', 'alpha', 'wa'])
    async def wolframalpha(self, ctx, *args):
        if len(args) > 0:
            words = ' '.join(args)
            out = external_api.wolfram_alpha(words)
            while sum(map(len, out)) > 2000:
                out.pop()
            await ctx.send(''.join(out))
