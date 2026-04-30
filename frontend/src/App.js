import React, { useEffect, useState } from "react";
import API from "./api";
import InteractionForm from "./components/InteractionForm";
import InteractionList from "./components/InteractionList";
import Dashboard from "./components/Dashboard";
import { useDispatch, useSelector } from "react-redux";
import { setData } from "./redux/interactionSlice";

function App() {
  const dispatch = useDispatch();

  const [search, setSearch] = useState("");
  const [sentimentFilter, setSentimentFilter] = useState("all");

  // Fetch data from backend → store in Redux
  const fetchData = async () => {
    try {
      const res = await API.get("/interactions");
      dispatch(setData(res.data));
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Get data from Redux store
  const data = useSelector((state) => state.interactions.data) || [];

  // Filter logic
  const filteredData = data.filter((item) => {
    const matchesSearch =
      item.hcp_name?.toLowerCase().includes(search.toLowerCase()) ||
      item.topics?.toLowerCase().includes(search.toLowerCase());

    const matchesSentiment =
      sentimentFilter === "all"
        ? true
        : item.sentiment?.toLowerCase() === sentimentFilter;

    return matchesSearch && matchesSentiment;
  });

  return (
    <div style={{ padding: "20px", fontFamily: "Inter" }}>
      <h1>AI CRM - HCP Interaction</h1>

      {/* FORM */}
      <InteractionForm fetchData={fetchData} />

      <hr />

      {/* DASHBOARD */}
      <Dashboard />

      <hr />

      {/* SEARCH + FILTER */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
        <input
          type="text"
          placeholder="Search by doctor or topic..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: "8px",
            width: "250px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
        />

        <select
          value={sentimentFilter}
          onChange={(e) => setSentimentFilter(e.target.value)}
          style={{
            padding: "8px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
        >
          <option value="all">All Sentiments</option>
          <option value="positive">Positive</option>
          <option value="neutral">Neutral</option>
          <option value="negative">Negative</option>
        </select>
      </div>

      {/* LIST */}
      <InteractionList data={filteredData} fetchData={fetchData} />
    </div>
  );
}

export default App;