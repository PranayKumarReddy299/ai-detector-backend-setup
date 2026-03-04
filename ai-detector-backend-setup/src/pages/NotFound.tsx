import React from 'react';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-blue-50 to-emerald-50 p-4">
      <div className="text-center">
        <div className="mb-8">
          <span className="text-9xl">🌾</span>
        </div>
        <h1 className="text-6xl font-bold text-gray-800 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-gray-600 mb-4">Page Not Found</h2>
        <p className="text-gray-500 mb-8 max-w-md mx-auto">
          Looks like this crop field doesn't exist. Let's get you back to familiar ground.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/dashboard"
            className="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-lg hover:from-green-600 hover:to-blue-600 transition-all"
          >
            Go to Dashboard
          </Link>
          <Link
            to="/detect"
            className="px-6 py-3 bg-white text-green-600 font-semibold rounded-lg border-2 border-green-500 hover:bg-green-50 transition-all"
          >
            Start Detection
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
