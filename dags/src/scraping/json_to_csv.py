import pandas as pd
import json
from pathlib import Path
import time


def json_to_csv():
    """
    Convert json file into a csv file.
    """
    # current_dnt = time.strftime("%Y_%m_%d-%p%I_%M")
    # csv_filename = f"scraped_data_{current_dnt}.csv"
    path_to_open = Path.cwd() / "data" / "scraped_data.json"
    path_to_save = Path.cwd() / "data" / "scraped_data.csv"

    with open(path_to_open, "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.to_csv(path_to_save, index_label="id", encoding="utf-8")
