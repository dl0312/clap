// imports

// actions

// action creators

// initial state

const initialState = {
  isLoggedIn: localStorage.getItem("jwt") || false
};

// reducer

function reducer(state = initialState, action) {
  switch (action.type) {
    default:
      return state;
  }
}

// reducer functions

// exports

// reuducer export

export default reducer;
