import Tab from './components/Tab.jsx';
import BarraMenu from './components/BarraMenu.jsx';
import CardComponent from './components/Card.jsx';

function App() {
  return (
    <div className="h-full grid-flow-col-dense"> 
      <div className='bg-zinc-900 text-sm space-x-0.5 text-white relative'> 
        <BarraMenu />
      </div>
      <div className="h-full bg-red-300 relative">
        <Tab />
        <CardComponent />
      </div>
    </div>
  )
}

export default App;
