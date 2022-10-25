import Head from 'next/head';
import React, {useState} from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import styles from '../styles/Home.module.css';
import TradeCard from '../components/TradeCard';


export async function getStaticProps(){
  const tree_data = require("../data/all_parent_trees_no_details.json")

  const topWAR = tree_data.sort((a, b) => parseFloat(b.total_stats.war_sal.WAR) - parseFloat(a.total_stats.war_sal.WAR)).slice(0,50)
  const topTransac =  tree_data.sort((a, b) => parseFloat(b.total_transac) - parseFloat(a.total_transac)).slice(0,50)
  // const longest 
  // const longestOngoing

  return { props: {topWAR, topTransac} }
}


export default function Home({topWAR, topTransac}) {
  var settings = {
    arrows:true,
    dots: true,
    dotsClass: "slick-dots",
    autoplay: true,
    autoplaySpeed: 4000,
    className: "carousel",
    speed: 900,
    slidesToShow: 3,
    slidesToScroll: 3,
    centerMode:false,
    infinite:true,
    initialSlide:0,

    responsive: [{
      breakpoint: 1300,
      settings:{
        centerMode:false,
        autoplay: true,
        slidesToShow: 2,
        slidesToScroll: 2
      }},
        {breakpoint: 600,
          settings: {
            arrows:true,
            dots: false,
            vertical: false,
            verticalSwiping: false,
            swipeToSlide: true,
            
            autoplay: true,
            speed: 0,
            autoplaySpeed: 2500,
            centerMode:false,
            infinite:false,
            slidesToShow: 1,
            slidesToScroll: 1}}
      ]
  };
  const WARCards = 
  <Slider {...settings} key={0} >
  {topWAR.map(trade => {
    return (
    <TradeCard data = {trade}
                pid = {trade.tree_id}
                key = {trade.tree_id}
    />
    )
  })}
  </Slider>

  const TransacCards =   
  <Slider {...settings} key={0} >
    {topTransac.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {trade.tree_id}
                  key = {trade.tree_id}
      />
      )
    })}
  </Slider>

  const [sliderData, setSliderData] = useState(WARCards)
  const [activeClass, setActiveClass] = useState("WARCards")

  

  return (
      <div className={styles.homePage}>
        <Head>
          <title>MLB Trade Trees- Analyze Any Trade in Baseball History</title>
        </Head>
      <h1 className={styles.mainHead}>Analyze any trade in MLB history.</h1>
      
      <div className={styles.statHeader}>
        <h3>View top trees by:</h3>
        <div className={styles.statBar}>
          <button onClick={() => {setSliderData(WARCards);setActiveClass("WARCards")}} className={activeClass=="WARCards" ? styles.ctaActive : styles.cta}>
              <span>WAR Gained</span>
        </button>
        <button onClick={() => {setSliderData(TransacCards);setActiveClass("TransacCards")}} className={activeClass=="TransacCards" ? styles.ctaActive : styles.cta}>
              <span>Total Transactions</span>
        </button>            
        <button onClick={() => setSliderData(TransacCards)} class={styles.cta}>
              <span>Year Span</span>
        </button>
        <button onClick={() => setSliderData(TransacCards)} class={styles.cta}>
              <span>Ongoing & Year Span</span>
        </button> 
        </div>
      </div>
      {sliderData}
      </div>
  )
}
