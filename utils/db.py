import aiosqlite, disnake
from utils import config
async def create_db():
    async with aiosqlite.connect("seller.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS sellerstat(sellerid INTEGER, successfully INTEGER)")
        await db.execute("CREATE TABLE IF NOT EXISTS queue(sellerid INTEGER, member INTEGER)")
async def getstat(sellerid):
    async with aiosqlite.connect("seller.db") as db:
        cursor = await db.execute("SELECT successfully FROM sellerstat WHERE sellerid = ?", (sellerid,))
        b = await cursor.fetchone()
        return b[0] if b else 0
    
async def addseller(sellerid):
    async with aiosqlite.connect("seller.db") as db:
        await db.execute("INSERT INTO sellerstat VALUES (?, ?)", (sellerid, 0))
        await db.commit()

async def getallstat():
    async with aiosqlite.connect("seller.db") as db:
        cursor = await db.execute("SELECT SUM(successfully) FROM sellerstat")
        results = await cursor.fetchone()
        total_successfully = results[0] if results[0] is not None else 0
        return total_successfully

async def addqueue(sellerid, member):
    async with aiosqlite.connect("seller.db") as db:
        await db.execute("INSERT INTO queue VALUES (?, ?)", (sellerid, member))
        await db.commit()

async def removequeue(sellerid, member):
    async with aiosqlite.connect("seller.db") as db:
        await db.execute("DELETE FROM queue WHERE sellerid = ? AND member = ?", (sellerid, member))
        await db.commit()

async def addstat(sellerid):
    async with aiosqlite.connect("seller.db") as db:
        await db.execute("UPDATE sellerstat SET successfully = successfully + 1 WHERE sellerid = ?", (sellerid,))
        await db.commit()
    if config.Notify == "1":
        print(f"Продавец {sellerid} Успешно провёл сделку.")
    if config.Notify == "2":
        channel = disnake.Object(id=config.NotifyChannel)
        embed = disnake.Embed(title="Статистика", description=f"Продавец {sellerid} успешно провёл сделку.")
        await channel.send(embed=embed)
    else:
        pass