import React, { useState } from "react"
import Link from 'next/link'
import Image from "next/image";

export default function Navbar({players}) {

    function randomLink() {
        var randomplayer = players[Math.floor(Math.random()*players.length)]
        // var randomid = randompage.trades[Math.floor(Math.random()*randompage.trades.length)].tree_id
        var pid = randomplayer.retro_id 
        var url = `/player/${pid}/`
        return url
    }

    const [isNavbarExpanded, setIsNavbarExpanded] = useState(false)
    
    const[filteredData, setFilteredData] = useState([]);
    const handleFilter = (event) => {
        const searchPlayer = event.target.value.toLowerCase()
        const newFilter = players.filter((player) => {
            return player.name.toLowerCase().includes(searchPlayer);
        });

        if (searchPlayer.length < 3) {
            setFilteredData([]);
        } else {
            setFilteredData(newFilter);
        }
    };

    return (
        <nav className="navbar">
            <Link href="/"><a><Image src="/logo.png" alt="logo" width="120" height="120"  className="navbar--brand"/></a></Link>
                
                <div className="search">
                    <input 
                        type="text"
                        className="searchInput" 
                        placeholder="Enter Player"
                        onChange={handleFilter}
                        />
                    <div className="search--icon"></div>

                    {filteredData.length != 0 &&  (
                        <div className="searchResults">
                            {filteredData.map((player) => {
                                return (<Link 
                                            key= {player.retro_id}
                                            href={{
                                                pathname: '/player/[pid]',
                                                query: { pid: player.retro_id },
                                            }}>   
                                            {"T" in player ? 
                                            <a className="dataItem" onClick={ () => { setFilteredData([]); }} > <h4>{player.name}</h4><p>{player.HOF}</p> <h6>(view non-trade info)</h6>  <h5 >{player.debut_year} - {player.last_year} </h5></a> 
                                            : 
                                            <a className="dataItem" onClick={ () => { setFilteredData([]); }} > <h4>{player.name}</h4> <p>{player.HOF}</p> <h6>(view trade info)</h6> <h5 >{player.debut_year} - {player.last_year}</h5></a> }
                                            
                                            
                                        </Link>
                                    )
                            })}
                        </div>
                    )}
                </div>    
            
                <Link href={randomLink()}>
                    <button className="navbar--random" style={{"marginLeft":"1%"}}>Random Player</button>
                </Link>

            <button 
                className="navbar--hamburger"
                onClick={() => {
                    setIsNavbarExpanded(!isNavbarExpanded);
                }}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="white">
                    <path
                        fillRule="evenodd"
                        d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM9 15a1 1 0 011-1h6a1 1 0 110 2h-6a1 1 0 01-1-1z"
                        clipRule="evenodd"/>
                </svg>
            </button>
            <div className={isNavbarExpanded ? "navbar--menu expanded" : "navbar--menu"}>
                
                <ul> 
                {/* change these to links */}
                    <Link href="/teams"><li><button className="navButton">Teams</button></li></Link>
                    {/* <Link href="/players"><li><button className="navButton">Players</button></li></Link> */}
                    <Link href="/search"><li><button className="navButton">Search | Stats</button></li></Link>
                    <Link href="/about"><li><button className="navButton">About</button></li></Link>
                </ul>
            </div>
        </nav>
    )
}