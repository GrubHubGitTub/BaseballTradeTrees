import React from "react"
import Link from 'next/link'
import styles from '../styles/PlayerBar.module.css'

export default function PlayerBar({data, tree_data}) {

    const batting_stats = tree_data.total_stats.batting_stats
    const b_stats = Object.keys(batting_stats).map(key => 
         <p>{key}:{batting_stats[key]}</p>
    )
    const pitching_stats = tree_data.total_stats.pitching_stats
    const p_stats = Object.keys(pitching_stats).map(key => 
        <p>{key}:{pitching_stats[key]}</p>
   )
    const other_stats = tree_data.total_stats.war_sal
    const o_stats = Object.keys(other_stats).map(key => 
        <p>{key}:{other_stats[key]}</p>
   )

    return ( 
        <div className={styles.PlayerBar}>
            <Link href={{
                pathname: '/players/[pid]',
                query: {pid: data.retro_id }}}>
                <a className= "playerLink"> {data.name} </a>
            </Link> 
            {b_stats}
            {p_stats}
            {o_stats}

            {/* {trades.map((trade) => {
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
            })} */}
        </div>

    )
}