import React, { useState } from "react"
import Link from 'next/link'
import Image from "next/image";

export default function Navbar({players}) {
    const [isNavbarExpanded, setIsNavbarExpanded] = useState(false)
    
    const[filteredData, setFilteredData] = useState([]);
    const handleFilter = (event) => {
        const searchPlayer = event.target.value.toLowerCase()
        const newFilter = players.filter((player) => {
            return player.Name.toLowerCase().includes(searchPlayer);
        });

        if (searchPlayer === "") {
            setFilteredData([]);
        } else {
            setFilteredData(newFilter);
        }
    };

    return (
        <nav className="navbar">
            <Link href="/"><Image src="/logo.png" alt="logo" width="75" height="75"  className="navbar--brand"/></Link>
                <div classname="search">
                    <input 
                        type="text"
                        className="searchInput" 
                        placeholder="Enter Player"
                        onChange={handleFilter} />
                    <div className="search--icon"></div>

                    {filteredData.length != 0 && (
                        <div className="searchResults">
                            {filteredData.map((player, key) => {
                                return (<Link 
                                            href={{
                                                pathname:'/players/[pid]',
                                                query: {pid: player.ID}
                                            }}>    
                                            <a className="dataItem"> {player.Name} {player.play_debut} </a>
                                        </Link>
                                    )
                            })}
                        </div>
                    )}
                </div>    

            <button
                className="navbar--random"
            >Random
            </button>

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
                    <li>Teams</li>
                    <li>Advanced Search</li>
                    <li>Stats</li>
                    <li>Blog</li>
                    <li>About</li>
                </ul>
            </div>
        </nav>
    )
}