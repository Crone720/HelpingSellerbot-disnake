import disnake
from disnake.ext import commands
from utils import config
class AddBuyer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Выдать Баера", guild_ids=config.GuildID)
    @commands.has_permissions(administrator=True)
    async def buyer(self, interaction: disnake.ApplicationCommandInteraction, 
                    member: disnake.Member = commands.Param(name="покупатель", description="Пользователь"),
                    selectbuyer: str = commands.Param(name="тип", description="Укажите какого баера хотите выдать", choices=['Обычный Баер', 'Постояный баер'])):
        if interaction.author == member:
            await interaction.response.send_message("Нельзя выдать баера самому себе!", ephemeral=True)
            return
        if member.bot:
            await interaction.response.send_message("Нельзя выдать баера боту!", ephemeral=True)
            return
        embed = disnake.Embed(title="Выдача баера")
        if selectbuyer == "Обычный Баер":
            buyer = 123
            embed.description = f"Вы выдали обычного баера покупателю {member.mention}"
            await member.add_roles(disnake.Object(id=buyer))
            await interaction.response.send_message(embed=embed)
        elif selectbuyer == "Постоянный баер":
            sbuyer = 123
            embed.description = f"Вы выдали постоянного баера покупателю {member.mention}"
            await member.add_roles(disnake.Object(id=sbuyer))
            await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(AddBuyer(bot))

