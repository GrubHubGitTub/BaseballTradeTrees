import Navbar from './Navbar'
import Footer from './Footer'
import {player_data} from '../data/player_data.js'

export default function Layout({ children }) {
  return (
    <div className='container'>
      <Navbar players={player_data} />
      { children }
      <Footer />
    </div> 
  );
}

