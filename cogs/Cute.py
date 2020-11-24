# Import statements
import discord
from discord.ext import commands
import json
import random


# Functions
def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


class Cute(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Says that a member likes another member')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def likes(self, ctx, target1: discord.Member, target2: discord.Member):
        if not is_banned(ctx):
            sitting_message = discord.Embed(
                description=f'{target1.mention} and {target2.mention} sitting in the tree\nK-i-s-s-i-n-g! \nFirst comes'
                            f' love.\nThen comes marriage.\nThen comes baby in the baby carriage.',
                color=discord.Color.purple()
            )

            await ctx.send(embed=sitting_message)

    @commands.command(help='Smash someone')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def smash(self, ctx, target: discord.Member):
        if not is_banned(ctx):
            smash_msg = discord.Embed(
                description=f'{ctx.author.mention} wants to smash {target.mention}',
                color=discord.Color.purple()
            )
            await ctx.send(embed=smash_msg)

    @commands.command(help='Specifies who is sus')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def sus(self, ctx, target: discord.Member):
        if not is_banned(ctx):
            sus_msg = discord.Embed(
                description=f'{ctx.author.mention} thinks {target.mention} is sus 😏',
                color=discord.Color.purple()
            )
            await ctx.send(embed=sus_msg)

    @commands.command(help='Says who is in the cult')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cummiecult(self, ctx, target: discord.Member):
        if not is_banned(ctx):
            result = random.randint(1, 10)
            if result != 1:
                msg = discord.Embed(
                    description=f'{target.mention} is part of the cummie cult',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=msg)
            else:
                msg = discord.Embed(
                    description=f'{ctx.author.mention} is part of the cummie cult',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=msg)


def setup(client):
    client.add_cog(Cute(client))
