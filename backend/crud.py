from sqlalchemy import text
from sqlalchemy.orm import Session

# Themesの表示
def get_all_themes(
        db: Session
):
    sql = text(
        """
        SELECT theme FROM Themes
        """
    )
    print(f"SQL:{sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

# Playersのnameの追加
def create_name(
        db:Session,
        content: dict
):
    sql = text(
        """
        INSERT INTO Players(name)
        VALUES(:name)
        """
    )
    params = {
        "name": content.get("name")
    }

    print(f"SQL: {sql}\nPrams: {params}")
    result = db.execute(sql, params)
    db.commit()
    new_player_id = result.lastrowid

    if new_player_id is None:
        raise ValueError("Playerの作成に失敗しました")

    new_player = get_name(db, player_id=new_player_id)
    print(f"DB操作の結果: {new_player}")


def get_name(
        db:Session,
        player_id: int
):
    sql = text(
        """
        SELECT name FROM Players
        WHERE id = :id
        """
    )
    params = {"id": player_id}

    print(f"SQL: {sql}\nParams: {params}")
    result = db.execute(sql, params).first()

    if result is not None:
        result = result._asdict()

    print(f"DB操作の結果: {result}")

    return result