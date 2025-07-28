import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Store from "./pages/Store";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/store" element={<Store />} />
        {/* More routes will go here */}
      </Routes>
    </Router>
  );
}

export default App;
