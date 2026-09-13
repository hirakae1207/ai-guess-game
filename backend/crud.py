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

#ラウンド追加
def create_game(db):
    result = db.execute(text("INSERT INTO Games () VALUES ()"))
    db.commit()
    new_game_id = result.lastrowid
    return new_game_id

#ラウンド取得
def get_game(
        db:Session,
        game_id: int
):
    sql = text(
        """
        SELECT id FROM Games
        WHERE id = :id
        """
    )
    params = {"id": game_id}

    print(f"SQL: {sql}\nParams: {params}")
    result = db.execute(sql, params).first()

    if result is not None:
        result = result._asdict()

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


#playerのnameを１人分だけ表示
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


# playerをお題へ割り振り
import random

def assign_groups(player_name, pattern):
    """
    player_name: プレイヤー名のリスト
    pattern: 人数に応じたグループの構成 例:['A', 'A', 'B']
    """
    labels = pattern.copy()
    random.shuffle(labels)

    assignment = {}
    for name, label in zip(player_name, labels):
        assignment[name] = label

    return assignment

def assign_groups_and_save(db):
    # DBからプレイヤー名の一覧を取得する
    players = db.execute(text("SELECT id, name FROM Players ORDER BY id DESC LIMIT 3")).mappings().all()
