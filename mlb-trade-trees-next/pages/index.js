import Head from 'next/head';
import Link from 'next/link';
import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import styles from '../styles/Home.module.css';
import TradeCard from '../components/TradeCard';


export async function getStaticProps(){
  const tree_data = require("../data/all_parent_trees_no_details.json")

  const topWAR = tree_data.sort((a, b) => parseFloat(b.total_stats.war_sal.WAR) - parseFloat(a.total_stats.war_sal.WAR)).slice(0,50)
  
  return { props: {topWAR} }
}


export default function Home({topWAR}) {

  const tradeCards = topWAR.map(trade => {
    return (
    <TradeCard data = {trade}
                pid = {trade.tree_id}
                key = {trade.tree_id}
    />
    )
  })

  var settings = {
    arrows:true,
    dots: true,
    autoplay: true,
    autoplaySpeed: 4000,
    className: "carousel",
    speed: 900,
    slidesToShow: 3,
    slidesToScroll: 3,
    centerMode:false,
    infinite:true,

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

  return (
      <div className={styles.homePage}>
        <Head>
          <title>MLB Trade Trees- Analyze Any Trade in Baseball History</title>
        </Head>
      <h1 className={styles.mainHead}>Analyze any trade in MLB history.</h1>
      <div className={styles.statBar}>
          <h5>WAR </h5>
          <h5>Transactions </h5>
          <h5>Year </h5>
          <h5>Ongoing </h5>
      </div>
      <Slider {...settings}>
        {tradeCards}
      </Slider>
      </div>
  )
}
