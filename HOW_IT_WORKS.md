-------------# The Market Simulation Lab: How It Works

This document explains the end-to-end process, architecture, and core functions behind the Market Simulation Lab.

## 🚀 The End-to-End Process

The application is divided into a 7-phase pipeline that takes a simple product idea and runs it through a simulated market of AI personas.

### Phase 1: Input Ingestion
The user provides the core details of their product (Name, Price, Description, and Key Features). This defines the baseline for all subsequent comparisons.

### Phase 2: Competitor Discovery
The system uses an LLM (typically via OpenRouter or Gemini) to identify the closest 5 competitors in the market based on the product description. It returns their names, URLs, and pricing.

### Phase 3: Web Crawling & Feature Extraction
The frontend orchestrates parallel web crawling (using a Jina AI reader or similar scraping API) to fetch the content of the competitor URLs. It then uses LLMs to extract a structured list of features for each competitor.

### Phase 4: Feature Matrix & Metrics
To avoid bias, the system asks the LLM to first pool all features from all competitors. It then objectively cross-references these features against the user's product to generate a **Feature Comparison Matrix**. This phase also renders visualizations:
- **Pricing Landscape:** A bar chart comparing prices.
- **Feature Frequency:** A doughnut chart showing how common certain features are.
- **Category Coverage:** A horizontal bar chart showing how many features each product has per category.

### Phase 5: Review & Confirm
The user reviews the generated data before initiating the expensive simulation phase.

### Phase 6: Simulated Persona Reactions
The UI transitions into a real-time simulation. The frontend opens a Server-Sent Events (SSE) connection to the Python FastAPI backend (`simulation_server.py`). The backend instantiates 9 distinct AI personas (e.g., Budget Buyer, Tech Enthusiast) and asks them to evaluate the user's product vs. the competitors. Their reactions, chosen products, and purchase probabilities are streamed live to the UI.

### Phase 7: Market Outcome
Once all personas have made their decisions, the UI aggregates the data into final KPIs:
- **Market Winner**
- **Market Share (Pie Chart)**
- **Downloads / Report Generation**

---

## 🧠 Behind the Screen: Core Functions

The system is a hybrid application involving a heavy-lifting JavaScript frontend (for data aggregation and UI) and a Python backend (for the AI agent simulation).

### 1. Multi-LLM Orchestration (Frontend)
Located in `index.html`, the system uses an intelligent fallback mechanism.
*   **`callLLM(providerKey, prompt)`**: The primary wrapper for making LLM calls.
*   **`callLLMWithFallback(prompt, primary, fallbacks)`**: If one LLM fails (e.g., rate limits, decommissioned models), it automatically retries with the next one in the chain (e.g., Gemini → Groq → OpenRouter).

### 2. Competitor & Feature Discovery
*   **`discoverCompetitors(productData)`**: Constructs a prompt to find 5 competitors with valid URLs.
*   **`crawlAndExtract(competitors)`**: Uses parallel fetching to read competitor websites and extract JSON-formatted feature lists.
*   **`generateAnalysisData()`**: The core logic for Phase 4. It uses strict prompt engineering to force the LLM to create an unbiased matrix by mapping all competitor features *before* evaluating the user's product.

### 3. Visualizations (Chart.js)
*   **`renderPhase4(...)`**: Dynamically creates `Chart.js` instances. It includes logic to destroy old chart instances before rendering new ones to prevent canvas ghosting.

### 4. Real-Time Simulation (Backend & Frontend via SSE)
*   **`simulation_server.py`**: A FastAPI application running on port 5501.
    *   **`/api/simulate`**: Uses `StreamingResponse` to push JSON events to the browser as soon as a persona completes its evaluation. It uses `asyncio.gather()` to evaluate personas concurrently.
*   **`runSimulation()` (JavaScript)**: Connects to `/api/simulate` using the browser's `EventSource` API. As `persona_result` events stream in, it triggers CSS animations to reveal the persona cards one by one.

---

## 🛠️ The Development Journey

1. **Initial Concept**: The original idea was built in Streamlit, but it was too rigid for the dynamic, highly visual, dashboard-like experience required.
2. **Migration to Vanilla Web**: We moved to a single-page HTML/JS/CSS architecture to gain absolute control over the UI, animations, and API flows without framework overhead.
3. **Fighting Hallucinations**: We implemented strict JSON formatting rules in the prompts to ensure the LLMs returned parsable data instead of conversational text.
4. **Removing Bias**: Initially, the LLM heavily favored the user's product. We re-engineered the prompt in `generateAnalysisData()` to enforce a "competitors-first" extraction approach, ensuring a highly objective feature matrix.
5. **Real-time Engine**: To make the persona simulation feel alive, we implemented Server-Sent Events (SSE). Instead of waiting 15 seconds for a loading spinner, the user watches the personas type out their decisions in real-time.
