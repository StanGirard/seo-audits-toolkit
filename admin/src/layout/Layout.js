import * as React from 'react';
import { useSelector } from 'react-redux';
import { Layout, Sidebar } from 'react-admin';
import AppBar from './AppBar';
import { darkTheme, lightTheme } from './theme';
const CustomSidebar = (props) => React.createElement(Sidebar, Object.assign({}, props, { size: 200 }));
export default (props) => {
    const theme = useSelector((state) => state.theme === 'light' ? darkTheme : lightTheme);
    return (React.createElement(Layout, Object.assign({}, props, { appBar: AppBar, theme: theme })));
};