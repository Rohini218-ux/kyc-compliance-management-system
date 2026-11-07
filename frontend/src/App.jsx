
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Customers from "./pages/Customers";
import CustomerDetails from "./pages/CustomerDetails";
import Documents from "./pages/Documents";
import RiskManagement from "./pages/RiskManagement";
import Reviews from "./pages/Reviews";
import Alerts from "./pages/Alerts";
import AuditLogs from "./pages/AuditLogs";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />

        <Route path="/customers" element={<Customers />} />

        <Route
          path="/customers/:customerId"
          element={<CustomerDetails />}
        />

        <Route path="/documents" element={<Documents />} />

        <Route
          path="/risk-management"
          element={<RiskManagement />}
        />

        <Route path="/reviews" element={<Reviews />} />

        <Route path="/alerts" element={<Alerts />} />

        <Route path="/audit-logs" element={<AuditLogs />} />

        {/* Keep wildcard route LAST */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
