import { useState, useRef } from 'react';

export default function Home({ onAnalyze, isAnalyzing }) {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);

  const handleFile = (file) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleChange = (e) => {
    handleFile(e.target.files?.[0]);
  };

  const handleAnalyze = () => {
    if (image) onAnalyze(image);
  };

  const resetImage = () => {
    setImage(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (cameraInputRef.current) cameraInputRef.current.value = '';
  };

  return (
    <>
      <div className="home-container">
        {/* Header */}
        <div className="hero">
          <h1>Crop Doctor AI</h1>
          <p>Upload a clear photo of the leaf, stem or fruit. Make sure the image is well lit and in focus.</p>
        </div>

        {/* Hidden Inputs */}
        <input ref={fileInputRef} type="file" accept="image/*" onChange={handleChange} style={{ display: 'none' }} />
        <input ref={cameraInputRef} type="file" accept="image/*" capture="environment" onChange={handleChange} style={{ display: 'none' }} />

        {/* Two Column Grid */}
        <div className="main-grid">
          
          {/* Left Column: Upload */}
          <div className="upload-section">
            <div 
              className={`dropzone ${preview ? 'has-image' : ''}`}
              onClick={() => !preview && fileInputRef.current?.click()}
            >
              {preview ? (
                <img src={preview} alt="Leaf preview" className="upload-preview" />
              ) : (
                <>
                  <div className="upload-icon">🖼️</div>
                  <div className="dropzone-text">
                  Drag and drop your image here
                  <span>or</span>
                  </div>
                  <button className="btn-choose" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
                    Choose File
                  </button>
                  <div className="format-info">Supported formats: JPG, PNG (Max 10MB)</div>
                </>
              )}
            </div>
            {preview && (
              <div style={{ marginTop: '16px', textAlign: 'center' }}>
                <button className="btn-choose" onClick={(e) => { e.stopPropagation(); cameraInputRef.current?.click(); }} style={{ background: '#f1f5f9', color: '#475569', marginRight: '10px' }}>
                  📷 Retake
                </button>
                <button className="btn-choose" onClick={(e) => { e.stopPropagation(); resetImage(); }} style={{ background: '#fee2e2', color: '#991b1b' }}>
                  Remove
                </button>
              </div>
            )}
          </div>

          {/* Right Column: Tips */}
          <div className="tips-section">
            <h3>Tips for a better result</h3>
            
            <div className="tip-item">
              <div className="tip-icon">📸</div>
              <div className="tip-text">Take a clear, close-up photo</div>
            </div>
            
            <div className="tip-item">
              <div className="tip-icon">🎯</div>
              <div className="tip-text">Make sure the leaf is in focus</div>
            </div>
            
            <div className="tip-item">
              <div className="tip-icon">🔍</div>
              <div className="tip-text">Include the affected area</div>
            </div>
            
            <div className="tip-item">
              <div className="tip-icon">☀️</div>
              <div className="tip-text">Good natural lighting</div>
            </div>
            
            <div className="tip-item">
              <div className="tip-icon">🚫</div>
              <div className="tip-text">Avoid blurry or dark images</div>
            </div>
          </div>

        </div>
      </div>

      {/* Bottom Fixed Action Bar */}
      <div className="action-bar">
        <div className="action-bar-text">
          You can also analyse multiple images to compare results.
        </div>
        <button 
          className="btn-analyze" 
          onClick={handleAnalyze} 
          disabled={!image || isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyse Now'}
        </button>
      </div>
    </>
  );
}