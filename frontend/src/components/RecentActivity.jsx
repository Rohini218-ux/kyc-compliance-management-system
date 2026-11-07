import { useEffect, useState } from "react";
import { Clock, Activity } from "lucide-react";
import api from "../services/api";

function RecentActivity() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/audit/", { params: { limit: 8 } })
      .then((response) => {
        setActivities(response.data);
      })
      .catch((error) => {
        console.error("Audit API Error:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="activity-card">
      <h3>
        <Activity size={20} />
        Recent Activity
      </h3>

      {loading && <p>Loading activities...</p>}

      {!loading && activities.length === 0 && (
        <p>No recent activities found.</p>
      )}

      {activities.map((activity) => (
        <div className="activity-item" key={activity.audit_event_id}>
          <div className="activity-icon">
            <Clock size={18} />
          </div>

          <div className="activity-details">
            <strong>{activity.action.replaceAll("_", " ")}</strong>

            <p>
              {activity.entity_type} · {activity.entity_id}
            </p>

            <small>
              By {activity.performed_by} ·{" "}
              {new Date(activity.event_timestamp).toLocaleString()}
            </small>
          </div>
        </div>
      ))}
    </div>
  );
}

export default RecentActivity;