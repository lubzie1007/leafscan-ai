import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Home from './pages/Home';
import Result from './pages/Result';
import History from './pages/History';
import Chatbot from './components/Chatbot';
import { predictLeaf } from './api';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [result, setResult] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [loadingStage, setLoadingStage] = useState(0);

  const handleAnalyze = async (file) => {
    const localUrl = URL.createObjectURL(file);
    setImageUrl(localUrl);
    setActiveTab('loading');
    setError(null);
    setLoadingStage(0);
    setIsAnalyzing(true);

    try {
      await new Promise((r) => setTimeout(r, 400));
      setLoadingStage(1);

      const data = await predictLeaf(file);

      setLoadingStage(2);
      await new Promise((r) => setTimeout(r, 300));

      const newRecord = {
        id: Date.now(),
        date: new Date().toLocaleDateString(),
        imageUrl: localUrl,
        result: data
      };
      setHistory(prev => [newRecord, ...prev]);

      setResult(data);
      setActiveTab('result');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'Backend error.');
      setActiveTab('analyse');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSelectHistory = (record) => {
    setImageUrl(record.imageUrl);
    setResult(record.result);
    setActiveTab('result');
  };

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={(tab) => {
          setActiveTab(tab);
          if (tab !== 'result') { setResult(null); setImageUrl(null); }
        }} 
      />

      {/* Main Content Area */}
      <main className="main-content">
        {error && <div className="error-toast">{error}</div>}

        {activeTab === 'dashboard' && (
          <Dashboard 
            history={history} 
            onStartScan={() => setActiveTab('analyse')} 
            onSelectHistory={handleSelectHistory} 
          />
        )}

        {activeTab === 'analyse' && (
          <Home onAnalyze={handleAnalyze} isAnalyzing={isAnalyzing} />
        )}

        {activeTab === 'history' && (
          <History history={history} onSelectHistory={handleSelectHistory} />
        )}

        {activeTab === 'result' && result && (
          <Result result={result} imageUrl={imageUrl} onBack={() => setActiveTab('analyse')} />
        )}

        {activeTab === 'loading' && (
          <div className="loading-overlay">
            <div className="spinner" />
            <div className="loading-steps">
              <div className={`loading-step ${loadingStage >= 0 ? 'done' : 'active'}`}>
                <div className="loading-step-icon">✓</div> <span>Image received</span>
              </div>
              <div className={`loading-step ${loadingStage > 1 ? 'done' : loadingStage === 1 ? 'active' : ''}`}>
                <div className="loading-step-icon">{loadingStage > 1 ? '✓' : '1'}</div> <span>Analyzing leaf</span>
              </div>
              <div className={`loading-step ${loadingStage > 2 ? 'done' : loadingStage === 2 ? 'active' : ''}`}>
                <div className="loading-step-icon">{loadingStage > 2 ? '✓' : '2'}</div> <span>Generating advice</span>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Floating Chatbot - Sits outside main so it stays on screen everywhere */}
      <Chatbot />
    </div>
  );
}