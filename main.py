import disnake
from disnake.ext import commands
from utils import config

bot = commands.Bot(command_prefix=config.CommandPrefix, intents=disnake.Intents.all())

bot.load_extensions("utils/cogs")
bot.run(config.TOKEN)