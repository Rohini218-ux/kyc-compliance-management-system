
import { useEffect, useState } from "react";
import {
  Search,
  ClipboardList,
  RefreshCw,
  AlertTriangle,
  CheckCircle
} from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function Reviews() {
  const [reviews, setReviews] = useState([]);
  const [overdueReviews, setOverdueReviews] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [selectedReview, setSelectedReview] = useState(null);
  const [newStatus, setNewStatus] = useState("");
  const [remarks, setRemarks] = useState("");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  // Fetch review data
  const fetchReviews = async () => {
    setLoading(true);
    setError("");

    try {
      const [reviewResponse, overdueResponse] = await Promise.all([
        api.get("/reviews/", {
          params: { skip: 0, limit: 100 }
        }),
        api.get("/reviews/overdue")
      ]);

      setReviews(reviewResponse.data);
      setOverdueReviews(overdueResponse.data);
    } catch (err) {
      console.error("Review API error:", err.response?.data || err);
      setError(
        err.response?.data?.detail || "Unable to load review information."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  // Update review
  const handleUpdate = async (e) => {
    e.preventDefault();

    if (!selectedReview || !newStatus) {
      setError("Please select a review status.");
      return;
    }

    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.patch(
        `/reviews/${selectedReview.review_case_id}`,
        {
          status: newStatus,
          remarks: remarks.trim() || null
        }
      );

      setMessage("Review updated successfully.");
      setSelectedReview(null);
      setNewStatus("");
      setRemarks("");

      await fetchReviews();
    } catch (err) {
      console.error("Review update error:", err.response?.data || err);

      setError(
        err.response?.data?.detail || "Unable to update review."
      );
    } finally {
      setSaving(false);
    }
  };

  // Search and filter
  const filteredReviews = reviews.filter((review) => {
    const searchText = search.toLowerCase();

    const matchesSearch =
      review.review_case_id?.toLowerCase().includes(searchText) ||
      review.customer_id?.toLowerCase().includes(searchText);

    const matchesStatus =
      statusFilter === "ALL" || review.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const formatDate = (value) => {
    if (!value) return "—";
    return new Date(value).toLocaleDateString("en-IN");
  };

  const openUpdateForm = (review) => {
    setSelectedReview(review);
    setNewStatus(review.status);
    setRemarks(review.remarks || "");
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
              <h1>Reviews Management</h1>
              <p>
                Monitor customer KYC reviews, deadlines and review status.
              </p>
            </div>

            <button
              className="add-customer-btn"
              onClick={fetchReviews}
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
            <p>Loading reviews...</p>
          ) : (
            <>
              {/* Summary cards */}
              <div className="stats-grid">

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Review Records Loaded</p>
                    <h2>{reviews.length}</h2>
                  </div>
                  <div className="stat-icon">
                    <ClipboardList size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Open Reviews</p>
                    <h2>
                      {reviews.filter((r) => r.status === "OPEN").length}
                    </h2>
                  </div>
                  <div className="stat-icon">
                    <ClipboardList size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Completed Reviews</p>
                    <h2>
                      {reviews.filter((r) => r.status === "COMPLETED").length}
                    </h2>
                  </div>
                  <div className="stat-icon">
                    <CheckCircle size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Overdue Reviews</p>
                    <h2>{overdueReviews.length}</h2>
                  </div>
                  <div className="stat-icon">
                    <AlertTriangle size={24} />
                  </div>
                </div>

              </div>

              <p className="page-description">
                Review summary counts are based on the first 100 records
                loaded. Overdue count uses the overdue API response.
              </p>

              {/* Update review form */}
              {selectedReview && (
                <div className="customer-table-card">
                  <h3>Update Review</h3>

                  <p>
                    Review ID: <strong>{selectedReview.review_case_id}</strong>
                  </p>

                  <p>
                    Customer ID: <strong>{selectedReview.customer_id}</strong>
                  </p>

                  <form
                    className="document-upload-form"
                    onSubmit={handleUpdate}
                  >
                    <label>Review Status</label>

                    <select
                      value={newStatus}
                      onChange={(e) => setNewStatus(e.target.value)}
                      required
                    >
                      <option value="OPEN">Open</option>
                      <option value="IN_PROGRESS">In Progress</option>
                      <option value="COMPLETED">Completed</option>
                      <option value="OVERDUE">Overdue</option>
                      <option value="CANCELLED">Cancelled</option>
                    </select>

                    <label>Remarks</label>

                    <textarea
                      value={remarks}
                      onChange={(e) => setRemarks(e.target.value)}
                      placeholder="Enter review remarks"
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
                        onClick={() => setSelectedReview(null)}
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Search and filter */}
              <div className="customer-toolbar">
                <div className="customer-search">
                  <Search size={18} />

                  <input
                    type="text"
                    placeholder="Search review ID or customer ID..."
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
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="COMPLETED">Completed</option>
                  <option value="OVERDUE">Overdue</option>
                  <option value="CANCELLED">Cancelled</option>
                </select>
              </div>

              {/* Reviews table */}
              <div className="customer-table-card">

                <div className="customer-table-heading">
                  <ClipboardList size={20} />
                  <h3>Review Cases ({filteredReviews.length})</h3>
                </div>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Review ID</th>
                        <th>Customer ID</th>
                        <th>Review Type</th>
                        <th>Due Date</th>
                        <th>Status</th>
                        <th>Completed Date</th>
                        <th>Action</th>
                      </tr>
                    </thead>

                    <tbody>
                      {filteredReviews.map((review) => (
                        <tr key={review.review_case_id}>
                          <td>{review.review_case_id}</td>
                          <td>{review.customer_id}</td>
                          <td>{review.review_type}</td>
                          <td>{formatDate(review.review_due_date)}</td>

                          <td>
                            <span
                              className={`status-badge ${
                                review.status.toLowerCase()
                              }`}
                            >
                              {review.status.replace("_", " ")}
                            </span>
                          </td>

                          <td>{formatDate(review.completed_date)}</td>

                          <td>
                            <button
                              type="button"
                              className="download-btn"
                              disabled={
                                review.status === "COMPLETED" ||
                                review.status === "CANCELLED"
                              }
                              onClick={() => openUpdateForm(review)}
                            >
                              Update
                            </button>
                          </td>
                        </tr>
                      ))}

                      {filteredReviews.length === 0 && (
                        <tr>
                          <td colSpan="7">No reviews found.</td>
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

export default Reviews;
