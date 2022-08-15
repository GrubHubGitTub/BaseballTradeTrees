import { OrgChart } from "d3-org-chart";
import React, {useEffect, useRef} from "react";
import * as d3 from 'd3'
import PlayerBar from "../../../../components/PlayerBar";
import styles from '../../../../styles/TreePage.module.css'
import { player_data } from "../../../../data/player_data";

export const getStaticPaths = async (context) => {
    const res = await fetch('http://localhost:3000/api/players');
    const all_data = await res.json();
    const paths = all_data
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
    const res = await fetch('http://localhost:3000/api/players/' + pid);
    const data = await res.json();
    let tree_data;

    data.trades.forEach((element) => {
        if (element.tree_id == context.params.treeid) {
            tree_data = element.tree_details
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
              const dataIn = nodeData.trade_in_stats
              const dataOut = nodeData.trade_out_stats
              chart.clearHighlighting()
              chart.setHighlighted(d).render()
              props.onNodeClick(d, dataIn, dataOut)
            })
            .nodeWidth((d) => 250)
            .initialZoom(0.7)
            .nodeHeight((d) => 175)
            .childrenMargin((d) => 40)
            .compactMarginBetween((d) => 15)
            .compactMarginPair((d) => 80)
            .nodeContent(function (d, i, arr, state) {
              return `
              <div style="padding-top:30px;background-color:none;margin-left:1px;height:${
                d.height
              }px;border-radius:2px;overflow:visible">
                <div style="height:${
                  d.height - 32
                }px;padding-top:0px;background-color:white;border:1px solid lightgray;">
  
                  <img src=" ${
                    d.data.imageUrl
                  }" style="margin-top:-0px;margin-left:${d.width / 2 - 30}px;border-radius:100px;width:60px;height:60px;" />
  
                 <div style="margin-right:10px;margin-top:15px;float:right">${
                   d.data.id
                 }</div>
                 
                 <div style="margin-top:-30px;background-color:#3AB6E3;height:10px;width:${
                   d.width - 2
                 }px;border-radius:1px"></div>
  
                 <div style="padding:20px; padding-top:35px;text-align:center">
                     <div style="color:#111672;font-size:16px;font-weight:bold"> ${
                       d.data.name
                     } </div>
                 </div> 
                 <div style="display:flex;justify-content:space-between;padding-left:15px;padding-right:15px;">
                   <div > Manages:  ${d.data._directSubordinates} 👤</div>  
                   <div > Oversees: ${d.data._totalSubordinates} 👤</div>    
                 </div>
                </div>     
        </div>
    `;
            })
            .render();
        }
    }, [props.data, d3Container.current]);
    
    return (
        <div>
        <div ref={d3Container} />
        </div>
    );
    };

export default function TreePage({ data, tree_data }) {
    const treeData = tree_data.tree_display
    const [statsIn, setStatsIn] = React.useState([])
    const [statsOut, setStatsOut] = React.useState([])

    function onNodeClick(nodeId, dataIn, dataOut) {
      setStatsIn(dataIn)
      setStatsOut(dataOut)
    }

    return (
        <div>
        <PlayerBar data={data}/>
        
        <div className={styles.statBox}>
          {statsIn.map(player => {
            return (
              <div>
              <p key={player.id}>name: {player.name}</p>
              <p>Stats in: {player.WARout}</p>
              </div>
            )
          })}
        </div>
        
        <OrgChartComponent
            data={treeData}
            onNodeClick={onNodeClick}
        />
        </div>
    );
    };
    