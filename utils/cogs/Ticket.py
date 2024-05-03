import disnake
from disnake.ext import commands
from utils.view.ticketbuttons import TicketButtons

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ticket(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.send("Отправил")
        embed = disnake.Embed(title="Тикет", description="- Есть вопросы?\n- Хотите купить?\n- Есть жалоба? Открывай Тикет!")
        await interaction.channel.send(embed=embed, view=TicketButtons())

def setup(bot):
    bot.add_cog(Ticket(bot))