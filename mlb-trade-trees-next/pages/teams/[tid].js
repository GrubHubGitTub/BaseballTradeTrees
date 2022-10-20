import Link from "next/link";
import React from "react";
// import player_data from "../../data/output.json"

export async function getServerSideProps(context) {
    const player_data = require("../../data/player_search.json");

    const tid = context.query.tid
    const res= await fetch(`https://statsapi.mlb.com/api/v1/teams/${tid}/roster`);
    const data = await res.json();
    const roster = data.roster

    var combined_ids = []
    await Promise.all(roster.map(async function(player) {
        const mlbid = Number(player.person.id)
        const filtered = player_data.filter((p) => p.mlb_id === mlbid)
             
        if (filtered.length > 0) {
            const playerdata = filtered[0];
            const pid = playerdata.retro_id;
            const name = player.person.fullName
            const position = player.position.name
            const number = player.jerseyNumber
            const combined = {retroid: pid, mlbid: mlbid, name: name, position:position, number:number}
            combined_ids.push(combined)
            }
        }))
        

    return ({props: {combined_ids}})
}

  export default function TeamPage(props) {
    const roster = props.combined_ids

    return (
        <div>
            {roster.map(player => {
                return (
                    <div key={player.pid}>
                        <p>{player.name}</p>
                        <Link 
                            key= {player.PLAYERID}
                            href={{
                            pathname: '/players/[pid]',
                            query: { pid: player.retroid } }}> 
                                <a>player page</a> 
                        </Link>
                        <p>{player.position}</p>
                        <p>{player.number}</p>
                    </div>
                )
            })}
        </div>
    )
  }