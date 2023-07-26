import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Row, Col, Container } from "react-bootstrap";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import UserContext from "../../context/UserContext";

function SignUp() {
  const { setUser } = useContext(UserContext);
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("")

  const initialValues = {
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  };

  const validationSchema = Yup.object({
    username: Yup.string().required("Username is required"),
    password: Yup.string().required("Password is required"),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref("password"), null], "Passwords must match")
      .required("Confirm Password is required"),
  });

  // const handleSubmit = (values) => {
  //   fetch("/api/signup", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify(values),
  //   })
  //     .then((response) => response.json())
  //     .then((user) => {
  //       setUser(user); // Updated: Use setUser to update user data
  //       navigate("/");
  //     })
  //     .catch((error) => console.error(error));
  // };

  const handleSubmit = (values) => {
    fetch("/api/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Signup failed."); // Throw an error if the response is not successful
        }
        return response.json();
      })
      .then((user) => {
        setUser(user);
        navigate("/");
      })
      .catch((error) => {
        console.error(error);
        setErrorMessage("Signup failed. Please try again."); // Set the error message in case of failure
      });
  };

  return (
    <div>
      <Row>
        <Col md={4} className="signup-image-col">
          <img
            src="https://raw.githubusercontent.com/Mttphan261/SFLabAssistant/main/.github/imgs/SignupPage/chun%20li%20world%20tour%20crop.png"
            alt="Signup"
            className="signup-image"
          />
        </Col>
        <Col md={8}>
          <div className="form-styling">
            <Col className="test">
              <h2>Here Comes A New Challenger!</h2>
              <h5>Sign Up:</h5>
              <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
              >
                <Form>
                  <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <Field
                      type="text"
                      name="email"
                      id="email"
                      className="form-field form-control"
                    />
                    <ErrorMessage
                      name="email"
                      component="div"
                      className="error-message"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <Field
                      type="text"
                      name="username"
                      id="username"
                      className="form-field form-control"
                    />
                    <ErrorMessage
                      name="username"
                      component="div"
                      className="form-group"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <Field
                      type="password"
                      name="password"
                      id="password"
                      className="form-field form-control"
                    />
                    <ErrorMessage
                      name="password"
                      component="div"
                      className="form-group"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="confirmPassword">Confirm Password:</label>
                    <Field
                      type="password"
                      name="confirmPassword"
                      id="confirmPassword"
                      className="form-field form-control"
                    />
                    <ErrorMessage
                      name="confirmPassword"
                      component="div"
                      className="form-group"
                    />
                  </div>
                  <button type="submit">Submit</button>
                </Form>
              </Formik>
              {errorMessage && <p>{errorMessage}</p>}
              <p>
                Already a user?
                <span
                  style={{ cursor: 
                  "pointer", 
                  "margin-left": "30px",}}
                  onClick={() => navigate("/login")}
                >
                  Sign In
                </span>
              </p>
            </Col>
          </div>
        </Col>
      </Row>
    </div>
  );
}

export default SignUp;
