import Link from "next/link";
import React from "react";
import styles from '../styles/TeamCard.module.css';

export default function TeamCard({data}) {

    const tid = data.team_id
    return (
        <div className={styles.card}>
            <Link href={`/teams/${tid}/`}>
                <div className={styles.cardStats}>
                    <p>{data.image}</p>
                    <p>{data.name}</p>
                    <p>{data.past_teams} </p>
                </div>
            </Link>
        </div>
    )
}