
import { useEffect, useState } from "react";

import {
  Users,
  FileText,
  ShieldAlert,
  Bell,
} from "lucide-react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

import api from "../services/api";
import Sidebar from "../components/sidebar";
import Header from "../components/Header";
import StatCard from "../components/StatCard";
import RecentActivity from "../components/RecentActivity";

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch dashboard data from FastAPI
  useEffect(() => {
    api
      .get("/dashboard/summary")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Dashboard API Error:", error);
        setError("Unable to load dashboard data.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // Customer chart data
  const customerChartData = data
    ? [
        {
          name: "Approved",
          value: data.approved_customers,
        },
        {
          name: "Pending",
          value: data.pending_customers,
        },
      ]
    : [];

  // Document chart data
  const documentChartData = data
    ? [
        {
          name: "Verified",
          value: data.verified_documents,
        },
        {
          name: "Pending",
          value: data.pending_documents,
        },
        {
          name: "Rejected",
          value: data.rejected_documents,
        },
      ]
    : [];

  const chartColors = [
    "#16a34a",
    "#f59e0b",
    "#ef4444",
  ];

  return (
    <div className="app-layout">

      {/* Sidebar */}
      <Sidebar />

      <main className="main-content">

        {/* Header */}
        <Header />

        <section className="dashboard-content">

          <h1>KYC Dashboard</h1>

          <p className="subtitle">
            Monitor customer onboarding and compliance activities.
          </p>

          {/* Loading state */}
          {loading && <p>Loading dashboard data...</p>}

          {/* Error state */}
          {error && <p className="error-message">{error}</p>}

          {/* Dashboard content */}
          {data && (
            <>

              {/* STATISTIC CARDS */}
              <div className="stats-grid">

                <StatCard
                  title="Total Customers"
                  value={data.total_customers}
                  icon={<Users />}
                  color="#e8efff"
                />

                <StatCard
                  title="Total Documents"
                  value={data.total_documents}
                  icon={<FileText />}
                  color="#e7f8ef"
                />

                <StatCard
                  title="High Risk Customers"
                  value={data.high_risk_customers}
                  icon={<ShieldAlert />}
                  color="#fff0e5"
                />

                <StatCard
                  title="Open Alerts"
                  value={data.open_alerts}
                  icon={<Bell />}
                  color="#fce8ed"
                />

                <StatCard
                  title="Approved Customers"
                  value={data.approved_customers}
                  icon={<Users />}
                  color="#e7f8ef"
                />

                <StatCard
                  title="Pending Documents"
                  value={data.pending_documents}
                  icon={<FileText />}
                  color="#fff6df"
                />

                <StatCard
                  title="Rejected Documents"
                  value={data.rejected_documents}
                  icon={<FileText />}
                  color="#fce8ed"
                />

                <StatCard
                  title="Overdue Reviews"
                  value={data.overdue_reviews}
                  icon={<ShieldAlert />}
                  color="#fff0e5"
                />

              </div>

              {/* ANALYTICS CHARTS */}
              <div className="charts-grid">

                {/* Customer Status Bar Chart */}
                <div className="chart-card">

                  <h3>Customer Status Overview</h3>

                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={customerChartData}>

                      <CartesianGrid strokeDasharray="3 3" />

                      <XAxis dataKey="name" />

                      <YAxis />

                      <Tooltip />

                      <Bar
                        dataKey="value"
                        fill="#3b82f6"
                        radius={[6, 6, 0, 0]}
                      />

                    </BarChart>
                  </ResponsiveContainer>

                </div>

                {/* Document Status Pie Chart */}
                <div className="chart-card">

                  <h3>Document Verification Status</h3>

                  <ResponsiveContainer width="100%" height={300}>

                    <PieChart>

                      <Pie
                        data={documentChartData}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        label
                      >

                        {documentChartData.map((entry, index) => (
                          <Cell
                            key={entry.name}
                            fill={chartColors[index]}
                          />
                        ))}

                      </Pie>

                      <Tooltip />

                      <Legend />

                    </PieChart>

                  </ResponsiveContainer>

                </div>

              </div>

            </>
          )}

        </section>

      </main>

    </div>
  );
}

export default Dashboard;
