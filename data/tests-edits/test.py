import json
gen = [{"name":"a","trans":123},{"name":"b","trans":1234}, {"name":"b","trans":12444} ]

for dicto in gen:
    tree = {
        "name": dicto["name"],
        "trans": dicto["trans"]
    }
    with open("output.json", "r") as file:
        file_data = json.load(file)
        match = False
        for data in file_data["player_data"]:
            if data["name"] == dicto["name"]:
                data["all_trans"].append(tree)
                match = True
                break
        if not match:
            output = {
                "name":dicto["name"],
                "trans":dicto["trans"],
                "all_trans":[tree]
            }
            file_data["player_data"].append(output)
    with open("output.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)


