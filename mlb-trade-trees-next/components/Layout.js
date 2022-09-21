import Navbar from './Navbar'
import Footer from './Footer'
// import player_data from '../data/output.json'

export default function Layout({ children }) {
  return (
    <div className='container'>
      <Navbar players=""/>
      { children }
      <Footer />
    </div> 
  );
}

