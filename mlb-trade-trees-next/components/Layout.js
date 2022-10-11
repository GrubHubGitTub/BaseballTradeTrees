import Navbar from './Navbar'
import Footer from './Footer'
import player_data from '../public/data/output.json'

export default function Layout({ children }) {
  return (
    <div className='container'>
      <Navbar players={player_data}/>
      { children }
      <Footer />
    </div> 
  );
}

