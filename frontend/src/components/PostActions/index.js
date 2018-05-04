import { connect } from "react-redux";
import Container from "./container";
import { actionCreators as postActions } from "redux/modules/posts";

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    handleHeartClick: () => {
      if (ownProps.isLiked) {
        dispatch(postActions.unclapPost(ownProps.postId));
      } else {
        dispatch(postActions.clapPost(ownProps.postId));
      }
    }
  };
};

export default connect(null, mapDispatchToProps)(Container);
