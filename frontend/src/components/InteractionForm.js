import React, { useState } from "react";
import API from "../api";
import "../App.css";

function InteractionForm({ fetchData }) {

  const [aiInput, setAiInput] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    hcp_name: "",
    interaction_type: "",
    topics: "",
    sentiment: "",
    outcomes: "",
    follow_up: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // =========================
  // SAVE FORM
  // =========================
  const submit = async (e) => {
    e.preventDefault();
    await API.post("/interactions", form);
    fetchData();

    setForm({
      hcp_name: "",
      interaction_type: "",
      topics: "",
      sentiment: "",
      outcomes: "",
      follow_up: ""
    });
  };

  // =========================
  // AI AUTOFILL
  // =========================
  const handleAI = async () => {
    if (!aiInput) {
      alert("Please enter interaction text");
      return;
    }

    try {
      setLoading(true);

      const res = await API.post("/ai/chat", {
        message: aiInput
      });

      const aiText = res.data.structured?.ai_output || "";

      const getValue = (label) => {
        const regex = new RegExp(label + ": (.*)");
        const match = aiText.match(regex);
        return match ? match[1].trim() : "";
      };

      setForm({
        hcp_name: getValue("HCP Name"),
        interaction_type: getValue("Interaction Type"),
        topics: getValue("Topics discussed"),
        sentiment: getValue("Sentiment"),
        outcomes: getValue("Outcomes"),
        follow_up: getValue("Follow up action")
      });

      setChatResponse("✅ Form autofilled using AI");
      setAiInput("");

    } catch (err) {
      console.error(err);
      alert("AI Autofill failed");
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // AI CHAT
  // =========================
  const handleChat = async () => {
    if (!aiInput) {
      alert("Please enter a message");
      return;
    }

    try {
      setLoading(true);

      const res = await API.post("/ai/chat", {
        message: aiInput
      });

      setChatResponse(`
Summary: ${res.data.summary?.summary || ""}
Insight: ${res.data.insight?.insight || ""}
Next Action: ${res.data.action?.next_best_action || ""}
      `);

    } catch (err) {
      console.error(err);
      alert("Chat failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">

      {/* ================= LEFT SIDE ================= */}
      <div className="form-section">
        <h2>Log Interaction</h2>

        <form onSubmit={submit}>
          <input name="hcp_name" placeholder="HCP Name" value={form.hcp_name} onChange={handleChange} />
          <input name="interaction_type" placeholder="Interaction Type" value={form.interaction_type} onChange={handleChange} />
          <input name="topics" placeholder="Topics" value={form.topics} onChange={handleChange} />
          <input name="sentiment" placeholder="Sentiment" value={form.sentiment} onChange={handleChange} />
          <input name="outcomes" placeholder="Outcomes" value={form.outcomes} onChange={handleChange} />
          <input name="follow_up" placeholder="Follow Up" value={form.follow_up} onChange={handleChange} />

          <button type="submit">Save</button>
        </form>
      </div>

      {/* ================= RIGHT SIDE AI PANEL ================= */}
      <div className="ai-panel">
        <h3>AI Assistant</h3>

        <textarea
          placeholder="Describe interaction or ask AI..."
          value={aiInput}
          onChange={(e) => setAiInput(e.target.value)}
        />

        <div className="btn-group">
          <button onClick={handleAI} disabled={loading}>
            ✨ Autofill
          </button>

          <button onClick={handleChat} disabled={loading}>
            💬 Chat
          </button>
        </div>

        {loading && <p>⏳ AI is thinking...</p>}

        <div className="ai-response">
          {chatResponse}
        </div>
      </div>

    </div>
  );
}

export default InteractionForm;