import React, {useState, useMemo} from "react";
import TradeCard from "../../../components/TradeCard";
import styles from '../../../styles/PlayerPage.module.css'
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

export async function getStaticPaths() {
  const players = require("../../../data/player_search.json")

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
  const player_data2 = require("../../../data/all_data2.json")
  const players = player_data1.concat(player_data2);
  
  const pid = context.params.pid;
  const filtered = players.filter((p) => p.retro_id === pid)
  let player;
  let ongoing_trees_data = []
  if (filtered.length > 0){
    player = filtered[0]

    if (player.in_ongoing_trees.length > 0){
      player.in_ongoing_trees.map(tree_id => {
        const ongoing_tree_data = players.find(p => p.trades.find(trade => trade.tree_id == tree_id));
        ongoing_trees_data.push(ongoing_tree_data)
      })
    }
  } else {
    const non_traded_data = require("../../../data/no_trades.json")
    const non_traded_player = non_traded_data.filter((p) => p.retro_id === pid)
    player = non_traded_player[0]
  }

  return { props: {player, ongoing_trees_data} }
}

export default function PlayerPage({ player, ongoing_trees_data }) {
    const pid = player.retro_id

    if ("trades" in player){
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
  } else {

    const rowData = player.retrosheet_data
    const columnData = [
      {field: "primary_date", headerName:"Date", valueFormatter: p => { return `${p.value.toString().slice(0,4)}-${p.value.toString().slice(4,6)}-${p.value.toString().slice(6,8)}` },
      width:150},
      {field: "from_franchise", headerName:"From Franchise",width:200},
      {field: "from_team", headerName:"From Team",width:150},
      {field: "type", headerName:"Type",width:350, cellStyle:{ fontWeight: "bold" }},
      {field: "to_franchise", headerName:"To Franchise",width:200},
      {field: "to_team", headerName:"To Team",width:200},

    ]

  //   const defaultColDef = useMemo ( ()=> ({
  //     // set every column width
  //     resizable: true,
  //     // make every column editable
  //     sortable:true,
  //     // make every column use 'text' filter by default
  //     filter: 'agTextColumnFilter',
  // }),[]);

    const dynamicHeight = Math.min(rowData.length * 2.4 + 20, 400) + 'vh'

    return (
      <div className={styles.notTraded}>
        <div className={styles.playerPage} >
          <div className={styles.playerBar}>
            <h1 className={styles.playerHead}>{player.name}</h1>
            <p>Debuted in <b>{player.debut_year}</b></p>
            {player.last_year != "" &&
            <p>Last played in <b>{player.last_year}</b></p>}
          </div>
        </div>
          <div className={styles.headerBar2}>            
            <h4>This player was never traded, however you can view his transaction history below: </h4>
          </div>
            <div className="ag-theme-alpine" style={{ height:dynamicHeight, width:"75%", marginLeft:"auto", marginRight:"auto" }}>
              
              <AgGridReact
                  reactNext={true}
                  // defaultColDef={defaultColDef}
                  rowData={rowData}
                  columnDefs={columnData}>
              </AgGridReact>
            </div>
      </div>
  );
  }
}

export const config = {
  unstable_excludeFiles: ["../../../data/all_data1.json", "../../../data/all_data2.json"],
}