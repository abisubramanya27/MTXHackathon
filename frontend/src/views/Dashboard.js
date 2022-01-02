import React, {Component} from 'react';
import LogoutButton from '../components/LogoutButton.js';
import '../styles/HomePage.css';
import Loading from '../components/Loading.js'
import { withAuthenticationRequired } from '@auth0/auth0-react';
import {
  Navbar,
  Container,
  Nav
} from 'react-bootstrap';
import { motion } from 'framer-motion/dist/framer-motion';

class Dashboard extends Component {
  render() {
    return (
      <div id="classichomepage">
        <motion.div className="header" 
            initial={{ y: -250, opacity: 0 }}
            animate={{ y: -2, opacity: 1 }}
            transition={{ delay: 0.7, duration: 2 }}
        >
          <Navbar id="homenavbar" scrolling dark expand="md" variant="dark" fixed="top">
            <Container>
              <Navbar.Brand href="#">MTX</Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav variant="pills" className="me-auto">
                  <Nav.Item>
                    <LogoutButton />
                  </Nav.Item>
                </Nav>
              </Navbar.Collapse>
            </Container>
          </Navbar>
        </motion.div>
        <motion.div className="body" 
            initial={{ y: 400, opacity: 0 }}
            animate={{ y: 100, opacity: 1 }}
            transition={{ delay: 0.8, duration: 2, type: "spring", stiffness: 100 }}
        >
          <div className="row">
            <Container className="text-white text-center justify-content-center align-items-center white-text mb-5 col-md-6 mt-xl-5">
              <h1 className="h1-responsive font-weight-bold">
                Welcome to the Dashboard!
              </h1>
              <hr className="hr-light" />
              <h6 className="mb-4 lead" style={{ lineHeight: 1.7 }}>
                You can upload the image for the task. 
                We will recognize the text, identify the key value pairs and output them as in JSON format.
              </h6>
            </Container>
          </div>
        </motion.div>
      </div>
    );
  }
}

export default withAuthenticationRequired(Dashboard, {
    onRedirecting: () => <Loading />,
});