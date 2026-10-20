export default function Dashboard({ history, onStartScan, onSelectHistory }) {
  // Generate some basic stats from our session history
  const totalScans = history.length;
  const healthyCount = history.filter(h => h.result.disease.includes('healthy')).length;
  const diseaseCount = totalScans - healthyCount;

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1>Welcome back! 🌱</h1>
          <p>Monitor your crops and get instant AI insights.</p>
        </div>
      </header>

      {/* Stats Row */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#f0fdf4', color: '#16a34a' }}>📊</div>
          <div>
            <h3>{totalScans}</h3>
            <p>Total Scans</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef2f2', color: '#dc2626' }}>⚠️</div>
          <div>
            <h3>{diseaseCount}</h3>
            <p>Diseases Found</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#f0f9ff', color: '#0284c7' }}>✅</div>
          <div>
            <h3>{healthyCount}</h3>
            <p>Healthy Plants</p>
          </div>
        </div>
      </div>

      {/* CTA Banner */}
      <div className="cta-banner desktop-only">
        <div>
          <h2>Analyse a New Plant</h2>
          <p>Upload a photo of a leaf to detect diseases and get treatment plans.</p>
          <button className="btn-analyze" onClick={onStartScan}>Upload Image →</button>
        </div>
        <div className="cta-icon">🌿</div>
      </div>

      {/* Recent History */}
      <div className="recent-section">
        <h3>Recent Analyses</h3>
        {history.length === 0 ? (
          <p className="empty-text">No recent scans. Upload a leaf to get started!</p>
        ) : (
          <div className="recent-grid">
            {history.slice(0, 4).map(item => (
              <div key={item.id} className="recent-card" onClick={() => onSelectHistory(item)}>
                <img src={item.imageUrl} alt="Leaf" />
                <div className="recent-info">
                  <h4>{item.result.disease.split('___')[0]}</h4>
                  <p className={item.result.disease.includes('healthy') ? 'text-green' : 'text-red'}>
                    {item.result.disease.split('___')[1]?.replace(/_/g, ' ') || 'Healthy'}
                  </p>
                  <span>{item.date}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}