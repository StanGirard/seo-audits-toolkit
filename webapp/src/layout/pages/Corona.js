import React from 'react'
import ButtonTodo from '../../components/ButtonTodo'
import { connect } from 'react-redux';
const Corona = ({dispatch}) => (
    <ButtonTodo onClick={() => dispatch({ type: 'BITCOIN_GET' })} />
)

export default connect()(Corona)