import React from 'react';
import "./css/home.css"
import Home from './layout/home.js'
import {HashRouter} from 'react-router-dom'


function App() {
  return (
    <HashRouter>
      <Home/>
    </HashRouter>
      
   
  );
}

export default App;
