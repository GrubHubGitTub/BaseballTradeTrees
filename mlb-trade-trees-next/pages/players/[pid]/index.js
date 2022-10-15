import React from "react";
import TradeCard from "../../../components/TradeCard";
import styles from '../../../styles/PlayerPage.module.css'
// import { getData } from "../../../data/data";

export async function getStaticPaths() {
  const player_data1 = require("../../../data/all_data1.json")
  const player_data2 = require("../../../data/all_data1.json")
  const players = player_data1.concat(player_data2);
  // const players = getData();
  // const player_data1 = require("../data/all_data1.json")
  // const player_data2 = require("../data/all_data2.json")
  // const players = player_data1.concat(player_data2);

  const paths = players.map(player => {
    return {
      params: { pid: player.retro_id }
    }
  })
  
  
  return { 
    paths, fallback: false
  }
}

export async function getStaticProps(context){
  const player_data1 = require("../../../data/all_data1.json")
  const player_data2 = require("../../../data/all_data1.json")
  const players = player_data1.concat(player_data2);
  
  const pid = context.params.pid;
  const filtered = players.filter((p) => p.retro_id === pid)
  const player = filtered[0]

  let ongoing_trees_data = []
  if (player.in_ongoing_trees.length > 0){
    player.in_ongoing_trees.map(tree_id => {
      const ongoing_tree_data = players.find(p => p.trades.find(trade => trade.tree_id == tree_id));
      ongoing_trees_data.push(ongoing_tree_data)
    })
  }

  return { props: {player, ongoing_trees_data} }
}

export default function PlayerPage({ player, ongoing_trees_data }) {
    const pid = player.retro_id

    let ongoingCards = []
    if(player.in_ongoing_trees.length > 0){
      ongoing_trees_data.map(p => {
          p.trades.map(trade => {
            if (player.in_ongoing_trees.includes(trade.tree_id)){
          ongoingCards.push(
            <TradeCard data = {trade}
              pid = {p.retro_id}
              key = {p.retro_id}
          />)     
        }
      })
    })
  }
    const inCards = ongoingCards.map(card => {
      return card
    })
    
    const tradeCards = player.trades.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {pid}
                  key = {pid}
      />
      )
    })

    return (
        <div className={styles.playerPage}>
          <div className={styles.playerBar}>
            <h1 className={styles.playerHead}>{player.name}</h1>
            <p>Debuted in <b>{player.debut_year}</b></p>
            {player.last_year != "" &&
            <p>Last played in <b>{player.last_year}</b></p>}
          </div>
            {ongoingCards.length > 0 &&
            <div className={styles.headerBar}>
              <h3 >In ongoing:</h3>
            </div>
            }
          <div className={styles.cardContainer}>
            {inCards}
          </div>
          <div className={styles.headerBar}>
            <h3 >Traded from:</h3>
          </div>
          <div className={styles.cardContainer}>
            {tradeCards}
          </div>
        </div>
  );
};

