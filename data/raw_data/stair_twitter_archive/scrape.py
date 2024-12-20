from csv import QUOTE_NONE
from pathlib import Path
from typing import List
import pandas as pd

def create_dictionary_of_dfs_from_paths(list_of_files: List[Path] = None, delimiter: str | None = "‎"):
    assert list_of_files, "Need to define a list of paths to create dataframe from"

    # Create a dictionary of csv files per perpetrator
    paths = dict()
    for csv in list_of_files:
        paths[csv.parents[0].name] = csv
    
    # Create a dictionary of dataframes per perpetrator
    dfs = dict()
    for key, value in paths.items():
        dfs[key] = pd.read_csv(value, delimiter=delimiter, engine='python', encoding="utf-8")
    
    return dfs


dict_of_dfs = create_dictionary_of_dfs_from_paths((Path(__file__).parent).rglob("tweets.csv"), delimiter=",")

# Create a dataframe in preferred format
# Concat dataframes
df = pd.concat(list(dict_of_dfs.values())).reset_index()
# Create date column
df["date"] = pd.to_datetime(df["timestamp"], yearfirst=True)
# Drop uneccessary columns
df = df.drop(["tweet_id","in_reply_to_status_id","in_reply_to_user_id", "timestamp", "source", "retweeted_status_id","retweeted_status_user_id","retweeted_status_timestamp","expanded_urls"], axis=1)
# Reorder columns
df = df[['date', "text"]]

# Create file
out = Path(__file__).parent / "data.csv"
print(out)
df.to_csv(out, sep="‎", header=True, index=False, date_format="%Y-%m-%d")