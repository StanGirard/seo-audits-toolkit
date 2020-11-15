import React from 'react';
import '../css/sections.css'
import MenuList from '../components/MenuList';
import logo from '../assets/dataguru-logo.png';
const LeftSection = () => (
  <div className="leftSection">
    <div className="leftSectionLogoAreaMain">
        <div className="logo">
          <img src={logo} alt="Logo" className="img-responsive" />
        </div>
    </div>
    <MenuList/>
  </div>
);

export default LeftSection;
