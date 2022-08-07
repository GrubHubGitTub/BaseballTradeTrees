import React from "react";
import Link from "next/link";
import PlayerBar from '../../../components/PlayerBar'

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
    const trade_num = data.trades.length
    return (
        <div>
            <PlayerBar data={data} />
            <h1>{data.name} was traded {trade_num} {trade_num < 2 ? "time" : "times"}</h1>
        </div>
  );
};

