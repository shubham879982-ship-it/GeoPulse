from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, to_timestamp, hour, count, round as spark_round
from sedona.spark import SedonaContext

from .config import APP_NAME, SEDONA_PACKAGES, RADIUS_METERS

def create_sedona_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .master("local[*]")
        .config("spark.jars.packages", SEDONA_PACKAGES)
        .config("spark.sql.extensions", "org.apache.sedona.sql.SedonaSqlExtensions")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.kryo.registrator", "org.apache.sedona.core.serde.SedonaKryoRegistrator")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    SedonaContext.create(spark)
    return spark

def run_spatial_analysis(spark: SparkSession, stores_file: Path, visits_file: Path):
    stores = (
        spark.read.option("header", True).option("inferSchema", True).csv(str(stores_file))
        .withColumn("latitude", col("latitude").cast("double"))
        .withColumn("longitude", col("longitude").cast("double"))
        .withColumn("store_point", expr("ST_Point(longitude, latitude)"))
    )

    visits = (
        spark.read.option("header", True).option("inferSchema", True).csv(str(visits_file))
        .withColumn("latitude", col("latitude").cast("double"))
        .withColumn("longitude", col("longitude").cast("double"))
        .withColumn("event_time", to_timestamp(col("timestamp")))
        .withColumn("visit_point", expr("ST_Point(longitude, latitude)"))
    )

    # ST_DistanceSphere returns approximate great-circle distance in metres.
    nearby = (
        visits.crossJoin(stores)
        .withColumn("distance_m", expr("ST_DistanceSphere(visit_point, store_point)"))
        .filter(col("distance_m") <= RADIUS_METERS)
        .select(
            "visit_id", "timestamp", "activity_type",
            "store_id", "store_name", "category",
            spark_round("distance_m", 1).alias("distance_m")
        )
    )

    store_summary = (
        nearby.groupBy("store_id", "store_name", "category")
        .agg(count("*").alias("nearby_visits"))
        .orderBy(col("nearby_visits").desc())
    )

    hourly_summary = (
        nearby.withColumn("hour", hour(to_timestamp(col("timestamp"))))
        .groupBy("hour")
        .agg(count("*").alias("nearby_visits"))
        .orderBy("hour")
    )

    return nearby, store_summary, hourly_summary, stores, visits
