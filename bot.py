import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")
    print(f"Bot ID: {bot.user.id}")
    print("------")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} slash komutu senkronize edildi.")
    except Exception as e:
        print(f"Komut senkronizasyon hatası: {e}")


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="genel")
    if channel:
        await channel.send(f"Hoş geldin {member.mention}! Sunucumuza katıldığın için mutluyuz! 🎉")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Böyle bir komut bulunamadı. `!yardim` yazarak komutları görebilirsin.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Eksik parametre: `{error.param.name}`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmak için gerekli izinlere sahip değilsin.")
    else:
        await ctx.send(f"❌ Bir hata oluştu: {error}")


async def load_extensions():
    await bot.load_extension("cogs.genel")
    await bot.load_extension("cogs.eglence")
    await bot.load_extension("cogs.moderasyon")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    keep_alive()
    asyncio.run(main())
