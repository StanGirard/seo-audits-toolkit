import Collapse from '@material-ui/core/Collapse';
import List from '@material-ui/core/List';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import MenuItem from '@material-ui/core/MenuItem';
import { makeStyles } from '@material-ui/core/styles';
import Tooltip from '@material-ui/core/Tooltip';
import Typography from '@material-ui/core/Typography';
import ExpandMore from '@material-ui/icons/ExpandMore';
import * as React from 'react';
import { Fragment } from 'react';

const useStyles = makeStyles(theme => ({
    icon: { minWidth: theme.spacing(5) },
    sidebarIsOpen: {
        '& a': {
            paddingLeft: theme.spacing(4),
            transition: 'padding-left 195ms cubic-bezier(0.4, 0, 0.6, 1) 0ms',
        },
    },
    sidebarIsClosed: {
        '& a': {
            paddingLeft: theme.spacing(2),
            transition: 'padding-left 195ms cubic-bezier(0.4, 0, 0.6, 1) 0ms',
        },
    },
}));

export const SubMenu = ({
    handleToggle,
    sidebarIsOpen,
    isOpen,
    name,
    icon,
    children,
    dense,
}) => {
    const classes = useStyles();

    const header = (
        <MenuItem dense={dense} button onClick={handleToggle}>
            <ListItemIcon className={classes.icon}>
                {isOpen ? <ExpandMore /> : icon}
            </ListItemIcon>
            <Typography variant="inherit" color="textSecondary">
                {name}
            </Typography>
        </MenuItem>
    );

    return (
        <Fragment>
            {sidebarIsOpen || isOpen ? (
                header
            ) : (
                <Tooltip title={name} placement="right">
                    {header}
                </Tooltip>
            )}
            <Collapse in={isOpen} timeout="auto" unmountOnExit>
                <List
                    dense={dense}
                    component="div"
                    disablePadding
                    className={
                        sidebarIsOpen
                            ? classes.sidebarIsOpen
                            : classes.sidebarIsClosed
                    }
                >
                    {children}
                </List>
            </Collapse>
        </Fragment>
    );
};
