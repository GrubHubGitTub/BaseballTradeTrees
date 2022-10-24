import Link from "next/link";
import React from "react";
import styles from '../styles/PlayerCard.module.css';
import {franchises} from "../data/franchise_colors"

export default function PlayerCard({player, team}) {
    const position = player.position

    let border;
    let shadow;
    let color;
    let name;
    if ("retroid" in player) {
        name = 
            <Link 
                key= {player.pid}
                href={{
                pathname: '/player/[pid]',
                query: { pid: player.retroid } }}> 
                    <h3 className={styles.playerLink}>{player.name}</h3> 
            </Link>
        if (team in franchises) {
            border= `3px solid ${franchises[team]}`
        }
        shadow = "0 4px 18px 0 rgba(0, 0, 0, 0.25)"
        color = "#f5f5f5"
    } else {
        name = <h3 className={styles.playerName}>{player.name}</h3>
        border = "1.5px solid #c3c6ce"
        shadow = "0"
        color = "#FFF8EC"
    }
    let position_display
    if (position == "Designated Hitter"){
        position_display = <p className={styles.playerPos}>DH</p>
    } else {
        position_display = <p className={styles.playerPos}>{position}</p>
    }

    let number 
    if (player.number != ""){
        number = <h3 className={styles.playerNumber}>{player.number}</h3>
    }


    return(
        <div className={styles.card} style={{"border": border, "box-shadow":shadow, "background":color}} >
            {position_display}
            {name}
            {number}
        </div>
    )
}