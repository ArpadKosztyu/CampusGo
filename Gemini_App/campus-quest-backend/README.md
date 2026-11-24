# CampusQuest Backend (MVP)

Egyetemi gamifikációs platform MVP törzse, amely lehetővé teszi a hallgatók számára, hogy valós és online egyetemi feladatok (QR kódok, kérdőívek) teljesítésével XP-t és egyetemi érméket gyűjtsenek, szintet lépjenek és jutalmakat oldjanak fel.

## Fő technológiák
- **FastAPI** (Python 3.10+)
- **SQLAlchemy** (ORM)
- **SQLite** (helyi fejlesztéshez) / **PostgreSQL** (élesítéshez)
- **JWT (JSON Web Tokens)** + Passlib (bcrypt) a biztonságos hitelesítéshez

---

## Gyors indítás helyi környezetben

### 1. Virtuális környezet és függőségek

Az alábbi lépések a teljes CampusGo projektet feltételezik: a `Gemini_App` mappában található a `frontend.py`, a `requirements.txt` és a `campus-quest-backend` almappa. A parancsokat a `campus-quest-backend` mappából futtasd.

```bash
python -m venv venv

# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Backend csomagok telepítése (ebből a mappából):
python -m pip install -r requirements.txt

# Frontend csomagok telepítése (Gemini_App mappából, ugyanebben a környezetben):
python -m pip install -r ..\requirements.txt
```

A függőségeket tartalmazó fájlok a `campus-quest-backend/requirements.txt` (backend) és a `Gemini_App/requirements.txt` (frontend). A virtuális környezetet mindkét terminálban aktiváld.

Backend indítása a `campus-quest-backend` mappából:

```bash
python -m uvicorn main:app --reload
```

Frontend indítása egy másik terminálban, a `Gemini_App` mappából:

```bash
python -m streamlit run frontend.py
```

## Questek tárolása

A questek nem a frontend kódjában vagy külön JSON-fájlban vannak, hanem SQLAlchemy `Quest` modellként az adatbázis `quests` táblájában. Alapértelmezésben a `DATABASE_URL` értéke `sqlite:///./campus.db`, ezért a backend mappájából indítva a fájl `campus-quest-backend/campus.db`; a `.env`-ben megadott URL másik adatbázist is kijelölhet.

A tábla mezői:

| Mező | Típus | Jelentés |
|---|---|---|
| `id` | szöveg, UUID | Elsődleges kulcs |
| `title` | szöveg | Quest címe |
| `description` | szöveg | Leírás |
| `type` | enum | `QR_EVENT`, `SURVEY` vagy `TEXT_INPUT` |
| `xp_reward` | egész | Jóváírandó XP |
| `coin_reward` | egész | Jóváírandó coin |
| `qr_secret_token` | szöveg, egyedi, lehet üres | A QR-kód tartalma; beváltáskor ehhez keres a backend |
| `expires_at` | dátum/idő, lehet üres | Lejárati idő |

A teljesítés külön, `user_quests` táblában tárolódik: `id`, `user_id`, `quest_id`, `completed_at`; a felhasználó–quest pár egyedi, így ugyanaz a felhasználó nem válthatja be ugyanazt a questet kétszer. A frontend a `GET /api/quests/` végpontból kapja az elérhető questek címét, leírását, típusát, jutalmát és lejáratát. Jelenleg a QR-beváltás van végigvezetve; a `SURVEY` és `TEXT_INPUT` értékekhez még nincs teljesítési API vagy frontend folyamat.

## Új QR quest hozzáadása

A backend mappájából szerkeszd a `seed.py` fájl `QUESTS` listáját, és vegyél fel egy új elemet. Minden questhez adj új, korábban nem használt QR tokent:

```python
{
    "title": "Kari stand felkeresése",
    "description": "Látogass el a kari standhoz, és olvasd be az ott kihelyezett QR-kódot!",
    "type": models.QuestType.QR_EVENT,
    "xp_reward": 100,
    "coin_reward": 20,
    "qr_secret_token": "KARI_STAND_2026_001",
    "expires_at": None,
},
```

A seed alapból tartalmazza a Gólyahét Megnyitót, a könyvtár felfedezését, a kari stand meglátogatását, a közösségi tér megtalálását, egy egyetemi eseményt és egy gólyahéti állomást. A `Gólyahét állomás` jelenleg egyetlen QR-es quest; többállomásos lánc külön questek felvételével valósítható meg.

A `QUESTS` lista ismételt futtatása biztonságos: a seeder token alapján kihagyja a már létező questeket, és csak újakat ad hozzá. Ugyanazon token új leírással vagy jutalommal nem frissíti a meglévő rekordot; ilyen módosításhoz használj új tokent, vagy módosítsd külön a meglévő adatbázisrekordot. A seeder ellenőrzi a tokenek ürességét és duplikáltságát, adatbázis-hiba esetén pedig visszagörgeti a tranzakciót és továbbadja a hibát.

A mezők kitöltése után, a backend mappájából futtasd:

```bash
python seed.py
```

Ha a fejlesztői mock QR-t is ehhez a questhez szeretnéd igazítani, állítsd át a `create_mock_qr.py` `qr_content` értékét ugyanarra a tokenre, majd futtasd:

```bash
python create_mock_qr.py
```

A jelenlegi mock QR a seedelt `GOLYAHET_MEGNYITO_2026` tokenhez tartozik. A `SURVEY` és `TEXT_INPUT` típus jelenleg nem seedelhető ezzel a szkripttel, mert még hiányzik a hozzájuk tartozó teljesítési folyamat.
