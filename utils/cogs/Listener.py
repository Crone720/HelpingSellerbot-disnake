import disnake
from disnake.ext import commands
from utils import db
class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message("У вас недостаточно прав!", ephemeral=True)
        if isinstance(error, commands.MissingRole):
            await inter.response.send_message("У вас недостаточно прав!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.activity.Streaming(name="discord.gg/cantery", url="https://discord.gg/cantery"))
        await db.create_db()
        b = await db.getallstat()
        print(f"""Бот {self.bot.user} / {self.bot.user.id} запущен
                  Пользователи: {len(self.bot.users)}
                  Проведено сделок: {b}
        """)

def setup(bot):
    bot.add_cog(Listener(bot))