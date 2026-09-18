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

# ラウンド追加
@router.post("/game")
def create_game(
    content:dict = Body(),
    db:Session = Depends(get_db)
):
    result = crud.create_game(db, content)

    print("返すデータ\n", result)
    return result


# ラウンド取得
@router.get("/game/{game_id}")
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    result = crud.get_game(db, game_id= game_id)

    if result is None:
        raise HTTPException(status_code=404, detail="game not found")
    return result

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


@router.get("/player/topic_id/{game_id}")
def get_player_topic_by_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_player_topic_by_game(db, game_id=game_id)

    if result is None:
        raise HTTPException(status_code=404, detail="topic_id not found")
    return result

# playerをお題へ割り振り
@router.post("/assignment")
def assign_groups_and_save(
    game_id:int,
    db:Session = Depends(get_db)
):
    result = crud.assign_groups_and_save(db, game_id)
    return result

# playerのtopicの表示
@router.get("/player/topic/{player_id}")
def get_player_topic(
    player_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_player_topic(db, player_id=player_id)

    if result is None:
        raise HTTPException(satus_code=404, detail="topic not found")
    return result

# keywordの追加
@router.post("/player/keyword")
def create_keyword(
    player_id: int,
    content: dict,
    db: Session = Depends(get_db)
):
    result = crud.create_keyword(db, content, player_id=player_id)

    return result

# keywordの表示（create_keyword)
@router.get("/player/keyword/{player_id}")
def get_keyword(
    player_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_keyword(db, player_id=player_id)

    if result is None:
        raise HTTPException(status_code=404, detail = "keyword not found")

    return result

# topicごとのkeywordの一覧表示
@router.get("/keyword/{topic_id}")
def get_keyword_by_topic(
    topic_id: int,
    game_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_keyword_by_topic(db, topic_id=topic_id, game_id=game_id)

    if result is None:
        raise HTTPException(status_code=404, detail = "keywords not found")

    return result