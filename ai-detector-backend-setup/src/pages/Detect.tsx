import React, { useState, useRef, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { predictionsApi } from '../services/api';
import { Prediction } from '../types';

const Detect: React.FC = () => {
  const { user } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<Prediction | null>(null);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError('');
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile || !user) return;
    
    setIsAnalyzing(true);
    setError('');
    
    try {
      const prediction = await predictionsApi.predict(selectedFile, user.id);
      setResult(prediction);
    } catch (err: any) {
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'text-green-600 bg-green-100';
    if (confidence >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          🔬 Disease Detection
        </h1>
        <p className="text-gray-600">
          Upload a photo of your crop and let AI identify any diseases
        </p>
      </div>

      {/* Upload Section */}
      {!result && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          {/* Drop Zone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all
              ${dragActive ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-green-400 hover:bg-green-50/50'}
              ${previewUrl ? 'border-green-500' : ''}`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleInputChange}
              className="hidden"
            />
            
            {previewUrl ? (
              <div className="space-y-4">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="max-h-64 mx-auto rounded-lg shadow-md"
                />
                <p className="text-gray-600">{selectedFile?.name}</p>
                <button
                  onClick={(e) => { e.stopPropagation(); handleReset(); }}
                  className="text-red-500 hover:text-red-700 text-sm font-medium"
                >
                  Remove image
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="w-20 h-20 mx-auto bg-gradient-to-r from-green-100 to-blue-100 rounded-full flex items-center justify-center">
                  <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <p className="text-lg font-medium text-gray-700">
                    Drag and drop your image here
                  </p>
                  <p className="text-gray-500">or click to browse</p>
                </div>
                <p className="text-xs text-gray-400">
                  Supports: JPG, PNG, WebP (Max 10MB)
                </p>
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
              <svg className="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-red-700">{error}</span>
            </div>
          )}

          {/* Analyze Button */}
          {selectedFile && (
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="mt-6 w-full py-4 px-6 bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold rounded-xl
                hover:from-green-600 hover:to-blue-600 disabled:opacity-70 disabled:cursor-not-allowed
                transition-all transform hover:scale-[1.02] flex items-center justify-center gap-3"
            >
              {isAnalyzing ? (
                <>
                  <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Analyzing... Please wait</span>
                </>
              ) : (
                <>
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <span>Analyze Image</span>
                </>
              )}
            </button>
          )}
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Result Header */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-blue-500 p-6 text-white">
              <h2 className="text-2xl font-bold mb-2">Analysis Complete! ✅</h2>
              <p className="text-green-100">Here's what we found in your crop image</p>
            </div>
            
            <div className="p-6">
              <div className="flex flex-col md:flex-row gap-6">
                {/* Image */}
                <div className="md:w-1/3">
                  <img
                    src={result.image_url}
                    alt="Analyzed crop"
                    className="w-full rounded-xl shadow-md"
                  />
                </div>
                
                {/* Disease Info */}
                <div className="md:w-2/3 space-y-4">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-2xl font-bold text-gray-800">
                        {result.predicted_disease}
                      </h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-bold ${getConfidenceColor(result.confidence)}`}>
                        {result.confidence.toFixed(1)}% Confidence
                      </span>
                    </div>
                    <p className="text-gray-500 text-sm">
                      Detected on {new Date(result.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Information */}
          <div className="grid md:grid-cols-3 gap-6">
            {/* Symptoms */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                  <span className="text-xl">🔴</span>
                </div>
                <h4 className="font-bold text-gray-800">Symptoms</h4>
              </div>
              <p className="text-gray-600 text-sm leading-relaxed">
                {result.symptoms || 'No specific symptoms identified'}
              </p>
            </div>

            {/* Treatment */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <span className="text-xl">💊</span>
                </div>
                <h4 className="font-bold text-gray-800">Treatment</h4>
              </div>
              <p className="text-gray-600 text-sm leading-relaxed">
                {result.treatment || 'Consult a local agricultural expert'}
              </p>
            </div>

            {/* Pesticide */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <span className="text-xl">🧪</span>
                </div>
                <h4 className="font-bold text-gray-800">Recommended Pesticide</h4>
              </div>
              <p className="text-gray-600 text-sm leading-relaxed">
                {result.pesticide || 'No pesticide recommendation available'}
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={handleReset}
              className="flex-1 py-4 px-6 bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold rounded-xl
                hover:from-green-600 hover:to-blue-600 transition-all flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Analyze Another Image
            </button>
            <button
              onClick={() => window.print()}
              className="flex-1 py-4 px-6 bg-gray-100 text-gray-700 font-bold rounded-xl
                hover:bg-gray-200 transition-all flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print Report
            </button>
          </div>

          {/* Warning */}
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <div className="flex items-start gap-3">
              <span className="text-2xl">⚠️</span>
              <div>
                <h4 className="font-semibold text-amber-800">Important Notice</h4>
                <p className="text-amber-700 text-sm">
                  This AI-based diagnosis is for informational purposes only. For accurate diagnosis and treatment, 
                  please consult a certified agricultural expert or your local agricultural extension office.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Detect;
