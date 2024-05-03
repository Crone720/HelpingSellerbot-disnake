import disnake, datetime
from utils import db
from utils import config
class LuckButton(disnake.ui.View):
    def __init__(self, author, member, embed):
        self.author = author
        self.member = member
        self.embed = embed
        super().__init__(timeout=None)

    @disnake.ui.button(label="💚", style=disnake.ButtonStyle.gray)
    async def luck(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if self.author == interaction.author:
            await db.removequeue(interaction.author.id, self.member.id)
            await db.addstat(interaction.author.id)
            em = self.embed.set_footer(text=f"Статус: ✅")
            await interaction.response.edit_message(embed=em, view=None)
        else:
            await interaction.response.send_message("Это не ваша очередь", ephemeral=True)

class BUserSelect(disnake.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Укажите пользователя", min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        member = self.values[0]
        if member.bot:
            return await interaction.response.send_message("Не взаимодействуйте с ботами", ephemeral=True)
        role = interaction.guild.get_role(config.banbuyer)
        em = disnake.Embed(title="Блокировка")
        if config.banbuyer in [role.id for role in member.roles]:
            await member.remove_roles(role)
            em.description = f"Вы сняли тикет блокировку пользователю {member.mention}"
            await interaction.response.edit_message(embed=em, view=Back())
            return
        await member.add_roles(role)
        em.description = f"Вы выдали тикет блокировку пользователю {member.mention}"
        await interaction.response.edit_message(embed=em, view=Back())
class UserSelect(disnake.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Укажите пользователя", min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        member = self.values[0]
        await db.addqueue(interaction.author.id, member.id)
        embed = disnake.Embed(title="Очередь", description=f"Вы добавили {member.mention} в очередь")
        await interaction.response.edit_message(embed=embed, view=Back())
        await interaction.send(f"Вы добавили {member.mention} в очередь", ephemeral=True)
        embed1 = disnake.Embed(title="Очередь", description=f"Покупатель: {member.mention}\nДата: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        embed1.set_footer(text=f"Статус: ❌")
        channel = interaction.guild.get_channel(config.QChannel)
        await channel.send(embed=embed1, view=LuckButton(interaction.author, member, embed1))
class Back(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.gray)
    async def back(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(title="Панель", description="")
        await interaction.response.edit_message(embed=embed, view=SettingsButtons())

class SettingsButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Посмотреть свою статистику", style=disnake.ButtonStyle.green)
    async def settings(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        b = await db.getstat(interaction.author.id)
        embed = disnake.Embed(title="Статистика", description=f"Вы успешно провели {b} сделок.")
        await interaction.response.edit_message(embed=embed, view=Back())

    @disnake.ui.button(label="Добавить в очередь", style=disnake.ButtonStyle.gray)
    async def addqueue(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(title="Добавление в очередь", description="Укажите пользователя")
        view = disnake.ui.View()
        view.add_item(UserSelect())
        await interaction.response.edit_message(embed=embed, view=view)
    
    @disnake.ui.button(label="Снять/Выдать Блокировку", style=disnake.ButtonStyle.gray, row=2)
    async def banticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(title="Выдача блокировки", description="Укажите пользователя")
        view = disnake.ui.View()
        view.add_item(BUserSelect())
        await interaction.response.edit_message(embed=embed, view=view)