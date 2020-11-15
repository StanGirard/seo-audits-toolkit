export const keywordsState = {
    data: {},
    status: "IDLE"
};

const keywords = (state = keywordsState, action) => {
    switch (action.type) {
        case 'KEYWORDS_GET':
            return { ...state, status: "PENDING" };

        case 'KEYWORDS_GET_SUCCESS':
            return { ...state, data: action.payload, status: "SUCCESS" }

        case 'KEYWORDS_GET_FAILURE':
            return { ...state, data: {}, status: "FAILURE" }
        default:
            return state;
    }
};

export default keywords;