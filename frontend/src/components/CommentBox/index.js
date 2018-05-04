import { connect } from "react-redux";
import Container from "./container";
import { actionCreators as postActions } from "redux/modules/posts";

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    submitComment: message => {
      dispatch(postActions.commentPost(ownProps.postId, message));
    }
  };
};

export default connect(null, mapDispatchToProps)(Container);
