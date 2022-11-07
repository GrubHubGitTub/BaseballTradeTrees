import React, { useState, useMemo } from "react";
import Link from "next/link";
import styles from "../../styles/SearchPage.module.css"
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

export async function getStaticProps() {
    const tree_data = require("../../data/all_parent_trees_no_details.json")
    return { props: {tree_data} }
}

export default function SearchPage({tree_data}) {

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

    return (
        <div className={styles.searchPage}>
        <h5 className={styles.Note}>Click a column to filter and sort. Drag a column to the left to pin.</h5>
        <div className="ag-theme-alpine" style={{height: "80vh", maxWidth:"2550px", marginTop: "1%", marginLeft:"auto", marginRight:"auto"}}>
           <AgGridReact
               reactNext={true}
               defaultColDef={defaultColDef}
               rowData={rowData}
               columnDefs={columnData}>
           </AgGridReact>
       </div>
       <h5 className={styles.Note}>Note- this is a list of all parent trade trees, meaning they are the largest version of each tree with no older transaction.</h5>

        </div>
        )
}