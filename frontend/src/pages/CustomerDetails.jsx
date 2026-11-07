
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, User, FileText, ShieldCheck } from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function CustomerDetails() {
  const { customerId } = useParams();
  const navigate = useNavigate();

  const [customer, setCustomer] = useState(null);
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchDetails() {
      try {
        const customerResponse = await api.get(
          `/customers/${customerId}`
        );

        setCustomer(customerResponse.data);

        try {
          const complianceResponse = await api.get(
            `/compliance/${customerId}`
          );
          setCompliance(complianceResponse.data);
        } catch (err) {
          console.error("Compliance data unavailable:", err);
        }
      } catch (err) {
        console.error(err);
        setError("Unable to load customer details.");
      } finally {
        setLoading(false);
      }
    }

    fetchDetails();
  }, [customerId]);

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="customers-page">

          <button
            className="cancel-btn"
            onClick={() => navigate("/customers")}
          >
            <ArrowLeft size={18} /> Back to Customers
          </button>

          {loading && <p>Loading customer details...</p>}

          {error && <p className="error-message">{error}</p>}

          {customer && (
            <>
              <h1>Customer Details</h1>

              <div className="customer-table-card">
                <div className="customer-table-heading">
                  <User size={22} />
                  <h3>Personal Information</h3>
                </div>

                <div className="details-grid">
                  <div>
                    <label>Customer ID</label>
                    <p>{customer.customer_id}</p>
                  </div>

                  <div>
                    <label>Customer Name</label>
                    <p>{customer.customer_name}</p>
                  </div>

                  <div>
                    <label>Customer Type</label>
                    <p>{customer.customer_type_id}</p>
                  </div>

                  <div>
                    <label>Date of Birth</label>
                    <p>{customer.date_of_birth || "Not available"}</p>
                  </div>

                  <div>
                    <label>Onboarding Date</label>
                    <p>{customer.onboarding_date}</p>
                  </div>

                  <div>
                    <label>Customer Status</label>
                    <p>
                      <span className={`status-badge ${customer.status.toLowerCase()}`}>
                        {customer.status}
                      </span>
                    </p>
                  </div>
                </div>
              </div>

              <div className="customer-table-card">
                <div className="customer-table-heading">
                  <ShieldCheck size={22} />
                  <h3>KYC Compliance</h3>
                </div>

                {compliance ? (
                  <div className="details-grid">
                    <div>
                      <label>Compliance Status</label>
                      <p>{compliance.status}</p>
                    </div>

                    <div>
                      <label>Completion Percentage</label>
                      <p>{compliance.completion_percentage}%</p>
                    </div>

                    <div>
                      <label>Total Requirements</label>
                      <p>{compliance.total_requirements}</p>
                    </div>
                  </div>
                ) : (
                  <p>Compliance information is unavailable.</p>
                )}
              </div>

              <div className="customer-table-card">
                <div className="customer-table-heading">
                  <FileText size={22} />
                  <h3>Documents</h3>
                </div>

                <p>Document management will be connected in the next step.</p>
              </div>
            </>
          )}

        </section>
      </main>
    </div>
  );
}

export default CustomerDetails;
