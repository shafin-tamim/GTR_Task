import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="phones",
        user="postgres",
        password="sk2000",
        host="localhost",
        port="5432"
    )


def fetch_phone_by_model(model):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT model, display, battery, camera, ram, storage, price
        FROM samsung_phones
        WHERE model ILIKE %s
        """,
        (f"%{model}%",)
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "model": row[0],
        "display": row[1],
        "battery": row[2],
        "camera": row[3],
        "ram": row[4],
        "storage": row[5],
        "price": row[6]
    }


def best_battery_under_price(max_price):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT model, battery
        FROM samsung_phones
        WHERE price <= %s
        ORDER BY battery DESC
        LIMIT 1
        """,
        (max_price,)
    )

    row = cur.fetchone()
    conn.close()
    return row
