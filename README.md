# MyTelkomsel Intelligent Search

This project is a semantic product search engine built for the MyTelkomsel ecosystem. It combines traditional fuzzy search with modern LLM-powered semantic search using OpenAI embeddings and ChromaDB, allowing users to query products in natural language and receive relevant product matches ranked by meaning and relevance.

![Telkomsel Logo](http://127.0.0.1:8000/images/telkomsel.png)

## 🔍 Features

- **Fuzzy Search**: Matches product names with user queries using approximate string matching.
- **LLM-Based Semantic Search**: Leverages OpenAI embeddings to find semantically relevant products.
- **ChromaDB Vector Store**: Stores and queries embeddings efficiently.
- **FastAPI Backend**: Provides API endpoints for fuzzy, vector, and LLM-based search.
- **React Frontend**: Clean UI for search input and result display.
- **Filtering**: Users can filter results by semantic relevance score and price (asc/desc).

## 🧠 Tech Stack

| Layer     | Technology               |
|----------|--------------------------|
| Frontend | React.js + Vite          |
| Backend  | FastAPI                  |
| ML       | OpenAI Embeddings        |
| VectorDB | ChromaDB                 |
| Language | Python, JavaScript       |

## 📂 Project Structure

