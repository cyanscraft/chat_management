from datetime import date, timedelta

from iris import ChatContext

from database.db import get_connection


def update_chat_count(chat: ChatContext):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                INSERT INTO user_state (user_id,sender, chat_count, exp, last_chat_at)
                VALUES (%s, %s, 1, 1, NOW()) ON DUPLICATE KEY
                UPDATE
                    chat_count = chat_count + 1,
                    exp = exp + 1,
                    last_chat_at = NOW()
                """, (chat.sender.id,chat.sender.name))

    conn.commit()
    cursor.close()
    conn.close()

def update_background_url(user_id, url):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("UPDATE user_state SET background_url=%s WHERE user_id=%s", (url, user_id))

    conn.commit()
    cursor.close()
    conn.close()

def update_about(user_id: str, message: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("UPDATE user_state SET about = %s WHERE user_id = %s", (message, user_id))
        conn.commit()
        success = cursor.rowcount > 0  # 실제로 영향을 받은 행이 있으면 성공
        return success

    except Exception as e:
        print("DB Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()

from database.db import get_connection
from datetime import date, timedelta

def handle_attendance(user_id: str, name: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    today = date.today()

    # 1) 사용자 조회
    cursor.execute("SELECT * FROM user_state WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    # 2) 신규 사용자 처리
    if not user:
        cursor.execute("""
            INSERT INTO user_state (
                user_id, sender, exp,
                stream_attend_count, total_attend_count,
                last_attend_date, last_attend_ts
            ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (user_id, name, 100, 1, 1, today))
        conn.commit()

        # 오늘 기준 ts 순 랭킹만 계산
        cursor.execute("""
            SELECT attend_rank, exp_rank
            FROM (
                SELECT
                  user_id,
                  RANK() OVER (ORDER BY last_attend_ts ASC)   AS attend_rank,
                  RANK() OVER (ORDER BY exp DESC)             AS exp_rank
                FROM user_state
                WHERE last_attend_date = CURDATE()
            ) ranked
            WHERE user_id = %s
        """, (user_id,))
        ranks = cursor.fetchone()
        print(ranks)
        cursor.close()
        conn.close()
        return {
            "success": True,
            "total_attend_count": 1,
            "stream_count": 1,
            "last_attend_date": today,
            "date": today,
            "attend_rank": ranks["attend_rank"],
            "exp_rank":    ranks["exp_rank"],
            "about":       "",
            "exp":         100,
            "chat_count":  0
        }

    # 3) 기존 사용자: 스트릭 계산
    total_attend_count = user["total_attend_count"]
    last_date   = user["last_attend_date"]
    stream_count = user.get("stream_attend_count", 0)

    if last_date is None:
        stream_count = 1
    elif last_date == today - timedelta(days=1):
        stream_count += 1
    elif last_date == today:
        # 이미 출석한 경우, 오늘 랭킹만 다시 조회
        cursor.execute("""
           SELECT
                    u.user_id,
                    attend_ranks.attend_rank,
                    exp_ranks.exp_rank
                FROM user_state u
                
                -- 경험치 랭크: 모든 유저에 대해 랭크
                JOIN (
                    SELECT user_id,
                           RANK() OVER (ORDER BY exp DESC) AS exp_rank
                    FROM user_state
                ) AS exp_ranks ON u.user_id = exp_ranks.user_id
                
                -- 출석 랭크: 오늘 출석한 유저만 랭크 계산 → 나머지는 NULL
                LEFT JOIN (
                    SELECT user_id,
                           RANK() OVER (ORDER BY last_attend_ts ASC) AS attend_rank
                    FROM user_state
                    WHERE last_attend_date = CURDATE()
                ) AS attend_ranks ON u.user_id = attend_ranks.user_id
                
                WHERE u.user_id = %s
        """, (user_id,))
        ranks = cursor.fetchone()
        print(user)
        print(ranks)
        print(user_id)
        cursor.close()
        conn.close()
        return {
            "success": False,
            "message": "오늘 이미 출석했습니다.",
            "total_attend_count": total_attend_count,
            "stream_count": stream_count,
            "last_attend_date": last_date,
            "date": today,
            "attend_rank": ranks["attend_rank"],
            "exp_rank":    ranks["exp_rank"]
        }
    else:
        stream_count = 1

    # 4) 출석 업데이트
    cursor.execute("""
        UPDATE user_state
        SET
          exp = exp + 100,
          stream_attend_count = %s,
          total_attend_count  = total_attend_count + 1,
          last_attend_date    = %s,
          last_attend_ts      = NOW()
        WHERE user_id = %s
    """, (stream_count, today, user_id))
    conn.commit()

    # 5) 오늘 기준 랭킹 재조회
    cursor.execute("""
        SELECT
                    u.user_id,
                    attend_ranks.attend_rank,
                    exp_ranks.exp_rank
                FROM user_state u
                
                -- 경험치 랭크: 모든 유저에 대해 랭크
                JOIN (
                    SELECT user_id,
                           RANK() OVER (ORDER BY exp DESC) AS exp_rank
                    FROM user_state
                ) AS exp_ranks ON u.user_id = exp_ranks.user_id
                
                -- 출석 랭크: 오늘 출석한 유저만 랭크 계산 → 나머지는 NULL
                LEFT JOIN (
                    SELECT user_id,
                           RANK() OVER (ORDER BY last_attend_ts ASC) AS attend_rank
                    FROM user_state
                    WHERE last_attend_date = CURDATE()
                ) AS attend_ranks ON u.user_id = attend_ranks.user_id
                
                WHERE u.user_id = %s
    """, (user_id,))
    ranks = cursor.fetchone()

    cursor.close()
    conn.close()
    return {
        "success": True,
        "total_attend_count": total_attend_count + 1,
        "stream_count": stream_count,
        "last_attend_date": today,
        "date": today,
        "attend_rank": ranks["attend_rank"],
        "exp_rank":    ranks["exp_rank"],
        "about":       user["about"] or "",
        "exp":         user["exp"] + 100,
        "chat_count":  user["chat_count"]
    }

