import { Box, Button, Card, CardActions, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import CodeIcon from '@material-ui/icons/Code';
import HomeIcon from '@material-ui/icons/Home';
import * as React from 'react';
import { useTranslate } from 'react-admin';
import publishArticleImage from './undraw_growth_chart.svg';


const useStyles = makeStyles(theme => ({
    root: {
        background:
            theme.palette.type === 'dark'
                ? '#535353'
                : `linear-gradient(to right, #8975fb 0%, #746be7 35%), linear-gradient(to bottom, #8975fb 0%, #6f4ceb 50%), #6f4ceb`,

        color: '#fff',
        padding: 20,
        marginTop: theme.spacing(2),
        marginBottom: '1em',
    },
    media: {
        background: `url(${publishArticleImage}) top right / cover`,
        marginLeft: 'auto',
    },
    actions: {
        [theme.breakpoints.down('md')]: {
            padding: 0,
            flexWrap: 'wrap',
            '& a': {
                marginTop: '1em',
                marginLeft: '0!important',
                marginRight: '1em',
            },
        },
    },
}));

const Welcome = () => {
    const translate = useTranslate();
    const classes = useStyles();
    return (
        <Card className={classes.root}>
            <Box display="flex">
                <Box flex="1">
                    <Typography variant="h5" component="h2" gutterBottom>
                        Welcome to OSAT ! The Open Source Audit Toolkit
                    </Typography>
                    <Box maxWidth="40em">
                        <Typography variant="body1" component="p" gutterBottom>
                            We are working hard on creating a free & Open source solution for all of your SEO issues. We'll keep on building and improving it. From SEO to NLP and Security. We'll add everything.
                        </Typography>
                    </Box>
                    <CardActions className={classes.actions}>
                        <Button
                            variant="contained"
                            href="https://osat.primates.dev"
                            startIcon={<HomeIcon />}
                        >
                            Documentation
                        </Button>
                        <Button
                            variant="contained"
                            href="https://github.com/StanGirard/seo-audits-toolkit"
                            startIcon={<CodeIcon />}
                        >
                            Github
                        </Button>
                    </CardActions>
                </Box>

                <Box
                    display={{ xs: 'none', sm: 'none', md: 'block' }}
                    className={classes.media}
                    width="16em"
                    height="9em"
                    overflow="hidden"
                />
            </Box>
        </Card>
    );
};

export default Welcome;