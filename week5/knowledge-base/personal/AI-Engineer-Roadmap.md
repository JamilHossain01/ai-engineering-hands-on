# From Senior Mobile Engineer to Principal AI Engineer
### A Tailored Roadmap Leveraging Your Flutter/Swift/Backend Background

---

## How To Read This Roadmap

You are not starting from zero. You already have the hardest skills a "bootcamp AI engineer" lacks: production system design, API design, state management, debugging under real constraints, and shipping to real users. This roadmap treats AI Engineering as **a new domain layered on top of your existing engineering maturity**, not a new career.

The roadmap has **5 sequential phases**. They are not strictly walled off — there's a deliberate overlap window between Phase 1 and Phase 2 (explained in detail below), because that transition point is where most self-taught engineers either quit or plateau. Everywhere else, finish a phase before moving to the next.

| Phase | Focus | Duration (at 1.5–2 hrs/day) |
|---|---|---|
| 0 | Foundation Mapping & Environment Setup | 1 week |
| 1 | Application-Layer AI Engineering (LLM APIs, RAG, Agents) | 6–8 weeks |
| 2 | Core Deep Learning & PyTorch (the "why" beneath the API calls) | 8–10 weeks |
| 3 | Open-Source Models, Fine-Tuning & On-Device AI | 6–8 weeks |
| 4 | Production MLOps, Evaluation & System Design | 6 weeks |
| 5 | Specialization & Portfolio Capstone | Ongoing |

Total: roughly **7–8 months** to genuine top-tier competency, working every day. This is realistic, not aspirational — Karpathy's own material assumes this kind of pace.

---

## Phase 0: Foundation Mapping & Environment Setup (Week 1)

**Goal:** Map your existing mental models onto AI engineering vocabulary so nothing in Phase 1–2 feels alien, and get your MacBook Pro configured as a proper local AI dev machine.

### Mental Model Mapping (do this consciously, write it down)
- REST API contract ↔ LLM prompt/response schema (structured outputs, function calling = your typed API contracts)
- State management (Bloc/Redux/Combine) ↔ Agent memory & conversation state
- Dependency injection ↔ Model/provider abstraction layers (swap OpenAI ↔ Claude ↔ local model)
- Async/await & concurrency (Swift Concurrency, Dart Futures) ↔ Streaming tokens, async agent tool calls
- Unit testing ↔ Model evaluation (evals) — same discipline, different metrics
- CI/CD ↔ MLOps pipelines (Phase 4)

