import Navbar from './Navbar'
import Footer from './Footer'
// import player_data from '../data/output.json'

export default function Layout({ children }) {
  // const player_data = fs.readFile('../data/output.json', 'utf8');
  return (
    <div className='container'>
      <Navbar players=""/>
      { children }
      <Footer />
    </div> 
  );
}

