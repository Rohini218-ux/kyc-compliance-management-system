function StatCard({ title, value, icon, color }) {
  return (
    <div className="stat-card">
      <div className="stat-info">
        <p>{title}</p>
        <h2>{value?.toLocaleString() ?? 0}</h2>
      </div>

      <div className="stat-icon" style={{ background: color }}>
        {icon}
      </div>
    </div>
  );
}

export default StatCard;