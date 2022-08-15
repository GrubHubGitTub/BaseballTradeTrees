import React from "react";
import TeamCard from "../../components/TeamCard";
import styles from "../../styles/AllTeams.module.css"

  export const getStaticProps = async () => {
    const res = await fetch('http://localhost:3000/api/teams/');
    const data = await res.json();
    return { props: {data} }
  }

export default function allTeams({data}) {

    const allTeams = data.map(team => {
        return (
            <TeamCard data = {team} />
        )
        })

    return (
        <div>
            <h1>List of current-day franchises, click to see team and roster information. </h1>
            <div className={styles.allCards}>{allTeams}</div>
        </div>
    )
}