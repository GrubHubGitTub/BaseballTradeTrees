import Navbar from './Navbar'
import Footer from './Footer'
import player_search from "../data/player_search.json"

export default function Layout({ children }) {
  const players = player_search.sort((a, b) => a.name.localeCompare(b.name));
  return (
    <div className='container'>
      <Navbar players={players}/>
      { children }
      <Footer />
    </div> 
  );
}

