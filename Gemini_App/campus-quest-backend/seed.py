from app.db.database import Base, SessionLocal, engine
from app.db import models


QUESTS = [
    {
        "title": "Gólyahét Megnyitó",
        "description": "Látogass el a megnyitóra és olvasd be a projektor kódját!",
        "type": models.QuestType.QR_EVENT,
        "xp_reward": 150,
        "coin_reward": 30,
        "qr_secret_token": "GOLYAHET_MEGNYITO_2026",
        "expires_at": None,
    },
    {
        "title": "Fedezd fel a könyvtárat",
        "description": "Látogass el az egyetemi könyvtárba, és olvasd be a kihelyezett QR-kódot!",
        "type": models.QuestType.QR_EVENT,
        "xp_reward": 50,
        "coin_reward": 10,
        "qr_secret_token": "KONYVTAR_FELFEDEZES_2026_001",
        "expires_at": None,
    },
    {
        "title": "Látogass el egy kari standhoz",
        "description": "Keresd fel a kari standot, és olvasd be az ott kihelyezett QR-kódot!",
        "type": models.QuestType.QR_EVENT,
        "xp_reward": 75,
        "coin_reward": 15,
        "qr_secret_token": "KARI_STAND_2026_001",
        "expires_at": None,
    },
    {
        "title": "Találd meg a közösségi teret",
        "description": "Látogass el a campus egyik közösségi terébe, és olvasd be a QR-kódot!",
        "type": models.QuestType.QR_EVENT,
        "xp_reward": 50,
        "coin_reward": 10,
        "qr_secret_token": "KOZOSSEGI_TER_2026_001",
        "expires_at": None,
    },
    {
        "title": "Vegyél részt egy egyetemi eseményen",
        "description": "Vegyél részt egy egyetemi eseményen, és olvasd be a helyszínen kihelyezett QR-kódot!",
        "type": models.QuestType.QR_EVENT,
        "xp_reward": 100,
        "coin_reward": 20,
        "qr_secret_token": "EGYETEMI_ESEMENY_2026_001",
        "expires_at": None,
    },
    {
        "title": "Gólyahét állomás",
        "description": "Teljesíts egy gólyahéti állomást, és olvasd be az ott kihelyezett QR-kódot!",
        "type": models.QuestType.QR_EVENT,
        "xp_reward": 150,
        "coin_reward": 30,
        "qr_secret_token": "GOLYAHET_ALLOMAS_2026_001",
        "expires_at": None,
    },
]


def seed_data():
    tokens = [quest["qr_secret_token"] for quest in QUESTS]
    if any(not token for token in tokens) or len(tokens) != len(set(tokens)):
        raise ValueError("Minden seedelt questhez egyedi, nem üres QR token szükséges.")
    if any(quest["type"] != models.QuestType.QR_EVENT for quest in QUESTS):
        raise ValueError("A seeder jelenleg csak QR_EVENT questeket támogat.")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        added = 0
        for quest_data in QUESTS:
            exists = db.query(models.Quest.id).filter(
                models.Quest.qr_secret_token == quest_data["qr_secret_token"]
            ).first()
            if exists:
                continue

            db.add(models.Quest(**quest_data))
            added += 1

        db.commit()
        print(f"Quest seed kész. Új questek száma: {added}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
