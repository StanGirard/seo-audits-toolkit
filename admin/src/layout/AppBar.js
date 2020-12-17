import * as React from 'react';
import { forwardRef } from 'react';
import { AppBar, UserMenu, MenuItemLink, useTranslate } from 'react-admin';
import Typography from '@material-ui/core/Typography';
import SettingsIcon from '@material-ui/icons/Settings';
import { makeStyles } from '@material-ui/core/styles';
import Logo from './Logo';
const useStyles = makeStyles({
    title: {
        flex: 1,
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
        overflow: 'hidden',
    },
    spacer: {
        flex: 1,
    },
});
const ConfigurationMenu = forwardRef((props, ref) => {
    const translate = useTranslate();
    return (React.createElement(MenuItemLink, { ref: ref, to: "/configuration", primaryText: translate('pos.configuration'), leftIcon: React.createElement(SettingsIcon, null), onClick: props.onClick, sidebarIsOpen: true }));
});
const CustomUserMenu = (props) => (React.createElement(UserMenu, Object.assign({}, props),
    React.createElement(ConfigurationMenu, null)));
const CustomAppBar = (props) => {
    const classes = useStyles();
    return (React.createElement(AppBar, Object.assign({}, props, { elevation: 1, userMenu: React.createElement(CustomUserMenu, null) }),
        React.createElement(Typography, { variant: "h6", color: "inherit", className: classes.title, id: "react-admin-title" }),
        React.createElement(Logo, null),
        React.createElement("span", { className: classes.spacer })));
};
export default CustomAppBar;