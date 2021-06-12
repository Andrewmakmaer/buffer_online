from fastapi import FastAPI
import sqlite3 as sq
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    text: str = None
    key: int = None


with sq.connect("key_value_base.db") as con:
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS value 
                    (key INTEGER,
                     value TEXT,
                     data INTEGER)""")  # в будущем может понадобиться от очищения старых записей

    app = FastAPI()

    origins = [
        '*'
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    @app.post("/app")
    async def comment(item: Item):
        if item.id == "add_text":
            new_key = generation_new_key()
            cursor.execute("INSERT INTO value VALUES(?, ?, 12)", [new_key, item.text])
            con.commit()
            return new_key
        elif item.id == "get_text":
            result = None
            for row in cursor.execute("SELECT value FROM value WHERE key = ?", [item.key]):
                result = row[0]

            cursor.execute("DELETE FROM value WHERE key = ?", [item.key])
            con.commit()

            if result is None:
                return 'Key not found'
            else:
                return result


    def get_key_all():
        result_list = []
        for row in cursor.execute("SELECT key FROM value"):
            result_list.append(row[0])

        return result_list


    def generation_new_key():
        for i in range(1001):
            if i not in get_key_all():
                return i
