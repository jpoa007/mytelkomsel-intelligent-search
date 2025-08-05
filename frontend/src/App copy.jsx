import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [sortBy, setSortBy] = useState("similarity");
  const [order, setOrder] = useState("desc");

  const handleSearch = async () => {
    if (!query) return;

    try {
      const params = new URLSearchParams({
        query,
        top_n: "10",
        threshold: "0.0",
        sort_by: sortBy,
        order,
      });

      const response = await fetch(`http://127.0.0.1:8000/api/llm-search?${params}`);
      const data = await response.json();

      if (data.results) {
        setResults(data.results);
      } else {
        setResults([]);
      }
    } catch (error) {
      console.error("Search error:", error);
      setResults([]);
    }
  };

  return (
    <div className="container">
      <h1>Telkomsel Intelligent Search</h1>

      <div className="search-bar">
        <input
          type="text"
          value={query}
          placeholder="Search for products"
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
        />

        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="similarity">Sort by Relevance</option>
          <option value="price">Sort by Price</option>
        </select>

        <select value={order} onChange={(e) => setOrder(e.target.value)}>
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>

        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="results">
        {results.map((item, index) => (
          <div key={index} className="card">
            <img
              src="http://127.0.0.1:8000/images/telkomsel.png"
              alt="Telkomsel"
              className="logo"
            />
            <h3>{item.title}</h3>
            <p>{item.description}</p>
            <p><strong>Category:</strong> {item.category}</p>
            <p><strong>Price:</strong> Rp {Number(item.price).toLocaleString("id-ID")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
