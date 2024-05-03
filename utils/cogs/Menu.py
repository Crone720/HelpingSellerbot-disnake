import disnake
from disnake.ext import commands
from utils import config
from utils import db
from utils.view.SettingsButtons import SettingsButtons
class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=config.GuildID)
    async def seller(self, interaction: disnake.ApplicationCommandInteraction):
        ...
    @seller.sub_command(description="Панель Продавца")
    @commands.has_role(config.seller)
    async def panel(self, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="Панель", description=f"**Панель селлера** - В этой панели вы сможете посмотреть свою статистику и\nуправлять своими заказамими.")
        await interaction.response.send_message(embed=embed, view=SettingsButtons(), ephemeral=True)
        
    @seller.sub_command(guild_ids=config.GuildID, description="Выдать seller")
    @commands.has_permissions(administrator=True)
    async def setseller(self, interaction: disnake.ApplicationCommandInteraction, target: disnake.Member):
        if target.bot:
            return await interaction.response.send_message("Нельзя выдать боту бота!", ephemeral=True)
        await db.addseller(target.id)
        await target.add_roles(disnake.Object(id=config.seller))
        await interaction.response.send_message(f"Вы выдали seller'а {target.mention}", ephemeral=True)

def setup(bot):
    bot.add_cog(Menu(bot))