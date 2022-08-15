import React from "react"
import Link from 'next/link'
import styles from '../styles/PlayerBar.module.css'

export default function PlayerBar({data}) {

    const trades = data.trades

    return ( 
        <div className={styles.PlayerBar}>
            <Link href={{
                pathname: '/players/[pid]',
                query: {pid: data.retro_id }}}>
                <a className= "playerLink"> {data.retro_id} </a>
                </Link> 
            {trades.map((trade) => {
                return (<Link 
                            key={trade.tree_id}
                            href={{
                                pathname: '/players/[pid]/[treeid]',
                                query: { pid: data.retro_id, treeid: trade.tree_id }
                            }}>   
                            <a className="treeLink" > 
                            {trade.tree_id} 
                            </a>
                        </Link>
                    )
            })}
        </div>

    )
}