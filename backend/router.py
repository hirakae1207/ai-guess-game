from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import crud

router = APIRouter()

# DBをpythonで扱えるようにする
DB_URL = f"mysql+pymysql://root:db1207@db:3306/ai_guess_game?charset=utf8"

db_engine = create_engine(DB_URL, echo=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


Base = declarative_base()

def get_db():
    with db_session() as session:
        yield session

# テーマの表示
@router.get("/theme")
def get_all_theme(
    db: Session = Depends(get_db),
):
    return crud.get_all_themes(db)

#playerのnameの追加
@router.post("/player")
def create_name(
    content:dict = Body(),
    db:Session = Depends(get_db)
):
    print("受けたデータ\n", content)
    result = crud.create_name(db, content)

    print("返すデータ\n", result)
    return result

# playerのnameの表示
@router.get("/player/{player_id}")
def get_name(
    player_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_name(db, player_id=player_id)

    if result is None:
        raise HTTPException(status_code=404, detail="player not found")
    return result