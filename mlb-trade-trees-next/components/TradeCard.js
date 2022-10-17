import Link from "next/link";
import React from "react";
import styles from '../styles/TradeCard.module.css';
import Image from "next/image";

export default function TradeCard(props) {

    const tree_id = props.data.tree_id 
    const pid = props.pid

    const largest_tree = props.data.largest_tree_id
    const parent_id = largest_tree.slice(0,8)

    const ws_wins = props.data.ws_wins.length

    // const outlineColor = () => {
    //     if (ws_wins > 0) return "rgb(255, 183, 0) 0px 1px 4px, rgb(174, 125, 0) 0px 0px 0px 3px"
    //     else if (props.data.total_stats.war_sal.WAR < 0 ) return "rgb(138, 1, 1) 0px 1px 4px, rgb(137, 0, 0) 0px 0px 0px 3px"
    //     else return "rgb(2, 122, 0) 0px 1px 4px, rgb(0, 120, 8) 0px 0px 0px 3px"
    //   };

    let largestButton
    if (largest_tree != "_"){
        largestButton = <Link href={`/players/${parent_id}/${largest_tree}`}><a className={styles.largestButton}> View Parent Tree</a></Link>
    } 

    let world_series_wins
    if (ws_wins > 0){
        world_series_wins = props.data.ws_wins.map(year => (
            <Image key={year} alt="WSTrophy" src="/team_logos/ws.gif" title={year} className={styles.wsWins} height="70px" width="40px"/>
            ))
        }

    const franchises = {"ANA": "Maroon", "ARI":"Maroon", "ATL":"Maroon", "BAL":"darkOrange", "BOS":"maroon", "CHC":"darkBlue", "CHW":"Darkgrey", 
    "CIN":"Maroon", "CLE":"Red", "COL":"Purple","DET":"navyblue", "FLA":"coral", "HOU":"orange", "KCR":"royalblue", 
    "LAD": "dodgerblue","MIL":"navyblue","MIN":"maroon", "NYM":"orange","NYY":"white","OAK":"darkgreen", "PHI": "red", 
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

    // , "boxShadow": outlineColor()

    return (

            <div className={styles.card} style={{"background": background, "boxShadow": "rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px" }}>
                <div className={styles.logodiv}>
                    <Image src={link} alt="TeamLogo" layout="fill" objectFit="contain"/>
                </div>
                    <h1>{props.data.from_t.team_name}</h1>
                    <div className={styles.content}>
                        <h4>→ {props.data.to_t.team_name}</h4>
                        <div style={{display:"inline-block"}}>
                        <h2>{props.data.start}-{props.data.last}</h2>{world_series_wins}
                        </div>                    
                        <h3>Total transactions: {props.data.total_transac}</h3>
                        <p>{props.data.total_stats.war_sal.WAR} WAR | {props.data.total_stats.batting_stats.R} Runs </p>
                    </div>
                    <Link href={`/players/${pid}/${tree_id}`}><a className={styles.treeButton}>View Tree</a></Link>
                    {largestButton}
                    
            </div>
    )
}