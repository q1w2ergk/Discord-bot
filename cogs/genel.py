import discord
from discord.ext import commands
from discord import app_commands
import platform
import time


class Genel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.baslangic_zamani = time.time()

    @commands.command(name="ping", help="Botun gecikme süresini gösterir.")
    async def ping(self, ctx):
        gecikme = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Gecikme süresi: **{gecikme}ms**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="yardim", aliases=["komutlar"], help="Tüm komutları listeler.")
    async def yardim(self, ctx):
        embed = discord.Embed(
            title="📋 Komut Listesi",
            description="Kullanılabilir tüm komutlar:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="🛠️ Genel Komutlar",
            value="`!ping` - Gecikmeyi göster\n`!bilgi` - Bot bilgilerini göster\n`!sunucu` - Sunucu bilgilerini göster\n`!kullanici [@kullanici]` - Kullanıcı bilgilerini göster",
            inline=False
        )
        embed.add_field(
            name="🎮 Eğlence Komutlar",
            value="`!zar` - Zar at\n`!yazi-tura` - Yazı tura at\n`!rastgele <sayı>` - Rastgele sayı üret\n`!seksen-sekiz` - 88 :D",
            inline=False
        )
        embed.add_field(
            name="🔨 Moderasyon Komutlar",
            value="`!temizle <adet>` - Mesajları temizle (Yönetici)\n`!sustur @kullanici <dakika>` - Kullanıcıyı sustur (Yönetici)\n`!at @kullanici` - Kullanıcıyı at (Yönetici)",
            inline=False
        )
        embed.set_footer(text=f"Prefix: ! | {ctx.guild.name}")
        await ctx.send(embed=embed)

    @commands.command(name="bilgi", help="Bot hakkında bilgi verir.")
    async def bilgi(self, ctx):
        uptime_saniye = int(time.time() - self.baslangic_zamani)
        saat = uptime_saniye // 3600
        dakika = (uptime_saniye % 3600) // 60
        saniye = uptime_saniye % 60

        embed = discord.Embed(
            title="🤖 Bot Bilgileri",
            color=discord.Color.purple()
        )
        embed.add_field(name="Bot Adı", value=self.bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Sunucu Sayısı", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Python Sürümü", value=platform.python_version(), inline=True)
        embed.add_field(name="discord.py Sürümü", value=discord.__version__, inline=True)
        embed.add_field(name="Çalışma Süresi", value=f"{saat}s {dakika}d {saniye}sn", inline=True)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="sunucu", help="Sunucu bilgilerini gösterir.")
    async def sunucu(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 {guild.name} Sunucu Bilgileri",
            color=discord.Color.gold()
        )
        embed.add_field(name="Sunucu ID", value=guild.id, inline=True)
        embed.add_field(name="Sahip", value=guild.owner.mention, inline=True)
        embed.add_field(name="Üye Sayısı", value=guild.member_count, inline=True)
        embed.add_field(name="Kanal Sayısı", value=len(guild.channels), inline=True)
        embed.add_field(name="Rol Sayısı", value=len(guild.roles), inline=True)
        embed.add_field(name="Oluşturulma Tarihi", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(name="kullanici", help="Kullanıcı bilgilerini gösterir.")
    async def kullanici(self, ctx, uye: discord.Member = None):
        uye = uye or ctx.author
        embed = discord.Embed(
            title=f"👤 {uye.display_name} Kullanıcı Bilgileri",
            color=uye.color
        )
        embed.add_field(name="Kullanıcı Adı", value=str(uye), inline=True)
        embed.add_field(name="ID", value=uye.id, inline=True)
        embed.add_field(name="Bot mu?", value="Evet" if uye.bot else "Hayır", inline=True)
        embed.add_field(name="Sunucuya Katılma", value=uye.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Hesap Oluşturma", value=uye.created_at.strftime("%d/%m/%Y"), inline=True)
        roller = [rol.mention for rol in uye.roles if rol.name != "@everyone"]
        embed.add_field(name=f"Roller ({len(roller)})", value=" ".join(roller) if roller else "Yok", inline=False)
        embed.set_thumbnail(url=uye.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Genel(bot))
