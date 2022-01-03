import React, { useState, useRef } from "react";

const UploadButton = (props) => {
  const [uploadedFileName, setUploadedFileName] = useState(null);
  const hiddenFileInput = useRef(null);

  const handleFileUpload = (e) => {
    e.preventDefault();
    hiddenFileInput.current.click();
  };

  const handleFileChange = (e) => {
    e.preventDefault();
    props.setFile(e.target.files[0]);
    e.target.files && setUploadedFileName(e.target.files[0].name);
  };

  return (
    <div className="col-md-6">
      <label htmlFor="image-file" className="form-label">{props.labelText} &ensp;</label>
      <input
        id="image-file"
        ref={hiddenFileInput}
        onChange={handleFileChange}
        className="d-none"
        type="file"
        accept={props.accept}
        required={props.isRequired}
      />
      <button
        onClick={handleFileUpload}
        className={`btn btn-outline-${
          uploadedFileName ? "success" : "primary"
        }`}
      >
        {uploadedFileName ? uploadedFileName : "Upload"}
      </button>
      {
        props.isRequired ? 
          <div className="invalid-feedback">
            Input Required!
          </div> : null
      }
    </div>
  );
};

export default UploadButton;