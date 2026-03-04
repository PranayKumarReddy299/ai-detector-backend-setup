import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const features = [
    {
      icon: '📸',
      title: 'Upload Image',
      description: 'Take or upload a photo of your crop',
      link: '/detect',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: '🔬',
      title: 'AI Analysis',
      description: 'Our AI detects diseases instantly',
      link: '/detect',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: '💊',
      title: 'Get Treatment',
      description: 'Receive treatment recommendations',
      link: '/detect',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: '📊',
      title: 'View History',
      description: 'Track all your past predictions',
      link: '/history',
      color: 'from-orange-500 to-amber-500'
    }
  ];

  const crops = [
    { name: 'Tomato', icon: '🍅', diseases: 9 },
    { name: 'Potato', icon: '🥔', diseases: 3 },
    { name: 'Corn', icon: '🌽', diseases: 4 },
    { name: 'Apple', icon: '🍎', diseases: 4 },
    { name: 'Grape', icon: '🍇', diseases: 4 },
    { name: 'Rice', icon: '🌾', diseases: 3 },
    { name: 'Wheat', icon: '🌿', diseases: 3 }
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-green-500 to-blue-500 rounded-2xl p-8 text-white">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold mb-2">
              Welcome back, {user?.email.split('@')[0]}! 👋
            </h1>
            <p className="text-green-100 text-lg">
              Ready to protect your crops? Upload an image to detect diseases.
            </p>
          </div>
          <Link
            to="/detect"
            className="mt-6 md:mt-0 px-8 py-4 bg-white text-green-600 font-bold rounded-xl hover:bg-green-50 transition-all transform hover:scale-105 shadow-lg flex items-center gap-2"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Start Detection
          </Link>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="text-3xl mb-2">🌱</div>
          <div className="text-2xl font-bold text-gray-800">30+</div>
          <div className="text-sm text-gray-500">Diseases Detectable</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="text-3xl mb-2">🎯</div>
          <div className="text-2xl font-bold text-gray-800">95%</div>
          <div className="text-sm text-gray-500">Accuracy Rate</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="text-3xl mb-2">⚡</div>
          <div className="text-2xl font-bold text-gray-800">&lt;2s</div>
          <div className="text-sm text-gray-500">Detection Speed</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="text-3xl mb-2">🌍</div>
          <div className="text-2xl font-bold text-gray-800">7</div>
          <div className="text-sm text-gray-500">Crop Types</div>
        </div>
      </div>

      {/* Features Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.link}
              className="group bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
            >
              <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform`}>
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-500 text-sm">{feature.description}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Supported Crops */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Supported Crops</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-4">
          {crops.map((crop, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 text-center hover:shadow-md transition-all"
            >
              <div className="text-4xl mb-2">{crop.icon}</div>
              <div className="font-semibold text-gray-800">{crop.name}</div>
              <div className="text-xs text-gray-500">{crop.diseases} diseases</div>
            </div>
          ))}
        </div>
      </div>

      {/* Tips Section */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl p-6 border border-amber-200">
        <h2 className="text-xl font-bold text-amber-800 mb-4 flex items-center gap-2">
          <span>💡</span> Tips for Best Results
        </h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-amber-200 rounded-full flex items-center justify-center text-amber-800 font-bold text-sm flex-shrink-0">1</div>
            <p className="text-amber-900 text-sm">Take clear, well-lit photos of the affected plant parts</p>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-amber-200 rounded-full flex items-center justify-center text-amber-800 font-bold text-sm flex-shrink-0">2</div>
            <p className="text-amber-900 text-sm">Focus on leaves, stems, or fruits showing symptoms</p>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-amber-200 rounded-full flex items-center justify-center text-amber-800 font-bold text-sm flex-shrink-0">3</div>
            <p className="text-amber-900 text-sm">Avoid blurry images and ensure good lighting</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
