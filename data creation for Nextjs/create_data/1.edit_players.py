import pandas as pd

# Filter chadwick biofile and add HOF info from retrosheet biofile
chadbiofile = pd.read_csv("../2022/ChadwickBiofile.csv", low_memory=False)
retrobiofile = pd.read_csv("../2022/RetroSheetBIOFILE.csv")

chadbiofile = chadbiofile.dropna(subset=['key_retro'])
chadbiofile.loc[chadbiofile['mlb_played_last'] == 2022.0, 'mlb_played_last'] = ""
chadbiofile["name"] = chadbiofile["name_first"] + " " + chadbiofile["name_last"]
chadbiofile["PLAYERID"] = chadbiofile["key_retro"]
chadbiofile = chadbiofile[["PLAYERID", "key_mlbam", "key_bbref", "name", "mlb_played_first", "mlb_played_last"]]
combined_info = pd.merge(chadbiofile, retrobiofile[["PLAYERID", "HOF"]], on="PLAYERID", how="left")
combined_info.loc[combined_info['HOF'] == "NOT", 'HOF'] = ""

combined_info.to_csv("playerdata.csv", index=False)
######### Then remove all .0 in csv






