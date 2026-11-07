
import { useEffect, useState } from "react";
import { Search, Plus, Users, X } from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState("");

  const [form, setForm] = useState({
    customer_name: "",
    customer_type_id: "CT-IND",
    date_of_birth: "",
    onboarding_date: new Date().toISOString().slice(0, 10),
    status: "ONBOARDING",
  });

  const fetchCustomers = () => {
    setLoading(true);

    api.get("/customers/", {
      params: { skip: 0, limit: 100 },
    })
      .then((response) => setCustomers(response.data))
      .catch((err) => {
        console.error(err);
        setError("Unable to load customers.");
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setFormError("");

    const payload = {
      ...form,
      date_of_birth: form.date_of_birth || null,
    };

    try {
      await api.post("/customers/", payload);

      setShowForm(false);

      setForm({
        customer_name: "",
        customer_type_id: "CT-IND",
        date_of_birth: "",
        onboarding_date: new Date().toISOString().slice(0, 10),
        status: "ONBOARDING",
      });

      fetchCustomers();
    } catch (err) {
      console.error(err);
      setFormError(
        err.response?.data?.detail || "Unable to create customer."
      );
    } finally {
      setSaving(false);
    }
  };

  const filteredCustomers = customers.filter((customer) => {
    const name = customer.customer_name?.toLowerCase() || "";
    const id = customer.customer_id?.toLowerCase() || "";

    const matchesSearch =
      name.includes(search.toLowerCase()) ||
      id.includes(search.toLowerCase());

    const matchesStatus =
      status === "ALL" || customer.status === status;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="customers-page">

          <div className="page-heading">
            <div>
              <h1>Customers</h1>
              <p>Manage your KYC customer records.</p>
            </div>

            <button
  type="button"
  className="add-customer-btn"
  onClick={() => setShowForm(true)}
>
  <Plus size={18} />
  Add Customer
</button>
          </div>

          <div className="customer-toolbar">
            <div className="customer-search">
              <Search size={18} />
              <input
                placeholder="Search by customer name or ID..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="ALL">All Statuses</option>
              <option value="ONBOARDING">Onboarding</option>
              <option value="PENDING">Pending</option>
              <option value="APPROVED">Approved</option>
              <option value="REJECTED">Rejected</option>
              <option value="SUSPENDED">Suspended</option>
            </select>
          </div>

          {loading && <p>Loading customers...</p>}
          {error && <p className="error-message">{error}</p>}

          {!loading && !error && (
            <div className="customer-table-card">
              <div className="customer-table-heading">
                <Users size={20} />
                <h3>Customer Records ({filteredCustomers.length})</h3>
              </div>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Customer ID</th>
                      <th>Name</th>
                      <th>Type</th>
                      <th>Status</th>
                      <th>Onboarding Date</th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredCustomers.map((customer) => (
                      <tr key={customer.customer_id}>
                        <td>{customer.customer_id}</td>
                        <td>{customer.customer_name}</td>
                        <td>{customer.customer_type_id}</td>
                        <td>
                          <span className={`status-badge ${customer.status.toLowerCase()}`}>
                            {customer.status}
                          </span>
                        </td>
                        <td>{customer.onboarding_date}</td>
                      </tr>
                    ))}

                    {filteredCustomers.length === 0 && (
                      <tr>
                        <td colSpan="5">No customers found.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Add Customer Modal */}
          {showForm && (
            <div className="modal-overlay">
              <div className="customer-modal">

                <div className="modal-heading">
                  <h2>Add New Customer</h2>

                  <button
                    type="button"
                    className="close-btn"
                    onClick={() => setShowForm(false)}
                  >
                    <X size={22} />
                  </button>
                </div>

                <form onSubmit={handleSubmit}>

                  <label>Customer Name</label>
                  <input
                    name="customer_name"
                    value={form.customer_name}
                    onChange={handleChange}
                    placeholder="Enter customer name"
                    maxLength={150}
                    required
                  />

                  <label>Customer Type</label>
                  <select
                    name="customer_type_id"
                    value={form.customer_type_id}
                    onChange={handleChange}
                    required
                  >
                    <option value="CT-IND">Individual</option>
                    <option value="CT-BUS">Business</option>
                  </select>

                  <label>Date of Birth (optional)</label>
                  <input
                    type="date"
                    name="date_of_birth"
                    value={form.date_of_birth}
                    onChange={handleChange}
                  />

                  <label>Onboarding Date</label>
                  <input
                    type="date"
                    name="onboarding_date"
                    value={form.onboarding_date}
                    onChange={handleChange}
                    required
                  />

                  <label>Customer Status</label>
                  <select
                    name="status"
                    value={form.status}
                    onChange={handleChange}
                  >
                    <option value="ONBOARDING">Onboarding</option>
                    <option value="PENDING">Pending</option>
                  </select>

                  {formError && (
                    <p className="error-message">{formError}</p>
                  )}

                  <div className="modal-actions">
                    <button
                      type="button"
                      className="cancel-btn"
                      onClick={() => setShowForm(false)}
                    >
                      Cancel
                    </button>

                    <button
                      type="submit"
                      className="add-customer-btn"
                      disabled={saving}
                    >
                      {saving ? "Saving..." : "Create Customer"}
                    </button>
                  </div>

                </form>
              </div>
            </div>
          )}

        </section>
      </main>
    </div>
  );
}

export default Customers;
