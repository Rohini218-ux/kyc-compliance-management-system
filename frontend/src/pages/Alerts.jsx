
import { useEffect, useState } from "react";
import {
  Search,
  Bell,
  AlertTriangle,
  CheckCircle,
  RefreshCw
} from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [openAlerts, setOpenAlerts] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [severityFilter, setSeverityFilter] = useState("ALL");

  const [selectedAlert, setSelectedAlert] = useState(null);
  const [newStatus, setNewStatus] = useState("");
  const [remarks, setRemarks] = useState("");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const fetchAlerts = async () => {
    setLoading(true);
    setError("");

    try {
      const [allResponse, openResponse] = await Promise.all([
        api.get("/alerts/", {
          params: { skip: 0, limit: 100 }
        }),
        api.get("/alerts/open")
      ]);

      setAlerts(allResponse.data);
      setOpenAlerts(openResponse.data);
    } catch (err) {
      console.error("Alert API error:", err.response?.data || err);
      setError(
        err.response?.data?.detail || "Unable to load alerts."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();

    if (!selectedAlert || !newStatus) {
      setError("Please select an alert status.");
      return;
    }

    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.patch(
        `/alerts/${selectedAlert.alert_id}`,
        {
          status: newStatus,
          performed_by: "api_user",
          remarks: remarks.trim() || null
        }
      );

      setMessage("Alert updated successfully.");
      setSelectedAlert(null);
      setNewStatus("");
      setRemarks("");

      await fetchAlerts();
    } catch (err) {
      console.error("Alert update error:", err.response?.data || err);

      setError(
        err.response?.data?.detail || "Unable to update alert."
      );
    } finally {
      setSaving(false);
    }
  };

  const filteredAlerts = alerts.filter((alert) => {
    const searchText = search.toLowerCase();

    const matchesSearch =
      alert.alert_id?.toLowerCase().includes(searchText) ||
      alert.customer_id?.toLowerCase().includes(searchText) ||
      alert.alert_type?.toLowerCase().includes(searchText) ||
      alert.description?.toLowerCase().includes(searchText);

    const matchesStatus =
      statusFilter === "ALL" || alert.status === statusFilter;

    const matchesSeverity =
      severityFilter === "ALL" || alert.severity === severityFilter;

    return matchesSearch && matchesStatus && matchesSeverity;
  });

  const counts = alerts.reduce(
    (result, alert) => {
      result[alert.status] = (result[alert.status] || 0) + 1;
      return result;
    },
    {}
  );

  const formatDate = (value) => {
    if (!value) return "—";
    return new Date(value).toLocaleString("en-IN");
  };

  const openUpdateForm = (alert) => {
    setSelectedAlert(alert);
    setNewStatus(alert.status);
    setRemarks("");
    setError("");
    setMessage("");
  };

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="customers-page">

          <div className="page-heading">
            <div>
              <h1>Alerts Management</h1>
              <p>
                Monitor compliance alerts and manage alert resolution.
              </p>
            </div>

            <button
              className="add-customer-btn"
              onClick={fetchAlerts}
              disabled={loading}
            >
              <RefreshCw size={18} />
              Refresh
            </button>
          </div>

          {message && (
            <p className="success-message">{message}</p>
          )}

          {error && (
            <p className="error-message">{error}</p>
          )}

          {loading ? (
            <p>Loading alerts...</p>
          ) : (
            <>
              {/* Summary cards */}
              <div className="stats-grid">

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Alert Records Loaded</p>
                    <h2>{alerts.length}</h2>
                  </div>
                  <div className="stat-icon">
                    <Bell size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Open Alerts</p>
                    <h2>{counts.OPEN || 0}</h2>
                  </div>
                  <div className="stat-icon">
                    <AlertTriangle size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Acknowledged</p>
                    <h2>{counts.ACKNOWLEDGED || 0}</h2>
                  </div>
                  <div className="stat-icon">
                    <Bell size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Resolved</p>
                    <h2>{counts.RESOLVED || 0}</h2>
                  </div>
                  <div className="stat-icon">
                    <CheckCircle size={24} />
                  </div>
                </div>

              </div>

              <p className="page-description">
                Status totals above are based on the first 100 alert
                records loaded. Open alert count from the separate
                endpoint: {openAlerts.length}.
              </p>

              {/* Update alert form */}
              {selectedAlert && (
                <div className="customer-table-card">
                  <h3>Update Alert</h3>

                  <p>
                    Alert ID: <strong>{selectedAlert.alert_id}</strong>
                  </p>

                  <p>
                    Customer ID: <strong>{selectedAlert.customer_id}</strong>
                  </p>

                  <form
                    className="document-upload-form"
                    onSubmit={handleUpdate}
                  >
                    <label>Alert Status</label>

                    <select
                      value={newStatus}
                      onChange={(e) => setNewStatus(e.target.value)}
                      required
                    >
                      <option value="OPEN">Open</option>
                      <option value="ACKNOWLEDGED">Acknowledged</option>
                      <option value="RESOLVED">Resolved</option>
                    </select>

                    <label>Remarks</label>

                    <textarea
                      value={remarks}
                      onChange={(e) => setRemarks(e.target.value)}
                      placeholder="Enter update remarks"
                      rows="3"
                    />

                    <div className="review-form-actions">
                      <button
                        type="submit"
                        className="add-customer-btn"
                        disabled={saving}
                      >
                        {saving ? "Saving..." : "Save Changes"}
                      </button>

                      <button
                        type="button"
                        className="download-btn"
                        onClick={() => setSelectedAlert(null)}
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Search and filters */}
              <div className="customer-toolbar">
                <div className="customer-search">
                  <Search size={18} />

                  <input
                    type="text"
                    placeholder="Search alert ID, customer ID or description..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                  />
                </div>

                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="ALL">All Statuses</option>
                  <option value="OPEN">Open</option>
                  <option value="ACKNOWLEDGED">Acknowledged</option>
                  <option value="RESOLVED">Resolved</option>
                </select>

                <select
                  value={severityFilter}
                  onChange={(e) => setSeverityFilter(e.target.value)}
                >
                  <option value="ALL">All Severities</option>
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>

              {/* Alerts table */}
              <div className="customer-table-card">

                <div className="customer-table-heading">
                  <AlertTriangle size={20} />
                  <h3>Alerts ({filteredAlerts.length})</h3>
                </div>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Alert ID</th>
                        <th>Customer ID</th>
                        <th>Alert Type</th>
                        <th>Severity</th>
                        <th>Description</th>
                        <th>Status</th>
                        <th>Created At</th>
                        <th>Action</th>
                      </tr>
                    </thead>

                    <tbody>
                      {filteredAlerts.map((alert) => (
                        <tr key={alert.alert_id}>
                          <td>{alert.alert_id}</td>
                          <td>{alert.customer_id}</td>
                          <td>{alert.alert_type}</td>

                          <td>
                            <span
                              className={`status-badge ${alert.severity.toLowerCase()}`}
                            >
                              {alert.severity}
                            </span>
                          </td>

                          <td>{alert.description}</td>

                          <td>
                            <span
                              className={`status-badge ${alert.status.toLowerCase()}`}
                            >
                              {alert.status.replace("_", " ")}
                            </span>
                          </td>

                          <td>{formatDate(alert.created_at)}</td>

                          <td>
                            <button
                              type="button"
                              className="download-btn"
                              disabled={alert.status === "RESOLVED"}
                              onClick={() => openUpdateForm(alert)}
                            >
                              Update
                            </button>
                          </td>
                        </tr>
                      ))}

                      {filteredAlerts.length === 0 && (
                        <tr>
                          <td colSpan="8">No alerts found.</td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default Alerts;
