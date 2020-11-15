import React from 'react';

import { connect } from 'react-redux';
import "../css/home.css"
import LeftSection from './LeftSection'
import RightSection from './RightSection'

const mapStateToProps = () => ({

});

const Home = ({ dispatch }) => (

    <div className="home">
        <LeftSection/>
        <RightSection/>
    </div>
);

export default connect(mapStateToProps)(Home);
