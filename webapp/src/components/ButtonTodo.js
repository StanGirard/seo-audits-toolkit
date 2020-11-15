import React from 'react';
import "../css/button.css"

const ButtonStart = ({ onClick = () => {} }) => (
  <div
    className="ButtonTodo"
    onClick={onClick}
  >
    TODO !
  </div>
);

export default ButtonStart;