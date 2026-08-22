# 🎙️ Voice RAG — Voice-to-Answer Retrieval-Augmented Generation

> **Speak a question. Retrieve the right evidence. Get a grounded answer.**

Voice RAG is an end-to-end **Voice-to-Answer Retrieval-Augmented Generation (RAG)** system that converts spoken questions into text, retrieves relevant information from a knowledge base, generates an evidence-grounded answer, and uses guardrails to avoid answering when sufficient evidence is unavailable.

The project is being built with a strong focus on **retrieval quality, latency benchmarking, reliability, and explainability**.

---

## 🚀 Project Status

🟡 **Work in Progress**

Current development stage:

- [x] Project architecture created
- [x] Python virtual environment configured
- [x] Dataset loading environment configured
- [ ] Dataset schema exploration
- [ ] Multiple chunking strategies
- [ ] Text embeddings
- [ ] Vector retrieval
- [ ] BM25 retrieval
- [ ] Hybrid retrieval
- [ ] LLM generation
- [ ] Speech-to-text
- [ ] Guardrails
- [ ] Error recovery and retries
- [ ] Benchmarking
- [ ] P50 / P70 / P100 latency evaluation
- [ ] Streamlit interface
- [ ] End-to-end deployment

---

# 🎯 Problem

Traditional question-answering systems can generate fluent answers even when they do not have reliable evidence.

This creates problems such as:

- Hallucinated answers
- Answers unrelated to the knowledge base
- Poor retrieval quality
- Slow response times
- Lack of measurable performance
- No clear mechanism for refusing unsupported questions

Voice RAG addresses these problems by combining:

```text
Voice Input
     ↓
Speech-to-Text
     ↓
Query Processing
     ↓
Multiple Retrieval Strategies
     ↓
Relevant Evidence
     ↓
Guardrails
     ↓
LLM Generation
     ↓
Grounded Answer / Safe Refusal
💡 What We Are Building

The final system will allow a user to:

1. 🎤 Speak a question

Instead of typing:

"What is the answer to this question?"

the user speaks naturally into the application.

2. 📝 Convert speech to text

The speech-to-text component converts the audio into a text query.

3. 🔎 Retrieve relevant information

The system searches the knowledge base using engineered retrieval strategies.

4. 🧩 Compare chunking strategies

Instead of relying on one naive text split, the project evaluates multiple chunking approaches.

Planned strategies include:

Fixed-size chunking
Sentence-based chunking
Semantic chunking
Metadata-aware chunking
5. 🤖 Generate an answer

The retrieved evidence is passed to a language model to generate a response.

6. 🛡️ Apply guardrails

The system checks whether enough reliable evidence exists before answering.

If the system cannot confidently ground an answer in the retrieved context, it should refuse rather than hallucinate.

7. ⚡ Measure performance

The system will benchmark multiple queries and report:

P50 latency
P70 latency
P100 latency
Retrieval latency
Generation latency
End-to-end latency
🏗️ System Architecture
                         🎤 USER
                            │
                            ▼
                  ┌──────────────────┐
                  │  Speech-to-Text  │
                  └────────┬─────────┘
                           │
                           ▼
                     Text Question
                           │
                           ▼
                  ┌──────────────────┐
                  │ Query Processing │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Vector Retrieval              BM25 Retrieval
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                   Ranked Evidence
                           │
                           ▼
                  ┌──────────────────┐
                  │    Guardrails    │
                  └────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
              Enough              Not enough
              evidence?            evidence?
                 │                   │
                YES                  NO
                 │                   │
                 ▼                   ▼
          ┌─────────────┐      Safe Refusal
          │     LLM     │
          └──────┬──────┘
                 │
                 ▼
          Grounded Answer
