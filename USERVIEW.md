# ProductScope — User Journey & System Workflows

This document provides a highly detailed, step-by-step breakdown of the ProductScope (Market Simulation Lab) workflow. It deeply documents both the frontend user experience and the backend architecture processes that power the application.

---

## 1. Full User Journey

The application follows a linear, 7-phase journey designed to build the competitive market landscape before ultimately simulating audience reception.

### Phase 1: Input Ingestion (Product Definition)
*   **User Action**: The user lands on the dashboard and fills out the "Define Your Product" form.
*   **Fields**:
    *   **Product Name**: Ensure recognizable branding.
    *   **Price ($)**: Baseline figure to compete against.
    *   **Description**: High-level value proposition.
    *   **Key Features**: Comma-separated or bulleted lists (e.g., "Waterproof, 24h battery, Eco-friendly").
*   **Expected Outcome**: The frontend standardizes this input into a structured internal state object to serve as the baseline for all competitive comparisons moving forward.

### Phase 2: Competitor Discovery
*   **User Action**: The user clicks to "Initialize Research". The user watches a progress overlay indicating search status.
*   **System Action**: The application builds a prompt with the Phase 1 input and queries an LLM to accurately deduce 5 real-world closest competitors, returning their Name, URL, and estimated pricing.
*   **Expected Outcome**: A visualization of the 5 discovered competitors smoothly renders on the dashboard, signaling the start of the heavy lifting.

### Phase 3: Web Crawling & Feature Extraction
*   **User Action**: Passive monitoring. The user sees a progress bar for each competitor being scraped.
*   **System Action**: The frontend initiates parallel fetch requests using a web-reading API (e.g., Jina AI reader) to obtain the raw text of the 5 competitor URLs. Following the scrape, multiple concurrent LLM calls extract features from this raw text into a strict JSON format.
*   **Expected Outcome**: All features globally available are saved to the internal state buffer.

### Phase 4: Feature Matrix & Metrics
*   **User Action**: The user reviews the generated comparative landscape.
*   **System Action**: The system compiles a master list of all features discovered globally across the competitors and the user's base product. It builds an unbiased true/false mapping of who has what. Chart.js is invoked to render three distinct visual tabs:
    *   **Pricing Landscape**: A horizontal bar chart comparing all products securely.
    *   **Feature Frequency**: A doughnut chart displaying market saturation of specific features.
    *   **Category Coverage**: Tracking domains like 'Hardware', 'Software', 'Support'.
*   **Expected Outcome**: Interactive charts are displayed. The button to proceed to the simulation is unlocked.

### Phase 5: Review & Confirm
*   **User Action**: The user reviews the data. If the LLM suffered hallucinations or fetched a poor competitor, they mentally note the landscape before initiating the final simulation.
*   **Expected Outcome**: User confirms readiness to spend heavier API tokens and wait for the market simulation.

### Phase 6: Simulated Persona Reactions
*   **User Action**: Clicks "Simulate Persona Reactions".
*   **System Action**: The UI transitions completely to the simulation stage. 20 distinct cards representing individuals (e.g., Budget Buyer, C-Suite Executive) appear empty. Over 10-30 seconds, these cards quickly populate with typing animations as Server-Sent Events (SSE) data streams in from the backend.
*   **Expected Outcome**: Real-time feedback! Each persona chooses to either purchase the user's product or defect to a competitor, supplying a unique quote, purchase probability, and reasoning uniquely matching their distinct income and traits.

### Phase 7: Market Outcome
*   **User Action**: Observes the final aggregated results and KPIs.
*   **System Action**: Once the SSE stream closes, the frontend calculates tallies for all 20 personas to deduce:
    *   **The Market Winner**: The product purchased most overall.
    *   **Market Share**: Rendered as a final summarizing pie chart.
    *   **Segment Preference**: Demographic breakdowns of purchasers.
*   **Expected Outcome**: The comprehensive validation cycle concludes natively, giving users a firm roadmap based on simulated facts.

---

## 2. Frontend Workflows

The frontend is a vanilla HTML/JS/CSS Single Page Application (SPA). State is maintained dynamically in JavaScript objects and directly injected into the DOM to keep a swift response time without overhead.

### DOM & Navigation Flow
*   The `index.html` file contains all sections mapped to `div` containers that rely on display toggling (e.g., `d-none` utility classes).
*   Transitions are handled by centralized JavaScript functions tracking the active step.
*   **Progress Indicators**: For tasks incurring network delay (Phases 2-4), spinners and real-time text updates are appended to the DOM to ensure the user perceives continuous action.

