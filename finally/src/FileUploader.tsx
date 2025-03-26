import React, { useState, useRef } from "react";
import "./FileUploader.css";

const FileUploader: React.FC = () => {

  // initialize state variables + their setters
  const [previews, setPreviews] = useState<{ name: string; url: string }[]>([]); // preview image 
  const [summary, setSummary] = useState<string | null>(null);  // ai summary variable
  const [dragging, setDragging] = useState<boolean>(false); // drag + drop upload 
  const fileInputRef = useRef<HTMLInputElement>(null); // ?????????????????

  // FUNCTION: file handler -- parameter(s): files (type: list of files from website)
  const handleFiles = async (files: FileList) => {
    const fileArray = Array.from(files); // converts files into an array (not an array to begin with)
    const previewUrls = fileArray.map((file) => ({ // mapping each file into an object with a name + its url
        name: file.name,
        url: file.type.startsWith("image/") ? URL.createObjectURL(file) : "",
      }));

    setPreviews(previewUrls); 
    console.log("Uploaded Files:", fileArray); // list of files uploaded

    await uploadFilesToServer(fileArray); // ?????????????????????
  };

  // FUNCTION: uploads files to backend -- parameter(s): files (type: ?)
  const uploadFilesToServer = async (files: File[]) => {
    const formData = new FormData(); 
    files.forEach((file) => { // each file is attached to formData 
      formData.append("file", file);
    });

    // attempting to send files to backend
    try {
      const response = await fetch("http://127.0.0.1:5000/document_contents", {
        method: "POST",
        body: formData,
      });

      const result = await response.json(); // ?
      console.log("Server Response:", result); // debugging: checking result in console

      if (!response.ok) { // exception handling: if the server does not get a response back
        throw new Error(result.error || `HTTP Error: ${response.status}`);
      }

      setSummary(result.summary);  // displays summary on page
    } catch (error) { // exception handling: if there is any error occurring from uploading the file
      console.error("Error uploading file:", error);
      alert("Failed to upload file. See console for details.");
    }
  };

  // FUNCTION: file is selected? --> send to handle files 
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      handleFiles(event.target.files);
    }
  };

  // FUNCTION: file is dropped in area? --> send to handle files
  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault(); // prevents the default browser behavior (would open the file otherwise)
    setDragging(false);
    if (event.dataTransfer.files) {
      handleFiles(event.dataTransfer.files);
    }
  };

  // FUNCTION: dragging over file upload area
  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(true);
  };

  // FUNCTION: not... dragging over file upload area
  const handleDragLeave = () => {
    setDragging(false);
  };

  return (
    <div className="file-uploader"> 
      <div
        className={`drop-zone ${dragging ? "dragging" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <p>{dragging ? "drop now!" : "drag + drop files here to upload!"}</p>
        <input
          type="file"
          multiple
          accept="image/*,application/pdf"
          onChange={handleFileChange}
          ref={fileInputRef}
          hidden
        />
      </div>

      {previews.length > 0 && (
        <div className="preview-container">
          {previews.map((file, index) => (
            <div key={index} className="preview-wrapper">
              {file.url && <img src={file.url} alt={`Preview ${index + 1}`} className="preview-image" />}
              <p className="file-label">{file.name}</p> 
            </div>
          ))}
        </div>
      )}

      {summary && (
        <div className="summary-container">
          <h3>AI Summary:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default FileUploader;
