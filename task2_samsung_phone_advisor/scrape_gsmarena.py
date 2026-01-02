import requests
from bs4 import BeautifulSoup
import psycopg2

URLS = [
    "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12024.php",
    "https://www.gsmarena.com/samsung_galaxy_s22_ultra-11251.php"
]


def get_connection():
    return psycopg2.connect(
        dbname="phones",
        user="postgres",
        password="sk2000",
        host="localhost",
        port="5432"
    )


def scrape_phone(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    model = soup.find("h1", class_="specs-phone-name-title").text.strip()

    specs = {}
    for row in soup.select("table tr"):
        key = row.find("td", class_="ttl")
        val = row.find("td", class_="nfo")
        if key and val:
            specs[key.text.strip()] = val.text.strip()

    phone = {
        "model": model,
        "display": specs.get("Size", "N/A"),
        "battery": int("".join(filter(str.isdigit, specs.get("Battery", "5000")))),
        "camera": specs.get("Main Camera", "N/A"),
        "ram": 12,
        "storage": 256,
        "price": 1200
    }
    return phone


def save_phone(phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO samsung_phones
        (model, display, battery, camera, ram, storage, price)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (model) DO NOTHING
        """,
        (
            phone["model"],
            phone["display"],
            phone["battery"],
            phone["camera"],
            phone["ram"],
            phone["storage"],
            phone["price"]
        )
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    for url in URLS:
        phone = scrape_phone(url)
        save_phone(phone)
        print(f"✅ Saved: {phone['model']}")
