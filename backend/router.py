from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from google import genai
import os

import json
from pydantic import BaseModel
from google.genai import types

import re

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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

# game_idのthemeの表示
@router.get("/game/theme")
def get_theme_by_game_id(
    game_id: int,
    db:Session = Depends(get_db)
):
    result = crud.get_theme_by_game_id(db, game_id=game_id)

    
    return result

# game_idのtopic_textの表示
@router.get("/game/topic")
def get_topic_by_game_id(
    game_id: int,
    db:Session = Depends(get_db)
):
    result = crud.get_topic_by_game_id(db, game_id=game_id)


    return result

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

# assigned_topic, game_idからチーム分けの表示
@router.get("/team/{game_id}")
def get_team(
    game_id:int,
    db:Session = Depends(get_db)
):
    result = crud.get_team(db, game_id = game_id)
    return result

# playerのtopicの表示
@router.get("/player/topic/{player_id}")
def get_player_topic(
    player_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_player_topic(db, player_id=player_id)

    if result is None:
        raise HTTPException(status_code=404, detail="topic not found")
    return result

# keywordの追加
@router.post("/player/keyword")
def create_keyword(
    player_id: int,
    content: dict,
    db: Session = Depends(get_db)
):
    try:
        result = crud.create_keyword(db, content, player_id=player_id)
    except crud.NgWordError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

# keywordの表示(sendAI)
@router.get("/keyword/player/{game_id}")
def get_keyword_by_game_id(
    game_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_keyword_by_game_id(db, game_id=game_id)

    if result is None:
        raise HTTPException(satus_code=404, detail="keywords not found")

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


# jsonでもらうために追加
class JudgeResult(BaseModel):
    answer: int      # 0 か 1
    message: str     # 100字以内の文章


#AIの判定に使う
@router.post("/judge")
def AI_judge(
    game_id: int,
    db: Session = Depends(get_db)
):
    theme_result = crud.get_theme_by_game_id(db, game_id)
    topic_result = crud.get_topic_by_game_id(db, game_id)
    keyword_result = crud.get_keyword_by_game_id(db, game_id)

    theme = theme_result["theme"]
    topics = [top["topic_text"] for top in topic_result]
    keywords = [key["keyword"] for key in keyword_result]

    options = [
    {"answer": 0, "team": "A", "topic": topics[0]},
    {"answer": 1, "team": "B", "topic": topics[1]},
]
    options_json = json.dumps(options, ensure_ascii=False, indent=2)

    prompt = (
        f"あなたはマジカルバナナに似たゲームに参加しています。"
        f"あなたのほかに3人の人間がいます。"
        f"テーマは「{theme}」です。"
        f"次の選択肢のうち、4人のキーワードから連想しやすいものを1つだけ選んでください。\n"
        f"選択肢(JSON):\n{options_json}\n"
        f"4人のキーワード: {'、'.join(f'「{k}」' for k in keywords)}\n"
        f"出力のanswerには、選んだ選択肢のanswerの値(0か1)をそのまま入れてください。"
        f"messageには、answerに従って選んだチームとお題、その理由を述べる文章のみを入れてください。"
        f"messageの制限: 100字以内、10歳から15歳ぐらいの話し方、マークダウン不使用。"
        f"これらの制限には言及しないでください。確認の文章も不要です。"
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JudgeResult,
        ),
    )

    result = json.loads(response.text)
    answer_index =result["answer"]
    message = result["message"]

    return {
        "response": message,
        "answer": answer_index,
        "winner_topic": topics[answer_index],
    }
