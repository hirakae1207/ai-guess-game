from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import crud

router = APIRouter()

# DBをpythonで扱えるようにする
DB_URL = "mysql+pymysql://root@db:3306/db?charset=utf8"

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