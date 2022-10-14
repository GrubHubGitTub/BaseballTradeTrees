import Link from "next/link";
import React from "react";
import styles from '../styles/TradeCard.module.css';

export default function TradeCard(props) {

    const tree_id = props.data.tree_id 
    const pid = props.pid

    const largest_tree = props.data.largest_tree_id
    const parent_id = largest_tree.slice(0,8)

    const ws_wins = props.data.ws_wins.length

    const outlineColor = () => {
        if (ws_wins > 0) return "rgb(255, 183, 0) 0px 1px 4px, rgb(174, 125, 0) 0px 0px 0px 3px"
        else if (props.data.total_stats.war_sal.WAR < 0 ) return "rgb(138, 1, 1) 0px 1px 4px, rgb(137, 0, 0) 0px 0px 0px 3px"
        else return "rgb(2, 122, 0) 0px 1px 4px, rgb(0, 120, 8) 0px 0px 0px 3px"
      };

    let largestButton
    if (largest_tree != "_"){
        largestButton = <Link href={`/players/${parent_id}/${largest_tree}`}><a className={styles.largestButton}> View Parent Tree</a></Link>
    } 

    let world_series_wins
    if (ws_wins > 0){
        world_series_wins = props.data.ws_wins.map(year => (
            <img key={year} src="/team_logos/ws.gif" title={year} className={styles.wsWins}></img>))
    }

    const franchises = {"ANA": "Maroon", "ARI":"Maroon", "ATL":"Maroon", "BAL":"Orange", "BOS":"maroon", "CHC":"darkBlue", "CHW":"Darkgrey", 
    "CIN":"Maroon", "CLE":"Red", "COL":"Purple","DET":"navyblue", "FLA":"coral", "HOU":"orange", "KCR":"royalblue", 
    "LAD": "dodgerblue","MIL":"navyblue","MIN":"maroon", "NYM":"orange","NYY":"darkgrey","OAK":"darkgreen", "PHI": "red", 
    "PIT":"yellow","SDP":"lightbrown","SEA":"navyblue","SFG":"orange", "STL":"red", "TBD":"navyblue", "TEX":"red","TOR":"blue","WSN":"maroon"}

    let background 
    let link
    const from_franch = props.data.from_f
    if (from_franch in franchises) {
        background = franchises[from_franch]
        link = `/team_logos/${from_franch}.png`
    }
    else{
        background = "black"
        link = `/team_logos/MLB.png`
    }

    return (

            <div className={styles.card} style={{"background": background, "boxShadow": outlineColor() }}>
                <div className={styles.logodiv}>
                <img className={styles.logo} src={link} ></img>
                </div>
                    <h1>{props.data.from_t.team_name}</h1>
                    <div className={styles.content}>
                        <h2>→ {props.data.to_t.team_name}</h2>
                        <div style={{display:"inline-block"}}>
                        <h3>{props.data.start}-{props.data.last}</h3>{world_series_wins}
                        </div>                    
                        <h3>Total transactions: {props.data.total_transac}</h3>
                        <p>{props.data.total_stats.war_sal.WAR} WAR | {props.data.total_stats.batting_stats.R} Runs </p>
                    </div>
                    <Link href={`/players/${pid}/${tree_id}`}><a className={styles.treeButton}>View Tree</a></Link>
                    {largestButton}
                    
            </div>
    )
}