from db import get_connection

# ================================
# Environment / Alert 저장
# ================================
def save_environment(data):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO environment_data (temperature, humidity)
            VALUES (%s, %s)
        """, (data["temperature"], data["humidity"]))
        db.commit()
        print("[DB] Environment data saved.")
    except Exception as e:
        db.rollback()
        print("[DB ERROR] env save failed:", e)
    finally:
        cursor.close()
        db.close()

def save_alert(data):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO alert_events (event_type, level, value, location, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["event_type"],
            data["level"],
            data["value"],
            data["location"],
            data["message"]
        ))
        db.commit()
        print("[DB] Alert event saved.")
    except Exception as e:
        db.rollback()
        print("[DB ERROR] alert save failed:", e)
    finally:
        cursor.close()
        db.close()

# ================================
# Admin / Access DB Functions
# ================================
def get_admin_by_id(admin_id: str):
    """
    admin_id(RFID)로 관리자 레코드 조회
    id(PK)와 access_points를 반환
    """
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, access_points 
            FROM admins 
            WHERE admin_id = %s
        """, (admin_id,))
        row = cursor.fetchone()
        return row
    finally:
        cursor.close()
        db.close()

def log_access_result(admin_id: str, access_point: str, result: str):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO access_logs (admin_id, access_point, result)
            VALUES (%s, %s, %s)
        """, (admin_id, access_point, result))
        db.commit()
        print(f"[DB] Access log saved: {admin_id} -> {access_point} ({result})")
    except Exception as e:
        db.rollback()
        print("[DB ERROR] access log save failed:", e)
    finally:
        cursor.close()
        db.close()

