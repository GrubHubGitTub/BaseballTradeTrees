import Head from 'next/head';
import Link from 'next/link';
import React from "react";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import styles from '../styles/Home.module.css';
import TradeCard from '../components/TradeCard';


export async function getStaticProps(){
  const tree_data = require("../data/all_parent_trees_no_details.json")

  const top50WAR = tree_data.sort((a, b) => parseFloat(b.total_stats.war_sal.WAR) - parseFloat(a.total_stats.war_sal.WAR)).slice(0,50)
  
  return { props: {top50WAR} }
}


export default function Home({top50WAR}) {
  const responsive = {
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3,
      slidesToSlide: 3 // optional, default to 1.
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2,
      slidesToSlide: 2 // optional, default to 1.
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1,
      slidesToSlide: 1 // optional, default to 1.
    }
  };
  const tradeCards = top50WAR.map(trade => {
    return (
    <TradeCard data = {trade}
                pid = {trade.tree_id}
                key = {trade.tree_id}
    />
    )
  })
  return (
      <div className={styles.homePage}>
        <Head>
          <title>MLB Trade Trees- Analyze Any Trade in Baseball History</title>
        </Head>
   
      <Carousel
      // swipeable={false}
      // draggable={false}
      // centerMode={false}
      // showDots={true}
      // responsive={responsive}
      // ssr={false} // means to render carousel on server-side.
      // infinite={true}
      // autoPlay={true}
      // autoPlaySpeed={0.5}
      // keyBoardControl={true}
      // customTransition="all .5"
      // transitionDuration={500}
      additionalTransfrom={0}
      arrows
      autoPlay
      autoPlaySpeed={6000}
      centerMode={false}
      className={styles.carousel}
      containerClass="container-with-dots"
      customTransition="all 1s linear"
      dotListClass=""
      draggable
      focusOnSelect={false}
      infinite
      itemClass=""
      keyBoardControl
      minimumTouchDrag={80}
      pauseOnHover
      renderArrowsWhenDisabled={false}
      renderButtonGroupOutside={false}
      renderDotsOutside={false}
      responsive={responsive}
      rewind={false}
      rewindWithAnimation={false}
      rtl={false}
      shouldResetAutoplay
      showDots={true}
      sliderClass={styles.slider}
      swipeable
      transitionDuration={100}
      >
      {tradeCards}
      </Carousel>
      </div>
  )
}
