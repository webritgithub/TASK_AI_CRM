import React from "react";
import { useSelector } from "react-redux";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

function Dashboard() {
  const data = useSelector((state) => state.interactions.data) || [];

  const sentimentCount = [
    {
      name: "Positive",
      value: data.filter((i) => i.sentiment === "positive").length,
    },
    {
      name: "Neutral",
      value: data.filter((i) => i.sentiment === "neutral").length,
    },
    {
      name: "Negative",
      value: data.filter((i) => i.sentiment === "negative").length,
    },
  ];

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Sentiment Analytics</h2>

      <BarChart width={450} height={300} data={sentimentCount}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="#4F46E5" />
      </BarChart>
    </div>
  );
}

export default Dashboard;