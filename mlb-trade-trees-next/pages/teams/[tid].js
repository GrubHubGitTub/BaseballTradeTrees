import Image from "next/image";
import React, {useState, useMemo} from "react";
import Link from "next/link";
import players from "../../data/player_search.json"
import teams from "../../data/team_info.json"
import styles from "../../styles/RosterPage.module.css"
import PlayerCard from "../../components/PlayerCard";
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import team_info from "../../data/team_info.json";
import {VictoryPie, VictoryTooltip, VictoryContainer, VictoryLegend} from 'victory';
import { franchises } from "../../data/franchise_colors";

export async function getServerSideProps(context) {
    const player_data = players
    const team_data = teams
    const franch = context.params.tid
    const team = team_data.filter((t) => t.team_id == franch)[0]
    const tree_data = require("../../data/all_parent_trees_no_details.json")
    const team_trees = tree_data.filter((t) => t.from_franch === franch)
 

    const tid = team.mlb_id
    const res= await fetch(`https://statsapi.mlb.com/api/v1/teams/${tid}/roster`);
    const data = await res.json();
    const roster = data.roster

    var combined_ids = []
    await Promise.all(roster.map(async function(player) {
        const mlbid = Number(player.person.id)
        const filtered = player_data.filter((p) => p.mlb_id === mlbid)
             
        if (filtered.length > 0) {
            const playerdata = filtered[0];
            const pid = playerdata.retro_id;
            const name = player.person.fullName
            const position = player.position.name
            const number = player.jerseyNumber
            const combined = {retroid: pid, mlbid: mlbid, name: name, position:position, number:number}
            combined_ids.push(combined)
            }
        else{
            const name = player.person.fullName
            const position = player.position.name
            const number = player.jerseyNumber
            const combined = {name: name, position:position, number:number}
            combined_ids.push(combined)
        }
        }))
    return ({props: {combined_ids, team, team_trees}})
}

  export default function TeamPage(props) {
    const tree_data = props.team_trees

    let relationship_data = []
    team_info.map(team => {
        var relationship_num = tree_data.filter((p) => p.to_team.team_name.to_franch === team.team_id).length
        var team_name = team.name
        var teamcolor = franchises[team.team_id]
        var add_to={ name: team_name, num:relationship_num, label:team_name, color:teamcolor}
        relationship_data.push(add_to)
    })
    console.log(relationship_data)
    
    const [rowData, setRowData] = useState(tree_data)
    const [columnData, setColumnData] = useState([
        {headerName:"Tree",field:"tree_id", 
        cellRendererFramework: function(p){
            return <Link href={`/player/${p.value.slice(0,8)}/${p.value}`}>{p.value}</Link>
          }, width:130},
        {field: "from_franch", headerName:"Franchise ID", width:140},
        {field: "from_team.team_id", headerName:"Team ID", width:110},
        {field: "from_team.team_name", headerName:"Team Name"},
        {headerName:"Date", field:"date", 
        valueFormatter: p => { return `${p.value.toString().slice(0,4)}-${p.value.toString().slice(4,6)}-${p.value.toString().slice(6,8)}` },
        width:120},
        {field: "y_last", headerName:"Last Year",width:120},
        {field: "year_span", headerName:"Year Span",width:120},        
        {field: "ongoing", headerName:"Ongoing?",width:100},
        {field: "total_transac", headerName:"Transactions", width:110},
        {field: "total_stats.war_sal.WAR", headerName:"WAR", width:90 },
        {field: "total_stats.war_sal.salary", headerName:"Salary", 
        valueFormatter: p => { return `$${p.value}`}, width:130},
        {field: "total_stats.war_sal.allstars", headerName:"All Star Appearances", width:110},
        {field: "ws_wins", headerName:"World Series Winners",width:140},
        {field: "p_traded_away", headerName:"Players Traded Away",width:140},
        {field: "p_traded_for", headerName:"Players Traded For",width:140},
        {field: "total_players", headerName:"Total Players",width:140},
        
        {
            headerName: "Batting Stats",
            children: [
                { field: "total_stats.batting_stats.G", headerName:"G"},
                { field: "total_stats.batting_stats.AB", headerName:"AB",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.R", headerName:"R",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.H", headerName:"H",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.2B", headerName:"2B",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.3B", headerName:"3B",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.HR", headerName:"HR",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.RBI", headerName:"RBI",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.SB", headerName:"SB",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.BB", headerName:"BB",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.IBB", headerName:"IBB",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.SO", headerName:"SO",columnGroupShow:"open" },
                { field: "total_stats.batting_stats.HBP", headerName:"HBP",columnGroupShow:"open" },
            ]
        },
        {
            headerName: "Pitching Stats",
            children: [
                { field: "total_stats.pitching_stats.W", headerName:"W" },
                { field: "total_stats.pitching_stats.L", headerName:"L",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.G", headerName:"G",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.GS", headerName:"GS" ,columnGroupShow:"open"},
                { field: "total_stats.pitching_stats.CG", headerName:"CG",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.SHO", headerName:"SHO" ,columnGroupShow:"open"},
                { field: "total_stats.pitching_stats.SV", headerName:"SV",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.IPouts", headerName:"Innings Pitched- Outs",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.H", headerName:"H" ,columnGroupShow:"open"},
                { field: "total_stats.pitching_stats.ER", headerName:"ER" ,columnGroupShow:"open"},
                { field: "total_stats.pitching_stats.HR", headerName:"HR",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.BB", headerName:"BB",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.SO", headerName:"SO",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.HBP", headerName:"HBP" ,columnGroupShow:"open"},
                { field: "total_stats.pitching_stats.ERA_p_out", headerName:"ERA- Pitchers Out" ,columnGroupShow:"open"},
                { field: "total_stats.pitching_stats.ERA_p_in", headerName:"ERA- Pitchers In",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.BAOpp_p_out", headerName:"BAOpp Pitchers Out",columnGroupShow:"open" },
                { field: "total_stats.pitching_stats.BAOpp_p_in", headerName:"BAOpp Pitchers In",columnGroupShow:"open" },
            ]
        } 
    ])

    const defaultColDef = useMemo ( ()=> ({
        // set every column width
        resizable: true,
        // make every column editable
        sortable:true,
        // make every column use 'text' filter by default
        filter: 'agTextColumnFilter',
    }),[]);

    const roster = props.combined_ids

    const Pcards = roster.map(player => {
        if (player.position == "Pitcher"){
        
        return (
            <PlayerCard 
                key={player.name}
                player={player} 
                team = {props.team.team_id}
                />
        )}
    })
    
    const OFcards = roster.map(player => {
        if (player.position == "Outfielder"){
        
        return (
            <PlayerCard 
                key={player.name}
                player={player} 
                team = {props.team.team_id}
                />
        )}
    })
    const IFcards = roster.map(player => {
        if (player.position == "Outfielder") {}
        else if (player.position == "Pitcher") {} 
        else {
            return (
            <PlayerCard 
                key={player.name}
                player={player} 
                team = {props.team.team_id}
                />
        )}
    })

    return (
        <div className={styles.rosterPage}>
    
            <div className={styles.teamHeader}>
                <h1 >{props.team.name}</h1>
                <div className={styles.logoDiv}>
                    <Image src={`/team_logos/${props.team.team_id}.png`} alt="TeamLogo" layout="fill" objectFit="contain"/>
                </div>
            </div>

            <VictoryPie
                data={relationship_data}
                padAngle={1}
                style={{
                    data: {
                    fill: (d) => d.slice.data.color
                    }
                }}
                // padding={{ top: 200}}
                startAngle={90}
                endAngle={-90}
                x="name"
                y="num"
                
                
                labels={({ datum }) => datum.num}
                containerComponent={<VictoryContainer preserveAspectRatio="none" responsive={true}/>}
                // labelRadius={({ innerRadius }) => innerRadius + 30 }
                // style={{labels:  {fontSize: 2 }}}
                radius={({ datum }) => datum.num * 10}
                labelComponent={<VictoryTooltip/>}  
                />

            <h3 style={{"border-bottom":"1px solid black"}}>All Tree Info</h3>
            <h6>Click a column to filter and sort. Drag a column to the left to pin.</h6>

            <div className="ag-theme-alpine" style={{ height:500, width:"90%", marginLeft:"auto", marginRight:"auto" }}>
                <AgGridReact
                    reactNext={true}
                    defaultColDef={defaultColDef}
                    rowData={rowData}
                    columnDefs={columnData}>
                </AgGridReact>
            </div>
            <h3 style={{"marginTop":"10px", "border-bottom":"1px solid black"}}>Current Roster Info</h3>
            <h4 style={{"margin-bottom":"1%"}}>Click name of highlighted player to go to his page</h4>
            <div className={styles.roster}>

                <div className={styles.posContainer}>
                        
                        {Pcards}
                </div>

                <div className={styles.posContainer}>
                    

                        {OFcards}

                </div>

                <div className={styles.posContainer}>
                    

                    {IFcards}

                </div>

            </div>
        </div>
    )
  }

  export const config = {
    unstable_excludeFiles: ["../../data/all_data1.json", "../../data/all_data2.json"],
  }