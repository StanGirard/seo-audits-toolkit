import {  takeEvery} from "redux-saga/effects";

function todoSagaLog(action) {
  try {
    console.log("TODO")
  } catch (e) {
    console.log("ERROR! Bip! Bip!")
  }
}


export  const  todosaga =
  [takeEvery("TODO", todoSagaLog)]
