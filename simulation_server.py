"""
Market Simulation Lab — TinyTroupe Multi-LLM Orchestration Engine
Distributes 20 AI personas across: Gemini + Groq + OpenRouter + Ollama (qwen3:8b)
Each backend evaluates personas in parallel using TinyTroupe-style agent prompts.
"""
import asyncio
import json
import os
import random
import sys
from pathlib import Path
from typing import AsyncGenerator

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

load_dotenv()

# ─── TinyTroupe Path ──────────────────────────────────────────────────────────
TINYTROUPE_PATH = Path(__file__).parent / "market" / "TinyTroupe"
if str(TINYTROUPE_PATH) not in sys.path:
    sys.path.insert(0, str(TINYTROUPE_PATH))

# ─── 20 Expanded TinyTroupe Persona Archetypes ───────────────────────────────
PERSONAS = [
    # ── Economy Segment ──
    {"id": "budget_buyer",     "name": "Budget Buyer",        "emoji": "💰", "age": 32, "occupation": "School Teacher",        "income": "$35k",  "segment": "Economy",   "traits": ["price-sensitive","practical","frugal"], "priorities": "lowest price that meets basics", "dealbreakers": "price above budget or hidden fees"},
    {"id": "student",          "name": "College Student",      "emoji": "🎓", "age": 21, "occupation": "University Student",     "income": "$12k",  "segment": "Economy",   "traits": ["budget-conscious","social","trendy"],    "priorities": "affordability and coolness factor", "dealbreakers": "expensive or uncool brand"},
    {"id": "retiree",          "name": "Senior Retiree",       "emoji": "🧓", "age": 67, "occupation": "Retired Accountant",     "income": "$28k",  "segment": "Economy",   "traits": ["value-seeker","simple-is-better","skeptical-of-tech"], "priorities": "ease of use and reliability", "dealbreakers": "complex interface or constant updates"},
    {"id": "blue_collar",      "name": "Blue Collar Worker",   "emoji": "🔧", "age": 38, "occupation": "Construction Foreman",   "income": "$52k",  "segment": "Economy",   "traits": ["durability-first","practical","no-frills"], "priorities": "ruggedness and battery life", "dealbreakers": "fragile build or too technical"},
    # ── Mid-Range Segment ──
    {"id": "young_parent",     "name": "Young Parent",         "emoji": "👨‍👩‍👧", "age": 34, "occupation": "Marketing Coordinator","income": "$65k",  "segment": "Mid-Range", "traits": ["family-focused","safety-conscious","time-pressed"], "priorities": "reliability, parental controls, family sharing", "dealbreakers": "no parental controls or complex setup"},
    {"id": "fitness_fanatic",  "name": "Fitness Fanatic",      "emoji": "💪", "age": 28, "occupation": "Personal Trainer",       "income": "$48k",  "segment": "Mid-Range", "traits": ["health-obsessed","outdoor-active","wearable-lover"], "priorities": "health tracking, GPS accuracy, waterproofing", "dealbreakers": "poor health sensors or short battery"},
    {"id": "creative_pro",     "name": "Creative Professional","emoji": "🎨", "age": 31, "occupation": "Graphic Designer",       "income": "$72k",  "segment": "Mid-Range", "traits": ["visual-thinker","color-accurate-display-lover","tool-power-user"], "priorities": "display quality, stylus support, creative apps", "dealbreakers": "poor display or no stylus/creative tools"},
    {"id": "social_influencer","name": "Social Media Influencer","emoji":"📱","age": 25, "occupation": "Content Creator",         "income": "$55k",  "segment": "Mid-Range", "traits": ["appearance-obsessed","social","camera-first"], "priorities": "camera quality, aesthetics, social features", "dealbreakers": "ugly design or bad camera"},
    {"id": "gamer",            "name": "Hardcore Gamer",        "emoji": "🎮", "age": 24, "occupation": "Esports Player",        "income": "$40k",  "segment": "Mid-Range", "traits": ["performance-first","competitive","fps-obsessed"], "priorities": "refresh rate, low latency, thermal management", "dealbreakers": "thermal throttle or low FPS"},
    {"id": "minimalist",       "name": "Digital Minimalist",   "emoji": "🌿", "age": 35, "occupation": "UX Researcher",          "income": "$80k",  "segment": "Mid-Range", "traits": ["simplicity-loving","eco-conscious","privacy-focused"], "priorities": "clean interface, privacy, sustainability", "dealbreakers": "bloatware or privacy violations"},
    # ── Premium Segment ──
    {"id": "premium_buyer",    "name": "Luxury Buyer",         "emoji": "💎", "age": 44, "occupation": "Investment Banker",      "income": "$250k", "segment": "Premium",   "traits": ["status-driven","luxury-loving","convenience-first"], "priorities": "prestige, exclusive feel, best of everything", "dealbreakers": "cheap feel or mass-market positioning"},
    {"id": "tech_enthusiast",  "name": "Tech Enthusiast",      "emoji": "⚡", "age": 27, "occupation": "Software Engineer",      "income": "$130k", "segment": "Premium",   "traits": ["spec-obsessed","early adopter","innovation-hungry"], "priorities": "latest specs, cutting-edge features, dev tools", "dealbreakers": "outdated tech or locked ecosystem"},
    {"id": "enterprise_exec",  "name": "C-Suite Executive",    "emoji": "🏢", "age": 52, "occupation": "Chief Operating Officer","income": "$400k", "segment": "Premium",   "traits": ["productivity-driven","brand-conscious","ROI-focused"], "priorities": "enterprise integrations, prestige, reliability", "dealbreakers": "unreliable or not enterprise-grade"},
    {"id": "photographer",     "name": "Pro Photographer",     "emoji": "📷", "age": 33, "occupation": "Wedding Photographer",   "income": "$85k",  "segment": "Premium",   "traits": ["image-quality-obsessed","detail-oriented","professional-grade"], "priorities": "sensor quality, RAW support, pro camera tools", "dealbreakers": "poor camera or no pro photo features"},
    {"id": "business_traveler","name": "Business Traveler",    "emoji": "✈️", "age": 41, "occupation": "Regional Sales VP",      "income": "$150k", "segment": "Premium",   "traits": ["globally-mobile","productivity-obsessed","connectivity-first"], "priorities": "battery life, lightweight, global connectivity", "dealbreakers": "heavy device or poor reception abroad"},
    # ── Specialty Segment ──
    {"id": "healthcare_worker","name": "Healthcare Worker",    "emoji": "⚕️", "age": 37, "occupation": "Registered Nurse",       "income": "$75k",  "segment": "Specialty", "traits": ["hygiene-conscious","reliability-first","easy-to-clean"], "priorities": "durability, splash resistance, simple access", "dealbreakers": "not water resistant or too fragile"},
    {"id": "rural_user",       "name": "Rural User",           "emoji": "🌾", "age": 45, "occupation": "Farming SMB Owner",      "income": "$60k",  "segment": "Specialty", "traits": ["durability-first","offline-capable","practical"], "priorities": "tough build, long battery, works without wifi", "dealbreakers": "requires constant internet or fragile"},
    {"id": "gen_z_zoomer",     "name": "Gen Z Zoomer",         "emoji": "✨", "age": 19, "occupation": "Part-time Barista",      "income": "$18k",  "segment": "Specialty", "traits": ["trend-chaser","authenticity-obsessed","meme-literate"], "priorities": "viral features, authenticity, short-form video", "dealbreakers": "uncool or boomer-targeted design"},
    {"id": "small_biz_owner",  "name": "Small Biz Owner",      "emoji": "🛍️", "age": 43, "occupation": "Boutique Shop Owner",    "income": "$90k",  "segment": "Specialty", "traits": ["ROI-focused","practical","multitasker"], "priorities": "payment tools, inventory apps, business workflow", "dealbreakers": "no business app ecosystem"},
    {"id": "developer",        "name": "Software Developer",   "emoji": "👨‍💻", "age": 30, "occupation": "Full-Stack Engineer",   "income": "$120k", "segment": "Specialty", "traits": ["power-user","open-ecosystem-lover","tools-obsessed"], "priorities": "developer tools, USB-C, terminal access, open ecosystem", "dealbreakers": "locked ecosystem or no dev tools"},
]

