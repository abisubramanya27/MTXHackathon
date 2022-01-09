import React, {useState} from 'react';
import '../styles/Dashboard.css';
import { Container } from 'react-bootstrap';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import paraisoDark from 'react-syntax-highlighter/dist/cjs/styles/hljs/paraiso-dark';
import javascript from 'react-syntax-highlighter/dist/cjs/languages/hljs/json';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { FaRegClipboard, FaRegCopy } from 'react-icons/fa';

SyntaxHighlighter.registerLanguage('javascript', javascript);

export default function Code(props) {
    const [isCopied, setIsCopied] = useState(false);

    return (
        <Container className="justify-content-center align-items-center mt-sm-5 pt-4 pb-4 codeDiv">
          <CopyToClipboard 
            onCopy={() => {
              setIsCopied(true);
              setTimeout(() => setIsCopied(false), 6000)
            }}
            className="copyButton"
            text={props.code}
          >
            <button type="button" aria-label="Copy to Clipboard Button" style={{border: "none transparent"}}>
              {isCopied ? <FaRegClipboard /> : <FaRegCopy />}
            </button>
          </CopyToClipboard>
          <SyntaxHighlighter className="syntax-highlighter" language="javascript" style={paraisoDark} showLineNumbers showInlineLineNumbers>
            {props.code}
          </SyntaxHighlighter>
        </Container>
    )
};