import { connect } from "react-redux";
import Container from "./container";
import { actionCreators as userActions } from "redux/modules/user";

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    getPostClaps: () => {
      dispatch(userActions.getPostClaps(ownProps.id));
    }
  };
};

export default connect(null, mapDispatchToProps)(Container);
