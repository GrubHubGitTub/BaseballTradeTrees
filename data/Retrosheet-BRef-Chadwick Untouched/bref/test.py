import pandas as pd
stats = pd.read_csv("war_daily_bat.txt")

stats = stats[["name_common","salary"]].sort_values(by="salary", ascending=False)

print(stats)