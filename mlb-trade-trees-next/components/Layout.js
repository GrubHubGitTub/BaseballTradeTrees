import Navbar from './Navbar'
import Footer from './Footer'
import player_search from "../public/data/player_search.json"

export default function Layout({ children }) {
  const players = player_search
  return (
    <div className='container'>
      <Navbar players={players}/>
      { children }
      <Footer />
    </div> 
  );
}

