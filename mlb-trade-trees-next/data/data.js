import player_data1 from "../../data/tests-edits/all_data1.json"
import player_data2 from "../../data/tests-edits/all_data2.json"

export function getData() {
    const data = player_data1.concat(player_data2);
    return data
}
