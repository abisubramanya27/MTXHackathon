import React, { Component } from 'react';
import LogoutButton from '../components/LogoutButton.js';
import UploadButton from '../components/UploadButton.js';
import Loading from '../components/Loading.js';
import Code from '../components/Code.js';
import '../styles/Dashboard.css';
import { withAuthenticationRequired } from '@auth0/auth0-react';
import {
  Navbar,
  Container,
  Nav
} from 'react-bootstrap';
import { motion } from 'framer-motion/dist/framer-motion';
import { withAuth0 } from '@auth0/auth0-react';
import ScrollDownGIF from '../assets/ScrollDown.gif';
import axios from 'axios';

const example = {
  a: 1,
  b: 2,
  c: [1, 2],
  d: {
    foo: 4,
    bar: 5
  }
}

const API_ENDPOINT = "http://api/api/submit"

class Dashboard extends Component {
  constructor(props) {
    super(props);

    this.state = {
      imageFile: null,
      annotFile: null,
      outputs: null
    };

    this.source = axios.CancelToken.source();

    this.setFile.bind(this);
    this.handleSubmit.bind(this);
  }

  setFile = (file, fileName) => {
    this.setState({[fileName]: file});
  }

  handleSubmit = (e) => {
    e.preventDefault();
    console.log(e);
    if (!e.target.form.checkValidity()) {
      e.stopPropagation();
      e.target.form.classList.add('was-validated');
    }
    else {
      e.target.form.classList.add('was-validated');
      const formData = new FormData();
      formData.append("img_file", this.state.imageFile);
      formData.append("annot_file", this.state.annotFile);
      axios({
        method: "post",
        url: API_ENDPOINT,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      }).then(res => {
        this.setState({
          outputs: {
            json: JSON.parse(res.data.output_json),
            image: res.data.output_img
          }
        })
      }).catch(e => console.log(e.message))
    }
  }

  componentWillUnmount() {
    if (this.source) {
      this.source.cancel("Landing Component got unmounted");
    }
  }

  render() {
    const { user } = this.props.auth0;

    return (
      <>
      <div id="classicmainpage" className="view">
        <motion.div
            initial={{ y: -250, opacity: 0 }}
            animate={{ y: -2, opacity: 1 }}
            transition={{ delay: 0.7, duration: 2 }}
        >
          <Navbar id="mainnavbar" expand="md" variant="dark" fixed="top">
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
        <motion.div
            initial={{ x: -400, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.8, duration: 2, type: "spring", stiffness: 100 }}
        >
          <div className="row">
            <Container className="text-white text-center justify-content-center align-items-center col-md-6  mt-sm-5">
              <h1 className="h1-responsive font-weight-bold">
                Hi, {user.name}!
              </h1>
              <hr className="hr-light" />
              <h6 className="mb-4 lead" style={{ lineHeight: 1.7 }}>
                You can upload the image for the task. 
                We will recognize the text, identify the key value pairs and output them as in JSON format.
              </h6>
            </Container>
          </div>
        </motion.div>
        <motion.div 
            initial={{ x: 400, opacity: 0 }}
            animate={{ x: -10, opacity: 1 }}
            transition={{ delay: 0.8, duration: 2, type: "spring", stiffness: 100 }}
        >
          <Container className="bg-light text-center justify-content-center align-items-center mt-sm-5 pt-4 pb-4">
            <form className="row g-1 needs-validation" noValidate>
              <UploadButton key={1} ref={this.inputImageFile} labelText={
                  <span>Choose Image <span className="blockquote-footer">supports .png, .jpeg</span></span> 
                }
                setFile={file => this.setFile(file, 'imageFile')}
                accept=".png,.jpg,.jpeg"
                isRequired={true}
              />
              <UploadButton key={2} ref={this.inputAnnotFile} labelText={
                  <span>Choose Annotation <mark>(optional)</mark> <span className="blockquote-footer">supports .json</span></span> 
                }
                setFile={file => this.setFile(file, 'annotFile')}
                accept=".json,.jsonl"
                isRequired={false}
              />
              <div className="col-12">
                <button className="btn btn-primary" aria-label="Submit Image and Annotation Button" type="submit" onClick={this.handleSubmit}>Submit</button>
              </div>
            </form>
          </Container>
        </motion.div>
        {
          this.state.outputs ? 
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1, duration: 1.5 }}
            >
              <Container className="text-center justify-content-center align-items-center">
                <img src={ScrollDownGIF} alt="scroll down for output..." style={{width: "50%"}} />
              </Container>
            </motion.div> : null
        }
      </div>
      {
        this.state.outputs ? 
          <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1, duration: 2 }}
          >
            {
              this.state.outputs.json ?
                <>
                <Container className="text-center justify-content-center align-items-center col-md-6 mt-sm-5">
                  <h1>Output JSON</h1>
                </Container>
                <Code code={JSON.stringify(this.state.outputs.json, null, 2)} /> 
                </> : null
            }
            {
              this.state.outputs.image ?
                <Container className="text-center justify-content-center align-items-center mt-sm-5 pb-5">
                  <h1>Output Image</h1>
                  <div className="image-output">
                    <img src={`data:image/png;base64,${this.state.outputs.image}`} alt="output image" />
                  </div>
                </Container> : null
            }
          </motion.div> : null
        }
      </>
    );
  }
}

export default withAuthenticationRequired(withAuth0(Dashboard), {
    onRedirecting: () => <Loading />,
});