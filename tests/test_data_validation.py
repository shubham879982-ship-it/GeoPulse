import tempfile
import unittest
from pathlib import Path
from src.data_validation import validate_csv, STORE_COLUMNS

class DataValidationTests(unittest.TestCase):
    def test_valid_store_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "stores.csv"
            path.write_text(
                "store_id,store_name,category,latitude,longitude\n"
                "S01,Sample Store,Grocery,19.9975,73.7898\n",
                encoding="utf-8"
            )
            valid, errors = validate_csv(path, STORE_COLUMNS)
            self.assertTrue(valid)
            self.assertEqual(errors, [])

    def test_missing_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "stores.csv"
            path.write_text("store_id,store_name\nS01,Sample\n", encoding="utf-8")
            valid, errors = validate_csv(path, STORE_COLUMNS)
            self.assertFalse(valid)
            self.assertTrue(errors)

if __name__ == "__main__":
    unittest.main()
