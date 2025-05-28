from database.db import get_connection
from datetime import datetime

def give_badge(user_id: str, badge_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 이미 뱃지를 갖고 있는지 확인
        cursor.execute("""
            SELECT 1 FROM user_badge WHERE user_id = %s AND badge_id = %s
        """, (user_id, badge_id))
        if cursor.fetchone():
            return {
                "success": False,
                "message": "이미 해당 뱃지를 보유하고 있습니다."
            }

        # 새 뱃지 지급
        cursor.execute("""
            INSERT INTO user_badge (user_id, badge_id)
            VALUES (%s, %s)
        """, (user_id, badge_id))
        conn.commit()


        return {
            "success": True,
            "message": "뱃지를 성공적으로 지급했습니다.",
            "badge_id": badge_id,
            "user_id": user_id,
            "acquired_at": datetime.now()
        }

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": f"오류 발생: {str(e)}"
        }
    finally:
        cursor.close()
        conn.close()

def get_badges(user_id: str) -> list[int]:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT badge_id FROM user_badge
            WHERE user_id = %s
            ORDER BY badge_id ASC
        """, (user_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        cursor.close()
        conn.close()
