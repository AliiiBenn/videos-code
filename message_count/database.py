import discord

import aiosqlite


async def create_guild_messages_table(connection : aiosqlite.Connection) -> None:
    await connection.execute("""
        CREATE TABLE IF NOT EXISTS guild_messages (
            guild_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            messages INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    await connection.commit()
    

async def create_channel_messages_table(connection : aiosqlite.Connection) -> None:
    await connection.execute("""
        CREATE TABLE IF NOT EXISTS channel_messages (
            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            messages INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    await connection.commit()
    
    
    
async def create_member_guild_messages(connection : aiosqlite.Connection,
                                       member : discord.Member,
                                       guild_id : int) -> None:
    
    await connection.execute("""
        INSERT INTO guild_messages (guild_id, member_id, messages)
        VALUES (?, ?, 0)
        """, (guild_id, member.id)
    )
    
    await connection.commit()
    
    
async def create_member_channel_messages(connection : aiosqlite.Connection,
                                         member : discord.Member,
                                         channel_id : int) -> None:

    await connection.execute("""
        INSERT INTO channel_messages (guild_id, channel_id, member_id, messages)
        VALUES (?, ?, ?, 0)
        """, (member.guild.id, channel_id, member.id)
    )
    
    await connection.commit()
    
    

async def remove_member_guild_messages(connection : aiosqlite.Connection,
                                       member : discord.Member,
                                       guild_id : int) -> None:
    
    await connection.execute("""
        DELETE FROM guild_messages
        WHERE guild_id = ?
        AND member_id = ?
        """, (guild_id, member.id)
    )
    
    await connection.commit()
    
    
async def remove_member_channel_messages(connection : aiosqlite.Connection,
                                         member : discord.Member,
                                         channel_id : int) -> None:
    
    await connection.execute("""
        DELETE FROM channel_messages
        WHERE channel_id = ?
        AND member_id = ?
        """, (channel_id, member.id)
    )
    
    await connection.commit()


async def get_member_guild_messages(connection : aiosqlite.Connection,
                                    member : discord.Member,
                                    guild_id : int) -> int:
    
    cursor = await connection.execute("""
        SELECT messages
        FROM guild_messages
        WHERE guild_id = ?
        AND member_id = ?
    """, (guild_id, member.id)
    
    )
    
    messages = await cursor.fetchone()
    
    if messages is None:
        return 0
    
    return messages[0]


async def increment_member_guild_messages(connection : aiosqlite.Connection,
                                          member : discord.Member,
                                          guild_id : int) -> None:
    
    await connection.execute("""
        UPDATE guild_messages
        SET messages = messages + 1
        WHERE guild_id = ?
        AND member_id = ?
        """, (guild_id, member.id)
    )
    
    await connection.commit()




async def get_member_channel_messages(connection : aiosqlite.Connection,
                                      member : discord.Member,
                                      channel_id : int) -> int:
    
    cursor = await connection.execute("""
        SELECT messages
        FROM channel_messages
        WHERE channel_id = ?
        AND member_id = ?
        """, (channel_id, member.id)
    )
    
    messages = await cursor.fetchone()
    
    if messages is None:
        return 0
    
    return messages[0]


async def get_member_channels_messages(connection : aiosqlite.Connection,
                                        member : discord.Member) -> list[tuple[int, int]]:
    
    messages = await connection.execute_fetchall("""
        SELECT channel_id, messages
        FROM channel_messages
        WHERE member_id = ?
        AND guild_id = ?
        """, (member.id, member.guild.id,)
    )
    
    return messages
    


async def increment_member_channel_messages(connection : aiosqlite.Connection,
                                            member : discord.Member,
                                            channel_id : int) -> None:
    
    await connection.execute("""
        UPDATE channel_messages
        SET messages = messages + 1
        WHERE channel_id = ?
        AND member_id = ?
        """, (channel_id, member.id)
    )
    
    await connection.commit()