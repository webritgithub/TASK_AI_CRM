import React from "react";
import API from "../api";

function InteractionList({ data, fetchData }) {

  const deleteItem = async (id) => {
    await API.delete(`/interactions/${id}`);
    fetchData();
  };

  // UPDATED AI EDIT (dynamic)
  const handleAIEdit = async (id) => {
    try {
      const instruction = prompt("Enter AI instruction (e.g., make it positive, suggest follow-up)");

      if (!instruction) return;

      await API.put(`/ai/edit/${id}`, {
        instruction: instruction
      });

      fetchData();
    } catch (err) {
      console.error("AI Edit Error:", err);
      alert("AI Edit failed");
    }
  };

  return (
    <div className="list-container">
      <h2>Interactions</h2>

      {data.map((item) => (
        <div key={item.id} className="card">
          <p><b>{item.hcp_name}</b></p>
          <p>{item.interaction_type}</p>
          <p>{item.topics}</p>
          <p className={`tag ${item.sentiment}`}>{item.sentiment}</p>
          <p>{item.outcomes}</p>
          <p>{item.follow_up}</p>

          <button onClick={() => deleteItem(item.id)}>Delete</button>

          {/* AI EDIT BUTTON */}
          <button onClick={() => handleAIEdit(item.id)}>
            AI Edit
          </button>
        </div>
      ))}
    </div>
  );
}

export default InteractionList;