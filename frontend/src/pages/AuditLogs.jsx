
import { useEffect, useState } from "react";
import {
  Search,
  History,
  RefreshCw,
  FileText
} from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function AuditLogs() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState("");
  const [entityType, setEntityType] = useState("ALL");
  const [action, setAction] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedEvent, setSelectedEvent] = useState(null);

  const fetchAuditEvents = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await api.get("/audit-logs/", {
        params: {
          skip: 0,
          limit: 100,
          ...(entityType !== "ALL" && { entity_type: entityType }),
          ...(action !== "ALL" && { action })
        }
      });

      setEvents(response.data);
    } catch (err) {
      console.error("Audit API error:", err.response?.data || err);
      setError(
        err.response?.data?.detail || "Unable to load audit events."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAuditEvents();
  }, [entityType, action]);

  const filteredEvents = events.filter((event) => {
    const searchText = search.toLowerCase();

    return (
      event.audit_event_id?.toLowerCase().includes(searchText) ||
      event.entity_id?.toLowerCase().includes(searchText) ||
      event.entity_type?.toLowerCase().includes(searchText) ||
      event.performed_by?.toLowerCase().includes(searchText) ||
      event.action?.toLowerCase().includes(searchText) ||
      event.details?.toLowerCase().includes(searchText)
    );
  });

  const formatDate = (value) => {
    if (!value) return "—";
    return new Date(value).toLocaleString("en-IN");
  };

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="customers-page">

          {/* Heading */}
          <div className="page-heading">
            <div>
              <h1>Audit Logs Management</h1>
              <p>
                Track system activities and maintain a history
                of compliance operations.
              </p>
            </div>

            <button
              className="add-customer-btn"
              onClick={fetchAuditEvents}
              disabled={loading}
            >
              <RefreshCw size={18} />
              Refresh
            </button>
          </div>

          {error && (
            <p className="error-message">{error}</p>
          )}

          {/* Summary */}
          {!loading && (
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-info">
                  <p>Audit Events Loaded</p>
                  <h2>{events.length}</h2>
                </div>
                <div className="stat-icon">
                  <History size={24} />
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-info">
                  <p>Entity Types</p>
                  <h2>
                    {new Set(events.map((e) => e.entity_type)).size}
                  </h2>
                </div>
                <div className="stat-icon">
                  <FileText size={24} />
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-info">
                  <p>Unique Actions</p>
                  <h2>
                    {new Set(events.map((e) => e.action)).size}
                  </h2>
                </div>
                <div className="stat-icon">
                  <History size={24} />
                </div>
              </div>
            </div>
          )}

          {/* Filters */}
          <div className="customer-toolbar">

            <div className="customer-search">
              <Search size={18} />

              <input
                type="text"
                placeholder="Search event, entity, user or action..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <select
              value={entityType}
              onChange={(e) => setEntityType(e.target.value)}
            >
              <option value="ALL">All Entity Types</option>
              <option value="CUSTOMER">Customer</option>
              <option value="DOCUMENT">Document</option>
              <option value="REVIEW_CASE">Review Case</option>
              <option value="ALERT">Alert</option>
            </select>

            <select
              value={action}
              onChange={(e) => setAction(e.target.value)}
            >
              <option value="ALL">All Actions</option>
              <option value="REVIEW_STATUS_UPDATED">
                Review Status Updated
              </option>
              <option value="ALERT_STATUS_UPDATED">
                Alert Status Updated
              </option>
              <option value="DOCUMENT_VERIFIED">
                Document Verified
              </option>
              <option value="DOCUMENT_REJECTED">
                Document Rejected
              </option>
            </select>

          </div>

          {/* Audit table */}
          <div className="customer-table-card">

            <div className="customer-table-heading">
              <History size={20} />
              <h3>Audit Events ({filteredEvents.length})</h3>
            </div>

            {loading ? (
              <p>Loading audit events...</p>
            ) : (
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Event ID</th>
                      <th>Entity Type</th>
                      <th>Entity ID</th>
                      <th>Action</th>
                      <th>Performed By</th>
                      <th>Timestamp</th>
                      <th>Details</th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredEvents.map((event) => (
                      <tr key={event.audit_event_id}>
                        <td>{event.audit_event_id}</td>
                        <td>{event.entity_type}</td>
                        <td>{event.entity_id}</td>
                        <td>{event.action}</td>
                        <td>{event.performed_by}</td>
                        <td>{formatDate(event.event_timestamp)}</td>
                        <td>
                          <button
                            type="button"
                            className="download-btn"
                            onClick={() => setSelectedEvent(event)}
                          >
                            View Details
                          </button>
                        </td>
                      </tr>
                    ))}

                    {filteredEvents.length === 0 && (
                      <tr>
                        <td colSpan="7">
                          No audit events found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Event details */}
          {selectedEvent && (
            <div className="customer-table-card">
              <div className="customer-table-heading">
                <FileText size={20} />
                <h3>Audit Event Details</h3>
              </div>

              <p><strong>Event ID:</strong> {selectedEvent.audit_event_id}</p>
              <p><strong>Entity:</strong> {selectedEvent.entity_type}</p>
              <p><strong>Entity ID:</strong> {selectedEvent.entity_id}</p>
              <p><strong>Action:</strong> {selectedEvent.action}</p>
              <p><strong>Performed By:</strong> {selectedEvent.performed_by}</p>
              <p><strong>Timestamp:</strong> {formatDate(selectedEvent.event_timestamp)}</p>
              <p><strong>Details:</strong> {selectedEvent.details || "—"}</p>

              <button
                className="download-btn"
                onClick={() => setSelectedEvent(null)}
              >
                Close Details
              </button>
            </div>
          )}

          <p className="page-description">
            Audit logs are read-only. This page displays up to 100
            records per request.
          </p>

        </section>
      </main>
    </div>
  );
}

export default AuditLogs;
