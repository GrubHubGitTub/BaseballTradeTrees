import pandas as pd

df = pd.read_json("output.json")

df.to_csv("outputcsv.csv", index = False)

