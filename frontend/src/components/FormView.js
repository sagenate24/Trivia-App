import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: null,
      category: null,
      categories: {},
      questionCreateSuccess: false
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/api/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    this.setState({ questionCreateSuccess: false })
    event.preventDefault();
    $.ajax({
      url: '/api/questions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({ questionCreateSuccess: true })
        this.resetLocalState()
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        if (error.status === 400) {
          alert('Please make sure to fill out all fields')  
        } else {
          alert('Unable to add question. Please try your request again')
        }
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  resetLocalState = () => {
    this.setState({
      question: "",
      answer: "",
      difficulty: null,
      category: null,
    })
  }

  render() {
    return (
      <div id="add-form">
        <div
          style={{"visibility": this.state.questionCreateSuccess ? 'visible' : 'hidden'}}
          className="success-message">
          <p>Question successfully created!</p>
        </div>
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <input
            className="text-field"
            type="text"
            name="question"
            placeholder="Question"
            onInput={this.handleChange}/>
          <input
            className="text-field"
            type="text"
            name="answer"
            placeholder="Answer"
            onInput={this.handleChange}/>
            <select
              className="select-field"
              name="difficulty"
              onChange={this.handleChange}
              defaultValue={'DEFAULT'}>
              <option disabled value='DEFAULT'>Select Difficulty</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
            <select
              className="select-field"
              name="category"
              onChange={this.handleChange}
              defaultValue={'DEFAULT'}>
              <option disabled value='DEFAULT'>Select Category</option>
              {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
            </select>
          <input
            type="submit"
            className="button"
            value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
