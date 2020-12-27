import { Box, useMediaQuery } from '@material-ui/core';
import DomainIcon from '@material-ui/icons/Domain';
import HighlightIcon from '@material-ui/icons/Highlight';
import LanguageIcon from '@material-ui/icons/Language';
import LinkIcon from '@material-ui/icons/Link';
import PlaylistAddCheckIcon from '@material-ui/icons/PlaylistAddCheck';
import SupervisorAccountIcon from '@material-ui/icons/SupervisorAccount';
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import * as React from 'react';
import { useState } from 'react';
import { DashboardMenuItem, MenuItemLink } from 'react-admin';
import { useSelector } from 'react-redux';
import { SubMenu } from './SubMenu';

const Menu = ({ onMenuClick, logout, dense = false }) => {
    const [state, setState] = useState({
        menuLighthouse: false,
        menuOrgs: false,
        menuExtractor: false,
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
                icon={<SupervisorAccountIcon />}
                dense={dense}
            >
                <MenuItemLink
                    to={`/website_user`}
                    primaryText="Websites"
                    leftIcon={<DomainIcon />}
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
                icon={<HighlightIcon />}
                dense={dense}
            >
                <MenuItemLink
                    to={`/lighthouse`}
                    primaryText="Lighthouse"
                    leftIcon={<LanguageIcon />}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                <MenuItemLink
                    to={`/lighthouse_details`}
                    primaryText="Results"
                    leftIcon={<PlaylistAddCheckIcon />}
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
                icon={<VpnKeyIcon />}
                dense={dense}
            >
                <MenuItemLink
                    to={`/extractor`}
                    primaryText="Images, Links, Headers"
                    leftIcon={<LinkIcon />}
                    onClick={onMenuClick}
                    sidebarIsOpen={open}
                    dense={dense}
                />
                <MenuItemLink
                    to={`/keywords/yake`}
                    primaryText="Yake"
                    leftIcon={<LinkIcon />}
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