
import { useEffect, useState } from "react";
import {
  Search,
  ShieldCheck,
  AlertTriangle,
  Users,
  RefreshCw
} from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function RiskManagement() {
  const [risks, setRisks] = useState([]);
  const [highRiskCustomers, setHighRiskCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchRiskData = async () => {
    setLoading(true);
    setError("");

    try {
      const [riskResponse, highRiskResponse] = await Promise.all([
        api.get("/risks-management/", {
          params: { skip: 0, limit: 100 }
        }),
        api.get("/risks-management/high-risk")
      ]);

      setRisks(riskResponse.data);
      setHighRiskCustomers(highRiskResponse.data);
    } catch (err) {
      console.error("Risk API error:", err.response?.data || err);
      setError("Unable to load risk information. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRiskData();
  }, []);

  const filteredHighRisk = highRiskCustomers.filter((customer) => {
    const searchText = search.toLowerCase();

    return (
      customer.customer_id?.toLowerCase().includes(searchText) ||
      customer.customer_name?.toLowerCase().includes(searchText) ||
      customer.reason?.toLowerCase().includes(searchText)
    );
  });

  const riskCounts = risks.reduce(
    (counts, risk) => {
      const level = risk.risk_level?.toUpperCase();

      if (level === "LOW") counts.low++;
      if (level === "MEDIUM") counts.medium++;
      if (level === "HIGH") counts.high++;

      return counts;
    },
    { low: 0, medium: 0, high: 0 }
  );

  const formatDate = (value) => {
    if (!value) return "—";

    return new Date(value).toLocaleDateString("en-IN");
  };

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="customers-page">

          {/* Page heading */}
          <div className="page-heading">
            <div>
              <h1>Risk Management</h1>
              <p>
                Monitor customer risk ratings and identify high-risk
                customers.
              </p>
            </div>

            <button
              className="add-customer-btn"
              onClick={fetchRiskData}
              disabled={loading}
            >
              <RefreshCw size={18} />
              Refresh
            </button>
          </div>

          {error && (
            <p className="error-message">{error}</p>
          )}

          {loading ? (
            <p>Loading risk information...</p>
          ) : (
            <>
              {/* Summary cards */}
              <div className="stats-grid">

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Risk Records Loaded</p>
                    <h2>{risks.length}</h2>
                  </div>
                  <div className="stat-icon">
                    <Users size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Low Risk</p>
                    <h2>{riskCounts.low}</h2>
                  </div>
                  <div className="stat-icon">
                    <ShieldCheck size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>Medium Risk</p>
                    <h2>{riskCounts.medium}</h2>
                  </div>
                  <div className="stat-icon">
                    <AlertTriangle size={24} />
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-info">
                    <p>High-Risk Customers</p>
                    <h2>{highRiskCustomers.length.toLocaleString()}</h2>
                  </div>
                  <div className="stat-icon">
                    <AlertTriangle size={24} />
                  </div>
                </div>

              </div>

              <p className="page-description">
                Risk distribution above is based on the first 100
                current risk records loaded. High-risk customer count
                comes from the complete high-risk API response.
              </p>

              {/* High-risk customer table */}
              <div className="customer-table-card">

                <div className="customer-table-heading">
                  <AlertTriangle size={20} />
                  <h3>
                    High-Risk Customers ({filteredHighRisk.length})
                  </h3>
                </div>

                {/* Search */}
                <div className="customer-toolbar">
                  <div className="customer-search">
                    <Search size={18} />

                    <input
                      type="text"
                      placeholder="Search customer ID, name or risk reason..."
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                    />
                  </div>
                </div>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Customer ID</th>
                        <th>Customer Name</th>
                        <th>Customer Status</th>
                        <th>Risk Level</th>
                        <th>Risk Reason</th>
                        <th>Effective From</th>
                      </tr>
                    </thead>

                    <tbody>
                      {filteredHighRisk.map((customer) => (
                        <tr key={customer.customer_id}>
                          <td>{customer.customer_id}</td>
                          <td>{customer.customer_name}</td>
                          <td>{customer.customer_status}</td>

                          <td>
                            <span className="status-badge rejected">
                              {customer.risk_level}
                            </span>
                          </td>

                          <td>{customer.reason || "—"}</td>

                          <td>
                            {formatDate(customer.effective_from)}
                          </td>
                        </tr>
                      ))}

                      {filteredHighRisk.length === 0 && (
                        <tr>
                          <td colSpan="6">
                            No high-risk customers found.
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>

              </div>

              {/* Current risk records */}
              <div className="customer-table-card">

                <div className="customer-table-heading">
                  <ShieldCheck size={20} />
                  <h3>Current Risk Ratings (First 100)</h3>
                </div>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Customer ID</th>
                        <th>Risk Level</th>
                        <th>Reason</th>
                        <th>Effective From</th>
                        <th>Effective To</th>
                      </tr>
                    </thead>

                    <tbody>
                      {risks.map((risk) => (
                        <tr key={risk.risk_rating_id}>
                          <td>{risk.customer_id}</td>

                          <td>
                            <span
                              className={`status-badge ${
                                risk.risk_level?.toLowerCase()
                              }`}
                            >
                              {risk.risk_level}
                            </span>
                          </td>

                          <td>{risk.reason || "—"}</td>

                          <td>{formatDate(risk.effective_from)}</td>

                          <td>{formatDate(risk.effective_to)}</td>
                        </tr>
                      ))}

                      {risks.length === 0 && (
                        <tr>
                          <td colSpan="5">
                            No current risk records found.
                          </td>
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

export default RiskManagement;
