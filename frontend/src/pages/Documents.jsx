
import { useEffect, useState } from "react";
import { Search, Upload, Download, FileText } from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("ALL");

  const [file, setFile] = useState(null);
  const [customerId, setCustomerId] = useState("");
  const [requirementId, setRequirementId] = useState("");
  const [documentType, setDocumentType] = useState("");

  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  // Fetch documents
  const fetchDocuments = async () => {
    setLoading(true);

    try {
      const response = await api.get("/documents/", {
        params: { skip: 0, limit: 100 },
      });

      setDocuments(response.data);
      setError("");
    } catch (err) {
      console.error("Fetch documents error:", err.response?.data || err);
      setError("Unable to load documents.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Upload document
  const handleUpload = async (e) => {
    e.preventDefault();

    setError("");
    setMessage("");

    if (
      !file ||
      !customerId.trim() ||
      !requirementId.trim() ||
      !documentType.trim()
    ) {
      setError("Please complete all fields and select a PDF.");
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Please select a valid PDF file.");
      return;
    }

    const formData = new FormData();

    formData.append("customer_id", customerId.trim());
    formData.append(
      "customer_requirement_id",
      requirementId.trim()
    );
    formData.append("document_type", documentType.trim());
    formData.append("file", file);

    setUploading(true);

    try {
      await api.post("/documents/upload", formData);

      setMessage("Document uploaded successfully!");

      setCustomerId("");
      setRequirementId("");
      setDocumentType("");
      setFile(null);

      e.target.reset();

      await fetchDocuments();
    } catch (err) {
      console.error(
        "Upload error:",
        err.response?.data || err.message
      );

      const detail = err.response?.data?.detail;

      setError(
        Array.isArray(detail)
          ? detail
              .map((item) => `${item.loc.join(".")}: ${item.msg}`)
              .join(" | ")
          : typeof detail === "string"
            ? detail
            : "Document upload failed."
      );
    } finally {
      setUploading(false);
    }
  };

  // Download document
  const handleDownload = async (documentId) => {
    setError("");
    setMessage("");

    try {
      const response = await api.get(
        `/documents/${documentId}/download`,
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(response.data);

      const link = document.createElement("a");
      link.href = url;
      link.download = `${documentId}.pdf`;

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(
        "Download error:",
        err.response?.data || err.message
      );

      setError(
        `Unable to download ${documentId}. The PDF may not exist in storage.`
      );
    }
  };

  // Search and filter
  const filteredDocuments = documents.filter((doc) => {
    const searchText = search.toLowerCase();

    const matchesSearch =
      doc.customer_id?.toLowerCase().includes(searchText) ||
      doc.document_id?.toLowerCase().includes(searchText) ||
      doc.document_type?.toLowerCase().includes(searchText);

    const matchesStatus =
      status === "ALL" || doc.status === status;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header />

        <section className="customers-page">

          {/* Page heading */}
          <div className="page-heading">
            <div>
              <h1>Document Management</h1>
              <p>Upload and manage customer KYC documents.</p>
            </div>
          </div>

          {/* Upload form */}
          <div className="customer-table-card">
            <h3>Upload a Document</h3>

            <form
              className="document-upload-form"
              onSubmit={handleUpload}
            >
              <label>Customer ID</label>

              <input
                type="text"
                value={customerId}
                onChange={(e) => setCustomerId(e.target.value)}
                placeholder="Example: CUS-000001"
                required
              />

              <label>Customer Requirement ID</label>

              <input
                type="text"
                value={requirementId}
                onChange={(e) => setRequirementId(e.target.value)}
                placeholder="Enter customer requirement ID"
                required
              />

              <label>Document Type</label>

              <select
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                required
              >
                <option value="">Select document type</option>
                <option value="IDENTITY">Identity</option>
                <option value="ADDRESS">Address</option>
                <option value="TAX">Tax</option>
                <option value="OWNERSHIP">Ownership</option>
                <option value="BUSINESS_REGISTRATION">
                  Business Registration
                </option>
                <option value="OTHER">Other</option>
              </select>

              <label>Select PDF</label>

              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={(e) =>
                  setFile(e.target.files?.[0] || null)
                }
                required
              />

              <button
                type="submit"
                className="add-customer-btn"
                disabled={uploading}
              >
                <Upload size={18} />
                {uploading ? "Uploading..." : "Upload PDF"}
              </button>
            </form>
          </div>

          {/* Messages */}
          {message && (
            <p className="success-message">{message}</p>
          )}

          {error && (
            <p className="error-message">{error}</p>
          )}

          {/* Search and filter */}
          <div className="customer-toolbar">
            <div className="customer-search">
              <Search size={18} />

              <input
                type="text"
                placeholder="Search by customer, document ID or type..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="ALL">All Statuses</option>
              <option value="PENDING">Pending</option>
              <option value="VERIFIED">Verified</option>
              <option value="REJECTED">Rejected</option>
              <option value="EXPIRED">Expired</option>
            </select>
          </div>

          {/* Documents table */}
          {loading ? (
            <p>Loading documents...</p>
          ) : (
            <div className="customer-table-card">

              <div className="customer-table-heading">
                <FileText size={20} />
                <h3>
                  Documents ({filteredDocuments.length})
                </h3>
              </div>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Document ID</th>
                      <th>Customer ID</th>
                      <th>Requirement ID</th>
                      <th>Document Type</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredDocuments.map((doc) => (
                      <tr key={doc.document_id}>
                        <td>{doc.document_id}</td>
                        <td>{doc.customer_id}</td>
                        <td>{doc.customer_requirement_id}</td>
                        <td>{doc.document_type}</td>

                        <td>
                          <span
                            className={`status-badge ${doc.status.toLowerCase()}`}
                          >
                            {doc.status}
                          </span>
                        </td>

                        <td>
                          <button
                            type="button"
                            className="download-btn"
                            onClick={() =>
                              handleDownload(doc.document_id)
                            }
                          >
                            <Download size={16} />
                            Download
                          </button>
                        </td>
                      </tr>
                    ))}

                    {filteredDocuments.length === 0 && (
                      <tr>
                        <td colSpan="6">
                          No documents found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Documents;
