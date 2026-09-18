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
def create_game(
        db:Session,
        content: dict
):
    sql = text(
        """
        INSERT INTO Games(theme_id)VALUES(:theme_id)
        """
    )
    params= {
        "theme_id":content.get("theme_id")
    }
    print(f"SQL:{sql}\nparams: {params}")
    result = db.execute(sql, params)
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
        INSERT INTO Players(name, game_id)
        VALUES(:name, :game_id)
        """
    )
    params = {
        "name": content.get("name"),
        "game_id": content.get("game_id")
    }

    print(f"SQL: {sql}\nPrams: {params}")
    result = db.execute(sql, params)
    db.commit()
    new_player_id = result.lastrowid

    if new_player_id is None:
        raise ValueError("Playerの作成に失敗しました")

    new_player = get_name(db, player_id=new_player_id)
    print(f"DB操作の結果: {new_player}")

    return new_player


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

# Player.id, name, assigned_topic_idを表示
def get_player_topic_by_game(
        db:Session,
        game_id: int
):
    sql = text(
        """
        SELECT id, name, assigned_topic_id from Players
        WHERE game_id = :game_id
        """
    )
    params = {"game_id": game_id}

    print(f"SQL: {sql}\n Params: {params}")
    result = db.execute(sql, params).mappings().all()

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

def assign_groups_and_save(
        db, game_id):
    # game_idに紐づくプレイヤーの取得
    sql = text(
        """
        SELECT id, name from Players
        WHERE game_id = :game_id
        """
    )
    params = {"game_id": game_id}
    print(f"SQL: {sql}\nParams: {params}")
    players =db.execute(sql, params).mappings().all()
    player_names = [p["name"] for p in players]
    player_id = {p["name"]: p["id"] for p in players}

    # game_idに紐づくtheme_idの取得
    sql_theme = text(
        """
        SELECT theme_id from Games WHERE id = :game_id
        """
    )
    params_theme = {"game_id": game_id}
    print(f"SQL: {sql_theme}\nParams: {params_theme}")
    theme_id_row = db.execute(sql_theme, params_theme).mappings().first()
    theme_id = theme_id_row["theme_id"]

    # テーマのトピックのペアを取得
    sql_pair = text(
        """
        SELECT topic1_id, topic2_id from Topic_pairs
        WHERE theme_id = :theme_id
        """
    )
    params_pair = {"theme_id": theme_id}
    print(f"SQL: {sql_pair}\nParams: {params_pair}")
    pair = db.execute(sql_pair, params_pair).mappings().first()
    topic1_id = pair["topic1_id"]
    topic2_id = pair["topic2_id"]


    # 割り振りパターンを決めて上記の関数を呼び出す
    pattern = ["A", "A", "B"]
    assignment = assign_groups(player_names, pattern)

    # "A"/"B"を実際のTopics.idに変換
    topic_id = {
        "A": topic1_id,
        "B": topic2_id
    }

    # 結果をDBに保存
    for name, label in assignment.items():
        sql_db = text(
            """
            UPDATE Players SET assigned_topic_id = :assigned_topic_id WHERE id = :player_id
            """
        )
        params_db = {"assigned_topic_id": topic_id[label], "player_id": player_id[name]}
        print(f"SQL; {sql_db}\nParams: {params_db}")
        db.execute(sql_db, params_db)
    db.commit()
    result = get_player_topic_by_game(db, game_id=game_id)

    return result

# playerのtopicの表示
def get_player_topic(
        db:Session,
        player_id:int
):
    sql = text(
        """
        SELECT Topics.topic_text FROM Players
        INNER JOIN Topics ON Players.assigned_topic_id = Topics.id
        WHERE Players.id = :player_id
        """
    )
    params = {"player_id": player_id}
    print(f"SQL: {sql}\nParams: {params}")
    result = db.execute(sql, params).mappings().first()
    
    print(f"DB操作の結果: {result}")
    
    return result


        # SELECT Topics.topic_text FROM Topics
        # INNER JOIN (SELECT assigned_topic_id FROM Players WHERE id = :player_id) as selected_player
        # ON Topics.id = selected_player.assigned_topic_id