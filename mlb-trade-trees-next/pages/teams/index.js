import React from "react";
import TeamCard from "../../components/TeamCard";
import styles from "../../styles/AllTeams.module.css"
import team_data from "../../data/team_info.json"

    export const getStaticProps = async () => {
    // const res = await fetch('http://localhost:3000/api/teams/');
    // const data = await res.json();
    const teams = team_data

    return { props: {teams} }
    }

    export default function teamsPage({teams}) {
        const ALE = teams.map(team => {
            if (team.division == "American League East")
            return (
                <TeamCard key={team.team_id} data = {team} />
            )
            })
        const ALC = teams.map(team => {
            if (team.division == "American League Central")
            return (
                <TeamCard key={team.team_id} data = {team} />
            )
            })
        const ALW = teams.map(team => {
            if (team.division == "American League West")
            return (
                <TeamCard key={team.team_id} data = {team} />
            )
            })
        const NLE = teams.map(team => {
            if (team.division == "National League East")
            return (
                <TeamCard key={team.team_id} data = {team} />
            )
            })
        const NLC = teams.map(team => {
            if (team.division == "National League Central")
            return (
                <TeamCard key={team.team_id} data = {team} />
            )
            })
        const NLW = teams.map(team => {
            if (team.division == "National League West")
            return (
                <TeamCard key={team.team_id} data = {team} />
            )
            })

        return (
            <div className={styles.teamPage}>
                
                    <h1 style={{"margin-top": "2%" }}>AL East</h1>
                    <div className={styles.cardContainer}>
                    {ALE}
                    </div>

                    <h1>AL Central</h1>
                    <div className={styles.cardContainer}>
                    {ALC}
                    </div>

                    <h1>AL West</h1>
                    <div className={styles.cardContainer}>
                    {ALW}
                    </div>

                    <h1>NL East</h1>
                    <div className={styles.cardContainer}>
                    {NLE}
                    </div>

                    <h1>NL Central</h1>
                    <div className={styles.cardContainer}>
                    {NLC}
                    </div>
                    
                    <h1>NL West</h1>
                    <div className={styles.cardContainer}>
                    {NLW}
                    </div>
                
            </div>
        )
    }
    export const config = {
        unstable_excludeFiles: ["../../data/all_data1.json", "../../data/all_data2.json"],
      }