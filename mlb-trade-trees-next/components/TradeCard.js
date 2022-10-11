import Link from "next/link";
import React from "react";
import styles from '../styles/TradeCard.module.css';

export default function TradeCard(props) {
    console.log(props.data)

    const tree_id = props.data.tree_id 
    const pid = props.pid

    const year = props.data.date.toString().slice(0,4)
    const month = props.data.date.toString().slice(4,6)
    const day = props.data.date.toString().slice(6,8)

    const largest_tree = props.data.largest_tree_id
    const parent_id = largest_tree.slice(0,8)

    const ws_wins = props.data.world_series_wins.length

    const getCardStyle = () => {
        if (ws_wins.length > 0) return styles.cardWS
        else if (props.data.total_stats.war_sal.WAR < 0 ) return styles.cardNeg;
        else return styles.cardPos;
      };

    let largestButton
    if (largest_tree != "_"){
        largestButton = <Link href={`/players/${parent_id}/${largest_tree}`}><a className={styles.largestButton}> View Parent Tree</a></Link>
    } 


    return (
        // <div className={styles.card}>
        //         <p>{props.data.from_team.team_name} → {props.data.to_team.team_name}</p>
        //         <p>{year}-{month}-{day}</p> 
        //         <p>{props.data.total_stats.war_sal.WAR} WAR</p>
        //         <Link href={`/players/${pid}/${tree_id}`}><a>View Tree</a></Link>
        //         {/* {props.data.largest_tree_id == "_" ? "" : `<a href=/players/${parent_id}/${largest_tree}> View Largest Version of this Tree</a>`} */}
        // </div>

            <div className={getCardStyle()}>
                <img src="/team_logos/TOR_logo.png"></img>
                <div className={styles.content}>
                    
                    <h2>{props.data.from_team.team_name}</h2>
                    <h3>→ {props.data.to_team.team_name}</h3>
                    <h4>{props.data.start}-{props.data.last}</h4>                    
                    <h4>Total transactions: {props.data.total_transactions}</h4>
                    <p>{props.data.total_stats.war_sal.WAR} WAR | {props.data.total_stats.batting_stats.R} Runs | </p>
                    <p>{props.data.total_stats.pitching_stats.W} Wins | {ws_wins == 0 ? "" : `${ws_wins} WS Wins`} </p>
                    
                    <Link href={`/players/${pid}/${tree_id}`}><a className={styles.treeButton}>View Tree</a></Link>
                    {largestButton}
                </div>
            </div>
    )
}