def get_or_create(user_id: str, name: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_state WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            cursor.execute(
                "INSERT INTO user_state (user_id, sender, exp, chat_count, about)"
                " VALUES (%s, %s, %s, %s, %s)",
                (user_id, name, 1, 1, "")
            )
            conn.commit()

            cursor.execute("""
                SELECT
                    u.user_id,
                    attend_ranks.attend_rank,
                    exp_ranks.exp_rank
                FROM user_state u
                
                -- 경험치 랭크: 모든 유저에 대해 랭크
                JOIN (
                    SELECT user_id,
                           RANK() OVER (ORDER BY exp DESC) AS exp_rank
                    FROM user_state
                ) AS exp_ranks ON u.user_id = exp_ranks.user_id
                
                -- 출석 랭크: 오늘 출석한 유저만 랭크 계산 → 나머지는 NULL
                LEFT JOIN (
                    SELECT user_id,
                           RANK() OVER (ORDER BY last_attend_ts ASC) AS attend_rank
                    FROM user_state
                    WHERE last_attend_date = CURDATE()
                ) AS attend_ranks ON u.user_id = attend_ranks.user_id
                
                WHERE u.user_id = %s
            """, (user_id,))
            ranks = cursor.fetchone()

            result = {
                "username":name,
                "attend_rank": ranks.get("attend_rank"),
                "exp_rank": ranks.get("exp_rank"),
                "about": "",
                "exp": 1,
                "chat_count": 1,
                "background_url": None
            }

        else:
            cursor.execute("""
                SELECT
                u.user_id,
                attend_ranks.attend_rank,
                exp_ranks.exp_rank
            FROM user_state u
            
            -- 경험치 랭크: 모든 유저에 대해 랭크
            JOIN (
                SELECT user_id,
                       RANK() OVER (ORDER BY exp DESC) AS exp_rank
                FROM user_state
            ) AS exp_ranks ON u.user_id = exp_ranks.user_id
            
            -- 출석 랭크: 오늘 출석한 유저만 랭크 계산 → 나머지는 NULL
            LEFT JOIN (
                SELECT user_id,
                       RANK() OVER (ORDER BY last_attend_ts ASC) AS attend_rank
                FROM user_state
                WHERE last_attend_date = CURDATE()
            ) AS attend_ranks ON u.user_id = attend_ranks.user_id
            
            WHERE u.user_id = %s
            """, (user_id,))
            ranks = cursor.fetchone() or {}

            result = {
                "username": name,
                "attend_rank": ranks.get("attend_rank"),
                "exp_rank": ranks.get("exp_rank"),
                "about": user["about"] or "",
                "exp": user["exp"],
                "chat_count": user["chat_count"],
                "background_url": user["background_url"]
            }

        return result

    finally:
        cursor.close()
        conn.close()
