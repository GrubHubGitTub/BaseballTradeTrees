import Link from "next/link";
import React from "react";
import styles from '../styles/TradeCard.module.css';
import Image from "next/image";
import {franchises} from "../data/franchise_colors"

export default function TeamCard({data}) {
    console.log(data)
    const tid = data.team_id
    const mlbid = data.mlb_id

    let background 
    let link

    if (tid in franchises) {
        background = franchises[tid]
        link = `/team_logos/${tid}.png`
    }

    return (

            <div className={styles.card} style={{"background": background, "boxShadow": "rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px", "transform": "scale(0.8)" }}>
                <div className={styles.logodiv}>
                    <Image src={link} alt="TeamLogo" layout="fill" objectFit="contain"/>
                </div>
                    <h1>{data.name}</h1>
                    <div className={styles.content}>
                        {/* <div style={{display:"inline-block"}}>
                        <h2>{props.data.y_start}-{props.data.y_last}</h2>{world_series_wins}
                        </div>                     */}
                        <h3>Franchise since: {data.first_year}</h3>
                        {/* <p>{props.data.total_stats.war_sal.WAR} WAR | {props.data.total_stats.batting_stats.R} Runs </p> */}
                    </div>
                    <Link href={`/teams/${tid}`}><a className={styles.treeButton}>View Current Roster and Info</a></Link>
                    
            </div>
    )
}