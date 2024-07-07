from sqlalchemy.orm import Session
from discord_memo.db.database import SessionLocal, engine
from discord_memo.db import models


def init_db(db: Session):
    hoge = [
        models.Hoge(name="hoge", number=1),
        models.Hoge(name="fuga", number=2),
    ]
    db.add_all(hoge)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    init_db(db)
    db.close()
