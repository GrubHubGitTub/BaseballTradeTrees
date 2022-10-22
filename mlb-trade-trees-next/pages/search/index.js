import React, {useState, useEffect} from "react";
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
        {field: "ws_wins", sortable:true, filter:true }
    ])

    // // useEffect(() => {
    // //     setRowData(searchResults); 
    // //   }, [searchResults]);
        
    // const handleSearch = async (event) => {
    //     event.preventDefault()

    //     const searchData = {
    //         team: event.target.team.value
    //     } 

    //     const JSONdata = JSON.stringify(searchData)
    //     const endpoint = "/api/tree_search"

    //     const options = {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json"
    //         },
    //         body: JSONdata
    //     }
    //     const response = await fetch(endpoint, options)
    //     const result = await response.json()
    //     setRowData(result)
    //     console.log(rowData)
    // }

    return (
        <div>
            <h1>Sort and search through every trade tree available:</h1>
            <form >
                <input type="text" id="team" name="team"
                     placeholder="Team name or location"> 
                </input>
                {/* <input type="text" id="year" name="year"></input> */}
                <button type="submit">Search</button>
            </form>

        <div className="ag-theme-alpine" style={{height: 400, width: 600}}>
           <AgGridReact
               rowData={rowData}
               columnDefs={columnData}>
           </AgGridReact>
       </div>
        </div>
        )
}