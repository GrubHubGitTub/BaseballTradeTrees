import React from "react";
import TeamCard from "../../components/TeamCard";
import styles from "../../styles/AllTeams.module.css"
import team_data from "../../data/team_info"

    export const getStaticProps = async () => {
    // const res = await fetch('http://localhost:3000/api/teams/');
    // const data = await res.json();
    const teams = team_data

    return { props: {teams} }
    }

    export default function teamsPage({teams}) {
        const allTeams = teams.map(team => {
            return (
                <TeamCard data = {team} />
            )
            })

        return (
            <div className={styles.teamPage}>
                <div className={styles.cardContainer}>
                    {allTeams}
                </div>
            </div>
        )
    }