from sqlalchemy.orm import Session
from discord_memo.db.database import SessionLocal, engine
from discord_memo.db import models, crud


if __name__ == "__main__":
	Base.metadata.create_all(bind=engine)
	crud.create_tag(SessionLocal(), channel_id=1, name="hoge")
	crud.create_tag(SessionLocal(), channel_id=1, name="fuga")
	print(crud.get_tags(SessionLocal()))
	print(crud.get_tag(SessionLocal(), 1))
	print(crud.get_tag(SessionLocal(), 2))

	crud.update_tag(SessionLocal(), 1, "piyo")
	print(crud.get_tag(SessionLocal(), 1))

	crud.delete_tag(SessionLocal(), 1)
	print(crud.get_tag(SessionLocal(), 1))
	print(crud.get_tags(SessionLocal()))

