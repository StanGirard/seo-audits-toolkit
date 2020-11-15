import React from 'react'
import '../css/sections.css'
import {
  Route,
} from "react-router-dom";

const RouteTemplate = ({children, path}) => (
    <Route path={path}>
        <div className="rightSection">
        {children}
        </div>
    </Route>

)

export default RouteTemplate