from tortoise import Tortoise
from . import kid, user, session, kidinteraction, option, question

async def init_db():
    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ["database.models"]},
    )
    # Generate schemas
    await Tortoise.generate_schemas()