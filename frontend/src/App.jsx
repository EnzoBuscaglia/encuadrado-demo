import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import ContentDetail from "./pages/ContentDetail";
import EventDetail from "./pages/EventDetail";
import Store from "./pages/Store";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/store" element={<Store />} />
        <Route path="/store/event/:id" element={<EventDetail />} />
        <Route path="/store/content/:id" element={<ContentDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
