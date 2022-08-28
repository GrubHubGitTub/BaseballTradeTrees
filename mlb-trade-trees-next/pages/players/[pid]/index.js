import React from "react";
import PlayerBar from '../../../components/PlayerBar';
import TradeCard from "../../../components/TradeCard";
import styles from '../../../styles/PlayerPage.module.css'

export async function getStaticPaths() {
  const res = await fetch('http://localhost:3000/api/players');
  const all_data = await res.json();

  const paths = all_data.map(player => {
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
  const res = await fetch('http://localhost:3000/api/players/' + pid);
  const data = await res.json();
  return { props: {data} }
}


export default function PlayerPage({ data }) {
  console.log(data)
    const trade_num = data.trades.length
    const pid = data.retro_id

    const tradeCards = data.trades.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {pid}
      />
      )
    })

    return (
        <div>
          <PlayerBar data={data} />
          <h2>Most recent retorosheet data/ node of longest ongoing tree</h2>
          <h3>{data.name} was traded {trade_num} {trade_num == 1 ? "time" : "times"}</h3>
          <div className={styles.allCards}>{tradeCards}</div>
        </div>
  );
};

