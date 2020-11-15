export const bitcoinState = {
    data: {},
    status: "IDLE"
};

const bitcoin = (state = bitcoinState, action) => {
    switch (action.type) {
        case 'BITCOIN_GET':
            return { ...state, status: "PENDING" };

        case 'BITCOIN_GET_SUCCESS':
            return { ...state, data: action.payload, status: "SUCCESS" }

        case 'BITCOIN_GET_FAILURE':
            return { ...state, data: {}, status: "FAILURE" }
        default:
            return state;
    }
};

export default bitcoin;