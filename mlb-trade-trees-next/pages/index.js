import Head from 'next/head';
import React, {useState, useEffect, useRef} from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import styles from '../styles/Home.module.css';
import TradeCard from '../components/TradeCard';


export async function getStaticProps(){
  const tree_data = require("../data/all_parent_trees_no_details.json")

  const topWAR = tree_data.sort((a, b) => parseFloat(b.total_stats.war_sal.WAR) - parseFloat(a.total_stats.war_sal.WAR)).slice(0,50)
  const topTransac = tree_data.sort((a, b) => parseFloat(b.total_transac) - parseFloat(a.total_transac)).slice(0,50)
  const longest = tree_data.sort((a, b) => parseFloat(b.year_span) - parseFloat(a.year_span)).slice(0,50)
  const ongoing = tree_data.filter((p) => p.ongoing === "Yes")
  const longestOngoing = ongoing.sort((a, b) => parseFloat(b.year_span) - parseFloat(a.year_span)).slice(0,50)

  return { props: {topWAR, topTransac, longest, longestOngoing} }
}


export default function Home({topWAR, topTransac, longest, longestOngoing}) {
  var settings = {
    arrows:true,
    dots: true,
    dotsClass: "slick-dots",
    autoplay: true,
    autoplaySpeed: 4000,
    className: "carousel",
    speed: 400,
    slidesToShow: 3,
    slidesToScroll: 3,
    centerMode:false,
    infinite:false,
    initialSlide:0,

    responsive: [{
      breakpoint: 1300,
      settings:{
        centerMode:false,
        autoplay: true,
        slidesToShow: 2,
        slidesToScroll: 2
      }},

        {breakpoint: 650,
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
  topWAR.map(trade => {
    return (
    <TradeCard data = {trade}
                pid = {trade.tree_id}
                key = {trade.tree_id}
    />
    )
  })

  const TransacCards =   
    topTransac.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {trade.tree_id}
                  key = {trade.tree_id}
      />
      )
    })

  const longestCards =   
    longest.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {trade.tree_id}
                  key = {trade.tree_id}
      />
      )
    })

  const ongoingCards =   
    longestOngoing.map(trade => {
      return (
      <TradeCard data = {trade}
                  pid = {trade.tree_id}
                  key = {trade.tree_id}
      />
      )
    })

  const [sliderData, setSliderData] = useState(WARCards)
  const [activeClass, setActiveClass] = useState("WARCards")
  const [filterChange, setFilterChange] = useState(false);

  const sliderRef = useRef(null);
  
  useEffect(() => {
    if (filterChange) {
      sliderRef.current?.slickGoTo(0);
      setFilterChange(false);
    }
  }, [filterChange]);
  
  return (
      <div className={styles.homePage}>
        <Head>
          <title>MLB Trade Trees- Analyze Any Trade in Baseball History</title>
        </Head>
      <h1 className={styles.mainHead}>Analyze any trade in MLB history.</h1>
      
      <div className={styles.statHeader}>
        <h3>View top trees by:</h3>
        <div className={styles.statBar}>
          <button onClick={() => {setFilterChange(true);setSliderData(WARCards);setActiveClass("WARCards")}} className={activeClass=="WARCards" ? styles.ctaActive : styles.cta}>
              <span>WAR Gained</span>
          </button>
        <button onClick={() => {setFilterChange(true);setSliderData(TransacCards);setActiveClass("TransacCards")}} className={activeClass=="TransacCards" ? styles.ctaActive : styles.cta}>
              <span>Total Transactions</span>
        </button>            
        <button onClick={() => {setFilterChange(true);setSliderData(longestCards);setActiveClass("longestCards")}} className={activeClass=="longestCards" ? styles.ctaActive : styles.cta}>
              <span>Year Span</span>
        </button>
        <button onClick={() => {setFilterChange(true);setSliderData(ongoingCards);setActiveClass("ongoingCards")}} className={activeClass=="ongoingCards" ? styles.ctaActive : styles.cta}>
              <span>Ongoing & Year Span</span>
        </button> 
        </div>
      </div>
      <Slider ref = {sliderRef} {...settings}>
        {sliderData}
      </Slider>
      </div>
  )
}
