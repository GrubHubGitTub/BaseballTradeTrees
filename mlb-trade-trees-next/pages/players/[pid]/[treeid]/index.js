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

    useEffect(() => {
        if (props.data && d3Container.current) {
        if (!chart) {
            chart = new OrgChart();
        }
        chart
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
            .nodeWidth((d) => 250)
            .initialZoom(0.7)
            .nodeHeight((d) => 175)
            .childrenMargin((d) => 40)
            .compactMarginBetween((d) => 15)
            .compactMarginPair((d) => 80)
             chart.connections(props.connections)
            .nodeContent(function (d, i, arr, state) {
              if ("transaction_id" in d.data) {
                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = d.data.name
                } else {
                  name = "<a href='../" + d.data.retro_id + "'>" + d.data.name + "</a>"; 
                }
                // end name url

                // create url for players with pages, otherwise just write name
                const traded_with_players = ""
                if (Object.keys(d.data.traded_with).length > 0) {
                  for (var k in d.data.traded_with) {
                    if (k.includes(" ")){
                       traded_with_players = traded_with_players + d.data.traded_with[k] + " ";
                  } else {
                        traded_with_players = traded_with_players + "<a href='../" + k + "'>" + d.data.traded_with[k] + "</a> ";
                  }
                }
              }
                // end traded_with check

                // choose stats to display on node
                // let WAR;
                // for (var k in d.data.trade_totals.) {
                  
                // }
                
                return `
                <div className='treeNode' style="
                  height:${d.height - 32}px;
                  border:1px solid lightgray;"
                >

                  <div style="
                  padding-top:10px;
                  text-align:center"
                  >
                    <div style="
                    color:#111672;
                    font-size:20px;
                    font-weight:bold"
                    > 
                      ${name}
                      ${traded_with_players}
                      ${d.data.to_team.team_name}
                      ${d.data.trade_totals.other_stats.WAR}   
                    </div>
                  </div>

                  <img src="/team_logos/${d.data.to_franch}_logo.png" alt="team logo"
                    style="
                      margin-top:-0px;
                      margin-left:${d.width / 2 - 30}px;
                      border-radius:100px;
                      width:60px;
                      height:60px;
                  "/>
                  
                </div>
                `
              } else if ("outcome" in d.data) {
                return `
                <!--outer div-->
                <div style=
                             "height:${d.height - 32}px;
                                padding-top:0px;
                                background-color:white;
                                border:1px solid lightgray;">
                <!---->
                    <img src=" ${
                                    d.data.imageUrl
                                  }"
                         style="margin-top:-0px;margin-left:${d.width / 2 - 30}px;border-radius:100px;width:60px;height:60px;"/>
                
                    <div style="margin-right:10px;margin-top:15px;float:right">${
                        d.data.id
                        }
                    </div>
                
                    <div style="margin-top:-30px;background-color:#3AB6E3;height:10px;width:${
                                   d.width - 2
                                 }px;border-radius:1px"></div>
                
                <!--name and centering-->
                    <div style="padding:10px; padding-top:35px;text-align:center">
                        <div style="color:#111672;font-size:16px;font-weight:bold"> ${
                            d.data.name
                            }
                        </div>
                    </div>
                <!---->
                    <div style="display:flex;justify-content:space-between;padding-left:15px;padding-right:15px;">
                        <div> Manages: ${d.data._directSubordinates} 👤</div>
                        <div> Oversees: ${d.data._totalSubordinates} 👤</div>
                    </div>
                </div>
                `
              } else{
                return `
                <!--outer div-->
                <div style=
                             "height:${d.height - 32}px;
                                padding-top:0px;
                                background-color:white;
                                border:1px solid lightgray;">
                <!---->
                    <img src=" ${
                                    d.data.imageUrl
                                  }"
                         style="margin-top:-0px;margin-left:${d.width / 2 - 30}px;border-radius:100px;width:60px;height:60px;"/>
                
                    <div style="margin-right:10px;margin-top:15px;float:right">${
                        d.data.id
                        }
                    </div>
                
                    <div style="margin-top:-30px;background-color:#3AB6E3;height:10px;width:${
                                   d.width - 2
                                 }px;border-radius:1px"></div>
                
                <!--name and centering-->
                    <div style="padding:10px; padding-top:35px;text-align:center">
                        <div style="color:#111672;font-size:16px;font-weight:bold"> ${
                            d.data.name
                            }
                        </div>
                    </div>
                <!---->
                    <div style="display:flex;justify-content:space-between;padding-left:15px;padding-right:15px;">
                        <div> Manages: ${d.data._directSubordinates} 👤</div>
                        <div> Oversees: ${d.data._totalSubordinates} 👤</div>
                    </div>
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
    