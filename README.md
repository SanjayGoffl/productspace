# ProductScope — Market Simulation Lab

## Overview
**ProductScope (Market Simulation Lab)** is an end-to-end, 7-phase analytical pipeline that allows users to test a product idea in a simulated market of AI personas. By leveraging multi-LLM orchestration (Gemini, Groq, OpenRouter, and Ollama) and real-time competitor analysis, this dashboard provides deep, data-driven insights into how a product might perform in the real world against actual competitors.

## Purpose and Scope
The purpose of this project is to eliminate guesswork in product development, marketing, and market research. Rather than manually researching competitors and guessing how target audiences will react, ProductScope automates continuous discovery, structural comparisons, and audience simulated decision-making. 

The scope of the project covers end-to-end simulation: taking an initial user-defined product, actively scraping the web for its top competitors, creating unbiased feature/pricing matrices, and simulating 20 distinct AI buyer personas (across Economy, Mid-Range, Premium, and Specialty segments) to determine market viability and capture actionable feedback.

## Key Features
- **Real-Time Competitor Discovery**: Identifies the top 5 closest competitors on the web utilizing generative LLMs.
- **Parallel Web Crawling & Feature Extraction**: Scrapes competitor domains to extract structured lists of product features using reading APIs and LLM parsers.
- **Unbiased Feature Matrix**: Cross-references competitor features against the user's product to highlight strengths and missing gaps.
- **Visual Analytics Dashboard**: Interactive phase-based visualizations (Pricing Landscape, Feature Frequency, Category Coverage) powered by Chart.js.
- **Multi-Backend Persona Simulation**: Evaluates the product with 20 distinct AI personas (Budget Buyer, Tech Enthusiast, C-Suite Executive, etc.) via a FastAPI backend, streaming reactions and purchase probabilities in real-time.
- **Comprehensive Final KPI Report**: Analyzes persona decisions to calculate overall market share, identify the market winner, and summarize segment preferences.

## Installation and Setup Instructions

### Prerequisites
- **Python 3.10+** (for the backend FastAPI server)
- **Node.js or Python** (for a simple HTTP server to serve the vanilla frontend)
- At least one valid API Key from supported LLM providers (Google Gemini, Groq, OpenRouter), or a locally running Ollama instance.

### Step-by-Step Setup
1. **Clone the repository** and navigate to the project folder.
   ```bash
   git clone <repository_url>
   cd "The Market Simulation Lab/103"
   ```

2. **Set up a Python Virtual Environment** and install dependencies:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install fastapi uvicorn httpx python-dotenv openai google-generativeai
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory (alongside `simulation_server.py`) and add your LLM API keys:
   ```env
   GOOGLE_GEMINI_API_KEY=your_gemini_key
   OPEN_ROUTER_API_KEY=your_openrouter_key
   GROQ_API_KEY=your_groq_key
   ```
   *(Note: You only need one active provider for the multi-orchestrator to function, but providing multiple ensures fallback capabilities in case of API limits or outages).*

4. **Start the Backend Server**:
   ```bash
   python simulation_server.py
   ```
   *The FastAPI simulation server will start on `http://localhost:5501`.*

5. **Start the Frontend Server**:
   In a new terminal, serve the directory containing `index.html`:
   ```bash
   python -m http.server 8080
   ```

6. **Open the Application**:
   Navigate your browser to `http://localhost:8080/index.html`.

## Usage Guidelines
1. **Input Your Product**: Begin by entering your product's name, price, description, and 4-6 key features in the provided form.
2. **Review the Data**: Let the system complete competitive discovery (Phases 1-4). Review the generated pricing landscape and feature mapping to ensure accuracy.
3. **Run the Market Simulation**: Click to instantiate the TinyTroupe AI personas. Watch as they evaluate your product against competitors in real-time.
4. **Analyze the Final Report**: Use the Phase 7 results to find out your potential market share, who your strongest purchaser segment is, and what dealbreakers your product might have.

## High-Level Workflow Summary
1. **Input Ingestion (Frontend)**: User provides baseline product definitions.
2. **Competitor Discovery (Frontend/LLM)**: LLM derives top 5 competitor URLs.
3. **Web Crawling (Frontend/Reading APIs/LLM)**: Content extracted and structured into feature lists.
4. **Feature Matrix Generation & Charting (Frontend)**: Data aggregated and rendered via Chart.js.
5. **Review Phase (Frontend)**: User confirms matrix accuracy.
6. **Persona Simulation (Backend)**: FastAPI Server-Sent Events stream choices of 20 distinct LLM-powered personas evaluating the market pool.
7. **Market Outcome (Frontend)**: System calculates winner, market share, and key takeaways.

## Contribution Notes
- **Bug Reports & Feature Requests**: Please use the project's issue tracker. Ensure you include browser console logs and backend traceback output when reporting bugs.
- **Adding Personas**: You can easily expand the market simulation by adding new dictionary entries to the `PERSONAS` list within `simulation_server.py`.
- **Pull Requests**: Ensure all backend changes are strictly type-hinted and maintain async compatibility. For frontend contributions, keep the architecture framework-free (vanilla JS/HTML/CSS) for the core orchestrator to prevent heavy overhead.
