import Navbar from './Navbar'
import Footer from './Footer'
import player_data from '../data/output.json'

export default function Layout({ children }) {
  return (
    <div className='container'>
      <Navbar players={player_data["player_data"]} />
      { children }
      <Footer />
    </div> 
  );
}

