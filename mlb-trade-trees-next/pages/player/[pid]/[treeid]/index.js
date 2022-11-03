import * as d3 from 'd3'
import { OrgChart } from "../../../../org-chart-master";
import React, {useEffect, useRef} from "react";
import PlayerBar from "../../../../components/PlayerBar";
import styles from '../../../../styles/TreePage.module.css'

export async function getStaticPaths() {
  const player_data1 = require("../../../../data/all_data1.json")
  const player_data2 = require("../../../../data/all_data2.json")
  const players = player_data1.concat(player_data2);

  const paths = players
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
}
  
export async function getStaticProps(context) {
  const player_data1 = require("../../../../data/all_data1.json")
  const player_data2 = require("../../../../data/all_data2.json")
  const players = player_data1.concat(player_data2);

    const pid = context.params.pid;
    const filtered = players.filter((p) => p.retro_id === pid)
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

    function saveChart(){
      chart.addNode({id:"saved",parentId:1,name:"saveButton"})
      chart.exportImg({full:true,  filename: "test"})
    }

    props.setClick(saveChart)

    useEffect(() => {
        if (props.data && d3Container.current) {
        if (!chart) {
            chart = new OrgChart();
        }
        chart
            .svgHeight(document.querySelector("#treeContainer").getBoundingClientRect().height - 1)
            .container(d3Container.current)
            .data(props.data)

            .onNodeClick((d) => {
              const nodeData = props.data.find(node => node.id === d);
              if ("transaction_id" in nodeData){
                chart.setCentered(d).initialZoom(0.5).render()}
              
              const trade_in_stats = nodeData.trade_in_stats
              const trade_out_stats = nodeData.trade_out_stats
              
              props.onNodeClick(trade_in_stats, trade_out_stats)
            })

            .nodeWidth((d) => {
                if ("traded_with" in d.data && (!("trade_totals" in d.data))) return 450
                else if ("traded_with" in d.data && Object.keys(d.data.traded_with).length >= 1) return 500
                else return 500
            })
            .nodeHeight((d) => {
              if ("traded_with" in d.data && (!("trade_totals" in d.data))) return 265
              else if ("traded_with" in d.data && Object.keys(d.data.traded_with).length >= 5) return 490
              else if ("traded_with" in d.data && Object.keys(d.data.traded_with).length >= 1) return 390
              else if ("outcome" in d.data || d.data.name === "PTBNL/Cash") return 300
              else return 350 
          })
            .childrenMargin((d) => 60)
            .compactMarginBetween((d) => 15)
            .compactMarginPair((d) => 40)
            .connections(props.connections)
            .nodeContent(function (d, i, arr, state) {
              const franchises = {"ANA": "Maroon", "ARI":"Maroon", "ATL":"Maroon", "BAL":"darkOrange", "BOS":"maroon", "CHC":"darkBlue", "CHW":"Darkgrey", 
    "CIN":"Maroon", "CLE":"Red", "COL":"Purple","DET":"navyblue", "FLA":"coral", "HOU":"orange", "KCR":"royalblue", 
    "LAD": "dodgerblue","MIL":"navyblue","MIN":"maroon", "NYM":"orange","NYY":"white","OAK":"darkgreen", "PHI": "red", 
    "PIT":"Gold","SDP":"lightbrown","SEA":"navyblue","SFG":"orange", "STL":"red", "TBD":"darkblue", "TEX":"red","TOR":"blue","WSN":"maroon"}

              
              if (d.data.name == "saveButton") {
                return "<h1> Tree downloaded from mlbtradetrees.com </h1>"
              }
              // Comp pick node
              if ("transaction_id" in d.data && "info" in d.data) {
                // format date
                const year = d.data.date.toString().slice(0,4)
                const month = d.data.date.toString().slice(4,6)
                const day = d.data.date.toString().slice(6,8)

                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = `<h2 style="
                  box-shadow: 0 2px 2px 2px rgba(9, 9, 9, 0.23);
                  border:1px solid black;
                  border-radius:20px;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h2>`
                } else {
                  name = `
                  <a style="
                  text-decoration: none; 
                  " 
                  href="../${d.data.retro_id}"> <h1 style="
                  box-shadow: 0 5px 2px 2px rgba(9, 9, 9, 0.23);
                  border:1px solid black;
                  border-radius:20px;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h1> </a> `
                }
                // end name url
                const outline = "Orange"

                return `
                <div class="treeNode" style="
                  border:8px solid ${outline};
                  border-radius: 50px;
                  height:${d.height}px;
                  "
                >
                  ${name}
                  <div style= background-color:${outline};height:5px;"></div>
                 
                      
                  <div style="display: flex; flex-direction:column;align-items: center;justify-content:center;text-align:center" >

                      <h2> Compensation picks for leaving team on: </h2>
                      <h2 style="margin-top:10px"> ${year}-${month}-${day} </h2>

                  </div>
                    
                </div>
                `
              // regular transaction node
              } else if ("transaction_id" in d.data){
                // format date
                const year = d.data.date.toString().slice(0,4)
                const month = d.data.date.toString().slice(4,6)
                const day = d.data.date.toString().slice(6,8)

                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = `<h2 style="
                  border:1px solid black;
                  border-radius:20px;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h2>`
                } else {
                  name = `
                  <a style="
                  text-decoration: none; 
                  " 
                  href="../${d.data.retro_id}"> <h1 style="
                  box-shadow: 0 5px 2px 2px rgba(9, 9, 9, 0.23);
                  border:1px solid black;
                  border-radius:20px;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h1> </a> `
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
                
                // check for Allstars'
                let allstars = []
                if (d.data.trade_totals.other_stats.allstars > 0) {
                  allstars = `<img src="/team_logos/as.png" alt="AllStar"
                  style="
                  position: absolute;
                  bottom:25px;
                  left:20px;
                  width:50px;
                  height:50px;
                  "/>`
                }
                let link
                const to_franch = d.data.to_team.team_name.to_franch
                if (to_franch in franchises) {
                    link = `/team_logos/${to_franch}.png`
                }
                else{
                    link = `/team_logos/MLB.png`
                }

                return `
                <div class="treeNode" style="
                  border:8px solid ${outline};
                  border-radius: 50px;
                  height:${d.height}px;
                  position:relative;
                  "
                >
                  ${name}
                  <div style= background-color:${outline};height:5px;"></div>
                 
                      <div style="display: flex; justify-content: center; align-items:center">
                        <h2 style="padding-top:15px;padding-right:10px;font-size:2.3em"> → ${d.data.to_team.team_name.name} </h2>
                        <div style="width:75px;height:75px">
                          <img src=${link} alt="team logo"
                          style="
                          padding:10px;
                          max-width:100%;
                          max-height:100%;
                          "/>
                        </div>
                      </div>
                      
                    <div style="display: flex; flex-direction:column;align-items: center;justify-content:center;text-align:center" >

                        <h2> ${traded_with_players} </h2>
                        <h2 style="margin-top:10px"> ${year}-${month}-${day} </h2>
                        <h2 style="margin-top:10px"> ${d.data.trade_totals.other_stats.WAR} WAR </h2>

                    </div>
                  ${allstars}
                    
                </div>
                `
              // did not play in MLB node
              } else if ("outcome" in d.data && (!("date" in d.data))) {
                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = `<h2 style="
                  border:1px solid black;
                  border-radius:20px;
                  color:black;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h2>`
                } else {
                  name = `
                  <a style="
                  text-decoration: none; 
                  " 
                  href="../${d.data.retro_id}"> <h1 className="nodePlayer" style="
                  box-shadow: 0 2px 2px 2px rgba(9, 9, 9, 0.23);
                  border:1px solid black;
                  border-radius:20px;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h1> </a> `
                }
                // end name url

                let outline;
                if (d.data.outcome == "No further transactions, likely in organization"){
                  outline = "DodgerBlue"
                } else {
                  outline = "black"
                }

                return `
                <div class="outcomeNode" style="
                  border:1px solid ${outline};
                  border-radius: 50px;
                  height:${d.height}px;
                  "
                >
                  ${name}
                  <div style= background-color:${outline};height:5px;"></div>
                  <div style="display: flex; flex-direction:column;align-items: center;justify-content:center;text-align:center" >

                    <h2 style="margin-top:10%"> ${d.data.outcome} </h2>
                  </div>
                </div>
                `
              // regular outcome node
              } else if ("outcome" in d.data) {
                // create url for player if he has a page
                let name;
                if (d.data.retro_id.includes(" ") || d.data.retro_id.includes("PTBNL/Cash")) {
                  name = `<h2 style="
                  border:1px solid black;
                  border-radius:20px;
                  color:black;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h2>`
                } else {
                  name = `
                  <a style="
                  text-decoration: none; 
                  " 
                  href="../${d.data.retro_id}"> <h1 style="
                  box-shadow: 0 5px 2px 2px rgba(9, 9, 9, 0.23);
                  border:1px solid black;
                  border-radius:20px;
                  font-size: 2.6em;
                  margin:25px; 
                  text-align:center;
                  ">  ${d.data.name} </h1> </a> `
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
                <div class="outcomeNode" style="
                  border:1px solid ${outline};
                  border-radius: 50px;
                  height:${d.height}px;
                  "
                >
                  ${name}
                  <div style= background-color:${outline};height:5px;"></div>
                  <div style="display: flex; flex-direction:column;align-items: center;justify-content:center;text-align:center" >

                    <h2 style="margin-top:10%"> ${d.data.outcome} </h2>
                    <h2> ${year}-${month}-${day} </h2>
                  </div>
                </div>
                `  
              // PTBNL node
              } else if ("info" in d.data){
                
                const info = d.data.info

                return `
                <div class="outcomeNode" style="
                  border:1px solid black;
                  border-radius: 50px;
                  text-align:center;
                  height:${d.height}px;"
                >

                <h2 style="
                border:1px solid black;
                border-radius:20px;
                color:black;
                font-size: 2.6em;
                margin:25px; 
                text-align:center;
                ">  ${d.data.name} </h2>

                    <div style= background-color:black;height:5px;"></div>

                    <h2 style="margin-top:10%"> ${info} </h2>
                    
                </div>
                `
              } else 

              // continuation node
              {
                return `
                <div style="
                  border:1px solid black;
                  border-radius: 50px;
                  text-align:center;
                  height:${d.height}px;"
                >

                <h2 style="
                border:1px solid black;
                border-radius:20px;
                color:black;
                font-size: 2.6em;
                margin:25px; 
                text-align:center;
                ">  ${d.data.name} </h2>

                    <div style= background-color:black;height:5px;"></div>

                    <h2 style="margin-top:10%"> Part of different transaction in tree </h2>
                    
                </div>
                `
              }
            ;  
            
            })
            .render()
            .fit();
            chart.expandAll()
        }
    }, [props.data, d3Container.current]);
    
    return (
        <div ref={d3Container}/>
    );
    };

export default function TreePage({ data, tree_data }) {
    const treeDisplay = tree_data.tree_details.tree_display
    const connections = tree_data.tree_details.connections
    const [statsInBat, setStatsInBat] = React.useState("")
    const [statsInPitch, setStatsInPitch] = React.useState("")
    const [statsOutBat, setStatsOutBat] = React.useState("")
    const [statsOutPitch, setStatsOutPitch] = React.useState("")
      

    function onNodeClick(trade_in_stats, trade_out_stats) {
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
        setStatsOutBat("")
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
        setStatsInBat("")
        setStatsInPitch("") 
      }
    }

    let saveButtonPass = null
    function saveButton() {
      saveButtonPass()
    }

    return (
        <div className={styles.treePage}>

          <PlayerBar data={data} tree_data={tree_data}/>
          <div id="treeContainer" className={styles.treeContainer}>
            <h6 className={styles.clickNode}>Click a transaction node to view stats</h6>
            <button className={styles.saveButton} onClick={()=>saveButton()}>Save as image</button>
            <OrgChartComponent
                setClick={click => (saveButtonPass = click)}
                data={treeDisplay}
                onNodeClick={onNodeClick}
                connections={connections}
            />
          </div>
          
        <div className={styles.statsContainer}> 
          <div className={styles.statBoxOut}>
              <h4 className={styles.tableHeader}>Players Traded Away</h4>
              {statsOutBat}
              {statsOutPitch}
          </div>
          <div className={styles.statBoxIn}>
              <h4 className={styles.tableHeader}>Players Traded For</h4>
              {statsInBat}
              {statsInPitch}
          </div>
        </div> 
      </div>
    );
  };
  
export const config = {
    unstable_excludeFiles: ["../../../../data/all_data1.json", "../../../../data/all_data2.json"],
  }