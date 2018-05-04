import React, { Component } from "react";
import PostActions from "./presenter";

class Container extends Component {
  render() {
    return <PostActions {...this.props} />;
  }
}

export default Container;
