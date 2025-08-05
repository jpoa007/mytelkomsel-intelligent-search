
---

## 🧪 Modules

Each search feature is developed independently as a module:

| Module                     | Status   | Description                          |
|----------------------------|----------|--------------------------------------|
| `fuzzy-search`             | ✅ WIP    | Typo-tolerant keyword search         |
| `semantic-search`          | ⏳        | Vector-based intent matching         |
| `auto-suggestion`          | ⏳        | Smart real-time suggestions          |
| `real-time-recommendations`| ⏳        | Contextual suggestions (soon)        |
| `personalized-search`      | ⏳        | Reranking based on user behavior     |

---

## 🚀 Deployment Plan

| Part      | Platform    | URL (sample)                                  |
|-----------|-------------|-----------------------------------------------|
| Frontend  | [Vercel](https://vercel.com)       | `https://search-demo.vercel.app`      |
| Backend   | [Railway](https://railway.app)     | `https://search-api.up.railway.app`   |
| GitHub    | Private Repo | [GitHub](https://github.com/jpoa007/mytelkomsel-intelligent-search) |

---

## 🧪 Testing Strategy

| Layer     | Tool        | Location                     |
|-----------|-------------|------------------------------|
| Backend   | `pytest`    | `backend/tests/test_*.py`    |
| Frontend  | `Playwright`| `frontend/tests/`            |
| API       | `Postman` / `pytest` | Endpoint coverage     |

---

## 🔐 Privacy

This is a **private, internal PoC** for Telkomsel. No sensitive production data is stored or exposed.

---

## 📎 License

© Telkomsel, 2024. All rights reserved.
