import { connect } from "react-redux";
import { actionCreators as postActions } from "redux/modules/posts";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const {
    posts: { feed }
  } = state;
  return {
    feed
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    getFeed: () => {
      dispatch(postActions.getFeed());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);
