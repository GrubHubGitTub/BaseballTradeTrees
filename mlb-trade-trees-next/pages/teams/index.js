import React from "react";
import TeamCard from "../../components/TeamCard";
import styles from "../../styles/AllTeams.module.css"

    export const getStaticProps = async () => {
    // const res = await fetch('http://localhost:3000/api/teams/');
    // const data = await res.json();
    const teams = require("../../data/team_info.json");

    return { props: {teams} }
    }

    export default function teamsPage({teams}) {
        const allTeams = teams.map(team => {
            return (
                <TeamCard key={team.team_id} data = {team} />
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