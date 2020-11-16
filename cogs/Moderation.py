# Import statements
import discord
from discord.ext import commands, tasks
import json
import random

# variables
statuses = ['You', 'My opponents', 'Italian royalty', 'Coup planning']


class Moderator(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Other
    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(random.choice(statuses)))

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # do some extra stuff here
        return

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as: {self.client.user}\nDiscord version: {discord.__version__}\n')
        self.change_status.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            error_message1 = discord.Embed(
                description=f'{ctx.author.mention} please pass in correct arguments. For more information, use >help '
                            f'\'command\'.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=error_message1)
        if isinstance(error, commands.CommandNotFound):
            error_message2 = discord.Embed(
                description=f'{ctx.author.mention} that command does not exist.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=error_message2)
        if isinstance(error, commands.MissingPermissions):
            error_message3 = discord.Embed(
                description=f'{ctx.author.mention} you do not have the required permissions for that command.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=error_message3)

    # Commands
    @commands.command(help='Returns the bot\'s ping')
    async def ping(self, ctx):
        ping_message = discord.Embed(
            description=f'Latency: {"{:.1f}".format(self.client.latency * 1000)}ms.',
            color=discord.Color.purple()
        )
        await ctx.send(embed=ping_message)

    @commands.command(help='Clears the specified number of messages (defaults to 5)')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

        cleared_message = discord.Embed(
            description=f'Cleared {amount} messages.',
            color=discord.Color.purple()
        )
        await ctx.send(embed=cleared_message)

    @commands.command(aliases=['dm'], help='dm\'s the specified user with the specified message')
    @commands.has_permissions(administrator=True)
    async def direct_message(self, ctx, messagee: discord.Member, *, message):
        dm_sent = discord.Embed(
            description=f':upside_down: {ctx.author.mention} sent!',
            color=discord.Color.purple()
        )
        await messagee.send(message)
        await ctx.send(embed=dm_sent)

    @commands.command(help='Gives link to source code on github')
    async def github(self, ctx):
        github_message = discord.Embed(
            description=f'My code is on Github here: https://github.com/EitherOr6917/eitherBot.py',
            color=discord.Color.purple()
        )
        await ctx.send(embed=github_message)

    @commands.command(help='Changes the prefix for the bot on the server')
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

        pc_message = discord.Embed(
            description=f'Server prefix changed to \'{prefix}\'',
            color=discord.Color.purple()
        )
        await ctx.send(embed=pc_message)

    @commands.command(help='Gives a votable message with the content provided')
    async def vote(self, ctx, *, question):
        await ctx.channel.purge(limit=1)
        op_msg = discord.Embed(
            description=f'{question}',
            color=discord.Color.purple()
        )
        message = await ctx.send(embed=op_msg)
        await message.add_reaction('❎')
        await message.add_reaction('✅')

    @commands.command(help='Spams the text provided in the channel provided the given number of times')
    @commands.has_permissions(administrator=True)
    async def looptext(self, ctx, channel: discord.TextChannel, loop_count: int, *, message):
        for x in range(loop_count):
            await channel.send(message)
        await ctx.author.send(f'{ctx.author.mention} I finished spamming lmao.')

    @commands.command(help='Same as looptext, except it sends an embed instead of plaintext')
    @commands.has_permissions(administrator=True)
    async def loopembed(self, ctx, channel: discord.TextChannel, loop_count: int, *, message):
        loop_embed = discord.Embed(
            description=message,
            color=discord.Color.purple()
        )
        for x in range(loop_count):
            await channel.send(embed=loop_embed)
        await ctx.author.send(f'{ctx.author.mention} I finished spamming lmao.')


def setup(client):
    client.add_cog(Moderator(client))
