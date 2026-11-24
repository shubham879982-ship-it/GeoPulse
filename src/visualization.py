from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

def save_charts(store_summary_file: Path, hourly_summary_file: Path,
                stores_file: Path, visits_file: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    stores = pd.read_csv(stores_file)
    visits = pd.read_csv(visits_file)
    store_summary = pd.read_csv(store_summary_file)
    hourly = pd.read_csv(hourly_summary_file)

    if not store_summary.empty:
        plt.figure(figsize=(9, 5))
        plt.bar(store_summary["store_name"], store_summary["nearby_visits"])
        plt.title("Nearby Visits by Retail Store")
        plt.xlabel("Store")
        plt.ylabel("Nearby visit records")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(output_dir / "visits_by_store.png", dpi=160)
        plt.close()

    if not hourly.empty:
        plt.figure(figsize=(8, 4))
        plt.plot(hourly["hour"], hourly["nearby_visits"], marker="o")
        plt.title("Nearby Visits by Hour")
        plt.xlabel("Hour of day")
        plt.ylabel("Nearby visit records")
        plt.xticks(range(0, 24, 2))
        plt.grid(True, alpha=0.25)
        plt.tight_layout()
        plt.savefig(output_dir / "hourly_visits.png", dpi=160)
        plt.close()

    plt.figure(figsize=(8, 7))
    plt.scatter(visits["longitude"], visits["latitude"], label="Activity points", alpha=0.65)
    plt.scatter(stores["longitude"], stores["latitude"], marker="^", s=100, label="Retail stores")
    for _, row in stores.iterrows():
        plt.annotate(row["store_name"], (row["longitude"], row["latitude"]),
                     xytext=(5, 5), textcoords="offset points", fontsize=8)
    plt.title("GeoPulse: Sample Retail and Activity Locations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "store_map.png", dpi=160)
    plt.close()
