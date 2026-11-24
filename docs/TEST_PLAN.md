# GeoPulse Test Plan

| Test ID | Test case | Expected result |
|---|---|---|
| TC-01 | Store CSV exists and has required headers | Validation passes |
| TC-02 | Visit CSV exists and has required headers | Validation passes |
| TC-03 | Latitude/longitude values are numeric and in range | Validation passes |
| TC-04 | Required CSV column is missing | Validation reports an error |
| TC-05 | Run the Spark/Sedona pipeline | Spatial analysis runs without errors |
| TC-06 | Activity point is within configured radius | Matching store appears in nearby output |
| TC-07 | Activity point is outside configured radius | No match for that store |
| TC-08 | Summary output is generated | CSV summaries and charts appear in outputs |

Run automated validation tests with:
`python -m unittest discover -s tests -v`

TC-05 to TC-08 require a working Java, PySpark, and Sedona environment and should be executed on the target laptop before project submission.
