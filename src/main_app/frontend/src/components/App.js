/* eslint-disable react/prefer-stateless-function */
import axios from "axios";
import React, { Component } from "react";
import ReactDOM from "react-dom";
import "@babel/polyfill";
import Button from "react-bootstrap/Button";
import { Spinner } from "react-bootstrap";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      isLoading: false,
      isSuccess: false,
    };
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onChange(e) {
    this.setState({ url: e.target.value });
  }

  async onSubmit(event) {
    event.preventDefault();
    this.setState({ isLoading: true });
    const response = await axios
      .post(`/link/`, this.state.url, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((res) => {
        if (res.status !== 200) {
          throw Error(res.status);
        }
        console.log(res);
        this.showSuccess();
      })
      .catch((err) => {
        console.log(err);
      });
    this.setState({ url: "", isLoading: false });
  }

  showSuccess() {
    this.setState({ isSuccess: true });
    setTimeout(() => {
      this.setState({ isSuccess: false });
    }, 2500);
  }

  check = () => {
    console.log(this.state);
  };

  render() {
    return (
      <div className={"w-50 mt-5 mx-auto"}>
        <div className={"form-group col-lg-12"}>
          <h1 className={"text-primary text-center"}>Bangers Transfer</h1>
          <form className={"m-3  text-center"} onSubmit={this.onSubmit}>
            <input
              name="url"
              type="text"
              onChange={this.onChange}
              value={this.state.url}
              className={"form-control"}
              placeholder={"Enter Apple Music Playlist URL"}
              autoComplete={"off"}
            />

            {this.state.isLoading ? (
              <Button className={"m-3"} variant="primary">
                <Spinner
                  as="span"
                  animation="grow"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />
                Creating...
              </Button>
            ) : (
              <button type="submit" className={"btn btn-primary m-3"}>
                Submit
              </button>
            )}
            {this.state.isSuccess && <p>Success</p>}
          </form>
        </div>
        <div className={"row col-lg-12"}></div>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
