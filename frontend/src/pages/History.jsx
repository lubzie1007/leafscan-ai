export default function History({ history, onSelectHistory }) {
  return (
    <div className="history-container">
      <h1 className="page-title">Scan History</h1>
      {history.length === 0 ? (
        <p>You haven't scanned any plants yet.</p>
      ) : (
        <div className="history-list">
          {history.map(item => (
            <div key={item.id} className="history-item" onClick={() => onSelectHistory(item)}>
              <img src={item.imageUrl} alt="Thumbnail" />
              <div className="history-details">
                <h3>{item.result.disease.replace(/___/g, ' • ').replace(/_/g, ' ')}</h3>
                <p>{item.date} • {(item.result.confidence * 100).toFixed(1)}% confidence</p>
              </div>
              <div className="history-arrow">→</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}