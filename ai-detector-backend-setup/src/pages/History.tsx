import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { predictionsApi } from '../services/api';
import { Prediction } from '../types';

const History: React.FC = () => {
  const { user } = useAuth();
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPrediction, setSelectedPrediction] = useState<Prediction | null>(null);

  useEffect(() => {
    loadHistory();
  }, [user]);

  const loadHistory = async () => {
    if (!user) return;
    
    setIsLoading(true);
    try {
      const response = await predictionsApi.getHistory(user.id);
      setPredictions(response.predictions);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this prediction?')) return;
    
    try {
      await predictionsApi.deletePrediction(id);
      setPredictions(prev => prev.filter(p => p.id !== id));
      if (selectedPrediction?.id === id) {
        setSelectedPrediction(null);
      }
    } catch (error) {
      console.error('Failed to delete:', error);
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'text-green-600 bg-green-100';
    if (confidence >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">📊 Prediction History</h1>
          <p className="text-gray-600">View all your past disease detections</p>
        </div>
        <div className="text-sm text-gray-500">
          Total: {predictions.length} predictions
        </div>
      </div>

      {predictions.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center">
          <div className="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
            <span className="text-5xl">📭</span>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">No predictions yet</h3>
          <p className="text-gray-500 mb-6">
            Upload a crop image to get your first disease detection
          </p>
          <a
            href="/detect"
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg hover:from-green-600 hover:to-blue-600 transition-all"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Start Detection
          </a>
        </div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Predictions List */}
          <div className="lg:col-span-2 space-y-4">
            {predictions.map((prediction) => (
              <div
                key={prediction.id}
                onClick={() => setSelectedPrediction(prediction)}
                className={`bg-white rounded-xl shadow-sm border-2 p-4 cursor-pointer transition-all hover:shadow-md
                  ${selectedPrediction?.id === prediction.id ? 'border-green-500' : 'border-transparent hover:border-green-200'}`}
              >
                <div className="flex gap-4">
                  {/* Thumbnail */}
                  <div className="w-20 h-20 flex-shrink-0">
                    <img
                      src={prediction.image_url}
                      alt={prediction.predicted_disease}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  </div>
                  
                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="font-semibold text-gray-800 truncate">
                        {prediction.predicted_disease}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-bold ${getConfidenceColor(prediction.confidence)}`}>
                        {prediction.confidence.toFixed(1)}%
                      </span>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">
                      {formatDate(prediction.created_at)}
                    </p>
                    <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                      {prediction.symptoms?.substring(0, 100)}...
                    </p>
                  </div>
                  
                  {/* Actions */}
                  <button
                    onClick={(e) => { e.stopPropagation(); handleDelete(prediction.id); }}
                    className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Detail Panel */}
          <div className="lg:col-span-1">
            {selectedPrediction ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 sticky top-24 space-y-6">
                <img
                  src={selectedPrediction.image_url}
                  alt={selectedPrediction.predicted_disease}
                  className="w-full rounded-xl shadow-md"
                />
                
                <div>
                  <h3 className="text-xl font-bold text-gray-800 mb-1">
                    {selectedPrediction.predicted_disease}
                  </h3>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${getConfidenceColor(selectedPrediction.confidence)}`}>
                      {selectedPrediction.confidence.toFixed(1)}% Confidence
                    </span>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <span>🔴</span> Symptoms
                  </h4>
                  <p className="text-sm text-gray-600">
                    {selectedPrediction.symptoms}
                  </p>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <span>💊</span> Treatment
                  </h4>
                  <p className="text-sm text-gray-600">
                    {selectedPrediction.treatment}
                  </p>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                    <span>🧪</span> Pesticide
                  </h4>
                  <p className="text-sm text-gray-600">
                    {selectedPrediction.pesticide}
                  </p>
                </div>

                <p className="text-xs text-gray-400">
                  Analyzed on {formatDate(selectedPrediction.created_at)}
                </p>
              </div>
            ) : (
              <div className="bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 p-8 text-center sticky top-24">
                <div className="text-4xl mb-4">👆</div>
                <p className="text-gray-500">
                  Select a prediction to view details
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
