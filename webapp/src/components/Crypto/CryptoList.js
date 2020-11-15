import React from 'react'
import "../../css/crypto.css"
import arrow_up from '../../assets/up-arrow.png'
import arrow_down from '../../assets/down-arrow.png'

const price_color = (value) => {

    return (
        <div className="CryptoPrice">
            <div className="CryptoIconPrice">
                <div className="CryptoChangeIcon">
                    <img src={value["price_change_24h"] > 0 ? arrow_up : arrow_down} alt='Price Change Logo' />
                </div>
                ${value["current_price"]}
            </div>
            <div className="CryptoPercentageChange">
                <div className="row" >
                    1h: <div className={value["price_change_percentage_1h_in_currency"] > 0 ? "green" : "red"}> {value["price_change_percentage_1h_in_currency"].toFixed(2)}% </div>
                </div>
                <div className="row" >
                    24h: <div className={value["price_change_percentage_24h_in_currency"] > 0 ? "green" : "red"}> {value["price_change_percentage_24h_in_currency"].toFixed(2)}% </div>
                </div>
                <div className="row" >
                    7d: <div className={value["price_change_percentage_7d_in_currency"] > 0 ? "green" : "red"}> {value["price_change_percentage_7d_in_currency"].toFixed(2)}% </div>
                </div>
            </div>
        </div>

    )

}

const CryptoList = ({ value }) => (
    <div className="CryptoElement">
        {/* Image and Name of the Crypto */}
        <div className="CryptoRank">
            {value["market_cap_rank"]}
        </div>
        <div className="CryptoHead">
            <div className="CryptoImage">
                <img src={value["image"]} alt="Logo" />
            </div>
            <div className="CryptoName">
                {value["name"]}
            </div>
        </div>
        {/* Generates the Price with the right color */}
        {price_color(value)}
        <div className="CryptoSupply">
            <p>Circulating Supply: {value["circulating_supply"]}</p>
            <p>Total Supply: {value["total_supply"] !== null ? value["total_supply"] : "No Maximum"}</p>
        </div>

    </div>
)

export default CryptoList
