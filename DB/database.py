import sqlite3
from contextlib import closing

DB_NAME = "parking.db"


def init_db() -> None:
    """
    Создаём (при первом запуске) таблицу parking со столбцами:
    spot  – номер парковочного места (PRIMARY KEY),
    occupied – занято / свободно (BOOLEAN).
    """
    with sqlite3.connect(DB_NAME) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS parking (
                spot     INTEGER PRIMARY KEY,
                occupied BOOLEAN NOT NULL
            )
            """
        )
        conn.commit()


def get_all_parking() -> dict[int, bool]:
    """Возвращает текущую ситуацию в виде словаря:
    {номер_места: True/False}"""
    with sqlite3.connect(DB_NAME) as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT spot, occupied FROM parking")
        rows = cur.fetchall()
    return {spot: bool(occ) for spot, occ in rows}


def set_parking_status(spot: int, occupied: bool) -> None:
    """
    Обновляет статус выбранного места.
    Если места ещё нет в таблице — добавляет его.
    """
    with sqlite3.connect(DB_NAME) as conn, closing(conn.cursor()) as cur:
        # Вставляем запись, если её нет
        cur.execute(
            "INSERT OR IGNORE INTO parking (spot, occupied) VALUES (?, ?)",
            (spot, occupied),
        )
        # Обновляем статус
        cur.execute(
            "UPDATE parking SET occupied = ? WHERE spot = ?",
            (occupied, spot),
        )
        conn.commit()


# --- пример использования ---
if __name__ == "__main__":
    init_db()

    # зададим начальные данные
    for n in range(1, 6):
        set_parking_status(n, False)

    print("До обновления:", get_all_parking())  # {1: False, 2: False, …}

    set_parking_status(3, True)  # заняли место №3
    set_parking_status(5, True)  # заняли место №5

    print("После обновления:", get_all_parking())  # {1: False, 2: False, 3: True, …}
