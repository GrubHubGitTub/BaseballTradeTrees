import { OrgChart } from "d3-org-chart";
import player_data from "../../../../data/output.json"
import React, {useEffect, useRef} from "react";
import * as d3 from 'd3'
import PlayerBar from "../../../../components/PlayerBar";
import styles from '../../../../styles/TreePage.module.css'
import Image from 'next/image'

export const getStaticPaths = async (context) => {
    const paths = player_data
      .map((player) =>
        player.trades.map((trade) => ({
          params: {
            pid: player.retro_id,
            treeid: trade.tree_id,
          },
        }))
      )
      .flat();

    return { paths, fallback: false };
};
  
export const getStaticProps = async (context) => {
    const pid = context.params.pid;
    const filtered = player_data.filter((p) => p.retro_id === pid || p.mlbid === pid)
    const data = filtered[0]
    let tree_data;

    data.trades.forEach((element) => {
        if (element.tree_id == context.params.treeid) {
            tree_data = element
        }
    })
    return { props: {data, tree_data} }
}

            
export const OrgChartComponent = (props, ref) => {
    const d3Container = useRef(null);
    let chart = null;
    console.log(props.data)

    useEffect(() => {
        if (props.data && d3Container.current) {
        if (!chart) {
            chart = new OrgChart();
        }
        chart
            .svgHeight(window.innerHeight - 218)
            .container(d3Container.current)
            .data(props.data)
            .onNodeClick((d) => {
              const nodeData = props.data.find(node => node.id === d);
              const trade_in_stats = nodeData.trade_in_stats
              const trade_out_stats = nodeData.trade_out_stats
              chart.clearHighlighting()
              chart.setHighlighted(d).render()
              props.onNodeClick(d, trade_in_stats, trade_out_stats)
            })
            .nodeWidth((d) => 300)
            .initialZoom(0.3)
            .nodeHeight((d) => 225)
            .childrenMargin((d) => 40)
            .compactMarginBetween((d) => 15)
            .compactMarginPair((d) => 80)
             chart.connections(props.connections)
            .nodeContent(function (d, i, arr, state) {
              if ("transaction_id" in d.data) {
                // format date
                const year = d.data.date.toString().slice(0,4)
                const month = d.data.date.toString().slice(4,6)
                const day = d.data.date.toString().slice(6,8)

                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = d.data.name
                } else {
                  name = "<a style='color: black' href='../" + d.data.retro_id + "'>" + d.data.name + "</a>"; 
                }
                // end name url

                // create url for players with pages, otherwise just write name
                const traded_with_players = "With: "
                if (Object.keys(d.data.traded_with).length > 0) {
                  for (var k in d.data.traded_with) {
                    if (k.includes(" ") || k.includes("PTBNL/Cash")){
                       traded_with_players = traded_with_players + d.data.traded_with[k] + " ";
                  } else {
                        traded_with_players = traded_with_players + "<a style='color: black' href='../" + k + "'>" + d.data.traded_with[k] + "</a> ";
                    }
                  }
                } 
                if (traded_with_players == "With: "){
                  traded_with_players = ""
                }
                // end traded_with check

                // set node color based on WAR
                let outline;
                if (d.data.trade_totals.other_stats.WAR >= 0){
                  outline = "DarkGreen"
                } else {
                  outline = "Maroon"
                }
                // end outline 

                return `
                <div style="
                  border:3px solid ${outline};
                  border-radius: 50px;
                  height:${d.height}px;
                  text-align: center"
                >

                  <h1 style="font-size: 2.6em"> ${name} </h1>
                  <div style= background-color:${outline};height:5px;"></div>

                  <div style="display: flex; flex-direction:column; justify-content: space-between;" >
                      <div style="display: flex; justify-content: center;">

                        <h2 style="padding-top:15px"> → ${d.data.to_team.team_name} </h2>
                        
                        <img src="/team_logos/TOR_logo.png" alt="team logo"
                        style="
                        width:50px;
                        height:50px;
                        "/>

                      </div>

                      <h3> ${traded_with_players} </h2>
                      <h2> ${year}-${month}-${day} </h2>
                      <h2> ${d.data.trade_totals.other_stats.WAR} WAR </h2>

                    </div>
                    
                </div>
                `
              } else if ("outcome" in d.data) {
                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = d.data.name
                } else {
                  name = "<a style='color: black' href='../" + d.data.retro_id + "'>" + d.data.name + "</a>"; 
                }
                // end name url
                let outline;
                if (d.data.outcome == "No further transactions, likely in organization"){
                  outline = "DodgerBlue"
                } else {
                  outline = "black"
                }

                // format date
                const year = d.data.date.toString().slice(0,4)
                const month = d.data.date.toString().slice(4,6)
                const day = d.data.date.toString().slice(6,8)

                return `
                <div style="
                  border:1px solid ${outline};
                  border-radius: 50px;
                  text-align:center;
                  height:${d.height}px;"
                >

                    <h1 style="
                    color: #111672;
                    font-weight: bold;
                    margin: 2% 0"> 
                    ${name} 
                    </h1>

                    <div style= background-color:${outline};height:5px;"></div>

                    <h1 style="margin-top:10%"> ${d.data.outcome} </h1>
                    <h2> ${year}-${month}-${day} </h2>
                  
                </div>
                `
                
              } else if ("info" in d.data){
                
                const info = d.data.info

                return `
                <div style="
                  border:1px solid black;
                  border-radius: 50px;
                  text-align:center;
                  height:${d.height}px;"
                >

                    <h1 style="
                    color: #111672;
                    font-weight: bold;
                    margin: 2% 0"> 
                    ${d.data.name} 
                    </h1>

                    <div style= background-color:black;height:5px;"></div>

                    <h2 style="margin-top:10%"> ${info} </h2>
                    
                </div>
                `
              } else {
                return `
                <div style="
                  border:1px solid black;
                  border-radius: 50px;
                  text-align:center;
                  height:${d.height}px;"
                >

                    <h1 style="
                    color: #111672;
                    font-weight: bold;
                    margin: 2% 0"> 
                    ${d.data.name} 
                    </h1>

                    <div style= background-color:black;height:5px;"></div>

                    <h2 style="margin-top:10%"> Part of different transaction in tree </h2>
                    
                </div>
                `
              }
            ;  
            })
            .render();
            chart.expandAll()
        }
    }, [props.data, d3Container.current]);
    
    return (
        
        <div ref={d3Container} className={styles.treeContainer}/>
        
    );
    };

