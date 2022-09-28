import React from "react";
import player_data from "../../../data/output.json"
import PlayerBar from '../../../components/PlayerBar';
import TradeCard from "../../../components/TradeCard";
import styles from '../../../styles/PlayerPage.module.css'

export async function getStaticPaths() {

  const paths = player_data.map(player => {
    return {
      params: { pid: player.retro_id }
    }
  })
  
  return { 
    paths, 
    fallback: false 
  }
}

export const getStaticProps = async (context) => {
  const pid = context.params.pid;
  const filtered = player_data.filter((p) => p.retro_id === pid || p.mlbid === pid)
  const data = filtered[0]
  return { props: {data} }
}


export default function PlayerPage({ data }) {
    const trade_num = data.trades.length
    const pid = data.retro_id
    console.log(data)
    const tradeCards = data.trades.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {pid}
                  key = {pid}
      />
      )
    })

    return (
        <div>
          {/* <PlayerBar data={data} /> */}
          {/* <h2>Most recent retorosheet data/ node of longest ongoing tree</h2> */}
          <h3 className={styles.playerHead}>{data.name}'s trade trees:</h3>
          <div className={styles.cardContainer}>
            {tradeCards}
          </div>
        </div>
  );
};

