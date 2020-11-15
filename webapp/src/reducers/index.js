import { combineReducers } from 'redux';
import todo from './todo'
import bitcoin from './bitcoin'
import keywords from './keywords'

const reducers = combineReducers({
  todo,
  bitcoin,
  keywords

});

export default reducers;