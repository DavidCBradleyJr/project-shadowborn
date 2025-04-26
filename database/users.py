from .connection import get_connection

# Check if a user already exists in the database
async def user_exists(user_id: int) -> bool:
    conn = await get_connection()
    query = '''
        SELECT 1 FROM users WHERE user_id = $1
    '''
    result = await conn.fetchrow(query, user_id)
    await conn.close()
    return result is not None

# Create a new user in the database
async def create_user(user_id: int, username: str, rank: str, user_class: str,
                      hp: int, attack: int, magic_attack: int, defense: int, speed: int, mana: int):
    conn = await get_connection()
    query = '''
        INSERT INTO users (user_id, username, rank, class, hp, attack, magic_attack, defense, speed, mana)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    '''
    await conn.execute(query, user_id, username, rank, user_class, hp, attack, magic_attack, defense, speed, mana)
    await conn.close()

# Fetch a user's full profile (for /profile command)
async def fetch_user_profile(user_id: int):
    conn = await get_connection()
    query = '''
        SELECT * FROM users WHERE user_id = $1
    '''
    record = await conn.fetchrow(query, user_id)
    await conn.close()
    if record:
        return dict(record)
    return None
