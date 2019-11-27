import React, { Component } from 'react'

import '../stylesheets/Search.css';

class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
          placeholder="Search questions..."
          className="question-search"
          ref={input => this.search = input}
          onChange={this.handleInputChange}
        />
        <input type="submit" value="Submit" className="question-search-action"/>
      </form>
    )
  }
}

export default Search
