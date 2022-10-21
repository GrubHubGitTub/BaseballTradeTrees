import Link from "next/link";
import React from "react";
import players from "../../data/player_search.json"
import teams from "../../data/team_info.json"
import styles from "../../styles/RosterPage.module.css"
import PlayerCard from "../../components/PlayerCard";

export async function getServerSideProps(context) {
    const player_data = players
    const team_data = teams
    const franch = context.params.tid
    const team = team_data.filter((t) => t.team_id == franch)[0]

    const tid = team.mlb_id
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
        else{
            const name = player.person.fullName
            const position = player.position.name
            const number = player.jerseyNumber
            const combined = {name: name, position:position, number:number}
            combined_ids.push(combined)
        }
        }))
    return ({props: {combined_ids, team}})
}

  export default function TeamPage(props) {
    const roster = props.combined_ids
    const team_info = props.team

    const Pcards = roster.map(player => {
        if (player.position == "Pitcher"){
        
        return (
            <PlayerCard 
                key={player.name}
                player={player} 
                team = {props.team.team_id}
                />
        )}
    })
    
    const OFcards = roster.map(player => {
        if (player.position == "Outfielder"){
        
        return (
            <PlayerCard 
                key={player.name}
                player={player} 
                team = {props.team.team_id}
                />
        )}
    })
    const IFcards = roster.map(player => {
        if (player.position == "Outfielder") {}
        else if (player.position == "Pitcher") {} 
        else {
            return (
            <PlayerCard 
                key={player.name}
                player={player} 
                team = {props.team.team_id}
                />
        )}
    })

    return (
        <div className={styles.rosterPage}>
            <h1>{props.team.name}</h1>
            <div className={styles.roster}>

                

                <div className={styles.posContainer}>
                        
                        {Pcards}
                </div>

                <div className={styles.posContainer}>
                    

                        {OFcards}

                </div>

                <div className={styles.posContainer}>
                    

                    {IFcards}

                </div>

            </div>
        </div>
    )
  }

  export const config = {
    unstable_excludeFiles: ["../../data/all_data1.json", "../../data/all_data2.json"],
  }