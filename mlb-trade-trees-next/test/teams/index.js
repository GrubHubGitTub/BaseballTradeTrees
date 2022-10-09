import React from "react";
import TeamCard from "../../components/TeamCard";
import styles from "../../styles/AllTeams.module.css"
import team_data from "../../data/team_data"

    export const getStaticProps = async () => {
    // const res = await fetch('http://localhost:3000/api/teams/');
    // const data = await res.json();
    const teams = team_data["teams"]

    return { props: {teams} }
    }

    export default function teamsPage({teams}) {
        console.log(teams)
        const allTeams = teams.map(team => {
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