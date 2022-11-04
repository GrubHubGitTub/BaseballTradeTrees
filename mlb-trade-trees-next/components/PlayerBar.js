import React from "react"
import Link from 'next/link'
import styles from '../styles/PlayerBar.module.css'
import Image from "next/image"
import {franchises} from "../data/franchise_colors"


export default function PlayerBar({data, tree_data}) {
    const from_team = tree_data.from_team.team_name

    let background 
    let link
    const from_franch = tree_data.from_franch
    if (from_franch in franchises) {
        if (from_franch == "NYY" ){
            background = "darkgrey"
            link = `/team_logos/${from_franch}.png`
        }
        else{
        background = franchises[from_franch]
        link = `/team_logos/${from_franch}.png`
        }
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
                    <th key={key} style={{"backgroundColor":background, "color":"white"}}> {key} </th>                    
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
        parent_tree= ""
    } else { 
        var rid = tree_data.largest_tree_id.slice(0,8)
        parent_tree =
            <Link href={{
                pathname: '/player/[pid]/[tid]',
                query: {pid: rid, tid: tree_data.largest_tree_id }}}>
                <button className={styles.parentTree} style={{"border":`2px solid ${background}`}}> View Parent Tree </button>
            </Link> 
    }

    let world_series_wins = ""
    if (tree_data.ws_wins.length > 0){
        world_series_wins = tree_data.ws_wins.map(year => (
            <div className={styles.wsDiv} key={year}>
            <Image  key={year}
                    alt="WSTrophy"
                    src="/team_logos/ws.gif"
                    title={year}
                    layout="fill"
                    objectFit="contain"
                    className={styles.wsWins}/>
            </div>
                    ))
    }

    return ( 
        <div className={styles.PlayerBar} style={{"border": `3px solid ${background}`}}>
            <Link href={{
                    pathname: '/player/[pid]',
                    query: {pid: data.retro_id }}}>
                    <a className={styles.playerName}> ← {data.name} </a>
            </Link>
                
                <div className={styles.teamHeader}>
                    <h1 className={styles.teamName}>{from_team}</h1>
                    <div className={styles.teamLogo}>
                        <Image src={link} alt="TeamLogo" layout="fill" objectFit="contain"/>
                    </div>
                    <h2 className={styles.years}>{tree_data.y_start}-{tree_data.y_last}</h2>
                    {world_series_wins != "" ? <div className={styles.wsContainer}>{world_series_wins}</div> : "" }
                    
                </div> 

                            
            <div className={styles.otherStats}>
                {parent_tree}
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
                                pathname: '/player/[pid]/[treeid]',
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