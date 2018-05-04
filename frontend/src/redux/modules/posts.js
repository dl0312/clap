// imports

import { actionCreators as userActions } from "redux/modules/user";

// actions

const SET_FEED = "SET_FEED";
const CLAP_POST = "CLAP_POST";
const UNCLAP_POST = "UNCLAP_POST";
const ADD_COMMENT = "ADD_COMMENT";

// action creators

function setFeed(feed) {
  return {
    type: SET_FEED,
    feed
  };
}

function doClapPost(postId) {
  return {
    type: CLAP_POST,
    postId
  };
}

function doUnclapPost(postId) {
  return {
    type: UNCLAP_POST,
    postId
  };
}

function addComment(postId, comment) {
  return {
    type: ADD_COMMENT,
    postId,
    comment
  };
}

// API Actions

function getFeed() {
  return (dispatch, getState) => {
    const {
      user: { token }
    } = getState();
    fetch("/posts/feed/", {
      headers: {
        Authorization: `JWT ${token}`
      }
    })
      .then(response => {
        if (response.status === 401) {
          dispatch(userActions.logout());
        }
        return response.json();
      })
      .then(json => {
        dispatch(setFeed(json));
      });
  };
}

function clapPost(postId) {
  return (dispatch, getState) => {
    dispatch(doClapPost(postId));
    const {
      user: { token }
    } = getState();
    fetch(`/posts/${postId}/claps/`, {
      method: "POST",
      headers: {
        Authorization: `JWT ${token}`
      }
    }).then(response => {
      if (response.status === 401) {
        dispatch(userActions.logout());
      } else if (!response.ok) {
        dispatch(doUnclapPost(postId));
      }
    });
  };
}

function unclapPost(postId) {
  return (dispatch, getState) => {
    dispatch(doUnclapPost(postId));
    const {
      user: { token }
    } = getState();
    fetch(`/posts/${postId}/unclap/`, {
      method: "DELETE",
      headers: {
        Authorization: `JWT ${token}`
      }
    }).then(response => {
      if (response.status === 401) {
        dispatch(userActions.logout());
      } else if (!response.ok) {
        dispatch(doClapPost(postId));
      }
    });
  };
}

function commentPost(postId, message) {
  return (dispatch, getState) => {
    const {
      user: { token }
    } = getState();
    fetch(`/posts/${postId}/comments/`, {
      method: "POST",
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message
      })
    })
      .then(response => {
        if (response.state === 401) {
          dispatch(userActions.logout());
        }
        return response.json();
      })
      .then(json => {
        if (json.message) {
          dispatch(addComment(postId, json));
        }
      });
  };
}

// Initial State

const initialState = {};

// Reducer

function reducer(state = initialState, action) {
  switch (action.type) {
    case SET_FEED:
      return applySetFeed(state, action);
    case CLAP_POST:
      return applyClapPost(state, action);
    case UNCLAP_POST:
      return applyUnclapPost(state, action);
    case ADD_COMMENT:
      return applyAddComment(state, action);
    default:
      return state;
  }
}

// Reducer Functions

function applySetFeed(state, action) {
  const { feed } = action;
  return {
    ...state,
    feed
  };
}

function applyClapPost(state, action) {
  const { postId } = action;
  const { feed } = state;
  const updatedFeed = feed.map(post => {
    if (post.id === postId) {
      return { ...post, is_claped: true, clap_count: post.clap_count + 1 };
    }
    return post;
  });
  return { ...state, feed: updatedFeed };
}

function applyUnclapPost(state, action) {
  const { postId } = action;
  const { feed } = state;
  const updatedFeed = feed.map(post => {
    if (post.id === postId) {
      return { ...post, is_claped: false, clap_count: post.clap_count - 1 };
    }
    return post;
  });
  return { ...state, feed: updatedFeed };
}

function applyAddComment(state, action) {
  const { postId, comment } = action;
  const { feed } = state;
  const updatedFeed = feed.map(post => {
    if (post.id === postId) {
      return {
        ...post,
        comments: [...post.comments, comment]
      };
    }
    return post;
  });
  return { ...state, feed: updatedFeed };
}

// Exports

const actionCreators = {
  getFeed,
  clapPost,
  unclapPost,
  commentPost
};

export { actionCreators };

// Export reducer by default

export default reducer;
