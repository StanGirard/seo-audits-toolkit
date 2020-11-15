/**
 * @module Sagas/GitHub
 * @desc GitHub
 */

import { call, put, takeLatest, debounce } from 'redux-saga/effects';
import { request } from '../modules/client';

/**
 * Get Repos
 *
 * @param {Object} action
 *
 */
export function* getBitcoin({ }) {
  try {
    console.log("HELLO")
    const response = yield call(
      request,
      `https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d%2C30d%2C1y`,
    );
    console.log(response)
    yield put({
      type: "BITCOIN_GET_SUCCESS",
      payload: response,
    });
  } catch (err) {
    /* istanbul ignore next */
    yield put({
      type: "BITCOIN_GET_FAILURE",
      payload: err,
    });
  }
}

/**
 * GitHub Sagas
 */
export const bitcoinsaga =
  [debounce(1000, "BITCOIN_GET", getBitcoin)]
