import Navbar from './Navbar'
import Footer from './Footer'
import { AnalyticsWrapper } from '../components/analytics';
import player_search from "../data/player_search.json"

export default function Layout({ children }) {
  const players = player_search.sort((a, b) => a.name.localeCompare(b.name));
  return (
    <div className='container'>
      <Navbar players={players}/>
      { children }
      <AnalyticsWrapper />
      <Footer />
    </div> 
  );
}

