import disnake
from utils import config

class DeleteButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Удалить", style=disnake.ButtonStyle.red)
    async def deleteticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.channel.delete()

class CloseButtons(disnake.ui.View):
    def __init__(self, member):
        self.member = member
        super().__init__(timeout=None)

    @disnake.ui.button(label="Закрыть", style=disnake.ButtonStyle.red)
    async def closeticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.channel.set_permissions(self.member, send_messages=False, read_messages=False)
        await interaction.response.send_message("Тикет закрыт", ephemeral=True)
        await interaction.send("Закрыть тикет", view=DeleteButtons())
class TicketButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Открыть", style=disnake.ButtonStyle.green)
    async def openticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if config.banbuyer in [role.id for role in interaction.author.roles]:
            await interaction.response.send_message("Вы были заблокированы в системе тиктов", ephemeral=True)
            return
        if config.category == 1:
            ticket = await interaction.channel.category.create_text_channel(f"ticket-{interaction.author.name}")
            await ticket.set_permissions(interaction.author, send_messages=True, read_messages=True)
            await ticket.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
            role = interaction.guild.get_role(config.seller)
            await ticket.set_permissions(role, send_messages=True, read_messages=True)
            embed = disnake.Embed(title="Тикет создан", description=f"Тикет {ticket.mention} был создан")
            emb = disnake.Embed(title="Тикет", description=f"Чтобы закрыть тикет отреагируйте на кнопку.")
            view = disnake.ui.View()
            view.add_item(disnake.ui.Button(label="Перейти в тикет", style=disnake.ButtonStyle.link, url=f"https://discord.com/channels/{interaction.guild.id}/{ticket.id}"))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            await ticket.send(embed=emb, view=CloseButtons(interaction.author))
            return
        if config.category != 1:
            ticket = await interaction.guild.create_text_channel(f"ticket-{interaction.author.name}", category=disnake.Object(id=config.category))
            await ticket.set_permissions(interaction.author, send_messages=True, read_messages=True)
            await ticket.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
            role = interaction.guild.get_role(config.seller)
            await ticket.set_permissions(role, send_messages=True, read_messages=True)
            embed = disnake.Embed(title="Тикет создан", description=f"Тикет {ticket.mention} был создан")
            emb = disnake.Embed(title="Тикет", description=f"Чтобы закрыть тикет отреагируйте на кнопку.")
            view = disnake.ui.View()
            view.add_item(disnake.ui.Button(label="Перейти в тикет", style=disnake.ButtonStyle.link, url=f"https://discord.com/channels/{interaction.guild.id}/{ticket.id}"))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            await ticket.send(embed=emb, view=CloseButtons(interaction.author))
            return
        await interaction.response.send_message("Не удалось создать тикет", ephemeral=True)