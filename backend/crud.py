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