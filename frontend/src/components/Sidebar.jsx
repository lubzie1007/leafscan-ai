import { Leaf, LayoutDashboard, ScanLine, Clock } from 'lucide-react';
// Note: Run `npm install lucide-react` in your terminal for the icons!

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { id: 'analyse', label: 'Analyse Plant', icon: <ScanLine size={20} /> },
    { id: 'history', label: 'History', icon: <Clock size={20} /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <Leaf size={28} color="#166534" />
        <h2>CropDoctor AI</h2>
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${activeTab === item.id || (activeTab === 'result' && item.id === 'analyse') ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}