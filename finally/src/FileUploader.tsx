import React, { useState, useRef } from "react";
import "./FileUploader.css";

const FileUploader: React.FC = () => {
  // initialize state variables
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [previews, setPreviews] = useState<{ name: string; url: string }[]>([]);
  const [dragging, setDragging] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // FUNCTION: handler for files + sends to flask backend
  const handleFiles = async (files: FileList) => {
    const fileArray = Array.from(files); // convert "FileList" to an array
    const previewUrls = fileArray.map((file) => ({
        name: file.name,
        url: file.type.startsWith("image/") ? URL.createObjectURL(file) : "",
      }));

    setPreviews(previewUrls);
    
    // console log each file uploaded
    console.log("Uploaded Files:", fileArray);

    await uploadFilesToServer(fileArray);
  };

  // FUNCTION: literally flask handling i'm begging please pleas eplpealplpleap lpealsplpel PLEASE :'(
  const uploadFilesToServer = async (files: File[]) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("file", file);
    });

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      console.log("Server Response:", result);
      alert(result.message);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file.");
    }
  };

  // FUNCTION: handle file selection in input field  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      handleFiles(event.target.files);
    }
  };

  // FUNCTION: drag and drop 
  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
    if (event.dataTransfer.files) {
      handleFiles(event.dataTransfer.files);
    }
  };

  // FUNCTION: file is dragged over 
  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(true);
  };

  // FUNCTION: file is dragged off 
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
        <p>{dragging ? "RAAAAAAAAAAAAH" : "drag + drop forms HERE to upload!"}</p>
        <input
          type="file"
          multiple
          accept="image/*,application/pdf"
          onChange={handleFileChange}
          ref={fileInputRef}
          hidden
        />
      </div>

      {/* displays name of the file inputted */}
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
    </div>
  );
};

export default FileUploader;
