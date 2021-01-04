import { Box, useMediaQuery } from '@material-ui/core';
import DomainIcon from '@material-ui/icons/Domain';
import HighlightIcon from '@material-ui/icons/Highlight';
import LanguageIcon from '@material-ui/icons/Language';
import LinkIcon from '@material-ui/icons/Link';
import PlaylistAddCheckIcon from '@material-ui/icons/PlaylistAddCheck';
import SupervisorAccountIcon from '@material-ui/icons/SupervisorAccount';
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import MyLocationIcon from '@material-ui/icons/MyLocation';
import MapIcon from '@material-ui/icons/Map';
import * as React from 'react';
import { useState } from 'react';
import { DashboardMenuItem, MenuItemLink } from 'react-admin';
import { useSelector } from 'react-redux';
import { SubMenu } from './SubMenu';
import SecurityIcon from '@material-ui/icons/Security';
import { green, red, blue, yellow, purple } from '@material-ui/core/colors';
import CreateIcon from '@material-ui/icons/Create';

const Menu = ({ onMenuClick, logout, dense = false }) => {
    const [state, setState] = useState({
        menuLighthouse: false,
        menuOrgs: false,
        menuExtractor: false,
        menuSecurity: false,
    });
    const isXSmall = useMediaQuery((theme) =>
        theme.breakpoints.down('xs')
    );
    const open = useSelector((state) => state.admin.ui.sidebarOpen);
    useSelector((state) => state.theme); // force rerender on theme change

    const handleToggle = (menu) => {
        setState(state => ({ ...state, [menu]: !state[menu] }));
    };

    return (
        <Box mt={1}>
            {' '}
            <DashboardMenuItem onClick={onMenuClick} sidebarIsOpen={open} />
            <SubMenu
                handleToggle={() => handleToggle('menuOrgs')}
                isOpen={state.menuOrgs}
                sidebarIsOpen={open}
                name="Organizations"
                icon={<SupervisorAccountIcon style={{ color: green[900] }}/>}
                dense={dense}
            >
                <MenuItemLink
                    to={`/website_user`}
                    primaryText="Websites"
                    leftIcon={<DomainIcon style={{ color: green[300] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
            </SubMenu>
            <SubMenu
                handleToggle={() => handleToggle('menuLighthouse')}
                isOpen={state.menuLighthouse}
                sidebarIsOpen={open}
                name="Lighthouse"
                icon={<HighlightIcon style={{ color: yellow[900] }}/>}
                dense={dense}
            >
                <MenuItemLink
                    to={`/lighthouse`}
                    primaryText="Lighthouse"
                    leftIcon={<LanguageIcon style={{ color: yellow[800] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                <MenuItemLink
                    to={`/lighthouse_details`}
                    primaryText="Results"
                    leftIcon={<PlaylistAddCheckIcon style={{ color: yellow[700] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
            </SubMenu>
            <SubMenu
                handleToggle={() => handleToggle('menuExtractor')}
                isOpen={state.menuExtractor}
                sidebarIsOpen={open}
                name="Extractor"
                icon={<VpnKeyIcon style={{ color: blue[900] }}/>}
                dense={dense}
            >
                <MenuItemLink
                    to={`/sitemap`}
                    primaryText="Sitemap"
                    leftIcon={<MapIcon style={{ color: blue["A700"] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                <MenuItemLink
                    to={`/extractor`}
                    primaryText="Images, Links, Headers"
                    leftIcon={<LinkIcon style={{ color: blue[700] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                <MenuItemLink
                    to={`/keywords/yake`}
                    primaryText="Yake"
                    leftIcon={<MyLocationIcon style={{ color: blue[600] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                
                <MenuItemLink
                    to={`/summarize`}
                    primaryText="Summarizer"
                    leftIcon={<CreateIcon style={{ color: blue[500] }}/>}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
            </SubMenu>
            
            <SubMenu
                handleToggle={() => handleToggle('menuSecurity')}
                isOpen={state.menuSecurity}
                sidebarIsOpen={open}
                name="Security"
                icon={<SecurityIcon style={{ color: red[500] }} />}
                dense={dense}
            >
                <MenuItemLink
                    to={`/security`}
                    primaryText="Security"
                    leftIcon={<SecurityIcon  style={{ color: red[300] }} />}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                <MenuItemLink
                    to={`/security_details`}
                    primaryText="Results"
                    leftIcon={<PlaylistAddCheckIcon style={{ color: red[200] }} />}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
            </SubMenu>
            
            {isXSmall && logout}
        </Box>
    );
};

export default Menu;