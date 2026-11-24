# GeoPulse
### Hyper-local Retail Mobility Analytics using Apache Spark and Apache Sedona

GeoPulse is an educational geospatial analytics project. It uses **PySpark** to process retail visit records and **Apache Sedona** to perform spatial distance analysis between customer activity points and retail stores. It produces CSV summaries and visual charts.

> **Dataset notice:** The included dataset is synthetic sample data created for demonstration. It does not represent real customers, businesses, or movement traces.

## Features
- Load retail store and visit CSV files with PySpark.
- Create spatial points from longitude/latitude using Apache Sedona.
- Identify visits occurring within a configurable radius of each store.
- Summarize nearby visits by store and by hour.
- Export analytical results and generate charts.
- Include basic data validation tests.

## Technology stack
- Python 3.10 or 3.11
- Java 17
- Apache Spark / PySpark 3.5.x
- Apache Sedona 1.9.1
- Pandas and Matplotlib

## Project structure
```text
GeoPulse/
├── data/                  # Synthetic demonstration CSV files
├── docs/                  # Project documentation
├── outputs/               # Generated CSV files and charts
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_validation.py
│   ├── analytics.py
│   └── visualization.py
├── tests/
│   └── test_data_validation.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup (Windows)
1. Install **Python 3.10/3.11** and **Java 17**.
2. Check Java from Command Prompt:
   ```bash
   java -version
   ```
3. Open the project folder in VS Code.
4. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
5. Install packages:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Run
From the GeoPulse project folder:
```bash
python main.py
```

The first run may download Spark/Sedona JVM dependencies from Maven Central. An internet connection is required for this step. The Sedona Spark JAR and GeoTools wrapper coordinates are configured in `src/config.py`.

Generated files are saved in `outputs/`:
- `nearby_visits.csv`
- `store_summary.csv`
- `hourly_summary.csv`
- `visits_by_store.png`
- `hourly_visits.png`
- `store_map.png`

## Configure the analysis
Change `RADIUS_METERS` in `src/config.py` to use another proximity radius. The default is 500 metres.

## Important limitations
- The sample dataset is synthetic and small; it is for a classroom prototype, not production retail decision-making.
- The current model uses straight-line geographic distance, not road-network travel time.
- A visit is associated with every store within the selected radius; a visit can therefore be counted for more than one store.
- No personal identifiers are included in the sample data.

## Testing
```bash
python -m unittest discover -s tests -v
```

## Suggested demonstration
1. Explain the problem: retailers need to understand local movement and nearby activity.
2. Show the store and visit sample CSV files.
3. Run `python main.py`.
4. Explain the Sedona point creation and spatial distance filter.
5. Open the generated charts and CSV summaries.
6. Change the radius and rerun to demonstrate how results change.

## References
- Apache Spark documentation: https://spark.apache.org/docs/3.5.6/
- Apache Sedona documentation: https://sedona.apache.org/latest/
- Apache Sedona Python installation: https://sedona.apache.org/latest/setup/install-python/

Improve retail sales analytics module
