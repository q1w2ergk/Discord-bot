import discord
from discord.ext import commands
import random


class Eglence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="zar", help="1-6 arası zar atar.")
    async def zar(self, ctx):
        sonuc = random.randint(1, 6)
        zarlar = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
        embed = discord.Embed(
            title="🎲 Zar Atıldı!",
            description=f"{zarlar[sonuc - 1]} **{sonuc}** geldi!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command(name="yazi-tura", aliases=["yazı-tura", "yt"], help="Yazı tura atar.")
    async def yazi_tura(self, ctx):
        sonuc = random.choice(["Yazı ✍️", "Tura 🪙"])
        embed = discord.Embed(
            title="🪙 Yazı-Tura!",
            description=f"**{sonuc}** geldi!",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)

    @commands.command(name="rastgele", help="Belirtilen aralıkta rastgele sayı üretir.")
    async def rastgele(self, ctx, maksimum: int = 100):
        if maksimum < 1:
            await ctx.send("❌ Maksimum değer 1'den büyük olmalıdır!")
            return
        sonuc = random.randint(1, maksimum)
        embed = discord.Embed(
            title="🎰 Rastgele Sayı",
            description=f"1-{maksimum} arasından: **{sonuc}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="seksen-sekiz", aliases=["88"], help="88 :D")
    async def seksen_sekiz(self, ctx):
        await ctx.send("8️⃣8️⃣ :D")

    @commands.command(name="secim", help="Seçenekler arasından rastgele seçim yapar.")
    async def secim(self, ctx, *, secenekler: str):
        liste = [s.strip() for s in secenekler.split(",")]
        if len(liste) < 2:
            await ctx.send("❌ Lütfen virgülle ayrılmış en az 2 seçenek gir! Örnek: `!secim elma, armut, muz`")
            return
        secilen = random.choice(liste)
        embed = discord.Embed(
            title="🎯 Seçim Yapıldı!",
            description=f"Seçenekler: {', '.join(liste)}\n\n✅ Seçilen: **{secilen}**",
            color=discord.Color.teal()
        )
        await ctx.send(embed=embed)

    @commands.command(name="sayi-bil", help="1-100 arası sayı tahmin oyunu başlatır.")
    async def sayi_bil(self, ctx):
        sayi = random.randint(1, 100)
        await ctx.send("🎮 1-100 arası bir sayı tuttum! Tahmin etmek için sayı yaz. İptal için `iptal` yaz.")

        def kontrol(m):
            return m.author == ctx.author and m.channel == ctx.channel

        deneme = 0
        while True:
            try:
                msg = await self.bot.wait_for("message", timeout=30.0, check=kontrol)
                if msg.content.lower() == "iptal":
                    await ctx.send(f"❌ Oyun iptal edildi. Sayı **{sayi}** idi.")
                    break
                try:
                    tahmin = int(msg.content)
                except ValueError:
                    await ctx.send("Lütfen bir sayı gir!")
                    continue

                deneme += 1
                if tahmin < sayi:
                    await ctx.send(f"📈 Daha büyük! (Deneme: {deneme})")
                elif tahmin > sayi:
                    await ctx.send(f"📉 Daha küçük! (Deneme: {deneme})")
                else:
                    await ctx.send(f"🎉 Tebrikler! **{deneme}** denemede buldun! Sayı **{sayi}** idi.")
                    break
            except Exception:
                await ctx.send(f"⏰ Süre doldu! Sayı **{sayi}** idi.")
                break


async def setup(bot):
    await bot.add_cog(Eglence(bot))
