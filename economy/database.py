import discord
import aiosqlite    
    
from enum import Enum
from typing import Union



async def create_table(connection : aiosqlite.Connection) -> None:
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS account (
            name TEXT,
            id INTEGER,
            guild_id INTEGER,
            bank_money INTEGER,
            pocket_money INTEGER
        )
    ''')
    
    await connection.commit()
    
    
async def account_exists(connection : aiosqlite.Connection, member : discord.Member) -> bool:
    cursor = await connection.execute('''
        SELECT id FROM account
        WHERE id = ? AND guild_id = ?''',
        (member.id, member.guild.id)
    )
    
    return await cursor.fetchone() is not None
    
    
async def create_account(connection : aiosqlite.Connection, member : discord.Member) -> None:
    await connection.execute('''
        INSERT INTO account (name, id, guild_id, bank_money, pocket_money)
        VALUES (?, ?, ?, ?, ?)''',
        (member.name, member.id, member.guild.id, 0, 0)
    )
    
    await connection.commit()
    
    
    
async def delete_account(connection : aiosqlite.Connection, member : discord.Member) -> None:
    await connection.execute('''
        DELETE FROM account
        WHERE id = ? AND guild_id = ?''',
        (member.id, member.guild.id)
    )
    
    await connection.commit()
    
    
    

    
    

    


class MoneyType(Enum):
    BANK_MONEY = "bank_money"
    POCKET_MONEY = "pocket_money"


async def get_money(connection : aiosqlite.Connection, 
                    member : discord.Member,
                    money_type : MoneyType) -> int:
    
    cursor = await connection.execute(f'''
        SELECT {money_type.value} FROM account
        WHERE id = ? AND guild_id = ?''',
        (member.id, member.guild.id)
    )
    
    money = await cursor.fetchone()
    
    if money is None:
        return 0
    
    return money[0]


async def get_bank_money(connection : aiosqlite.Connection,
                         member : discord.Member) -> int:

    return await get_money(connection, member, MoneyType.BANK_MONEY)


async def get_pocket_money(connection : aiosqlite.Connection,
                           member : discord.Member) -> int:

    return await get_money(connection, member, MoneyType.POCKET_MONEY)



async def has_pocket_money(connection : aiosqlite.Connection,
                           member : discord.Member,
                           money : int) -> bool:
    
    return await get_pocket_money(connection, member) >= money


async def has_bank_money(connection : aiosqlite.Connection,
                         member : discord.Member,
                         money : int) -> bool:
    
    return await get_bank_money(connection, member) >= money




async def get_most_money_members(connection : aiosqlite.Connection, guild_id : int) -> list[dict[str, Union[str, int]]]:
    members = await connection.execute_fetchall('''
        SELECT * FROM account
        WHERE guild_id = ?
        ORDER BY bank_money + pocket_money DESC
    ''', (guild_id,))
    
    result : list[dict[str, Union[str, int]]] = []
    for member in members:
        result.append({
            "name" : member[0],
            "money" : member[3] + member[4]
        })
    
    return result



async def add_money(connection : aiosqlite.Connection,
                    member : discord.Member, 
                    money : int,
                    money_type : MoneyType) -> None:
    
    await connection.execute(f'''
        UPDATE account
        SET {money_type.value} = {money_type.value} + ?
        WHERE id = ? AND guild_id = ?''',
        (money, member.id, member.guild.id)
    )
    
    await connection.commit()
    
    
    
async def remove_money(connection : aiosqlite.Connection,
                    member : discord.Member, 
                    money : int,
                    money_type : MoneyType) -> None:
        
    await connection.execute(f'''
        UPDATE account
        SET {money_type.value} = {money_type.value} - ?
        WHERE id = ? AND guild_id = ?''',
        (money, member.id, member.guild.id)
    )
    
    await connection.commit()
    
    
async def add_pocket_money(connection : aiosqlite.Connection, member : discord.Member, money : int) -> None:
    return await add_money(connection, member, money, MoneyType.POCKET_MONEY)
    
    
async def remove_pocket_money(connection : aiosqlite.Connection, member : discord.Member, money : int) -> None:
    return await remove_money(connection, member, money, MoneyType.POCKET_MONEY)
    
    
    
async def add_bank_money(connection : aiosqlite.Connection, member : discord.Member, money : int) -> None:
    return await add_money(connection, member, money, MoneyType.BANK_MONEY)
    
    
    
async def remove_bank_money(connection : aiosqlite.Connection, member : discord.Member, money : int) -> None:
    return await remove_money(connection, member, money, MoneyType.BANK_MONEY)
    