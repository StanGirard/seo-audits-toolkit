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
export function* getKeywords({ }) {
  try {
    console.log("HELLO")
    const response = yield call(
      request,
      `http://localhost:5000/api/keywords`,
    );
    console.log("Response")
    console.log(response)
    yield put({
      type: "KEYWORDS_GET_SUCCESS",
      payload: response,
    });
  } catch (err) {
    /* istanbul ignore next */
    yield put({
      type: "KEYWORDS_GET_FAILURE",
      payload: err,
    });
  }
}

/**
 * GitHub Sagas
 */
export const keywordssaga =
  [debounce(1000, "KEYWORDS_GET", getKeywords)]