### LLM Orchestration Wrapper (Frontend)
The frontend implements an intelligent fallback mechanism for its own direct LLM calls (Competitor discovery, extraction, matrix generation) to prevent pipeline failures.
```javascript
// Pseudocode representing the intelligent fallback loop
async function callLLMWithFallback(prompt) {
    const providers = ['gemini', 'groq', 'openrouter'];
    for (let provider of providers) {
        try {
            return await callSpecificProvider(provider, prompt);
        } catch (error) {
            console.warn(`Provider ${provider} failed. Failing over to next...`); // Logic continues to next provider
        }
    }
    throw new Error("Pipeline Exhausted: All LLM providers failed.");
}
```

### Visualization (`Chart.js`)
*   To prevent "canvas ghosting" (where hovering over a redrawn chart flashes old, previously rendered data datasets), the frontend globally stores variables referencing the Chart objects. 
*   Before `renderPhase4()` dynamically repopulates, it explicitly scopes `.destroy()` onto the existing chart objects.

---

## 3. Backend Workflows

The backend is built in Python using **FastAPI** (`simulation_server.py`) and is rigidly dedicated to **Phase 6: Multi-LLM Persona Simulation**. 

### Key Capabilities & Data Handling
*   **Stateless Execution**: The backend maintains no persistent connection pool to a DB. The entire market state (product details + 5 competitors) is ingested on every POST request directly onto `/api/simulate`. 
*   **Orchestrator Design**: Implements an `LLMOrchestrator` class that dynamically checks connections and distributes 20 personas across multiple AI backends (Groq, Gemini, OpenRouter, and local Ollama) using async Python `asyncio.Semaphore` limiters to bypass rate-limiting.

### API Endpoints

#### 1. `GET /api/health`
*   **Role**: Pings the orchestrator to confirm functionality and node availability.
*   **Data Structure Returns**: Active backends, models loaded (e.g., `llama-3.3-70b-versatile`, `gemini-2.0-flash`), and the total count of valid personas.

#### 2. `GET /api/personas`
*   **Role**: Exposes the internal, hard-coded `PERSONAS` dictionary list to the frontend.
*   **Data Structure Returns**: A JSON array containing the age, segment, distinct traits, and absolute dealbreakers of each simulated participant.

#### 3. `POST /api/simulate`
*   **Role**: The heavy lifter handling parallel execution.
*   **Data Handling**: Accepts a JSON payload containing exactly the user's product and the 5 structured competitors created from Phase 4.
*   **Processing Journey**:
    1.  Receives the request and immediately returns a `StreamingResponse` (Server-Sent Event).
    2.  Spawns exactly 20 concurrent `asyncio` task futures (one for each persona).
    3.  A system Prompt is automatically generated forcing the LLM to adopt the persona's socio-economic worldview entirely ("You are a Senior Retiree with $28k income. Your dealbreaker is complex interfaces...").
    4.  The selected Node evaluates the product vs. competitors.
    5.  As each Node completes its generation, the backend parses out the Markdown and JSON structure, verifies it, and `yields` the formatted string chunk back down the active HTTP stream.
*   **Validation Fallback**: The backend expects valid JSON returns from the LLMs. If an LLM hallucinates conversational filler and breaks the JSON parse, an internal `except` block automatically supplies a statistically realistic "fallback" probabilistic vote rather than allowing the SSE stream to crash entirely.

---

## 4. Key Takeaways and Operations Guidelines

*   **For Developers**: The application is highly decoupled. Changes to the frontend user interface can be made with absolutely no concern for backend breakage, so long as the contract payload to `POST /api/simulate` (the structured product array) remains untouched. Make use of the `health` endpoint heavily during QA.
*   **For Testers**: Since outputs from LLMs are non-deterministic, testing should focus heavily on the edge cases: robust JSON parsing, ensuring fallback mechanisms trigger repeatedly when a provider is manually taken offline, and verifying that the `Chart.js` canvases are properly scoped to `destroy()`.
*   **For End-Users**: Treat the system as a structural validation of your copy and feature sets. If 15 out of 20 personas refuse to choose your product due to high price or poor features, do not ignore them. Take that simulation as actionable data to lower your baseline in Phase 1 and run the simulation again.