### Environment Setup (Apple Silicon-specific)
1. Install `uv` (modern Python package manager — faster than pip/poetry, use it from day one).
2. Install [Ollama](https://ollama.com) — run quantized open models locally (Llama 3.x, Qwen, Phi, Mistral) via Metal acceleration.
3. Install **MLX** (`pip install mlx mlx-lm`) — Apple's own array framework, built for Apple Silicon. This becomes critical in Phase 3.
4. Set up a proper `venv`/`uv venv` per project — never global installs.
5. Get a GitHub repo scaffolded now: `ai-engineering-journal`. Commit daily. This is your visible proof of consistency for recruiters/hiring managers later — treat it like a work log, not a toy.
6. Get API keys: OpenAI, Anthropic, and (free tier) Google Gemini — you'll compare providers throughout Phase 1.

### Daily Routine This Week
- 30 min: environment setup / troubleshooting
- 45 min: skim the syllabus of Ed Donner's course AND Karpathy's Zero to Hero playlist side by side, noting where topics rhyme
- 15 min: journal your mental-model mapping in the GitHub repo's README

---

## Phase 1: Application-Layer AI Engineering (Weeks 2–9)

**Goal:** Become fluent and *production-grade* competent at building with LLM APIs — RAG, agents, tool use, structured outputs — before you touch the math. This is where Ed Donner's course lives, and it's the correct starting point for someone with your background, because it maps directly onto skills you already have (API integration, backend design).

### Why this order (not "learn PyTorch first")
Most people who "start with the math" burn out before they ever ship anything, because they can't see how transformer internals connect to a working product. You're the opposite risk profile: you could ship a RAG app in a week, but without Phase 2 you'll hit a ceiling — you won't be able to debug hallucinations, reason about context windows, do real fine-tuning, or speak credibly to an ML team. Phase 1 gives you the product intuition; Phase 2 gives you the depth to back it up.

### Curriculum
1. **Continue Ed Donner's course to completion**, but treat every module as a project seed, not just a lesson:
   - LLM API fundamentals (OpenAI, Anthropic, open-source via Ollama) → build a provider-agnostic wrapper (this is literally an interface/abstract-class pattern you already know from Swift/Dart)
   - RAG (retrieval-augmented generation) → don't just follow along, rebuild it with a different vector DB (Chroma → then try Qdrant or LanceDB, which runs great locally on macOS)
   - Agentic workflows / tool calling → this is the closest analog to what you already do wiring up APIs and handling async responses
   - Multi-agent systems → treat this like a distributed systems problem (message passing, orchestration)

2. **Parallel reading (20 min/day, not video):**
   - Anthropic's own prompt engineering & agent-building docs (docs.claude.com) — these are the actual production patterns used at a top AI lab, and directly relevant since you'll likely build with Claude too
   - "Building LLM Applications for Production" (Chip Huyen's blog series) — bridges application engineering and the MLOps mindset you'll need in Phase 4

### Portfolio Projects for Phase 1 (build 2–3, not all)
These are specifically chosen to combine your mobile expertise with what most AI-only engineers *cannot* build:

1. **"On-Device RAG Assistant" (iOS/macOS)** — SwiftUI app that runs a local RAG pipeline: user's documents embedded and stored locally (SQLite + vector search, or Core Data), retrieval done on-device, generation via Ollama running locally or a cloud API as fallback. This is a genuinely rare portfolio piece — almost no AI engineers can ship a real native app, and almost no mobile engineers understand RAG.
2. **"Flutter Agentic Task App"** — a Flutter app with a backend (FastAPI) implementing a tool-calling agent (e.g., an agent that manages calendar/tasks, calls real APIs, has memory). Focus on clean separation: Flutter client ↔ your own API layer ↔ LLM provider abstraction. This demonstrates you can build the *full stack* around an agent, not just prompt it.
3. **"Provider-Agnostic LLM Gateway"** — a small backend service (FastAPI) that abstracts OpenAI/Anthropic/local Ollama behind one interface, with streaming, retries, cost/token logging, and structured-output validation (Pydantic). This is exactly the kind of internal tool real AI platform teams build — put this on GitHub with a proper README and tests.

### Daily Routine (Phase 1)
- 45 min: Ed Donner course (video + follow-along code)
- 45 min: extend/modify what you just learned into your own project (never copy-paste passively — always change something: swap the vector DB, change the prompt schema, add error handling)
- 15–20 min: commit to GitHub with a meaningful message + short note in your journal on what broke and why

**Exit criterion for Phase 1:** You can explain, without notes, how RAG retrieval works, how an agent decides to call a tool, and why context window size matters — and you have at least one deployed (even locally-hosted) project.

---

## Phase 2: Core Deep Learning & PyTorch — The Karpathy Transition (Weeks 10–19)

**Goal:** Understand *what's actually happening* inside the black box you've been calling via API. This phase converts you from "prompt engineer" to someone who can read a paper, debug training, and eventually fine-tune models with real understanding.

### The Transition Strategy (this is the part you specifically asked about)

The biggest failure mode here is **full context-switch whiplash** — stopping application work cold turkey and drowning in backprop math for 10 weeks, losing momentum and motivation. Avoid it with this specific method:

**Step 1 — Overlap week (do this now, at the start of Phase 2, not before):**
Spend one week doing *only* Karpathy's first two videos back to back:
- "The spelled-out intro to neural networks and backpropagation: building micrograd"
- "The spelled-out intro to language modeling: building makemore"

Do NOT watch ahead. Build `micrograd` from scratch, by hand, in your own repo, without looking at his code except when stuck. This is the single highest-leverage exercise in the entire roadmap — it's where "backpropagation" stops being a word and becomes something you built with your own hands. Your engineering background means you'll grok computational graphs fast (it's just a DAG + reverse-mode autodiff — you've built dependency graphs before).

**Step 2 — Sequential immersion (weeks 11–17):**
Now go fully sequential through the rest of *Neural Networks: Zero to Hero*, in order:
1. makemore part 2–5 (MLP → BatchNorm → backprop internals → WaveNet)
2. Building GPT from scratch (this is the big one — budget 2 full weeks)
3. Tokenization (build your own BPE tokenizer)
4. **nanoGPT** — clone the repo, train a tiny model on your MacBook Pro (use MPS backend, not CPU) on a small dataset (Shakespeare corpus is the classic starting point). This is non-negotiable: actually train it, watch the loss curve, break it on purpose (change learning rate, remove layer norm) and observe what happens.

During this window, **pause new Ed Donner modules** (or move to 1x/week maintenance mode). This is the one deliberate non-overlap in the roadmap — depth work needs protected, uninterrupted time. Your brain needs to stay inside "gradient descent and matrix shapes" mode, not toggle between that and "which agent framework should I use."

**Step 3 — Reintegration (weeks 18–19):**
Go back to your Phase 1 projects and *rebuild one small piece from the API level down*. Concretely: take your provider-agnostic LLM gateway and add a tiny local model you trained yourself (even a toy character-level model) as one of the swappable "providers." This forces you to reconcile the two mental models — API-level thinking and tensor-level thinking — into one coherent system. This single exercise is what separates people who "did a PyTorch course" from people who actually understand the stack top to bottom.

### Supplementary material (use only after Karpathy, as reinforcement — don't parallelize)
- fast.ai "Practical Deep Learning for Coders" Part 1 — good for solidifying PyTorch idioms (Dataset/DataLoader, training loops) with a more software-engineering-friendly framing than most ML courses
- PyTorch official 60-minute blitz — just for API reference, not conceptual learning (you'll already understand the concepts from Karpathy)

### Portfolio Projects for Phase 2
1. **"micrograd-swift" or "micrograd-dart"** — port Karpathy's micrograd to Swift or Dart. This is a genuinely unique portfolio piece: almost nobody has done this, and it proves you understand autodiff deeply enough to reimplement it in an unfamiliar paradigm (value semantics, no numpy). Huge talking point in interviews.
2. **"nanoGPT on my Mac"** — a documented repo showing training runs, loss curves (log them with a simple matplotlib script or wandb), and an explanation of every hyperparameter you changed and why. Treat the README like an engineering postmortem, not a tutorial follow-along.
3. **"Tokenizer from Scratch"** — implement BPE tokenization for a small custom vocabulary (e.g., tokenize Dart or Swift source code as a fun domain-specific twist), and write up how vocabulary size trades off against sequence length.

### Daily Routine (Phase 2)
- 50 min: Karpathy video (watch actively — pause constantly, predict the next line of code before he writes it)
- 50–60 min: type the code yourself from scratch in a fresh file (never copy his repo directly — typing it yourself is where the learning happens; only diff against his code when stuck)
- 10 min: journal — one specific thing that "clicked" and one thing still fuzzy (re-derive fuzzy items the next day before moving on)

**Exit criterion for Phase 2:** You can derive backpropagation through a small network on paper, explain self-attention's matrix shapes without notes, and have a trained (even if tiny) GPT-style model with a training log you can defend line by line.

---

## Phase 3: Open-Source Models, Fine-Tuning & On-Device AI (Weeks 20–27)

**Goal:** Take real pretrained open-weight models and adapt them — fine-tuning, quantization, and deployment to constrained environments (including your iPhone/Mac). This is where your mobile background becomes a genuine competitive advantage.

### Curriculum
1. **Hugging Face ecosystem**: `transformers`, `datasets`, `peft`, `trl` — learn these as libraries, not magic. You already understand package ecosystems (CocoaPods/SPM/pub.dev) — treat this the same way, read source when docs are unclear.
2. **Parameter-efficient fine-tuning**: LoRA and QLoRA in depth — understand *why* freezing base weights and training low-rank adapters works (this connects directly back to the matrix/gradient intuition from Phase 2).
3. **Full fine-tuning vs. PEFT vs. RAG vs. prompting** — build a mental decision tree for when each is the right engineering choice (this is a favorite senior-level interview question).
4. **Quantization**: GGUF, 4-bit/8-bit quantization, and why it matters for on-device deployment.
5. **Apple-specific deployment**: MLX fine-tuning (`mlx-lm` supports LoRA fine-tuning natively on Apple Silicon), and Core ML conversion for shipping models inside actual iOS apps.

### Portfolio Projects for Phase 3 (this is where you differentiate hardest)
1. **"Fine-Tuned Domain Assistant, Deployed On-Device"** — fine-tune a small open model (e.g., Qwen2.5-0.5B/1.5B or Llama 3.2 1B/3B) with LoRA on a domain-specific dataset you curate yourself (e.g., Flutter/Swift documentation Q&A, or your own past Stack Overflow answers), then convert it to Core ML or run it via MLX, and ship it inside a real SwiftUI app. **This single project — fine-tune → quantize → deploy on iPhone — is something the vast majority of "AI engineers" cannot do end-to-end.** It's your flagship portfolio piece.
2. **"Mobile Model Benchmark Suite"** — a small tool (CLI or app) that benchmarks different quantized model sizes on your Mac/iPhone for latency, memory, and quality tradeoffs — genuinely useful content for a technical blog post too.
3. **"LoRA Adapter Swapping Demo"** — one base model, multiple LoRA adapters trained for different tasks/personas, swapped at inference time — demonstrates deep understanding of PEFT architecture.

### Daily Routine (Phase 3)
- 40 min: reading/video (Hugging Face course modules, MLX documentation, relevant papers' abstracts + methodology sections — not full papers yet)
- 60 min: hands-on fine-tuning runs (these take real wall-clock time on a MacBook — queue a training run, work on deployment code while it runs)
- 10–15 min: document results (loss, before/after examples, what you'd change) in the GitHub repo

**Exit criterion for Phase 3:** A fine-tuned, quantized model running inside a real native app on your own device, with a written explanation of every architectural decision.

---

## Phase 4: Production MLOps, Evaluation & System Design (Weeks 28–33)

**Goal:** Everything a "top-tier" AI engineer needs beyond model-building — evaluation rigor, observability, cost control, and system design for AI products at scale. This phase maps almost one-to-one onto backend/DevOps skills you already have; the job here is translation, not new fundamentals.

### Curriculum
1. **Evaluation ("evals")** — the AI-native equivalent of your unit/integration tests. Learn LLM-as-judge patterns, golden datasets, regression testing for prompts/models (frameworks: `promptfoo`, or build your own harness — building your own is better for learning).
2. **Observability** — tracing agent/LLM calls (LangSmith, or Anthropic's own tooling), token/cost monitoring, latency budgets — same discipline as APM in mobile/backend, new vocabulary.
3. **RAG system design at scale** — chunking strategy tradeoffs, hybrid search (keyword + vector), re-ranking, caching strategies.
4. **Deployment patterns** — serving open models (vLLM, TGI) vs. managed APIs, cost/latency/control tradeoffs, autoscaling for bursty LLM traffic.
5. **AI system design interviews** — practice designing (on paper/whiteboard) systems like "design a customer support agent for 1M users," "design a code-review AI system," using the same rigor you'd apply to a mobile app's architecture doc.

### Portfolio Projects for Phase 4
1. **"Eval Harness for Your Own Fine-Tuned Model"** — go back to your Phase 3 model and build a proper eval suite: golden Q&A set, automated scoring, regression tracking across model versions. This demonstrates the rigor that separates senior from junior AI engineers.
2. **"Full-Stack AI Product with Observability"** — take your Phase 1 agentic app, add tracing, cost dashboards, and a fallback/retry strategy for provider outages — essentially "productionize" your earlier project. Write an architecture decision record (ADR) — a document format you likely already use.
3. **System design write-ups** — publish 3–5 written system design docs (even if never built) for AI products, in your GitHub or a blog. This is a high-signal, low-effort portfolio addition that most candidates skip.

### Daily Routine (Phase 4)
- 30 min: reading (Chip Huyen's "AI Engineering" book or Eugene Yan's blog — both are widely respected practitioner-level resources)
- 60 min: building the eval/observability tooling
- 20–30 min: one system design "sketch" per week (not daily) — draw it, write the tradeoffs, critique your own design the next day

**Exit criterion for Phase 4:** You can defend a production AI system design end to end — cost, latency, failure modes, evaluation strategy — the way you'd defend a mobile app architecture in a design review.

---

## Phase 5: Specialization & Portfolio Capstone (Ongoing)

By this point (~7–8 months in) you have a genuinely rare profile: someone who can ship native mobile apps, understands transformers at the tensor level, has fine-tuned and deployed models on-device, and thinks in production system design. Pick **one** specialization to go deep on for your capstone and job search:

- **On-device/Edge AI Specialist** (strongest fit for your background): become the person companies hire specifically because you can put real AI *inside* an iOS/Flutter app efficiently — this is a genuinely underserved niche.
- **Agentic Systems Engineer**: deep multi-agent orchestration, tool ecosystems, long-horizon planning.
- **AI Platform/Infra Engineer**: the person who builds the internal tooling (gateways, eval systems, fine-tuning pipelines) that other engineers use.

### Capstone Project
Combine everything: a fine-tuned, on-device model, wrapped in a real cross-platform (Flutter or native) app, with RAG for grounding, agentic tool use for actions, full observability, and a public eval report. Ship it to TestFlight or open-source it fully. Write a long-form technical blog post walking through the entire architecture — this becomes your primary interview artifact.

---

## Summary Timeline

```
Week 1        Phase 0 — Setup & mental model mapping
Weeks 2–9     Phase 1 — Ed Donner course, RAG/Agents/APIs, 3 portfolio projects
Week 10       Overlap week — micrograd + makemore (Karpathy)
Weeks 11–17   Phase 2 — Karpathy Zero to Hero + nanoGPT, deep PyTorch
Weeks 18–19   Reintegration — merge API-level and tensor-level projects
Weeks 20–27   Phase 3 — Fine-tuning, quantization, on-device deployment (flagship project)
Weeks 28–33   Phase 4 — Evals, observability, system design
Week 34+      Phase 5 — Specialization + capstone + job search
```

## Non-Negotiable Habits Throughout
1. **Daily GitHub commits** — even a 10-line change. This becomes both a forcing function and a portfolio.
2. **Never passively watch** — always retype code from scratch, never copy-paste from a tutorial repo.
3. **Weekly written reflection** — one paragraph: what you understood, what's still fuzzy, what you'll test next. This is the single best predictor of retention for engineers moving into a new domain.
4. **Ship something visible every phase** — a working app, a trained model, a benchmark — not just notebooks. Your unfair advantage over "notebook-only" AI learners is that you know how to ship.
