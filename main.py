from src.config import STORES_FILE, VISITS_FILE, OUTPUT_DIR
from src.data_validation import validate_inputs
from src.analytics import create_sedona_session, run_spatial_analysis
from src.visualization import save_charts

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    validate_inputs(STORES_FILE, VISITS_FILE)

    spark = create_sedona_session()
    try:
        nearby, store_summary, hourly_summary, _, _ = run_spatial_analysis(
            spark, STORES_FILE, VISITS_FILE
        )

        nearby_count = nearby.count()
        print(f"GeoPulse analysis completed. Nearby visit-store matches: {nearby_count}")

        nearby.coalesce(1).write.mode("overwrite").option("header", True).csv(
            str(OUTPUT_DIR / "nearby_visits")
        )
        store_summary.coalesce(1).write.mode("overwrite").option("header", True).csv(
            str(OUTPUT_DIR / "store_summary")
        )
        hourly_summary.coalesce(1).write.mode("overwrite").option("header", True).csv(
            str(OUTPUT_DIR / "hourly_summary")
        )

        # Spark writes CSV output as folders containing part files.
        # Copy a convenient single CSV file from each output folder for users.
        import shutil
        for folder_name, final_name in [
            ("nearby_visits", "nearby_visits.csv"),
            ("store_summary", "store_summary.csv"),
            ("hourly_summary", "hourly_summary.csv"),
        ]:
            folder = OUTPUT_DIR / folder_name
            part_files = list(folder.glob("part-*.csv"))
            if part_files:
                shutil.copy2(part_files[0], OUTPUT_DIR / final_name)

        save_charts(
            OUTPUT_DIR / "store_summary.csv",
            OUTPUT_DIR / "hourly_summary.csv",
            STORES_FILE,
            VISITS_FILE,
            OUTPUT_DIR,
        )
        print(f"Results saved in: {OUTPUT_DIR}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
