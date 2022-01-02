import React from 'react';
import '../styles/Loading.css';

const Loading = () => {
    return (
        <div className="spinner-center">
            <div className="spinner-grow text-primary" role="status" style={{margin: 10}}>
            </div>
            <div className="spinner-grow text-secondary" role="status" style={{margin: 10}}>
            </div>
            <div className="spinner-grow text-success" role="status" style={{margin: 10}}>
            </div>
            <div className="spinner-grow text-danger" role="status" style={{margin: 10}}>
            </div>
            <div className="spinner-grow text-warning" role="status" style={{margin: 10}}>
            </div>
            <div className="spinner-grow text-info" role="status" style={{margin: 10}}>
            </div>
        </div>
    )
}

export default Loading;