# ─── Multi-Backend LLM Orchestrator ──────────────────────────────────────────
class LLMOrchestrator:
    """
    TinyTroupe-style multi-backend orchestrator.
    Distributes persona evaluations across Groq, Gemini, OpenRouter, Ollama.
    """
    
    def __init__(self):
        self.backends = []
        self._gemini_models_cache = {}
        self._init_backends()
    
    def _init_backends(self):
        """Initialize all available LLM backends."""
        
        # 1. Groq — fastest, free tier, best for bulk persona simulation
        groq_key = os.getenv("GROQ_API_KEY", "")
        if groq_key:
            from openai import AsyncOpenAI as AsyncOAI
            self.backends.append({
                "name": "Groq",
                "type": "openai_compat",
                "client": AsyncOAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1"),
                "model": "llama-3.3-70b-versatile",
                "emoji": "⚡",
                "max_concurrent": 4,
                "semaphore": asyncio.Semaphore(4),
            })
        
        # 2. Gemini — via google.generativeai
        gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY", "")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self.backends.append({
                    "name": "Gemini",
                    "type": "gemini",
                    "model": "models/gemini-2.0-flash",
                    "gemini_key": gemini_key,
                    "emoji": "🔮",
                    "max_concurrent": 3,
                    "semaphore": asyncio.Semaphore(3),
                })
            except Exception:
                pass
        
        # 3. OpenRouter — free models via OpenAI-compat
        or_key = os.getenv("OPEN_ROUTER_API_KEY", "")
        if or_key:
            from openai import AsyncOpenAI as AsyncOAI
            self.backends.append({
                "name": "OpenRouter",
                "type": "openai_compat",
                "client": AsyncOAI(api_key=or_key, base_url="https://openrouter.ai/api/v1"),
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "emoji": "🌐",
                "max_concurrent": 2,
                "semaphore": asyncio.Semaphore(2),
            })
        
        # 4. Ollama — local qwen3:8b (check if running)
        self.backends.append({
            "name": "Ollama",
            "type": "ollama",
            "model": "qwen3:8b",
            "base_url": "http://localhost:11434",
            "emoji": "🦙",
            "max_concurrent": 2,
            "semaphore": asyncio.Semaphore(2),
            "available": None,  # lazily checked
        })
        
        print(f"\n🤖 TinyTroupe Orchestrator — {len(self.backends)} backends configured:")
        for b in self.backends:
            print(f"   {b['emoji']} {b['name']}: {b['model']}")
    
    async def _check_ollama(self) -> bool:
        """Check if Ollama is running locally."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                r = await client.get("http://localhost:11434/api/tags")
                if r.status_code == 200:
                    models = [m["name"] for m in r.json().get("models", [])]
                    return any("qwen" in m for m in models)
        except Exception:
            pass
        return False
    
    def _assign_backend(self, persona_idx: int) -> dict:
        """Round-robin backend assignment weighted by capacity."""
        if not self.backends:
            raise ValueError("No LLM backends available.")
        # Filter out unavailable backends
        available = [b for b in self.backends if b.get("name") != "Ollama" or b.get("available", True)]
        if not available:
            available = self.backends
        return available[persona_idx % len(available)]
    
    async def _call_openai_compat(self, backend: dict, messages: list) -> str:
        """Call an OpenAI-compatible endpoint (Groq, OpenRouter)."""
        async with backend["semaphore"]:
            response = await backend["client"].chat.completions.create(
                model=backend["model"],
                messages=messages,
                temperature=0.85,
                max_tokens=450,
            )
            return response.choices[0].message.content
    
    async def _call_gemini(self, backend: dict, messages: list) -> str:
        """Call Gemini API."""
        import google.generativeai as genai

        model_name = backend["model"]
        if model_name not in self._gemini_models_cache:
            self._gemini_models_cache[model_name] = genai.GenerativeModel(model_name)
        model = self._gemini_models_cache[model_name]

        async with backend["semaphore"]:
            loop = asyncio.get_event_loop()
            
            def _sync_call():
                gemini_msgs = []
                for m in messages:
                    role = "user" if m["role"] in ["user","system"] else "model"
                    gemini_msgs.append({"role": role, "parts": [m["content"]]})
                response = model.generate_content(gemini_msgs)
                return response.text
            
            return await loop.run_in_executor(None, _sync_call)
    
    async def _call_ollama(self, backend: dict, messages: list) -> str:
        """Call local Ollama API."""
        async with backend["semaphore"]:
            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {
                    "model": backend["model"],
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.85, "num_predict": 450}
                }
                r = await client.post(f"{backend['base_url']}/api/chat", json=payload)
                return r.json()["message"]["content"]
    
    async def call_backend(self, backend: dict, messages: list) -> str:
        """Route call to the appropriate backend."""
        if backend["type"] == "openai_compat":
            return await self._call_openai_compat(backend, messages)
        elif backend["type"] == "gemini":
            return await self._call_gemini(backend, messages)
        elif backend["type"] == "ollama":
            return await self._call_ollama(backend, messages)
        raise ValueError(f"Unknown backend type: {backend['type']}")
    
    async def evaluate_persona(self, persona: dict, product: dict, competitors: list, persona_idx: int) -> dict:
        """
        TinyTroupe agent evaluation — persona thinks in-character and decides.
        """
        backend = self._assign_backend(persona_idx)
        
        # Check Ollama lazily
        if backend["name"] == "Ollama" and backend.get("available") is None:
            backend["available"] = await self._check_ollama()
            if not backend["available"]:
                backend = self.backends[0]  # fallback to first backend
        
        all_products = [{"name": product["name"], "is_ours": True}] + [
            {"name": c["name"], "is_ours": False} for c in competitors[:6]
        ]
        product_list = "\n".join(
            f"  • {p['name']}" + (" ← [Product Being Evaluated]" if p["is_ours"] else "")
            for p in all_products
        )
        
        system_prompt = f"""You are a TinyTroupe AI persona — a fully simulated market research participant.
