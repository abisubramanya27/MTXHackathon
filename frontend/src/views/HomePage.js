import React, { Component } from 'react';
import LoginButton from '../components/LoginButton.js';
import SignupButton from '../components/SignupButton.js';
import '../styles/HomePage.css';
import {
  Navbar,
  Container,
  Nav
} from 'react-bootstrap';
import { motion } from 'framer-motion/dist/framer-motion';

class HomePage extends Component {
  render() {
    return (
      <div id="classichomepage">
        <motion.div
            initial={{ y: -250, opacity: 0 }}
            animate={{ y: -2, opacity: 1 }}
            transition={{ delay: 0.7, duration: 2 }}
        >
          <Navbar id="homenavbar" expand="md" variant="dark" fixed="top">
            <Container>
              <Navbar.Brand href="#">MTX</Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav variant="pills" className="me-auto">
                  <Nav.Item>
                    <LoginButton />
                  </Nav.Item>
                  <Nav.Item>
                    <SignupButton />
                  </Nav.Item>
                </Nav>
              </Navbar.Collapse>
            </Container>
          </Navbar>
        </motion.div>
        <motion.div
            initial={{ y: 400, opacity: 0 }}
            animate={{ y: 100, opacity: 1 }}
            transition={{ delay: 0.8, duration: 2, type: "spring", stiffness: 100 }}
        >
          <div className="row">
            <Container className="text-white text-center justify-content-center align-items-center mb-5 col-md-6 mt-sm-5">
              <h1 className="h1-responsive font-weight-bold">
                Welcome to the App!
              </h1>
              <hr className="hr-light" />
              <h6 className="mb-4 lead" style={{ lineHeight: 1.7 }}>
                This website is created for the MTX HackOlympics 2.0 in Shaastra 2022. <br />
                We worked on the problem statement: <i><strong>Key-Value Pair Detection in Documents</strong></i>. 
                You can login to use the application using your Gmail ID or can sign up if you wish to create a new account on the website.
              </h6>
            </Container>
          </div>
        </motion.div>
      </div>
    );
  }
}

export default HomePage;