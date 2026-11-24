# GeoPulse — Project Overview

## 1. Problem statement
Retailers need a way to understand how activity is distributed around nearby stores. Raw latitude and longitude records are difficult to interpret without spatial processing.

## 2. Proposed solution
GeoPulse reads retail store locations and timestamped activity points, creates spatial geometries, and uses Apache Sedona spatial SQL on Apache Spark to find activity points within a configurable radius of each store.

## 3. Objectives
- Process location records using distributed data processing concepts.
- Apply geospatial point creation and distance calculations.
- Identify activity points close to retail locations.
- Summarize nearby activity by store and hour.
- Present results using charts and a location plot.

## 4. Methodology
1. Read and validate CSV inputs.
2. Start a local Spark session with Sedona SQL support.
3. Convert coordinates to spatial points using `ST_Point`.
4. Pair activity records with store locations.
5. Calculate great-circle distance using `ST_DistanceSphere`.
6. Filter records by the configured radius.
7. Aggregate and export summaries.
8. Generate charts for interpretation.

## 5. Input data
`stores.csv` contains store identifiers, names, categories, and coordinates.
`visits.csv` contains synthetic activity identifiers, timestamps, coordinates, and activity types.

## 6. Output
- Nearby activity-to-store matches with distance in metres.
- Nearby activity count per store.
- Nearby activity count by hour.
- Store/activity location plot and summary charts.

## 7. Scope and limitations
This is a local academic prototype using synthetic sample data. It does not identify people, infer demographics, or use live GPS tracking. Straight-line distance is used instead of actual walking/driving distance. Production use would require consent, privacy controls, real validated data, scalability testing, and careful business interpretation.