You ARE this specific person. Respond only as them, never as an AI assistant.

═══ YOUR PERSONA SPECIFICATION ═══
Name: {persona['name']}  
Age: {persona['age']} | Occupation: {persona['occupation']} | Annual Income: {persona['income']}
Market Segment: {persona['segment']}
Core Personality Traits: {', '.join(persona['traits'])}
Purchase Priorities: {persona['priorities']}
Absolute Dealbreakers: {persona['dealbreakers']}

Stay deeply in character. Let your income, job, life stage, and values guide every word."""

        user_prompt = f"""You are at a product evaluation session comparing options in the "{product.get('category', 'consumer product')}" space.

Products available:
{product_list}

Featured Product Details:
  Name: {product['name']}
  Description: {product.get('description', 'A new product on the market')}
  Key Highlights: {', '.join(product.get('features', [])[:6])}
  Price: ${product.get('price', '?')}

As {persona['name']}, deeply consider these products from YOUR perspective (income: {persona['income']}, priorities: {persona['priorities']}).

Make your decision and respond ONLY with this JSON (no markdown, no extra text):
{{
  "chosen_product": "<exact product name>",
  "purchase_probability": <integer 25-95>,
  "top_features": ["<feature 1>", "<feature 2>", "<feature 3>"],
  "quote": "<one sentence in your authentic voice>",
  "reasoning": "<2-3 sentences of in-character thinking>"
}}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        
        try:
            raw = await self.call_backend(backend, messages)
            
            # Clean markdown if present
            raw = raw.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            # Extract JSON block
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start != -1 and end > start:
                raw = raw[start:end]
            
            data = json.loads(raw)
            return {
                "persona_id": persona["id"],
                "persona_name": persona["name"],
                "emoji": persona["emoji"],
                "segment": persona["segment"],
                "backend": backend["name"],
                "chosen_product": data.get("chosen_product", product["name"]),
                "purchase_probability": max(25, min(95, int(data.get("purchase_probability", 60)))),
                "top_features": data.get("top_features", [])[:3],
                "quote": data.get("quote", "This fits my needs."),
                "reasoning": data.get("reasoning", ""),
            }
        except Exception as e:
            # Realistic fallback (not everyone picks the same thing)
            all_names = [product["name"]] + [c["name"] for c in competitors[:6]]
            weights = [50] + [10] * len(competitors[:6])
            chosen = random.choices(all_names, weights=weights[:len(all_names)], k=1)[0]
            prob = random.randint(30, 80)
            return {
                "persona_id": persona["id"],
                "persona_name": persona["name"],
                "emoji": persona["emoji"],
                "segment": persona["segment"],
                "backend": f"{backend['name']} (fallback)",
                "chosen_product": chosen,
                "purchase_probability": prob,
                "top_features": persona["priorities"].split(",")[:3],
                "quote": f"As a {persona['name'].lower()}, this matches my priorities.",
                "reasoning": f"Based on my key priorities: {persona['priorities']}.",
            }


