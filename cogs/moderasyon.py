import discord
from discord.ext import commands
import asyncio


class Moderasyon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="temizle", aliases=["clear", "sil"], help="Belirtilen sayıda mesajı siler.")
    @commands.has_permissions(manage_messages=True)
    async def temizle(self, ctx, adet: int = 10):
        if adet < 1 or adet > 100:
            await ctx.send("❌ Lütfen 1-100 arası bir değer gir!")
            return
        await ctx.channel.purge(limit=adet + 1)
        bilgi = await ctx.send(f"✅ **{adet}** mesaj silindi.")
        await asyncio.sleep(3)
        await bilgi.delete()

    @commands.command(name="at", aliases=["kick"], help="Belirtilen kullanıcıyı sunucudan atar.")
    @commands.has_permissions(kick_members=True)
    async def at(self, ctx, uye: discord.Member, *, sebep: str = "Sebep belirtilmedi"):
        if uye == ctx.author:
            await ctx.send("❌ Kendini atamazsın!")
            return
        if uye.top_role >= ctx.author.top_role:
            await ctx.send("❌ Bu kullanıcıyı atmak için yeterli yetkiye sahip değilsin!")
            return
        await uye.kick(reason=f"{ctx.author} tarafından: {sebep}")
        embed = discord.Embed(
            title="👟 Kullanıcı Atıldı",
            description=f"**{uye}** sunucudan atıldı.\nSebep: {sebep}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name="yasakla", aliases=["ban"], help="Belirtilen kullanıcıyı yasaklar.")
    @commands.has_permissions(ban_members=True)
    async def yasakla(self, ctx, uye: discord.Member, *, sebep: str = "Sebep belirtilmedi"):
        if uye == ctx.author:
            await ctx.send("❌ Kendini yasaklayamazsın!")
            return
        if uye.top_role >= ctx.author.top_role:
            await ctx.send("❌ Bu kullanıcıyı yasaklamak için yeterli yetkiye sahip değilsin!")
            return
        await uye.ban(reason=f"{ctx.author} tarafından: {sebep}")
        embed = discord.Embed(
            title="🔨 Kullanıcı Yasaklandı",
            description=f"**{uye}** yasaklandı.\nSebep: {sebep}",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

    @commands.command(name="sustur", aliases=["mute"], help="Kullanıcıyı belirtilen süre susturur.")
    @commands.has_permissions(moderate_members=True)
    async def sustur(self, ctx, uye: discord.Member, dakika: int = 10, *, sebep: str = "Sebep belirtilmedi"):
        if uye == ctx.author:
            await ctx.send("❌ Kendini susturamazsın!")
            return
        if dakika < 1 or dakika > 40320:
            await ctx.send("❌ Süre 1-40320 dakika (28 gün) arasında olmalıdır!")
            return
        import datetime
        sure = datetime.timedelta(minutes=dakika)
        await uye.timeout(sure, reason=f"{ctx.author} tarafından: {sebep}")
        embed = discord.Embed(
            title="🔇 Kullanıcı Susturuldu",
            description=f"**{uye.mention}** {dakika} dakika susturuldu.\nSebep: {sebep}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command(name="duyuru", aliases=["announce"], help="Belirtilen kanala duyuru gönderir.")
    @commands.has_permissions(manage_messages=True)
    async def duyuru(self, ctx, kanal: discord.TextChannel, *, mesaj: str):
        embed = discord.Embed(
            title="📢 Duyuru",
            description=mesaj,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Duyuruyu yapan: {ctx.author.display_name}")
        await kanal.send(embed=embed)
        await ctx.send(f"✅ Duyuru {kanal.mention} kanalına gönderildi!")


async def setup(bot):
    await bot.add_cog(Moderasyon(bot))
