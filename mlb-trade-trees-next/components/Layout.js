import Navbar from './Navbar'
import Footer from './Footer'
import PlayerData from '../json/players.json'

export default function Layout({ children }) {
  return (
    <div className='container'>
      <Navbar players={PlayerData} />
      { children }
      <Footer />
    </div> 
  );
}