# ─── Global orchestrator instance ────────────────────────────────────────────
orchestrator = LLMOrchestrator()

# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(title="Market Simulation Lab — TinyTroupe Edition")

allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def simulation_stream(product: dict, competitors: list) -> AsyncGenerator[str, None]:
    """Stream 20-persona evaluations using multi-backend orchestration."""
    total = len(PERSONAS)
    
    backend_names = [b["name"] for b in orchestrator.backends]
    yield f"data: {json.dumps({'type': 'start', 'total': total, 'backends': backend_names})}\n\n"
    
    results = []
    completed = 0
    
    # Launch ALL personas concurrently across backends — true parallel orchestration
    tasks = {
        asyncio.ensure_future(
            orchestrator.evaluate_persona(persona, product, competitors, idx)
        ): persona
        for idx, persona in enumerate(PERSONAS)
    }
    
    # Stream results as they complete (fastest backend wins each slot)
    for coro in asyncio.as_completed(list(tasks.keys())):
        try:
            result = await coro
            results.append(result)
            completed += 1
            yield f"data: {json.dumps({'type': 'persona_result', 'data': result, 'progress': completed, 'total': total})}\n\n"
            await asyncio.sleep(0.05)
        except Exception:
            completed += 1
    
    # Compute segment-aware summary
    product_votes: dict = {}
    segment_votes: dict = {}
    for r in results:
        p = r["chosen_product"]
        s = r.get("segment", "General")
        product_votes[p] = product_votes.get(p, 0) + 1
        if s not in segment_votes:
            segment_votes[s] = {}
        segment_votes[s][p] = segment_votes[s].get(p, 0) + 1
    
    winner = max(product_votes, key=product_votes.get) if product_votes else product["name"]
    
    yield f"data: {json.dumps({'type': 'simulation_complete', 'results': results, 'summary': {'total_personas': len(results), 'winner': winner, 'vote_distribution': product_votes, 'segment_breakdown': segment_votes}})}\n\n"


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "backend": "TinyTroupe Multi-Orchestrator",
        "backends": [{"name": b["name"], "model": b["model"], "emoji": b["emoji"]} for b in orchestrator.backends],
        "personas_available": len(PERSONAS),
        "segments": list(set(p["segment"] for p in PERSONAS)),
    }


@app.get("/api/personas")
async def get_personas():
    return {"personas": PERSONAS, "total": len(PERSONAS)}


@app.post("/api/simulate")
async def simulate(payload: dict):
    product = payload.get("product", {})
    competitors = payload.get("competitors", [])
    return StreamingResponse(
        simulation_stream(product, competitors),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 TinyTroupe Multi-LLM Market Simulation Lab")
    print("=" * 52)
    print(f"   Personas:  {len(PERSONAS)} archetypes across 4 market segments")
    print(f"   Backends:  {', '.join(b['name'] for b in orchestrator.backends)}")
    print(f"   API:       http://localhost:5501/api/health")
    print("=" * 52 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=5501)
