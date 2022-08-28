import Link from "next/link";
import React from "react";
import styles from '../styles/TradeCard.module.css';

export default function TradeCard(props) {

    const tree_id = props.data.tree_id 
    const pid = props.pid
    return (
        <div className={styles.card}>
            <Link href={`/players/${pid}/${tree_id}`}>
            <div className={styles.cardStats}>
                <p>Traded from: {props.data.from_team.team_name}</p>
                <p>Traded to: {props.data.to_team.team_name} </p>
                <p>Transaction #: {props.data.transac_id}</p>
                <p>Date:{props.data.date}</p>
                
            </div>
            </Link>
        </div>
    )
}