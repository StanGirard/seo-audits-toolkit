import React from 'react';
import { connect } from 'react-redux';
import Loader from "../../components/Loader"
import CryptoList from '../../components/Crypto/CryptoList'
import "../../css/crypto.css"

const generateColumn = ({ bitcoinPrice, bitcoinStatus, value }) => {

    console.log(bitcoinStatus + "HAHAHAH")
    if (bitcoinStatus === "SUCCESS") {
        return (
            <div>
                {bitcoinPrice[value]["15m"]}
            </div>
        )

    } else {
        return (
            <div>
                Hello it's empty
            </div>
        )

    }

}

export class Crypto extends React.Component {




    componentDidMount() {
        const { bitcoin, dispatch } = this.props;
        if (bitcoin.status !== "SUCCESS" && bitcoin.status !== "PENDING")
        {
            dispatch({ type: "BITCOIN_GET" });
        }
     
    }

    componentDidUpdate() {
        const { dispatch, bitcoin } = this.props;
    }
    render() {
        const { bitcoin } = this.props;
        if (bitcoin.status === "SUCCESS") {
            return (
                <div className="CryptoList">
                    <div className="CryptoHeader"> Cryptocurrencies Prices & Variations</div>
                    {bitcoin.data.map((value) => (
                        <CryptoList value={value}/>
                    ))}
                    
                </div>
                
            )
        }
        if (bitcoin.status === "PENDING"){
            return (
                <Loader/>
            )
        }
        
        else {
            return (
                <div>
                    {bitcoin.status}
                </div>)

        }


    }

};
function mapStateToProps(state) {
    return { bitcoin: state.bitcoin };
}

export default connect(mapStateToProps)(Crypto);