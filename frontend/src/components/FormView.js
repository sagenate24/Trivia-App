import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
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
      difficulty: 1,
      category: 1,
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
          <label>
            Question
            <input type="text" name="question" onChange={this.handleChange}/>
          </label>
          <label>
            Answer
            <input type="text" name="answer" onChange={this.handleChange}/>
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
