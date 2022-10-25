import Link from "next/link";
import React from "react";
import styles from '../styles/TeamCard.module.css';
import Image from "next/image";
import {franchises} from "../data/franchise_colors"

export default function TeamCard({data}) {
    console.log(data)
    const tid = data.team_id

    let background 
    let link
    if (tid in franchises) {
        background = franchises[tid]
        link = `/team_logos/${tid}.png`
    }

     let names = ""
     names = data.other_names.map((name) => {
        if (name == data.name){}
        else{ return (<p className={styles.name}> {name} </p>)}
     })

    return (

            <div className={styles.card} style={{ "background": background }}>
                <div className={styles.logodiv}>
                    <Image src={link} alt="TeamLogo" layout="fill" objectFit="contain"/>
                </div>
                    <h1>{data.name}</h1>
                    <div className={styles.content}>
                        <h3>Franchise since: {data.first_year}</h3>
                        <div className={styles.otherNames}>
                        {names != "" && <p><b>Also known as:</b></p>}
                        {names}
                        </div>
                    </div>
                    <Link href={`/teams/${tid}`}><a className={styles.treeButton}>View Roster and Trade Info</a></Link>
                    
            </div>
    )
}