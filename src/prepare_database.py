
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "retail_sales.db"

DATABASE_URL = (
    "https://github.com/Harsh4W/"
    "Retail-Sales-Analytics-API/releases/download/"
    "v1.0-data/retail_sales_db.zip"
)


def prepare_database():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists() and DB_PATH.stat().st_size > 0:
        print("Database already exists.")
        return

    print("Downloading database from GitHub Release...")

    with urlopen(DATABASE_URL, timeout=180) as response:
        zip_data = response.read()

    print("Download completed.")

    with ZipFile(BytesIO(zip_data)) as archive:

        if "retail_sales.db" not in archive.namelist():
            raise FileNotFoundError(
                "Database file not found inside ZIP."
            )

        archive.extract("retail_sales.db", DATA_DIR)

    if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
        raise RuntimeError("Database extraction failed.")

    print("Database downloaded and extracted successfully.")
    print("Database location:", DB_PATH)


if __name__ == "__main__":
    prepare_database()

