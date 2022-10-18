import React from "react"
import Link from 'next/link'
import styles from '../styles/PlayerBar.module.css'
import Image from "next/image"


export default function PlayerBar({data, tree_data}) {
    const from_team = tree_data.from_team.team_name

    const franchises = {"ANA": "Maroon", "ARI":"Maroon", "ATL":"Maroon", "BAL":"darkOrange", "BOS":"maroon", "CHC":"darkBlue", "CHW":"Darkgrey", 
    "CIN":"Maroon", "CLE":"Red", "COL":"Purple","DET":"navyblue", "FLA":"coral", "HOU":"orange", "KCR":"royalblue", 
    "LAD": "dodgerblue","MIL":"navyblue","MIN":"maroon", "NYM":"orange","NYY":"white","OAK":"darkgreen", "PHI": "red", 
    "PIT":"Gold","SDP":"lightbrown","SEA":"navyblue","SFG":"orange", "STL":"red", "TBD":"darkblue", "TEX":"red","TOR":"blue","WSN":"maroon"}

    let background 
    let link
    const from_franch = tree_data.from_franch
    if (from_franch in franchises) {
        background = franchises[from_franch]
        link = `/team_logos/${from_franch}.png`
    }
    else{
        background = "black"
        link = `/team_logos/MLB.png`
    }

    var batting_stats = tree_data.total_stats.batting_stats
    const b_stats =    
        <table className={styles.statsTable}> 
            <thead>
                <tr>
                {Object.keys(batting_stats).map(key => (
                    <th key={key} style={{"background-color":background, "color":"white"}}> {key} </th>                    
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
                <th key={key} style={{"background-color":background, "color":"white"}}> {key} </th>                    
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
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0,
      });
    const salary = formatter.format(other_stats.salary)

    let parent_tree;
    if ( tree_data.largest_tree_id == "_" ) {
        parent_tree= <p className={styles.noParent}></p>
    } else { 
        var rid = tree_data.largest_tree_id.slice(0,8)
        parent_tree = 
            <Link href={{
                pathname: '/players/[pid]/[tid]',
                query: {pid: rid, tid: tree_data.largest_tree_id }}}>
                <a className={styles.parentTree}> View Parent Tree </a>
            </Link> 
    }

    let world_series_wins
    if (tree_data.ws_wins.length > 0){
        world_series_wins = tree_data.ws_wins.map(year => (
            <Image  key={year}
                    alt="WSTrophy"
                    src="/team_logos/ws.gif"
                    title={year}
                    height="60px" 
                    width="30px"
                    className={styles.wsWins}/>
                    ))
    }

    return ( 
        <div className={styles.PlayerBar}>

            <div className={styles.playerTeamTree}>
                <Link href={{
                    pathname: '/players/[pid]',
                    query: {pid: data.retro_id }}}>
                    <a className={styles.playerName}> ← {data.name} </a>
                </Link>
                <div className={styles.teamHeader}>
                    <h1 className={styles.teamName}>{from_team}</h1>
                    <div className={styles.teamLogo}>
                        <Image src={link} alt="TeamLogo" objectFit="contain" width="100%" height="100%"/>
                    </div>
                    <h2>{tree_data.y_start}-{tree_data.y_last}</h2>
                    {world_series_wins}
                    
                </div> 
                {parent_tree}
            </div>
            
            <div className={styles.otherStats}>
                <h4>{tree_data.total_transac} {tree_data.total_transac > 1 ? "transactions" : "transaction"} </h4>
                <h4>{other_stats.WAR > 0 ? "+" : ""}{other_stats.WAR} WAR | 
                {salary.toString().slice(0,1) == "-" ? "" : " +"}{salary} </h4>
            </div>

            <div className={styles.allStats}>
                <div className={styles.statsContainer}>
                    <h5 className={styles.tableHeader}>Batting </h5>
                    {b_stats}
                </div>
                <div className={styles.statsContainer}>
                    <h5 className={styles.tableHeader}>Pitching </h5>
                    {p_stats}
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