import React from "react"
import Link from 'next/link'
import styles from '../styles/PlayerBar.module.css'


export default function PlayerBar({data, tree_data}) {

    var batting_stats = tree_data.total_stats.batting_stats
    const b_stats =    
        <table className={styles.statsTable}> 
            <thead>
                <tr>
                {Object.keys(batting_stats).map(key => (
                    <th key={key}> {key} </th>                    
                ))}
                </tr>
            </thead>
            <tbody>  
                <tr>
                {Object.keys(batting_stats).map(key => (
                <td key={key}>{batting_stats[key]}</td>
                ))}
                </tr>
            </tbody> 
        </table> 

    var pitching_stats = tree_data.total_stats.pitching_stats
    const p_stats =  
        <table className={styles.statsTable}> 
        <thead>
            <tr>
            {Object.keys(pitching_stats).map(key => (
                <th key={key}> {key} </th>                    
            ))}
            </tr>
        </thead>
        <tbody>  
            <tr>
            {Object.keys(pitching_stats).map(key => (
            <td key={key}>{pitching_stats[key]}</td>
            ))}
            </tr>
        </tbody> 
        </table> 

    var other_stats = tree_data.total_stats.war_sal
    const o_stats = 
        <table className={styles.statsTable}> 
        <thead>
            <tr>
            {Object.keys(other_stats).map(key => (
                <th key={key}> {key} </th>                    
            ))}
            </tr>
        </thead>
        <tbody>  
            <tr>
            {Object.keys(other_stats).map(key => (
            <td key={key}>{other_stats[key]}</td>
            ))}
            </tr>
        </tbody> 
    </table> 

    let parent_tree;
    if ( tree_data.largest_tree_id == "_" ) {
        parent_tree = <p className={styles.invisible}>No Parent Tree</p>
    } else { 
        var rid = tree_data.largest_tree_id.slice(0,8)
        parent_tree = 
            <Link href={{
                pathname: '/players/[pid]/[tid]',
                query: {pid: rid, tid: tree_data.largest_tree_id }}}>
                <a className={styles.playerName}> View Parent Tree </a>
            </Link> 
    }
    console.log(tree_data.from_team)
    const from_team = tree_data.from_team.team_name

    return ( 
        <div className={styles.PlayerBar}>

            <div className={styles.playerTeamTree}>
                <Link href={{
                    pathname: '/players/[pid]',
                    query: {pid: data.retro_id }}}>
                    <a className={styles.playerName}> ← {data.name} </a>
                </Link>
                <div className={styles.teamHeader}>
                    <h3>{from_team}</h3>
                    <img className={styles.teamLogo} src="/team_logos/TOR_logo.png"></img>
                </div> 
                {parent_tree}
            </div>

            <div className={styles.allStats}>
                <div className={styles.statsContainer}>
                    <h6 className={styles.tableHeader}>Batting: </h6>
                    {b_stats}
                </div>
                <div className={styles.statsContainer}>
                    <h6 className={styles.tableHeader}>Pitching: </h6>
                    {p_stats}
                </div>
                <div className={styles.statsContainer}>
                    <h6 className={styles.tableHeader}>Other: </h6>
                    {o_stats}
                </div>
            </div>

        </div>
            /* {trades.map((trade) => {
                return (<Link 
                            key={trade.tree_id}
                            href={{
                                pathname: '/players/[pid]/[treeid]',
                                query: { pid: data.retro_id, treeidcd: trade.tree_id }
                            }}>   
                            <a className="treeLink" > 
                            {trade.tree_id} 
                            </a>
                        </Link>
                    )
            })} */
        

    )
}