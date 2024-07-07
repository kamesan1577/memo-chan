from .database import SessionLocal

from .models import Hoge


def create_hoge(hoge_data):
    db = SessionLocal()
    hoge = Hoge(**hoge_data)
    db.add(hoge)
    db.commit()
    db.refresh(hoge)
    return hoge


def get_hoge(hoge_id):
    db = SessionLocal()
    hoge = db.query(Hoge).filter(Hoge.id == hoge_id).first()
    return hoge


def update_hoge(hoge_id, hoge_data):
    db = SessionLocal()
    hoge = db.query(Hoge).filter(Hoge.id == hoge_id).first()
    for key, value in hoge_data.items():
        setattr(hoge, key, value)
    db.commit()
    db.refresh(hoge)
    return hoge


def delete_hoge(hoge_id):
    db = SessionLocal()
    hoge = db.query(Hoge).filter(Hoge.id == hoge_id).first()
    db.delete(hoge)
    db.commit()
    return {"message": "Hoge deleted"}


if __name__ == "__main__":
    hoge_data = {
        "name": "hoge",
        "number": 1,
    }
    hoge = create_hoge(hoge_data)
    print(hoge)
    print(get_hoge(hoge.id))
    hoge_data = {
        "name": "fuga",
        "number": 2,
    }
    hoge = update_hoge(hoge.id, hoge_data)
    print(hoge)
    print(delete_hoge(hoge.id))
