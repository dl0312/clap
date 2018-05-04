import React, { Component } from "react";
import FeedPost from "./presenter";

class Container extends Component {
  state = {
    seeingClaps: false
  };
  render() {
    return (
      <FeedPost
        {...this.props}
        {...this.state}
        openClaps={this._openClaps}
        closeClaps={this._closeClaps}
      />
    );
  }
  _openClaps = () => {
    const { getPostClaps, claps } = this.props;
    this.setState({
      seeingClaps: true
    });
    if (!claps) {
      getPostClaps();
    }
  };
  _closeLikes = () => {
    this.setState({
      seeingClaps: false
    });
  };
}

export default Container;
