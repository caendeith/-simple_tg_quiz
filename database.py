import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица для состояния квиза
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY, 
            question_index INTEGER)''')
        
        # Таблица для результатов
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
            user_id INTEGER,
            username TEXT,
            full_name TEXT,
            score INTEGER,
            total INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Индекс для быстрого поиска результатов пользователя
        await db.execute('''CREATE INDEX IF NOT EXISTS idx_user_results 
                        ON quiz_results(user_id)''')
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT question_index FROM quiz_state WHERE user_id = ?', 
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)',
            (user_id, index)
        )
        await db.commit()

async def save_quiz_result(user_id, username, full_name, score, total):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''INSERT INTO quiz_results (user_id, username, full_name, score, total)
            VALUES (?, ?, ?, ?, ?)''',
            (user_id, username, full_name, score, total)
        )
        await db.commit()

async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Последний результат
        async with db.execute(
            '''SELECT score, total, timestamp 
            FROM quiz_results 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1''',
            (user_id,)
        ) as cursor:
            last_result = await cursor.fetchone()
        
        # Лучший результат
        async with db.execute(
            '''SELECT MAX(score), total 
            FROM quiz_results 
            WHERE user_id = ?''',
            (user_id,)
        ) as cursor:
            best_result = await cursor.fetchone()
        
        # Общее количество попыток
        async with db.execute(
            'SELECT COUNT(*) FROM quiz_results WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            attempts = await cursor.fetchone()
        
        return {
            'last_result': last_result,
            'best_result': best_result,
            'attempts': attempts[0] if attempts else 0
        }

async def get_leaderboard(limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            '''SELECT username, full_name, MAX(score), total
            FROM quiz_results
            GROUP BY user_id
            ORDER BY MAX(score) DESC, timestamp
            LIMIT ?''',
            (limit,)
        ) as cursor:
            return await cursor.fetchall()