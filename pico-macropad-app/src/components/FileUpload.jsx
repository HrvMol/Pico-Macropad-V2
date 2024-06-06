import React, { useState } from 'react';

const FileUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
  
    const handleFileChange = (event) => {
      const file = event.target.files[0];
      setSelectedFile(file);

      const previewUrl = URL.createObjectURL(file);
      setPreview(previewUrl);
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
      if (selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
  
        // Replace the URL with your upload endpoint
        fetch('YOUR_UPLOAD_URL', {
          method: 'POST',
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            console.log('File upload success:', data);
          })
          .catch((error) => {
            console.error('File upload error:', error);
          });
      } else {
        console.error('No file selected');
      }
    };
  
    return (
      <div>
        <input type="file" onChange={handleFileChange} />
        <div className='flex flex-col items-center'>
          <img src={preview} className='w-fit h-fit'/>
        </div>
      </div>
    );
  };
  
  export default FileUpload;