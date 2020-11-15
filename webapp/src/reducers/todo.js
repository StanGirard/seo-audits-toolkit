const defaultState = {
    message: "",
    status: "ACTIVE",
    
}

const todo = (state = defaultState, action) => {
    switch (action.type) {
      case 'TODO':
        return {...state}
      default:
        return state;
    }
  };
  
  export default todo;