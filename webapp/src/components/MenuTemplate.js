import React from 'react'
import "../css/menu.css"
import { Link } from "react-router-dom";
const MenuList = ({path, text}) => (
        <Link to={path} className="menu-element" style={{ textDecoration: 'none' }}>
             {text}
        </Link>
)

export default MenuList;