from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

STORES_FILE = DATA_DIR / "stores.csv"
VISITS_FILE = DATA_DIR / "visits.csv"

# Change this value to test a different hyper-local catchment radius.
RADIUS_METERS = 500

APP_NAME = "GeoPulse Retail Mobility Analytics"

# These coordinates are for Spark 3.5 / Scala 2.12 with Sedona 1.9.1.
SEDONA_PACKAGES = (
    "org.apache.sedona:sedona-spark-3.5_2.12:1.9.1,"
    "org.datasyslab:geotools-wrapper:1.9.1-33.5"
)
