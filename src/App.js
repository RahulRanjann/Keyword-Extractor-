import logo from './logo.svg';
import './App.css';
import InputUrl from './component/InputUrl';
import Navbar from './component/NavBar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Profitability from './component/Profitability';


const About = () => <h1>About Page</h1>;
const Projects = () => <h1>Projects Page</h1>;
const Contact = () => <h1>Contact Page</h1>;
function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<InputUrl />} />
        <Route path="/profitability" element={<Profitability />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </BrowserRouter>
      
    </div>
  );
}

export default App;
