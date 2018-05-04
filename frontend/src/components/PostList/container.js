import React, { Component } from "react";
import PostList from "./presenter";

class Container extends Component {
  render() {
    return <PostList {...this.props} />;
  }
}

export default Container;