export default function TreePage({ data, tree_data }) {
    const treeDisplay = tree_data.tree_details.tree_display
    const connections = tree_data.tree_details.connections
    const [statsInBat, setStatsInBat] = React.useState("Click a transaction to view stats")
    const [statsInPitch, setStatsInPitch] = React.useState("")
    const [statsOutBat, setStatsOutBat] = React.useState("Click a transaction to view stats")
    const [statsOutPitch, setStatsOutPitch] = React.useState("")

    function onNodeClick(nodeId, trade_in_stats, trade_out_stats) {

      if (trade_out_stats != undefined) {
        let trade_out_bat_table = [];
        let trade_out_pitch_table = [];
        {trade_out_stats.map(player => {
          if (player.batting_stats.length > 0) {
            trade_out_bat_table.push(
              <table className={styles.statTable}>
                <tr key={"header"}>
                  {Object.keys(player["batting_stats"][0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
                {player.batting_stats.map((item ) => (
                  <tr key={item.yearID}>
                    {Object.values(item).map((val,i) => (
                      <td key={i}>{val}</td>
                    ))}
                  </tr>
                ))}
              </table>
            );            
          } else {
            trade_out_bat_table = []
          }
          if (player.pitching_stats.length > 0) {
            trade_out_pitch_table.push(
              <table className={styles.statTable}>
                <tr key={"header"}>
                  {Object.keys(player["pitching_stats"][0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
                {player.pitching_stats.map((item ) => (
                  <tr key={item.playerID}>
                    {Object.values(item).map((val, i) => (
                      <td key={i}>{val}</td>
                    ))}
                  </tr>
                ))}
              </table>
            );            
          } else {
            trade_out_pitch_table = []
          }
        })}
        setStatsOutBat(trade_out_bat_table)
        setStatsOutPitch(trade_out_pitch_table) 
      } else {
        setStatsOutBat("No stats - not a transaction")
        setStatsOutPitch("") 
      }
      if (trade_in_stats != undefined) {
        let trade_in_bat_table = [];
        let trade_in_pitch_table = [];
        {trade_in_stats.map(player => {

          if (player.batting_stats.length > 0) {
            trade_in_bat_table.push(
              <table className={styles.statTable}>
                <tr key={"header"}>
                  {Object.keys(player["batting_stats"][0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>

                {player.batting_stats.map((item ) => (
                  <tr key={item.yearID}>
                    {Object.values(item).map((val, i) => (
                      <td key={i}>{val}</td>
                    ))}
                  </tr>
                ))}
              </table>
            );            
          } else {
            trade_in_bat_table = []
          }
          if (player.pitching_stats.length > 0) {
            trade_in_pitch_table.push(
              <table className={styles.statTable}>
                <tr key={"header"}>
                  {Object.keys(player["pitching_stats"][0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
                {player.pitching_stats.map((item ) => (
                  <tr key={item.playerID}>
                    {Object.values(item).map((val,i) => (
                      <td key={i}>{val}</td>
                    ))}
                  </tr>
                ))}
              </table>
            );            
          } else {
            trade_in_pitch_table = []
          }
        })}
        setStatsInBat(trade_in_bat_table)
        setStatsInPitch(trade_in_pitch_table) 
      } else {
        setStatsInBat("No stats - not a transaction")
        setStatsInPitch("") 
      }
    }

    return (
        <div className={styles.treePage}>

          <PlayerBar data={data} tree_data={tree_data}/>
          
          <OrgChartComponent
              data={treeDisplay}
              onNodeClick={onNodeClick}
              connections={connections}
          />
        <div className={styles.statsContainer}> 
          <div className={styles.statBoxOut}>
              <p>Players Traded Away</p>
              {statsOutBat}
              {statsOutPitch}
          </div>
          <div className={styles.statBoxIn}>
              <p>Players Traded For</p>
              {statsInBat}
              {statsInPitch}
          </div>
        </div> 
      </div>
    );
  };
    