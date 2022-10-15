// import player_data1 from "../../data/tests-edits/all_data1.json"
// import player_data2 from "../../data/tests-edits/all_data2.json"
import { readFileSync } from 'fs';
import path from 'path';

export function getData() {
    
    const file1 = path.join(process.cwd(), 'data', "/all_data1.json");
    const file2 = path.join(process.cwd(), 'data', "/all_data2.json");
    const player_data1 = JSON.parse(readFileSync(file1, 'utf8'));
    const player_data2 = JSON.parse(readFileSync(file2, 'utf8'));
    const data = player_data1.concat(player_data2);
    return data
}
