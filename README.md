````markdown
# 🎙️ RAG-O-RAMA

## Voice-Enabled Retrieval-Augmented Generation System

> **Speak a question. Retrieve the right evidence. Get a grounded answer.**

RAG-O-RAMA is an end-to-end **Voice-Enabled Retrieval-Augmented Generation (RAG)** system designed to allow users to ask questions using natural voice input and receive answers grounded in information retrieved from a knowledge base.

Unlike a simple Voice → LLM application, RAG-O-RAMA implements a complete retrieval pipeline consisting of **speech-to-text, document processing, multiple chunking strategies, embeddings, vector retrieval, lexical retrieval, hybrid retrieval, LLM-based answer generation, guardrails, error handling, and latency benchmarking**.

The system is designed around a simple principle:

> **Retrieve evidence first. Generate an answer only when the evidence is sufficient.**

---

# 🚀 Overview

Large Language Models are powerful at generating natural-language responses, but they can sometimes provide confident answers that are unsupported by the available information.

RAG-O-RAMA addresses this problem by introducing a retrieval layer between the user's question and the language model.

Instead of directly sending a question to an LLM:

```text
User
 ↓
LLM
 ↓
Answer
````

RAG-O-RAMA follows:

```text
🎤 Voice Question
       ↓
Speech-to-Text
       ↓
Query
       ↓
Document Retrieval
       ↓
Relevant Evidence
       ↓
Guardrails
       ↓
LLM
       ↓
Grounded Answer
```

If sufficient evidence cannot be retrieved, the system is designed to **avoid generating an unsupported answer**.

---

# 🎯 Problem Statement

Traditional LLM-based question-answering systems have several limitations:

* They may hallucinate information.
* They may answer questions outside their knowledge base.
* They may retrieve irrelevant information.
* A single retrieval strategy may not work well for every query.
* System latency may vary significantly between queries.
* A single successful test does not accurately represent system performance.
* API or pipeline failures can interrupt the entire application.

RAG-O-RAMA addresses these challenges by building an engineered, measurable, and guardrailed voice-based RAG pipeline.

---

# 💡 Our Solution

RAG-O-RAMA combines several components into one end-to-end system:

### 🎤 Voice Input

Users can speak their questions naturally instead of typing them.

### 📝 Speech-to-Text

The spoken question is converted into text.

### ✂️ Engineered Chunking

Documents are processed using multiple chunking approaches instead of relying on one simple text split.

### 🧠 Embeddings

Text is transformed into vector representations that capture semantic meaning.

### 🔎 Retrieval

Relevant information is retrieved using semantic and lexical retrieval techniques.

### 🔀 Hybrid Retrieval

Multiple retrieval signals are combined to improve the quality of retrieved evidence.

### 🤖 Generation

The retrieved evidence is provided to an LLM to generate the final response.

### 🛡️ Guardrails

The system checks whether enough evidence exists before allowing an answer to be generated.

### ⚡ Benchmarking

The pipeline is tested across multiple queries and evaluated using latency percentiles such as P50, P70, and P100.

### 🔄 Error Handling

The runtime pipeline includes structured execution, retries, and recovery mechanisms to handle failures gracefully.

---

# 🏗️ System Architecture

```text
                         🎤 USER
                            │
                            ▼
                 ┌────────────────────┐
                 │  Speech-to-Text    │
                 └─────────┬──────────┘
                           │
                           ▼
                    Text Question
                           │
                           ▼
                 ┌────────────────────┐
                 │  Query Processing  │
                 └─────────┬──────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │     Retrieval Layer      │
              │                          │
              │  Vector Search + BM25    │
              └────────────┬─────────────┘
                           │
                           ▼
                  Relevant Evidence
                           │
                           ▼
                 ┌────────────────────┐
                 │     Guardrails     │
                 └─────────┬──────────┘
                           │
                    Evidence Sufficient?
                       /           \
                     YES            NO
                      │              │
                      ▼              ▼
              ┌──────────────┐    REFUSE
              │     LLM      │
              └──────┬───────┘
                     │
                     ▼
              Grounded Answer
                     │
                     ▼
              Benchmark / Logs
```

---

# 🔄 End-to-End Pipeline

The complete pipeline can be represented as:

```text
Voice
  ↓
Speech-to-Text
  ↓
Text Query
  ↓
Query Processing
  ↓
Chunk Retrieval
  ↓
Vector Search
  +
BM25 Search
  ↓
Hybrid Ranking
  ↓
Relevant Context
  ↓
Guardrails
  ↓
LLM Generation
  ↓
Grounded Answer
```

---

# 🧩 Core Components

## 1. 🎤 Voice Input

RAG-O-RAMA is designed around voice-first interaction.

The user speaks a question through the application.

Example:

```text
"What information is available about this topic?"
```

The audio is passed to the speech recognition component.

---

## 2. 📝 Speech-to-Text

The speech-to-text layer converts the user's voice into a text query.

```text
Audio
 ↓
Speech Recognition
 ↓
Text
```

This text becomes the input to the RAG pipeline.

---

## 3. 📚 Data Processing

The system works with a knowledge base containing documents and associated information.

The data pipeline prepares the source material for retrieval.

The general process is:

```text
Raw Dataset
     ↓
Data Processing
     ↓
Documents
     ↓
Chunking
     ↓
Embeddings
     ↓
Retrieval Index
```

---

# ✂️ 4. Engineered Chunking

One of the important design decisions in RAG-O-RAMA is that documents are not treated as one large block of text.

Large documents are divided into smaller retrieval units called **chunks**.

```text
Large Document
      ↓
┌─────────────┐
│   Chunk 1   │
├─────────────┤
│   Chunk 2   │
├─────────────┤
│   Chunk 3   │
├─────────────┤
│   Chunk 4   │
└─────────────┘
```

The system implements multiple chunking approaches to evaluate how chunk structure affects retrieval.

Examples include:

* Fixed-size chunking
* Sentence-based chunking
* Semantic chunking
* Metadata-aware chunking

Each strategy has different trade-offs between context preservation, retrieval precision, and computational cost.

---

# 🧠 5. Embeddings

After chunking, text is converted into numerical vector representations called **embeddings**.

Conceptually:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

For example:

```text
"What is retrieval augmented generation?"
                    ↓
        [0.12, -0.42, 0.81, ...]
```

The vectors allow the system to compare the semantic similarity between a user query and stored chunks.

---

# 🔎 6. Vector Retrieval

The query is converted into an embedding and compared with the indexed document embeddings.

```text
User Query
    ↓
Query Embedding
    ↓
Vector Search
    ↓
Top-K Relevant Chunks
```

This enables the system to retrieve information based on **meaning**, rather than requiring an exact keyword match.

---

# 🔤 7. BM25 Retrieval

RAG-O-RAMA also uses lexical retrieval through BM25.

BM25 is useful when exact terms, keywords, names, or phrases are important.

The pipeline becomes:

```text
                 Query
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Vector Retrieval       BM25
          │                 │
          └────────┬────────┘
                   ▼
             Combined Results
```

---

# 🔀 8. Hybrid Retrieval

Semantic and lexical retrieval have different strengths.

Vector retrieval is useful for understanding semantic similarity.

BM25 is useful for exact keyword matching.

RAG-O-RAMA combines these retrieval signals through hybrid retrieval.

```text
Vector Search
      +
BM25 Search
      ↓
Hybrid Retrieval
      ↓
Ranked Evidence
```

This provides a more robust retrieval pipeline than depending on only one retrieval mechanism.

---

# 🤖 9. LLM Generation

Once relevant evidence has been retrieved, it is passed to the language model along with the original question.

```text
User Question
      +
Retrieved Context
      ↓
     LLM
      ↓
Generated Answer
```

The goal is to make the model generate an answer based on the retrieved evidence rather than relying solely on its pretrained knowledge.

---

# 🛡️ 10. Guardrails

A key feature of RAG-O-RAMA is that the system is designed to know when **not to answer**.

The system checks whether retrieved information is sufficient to support an answer.

```text
Question
   ↓
Retrieve Evidence
   ↓
Evidence Sufficient?
   │
   ├── YES → Generate Answer
   │
   └── NO  → Refuse / Safe Response
```

This helps reduce hallucinations and unsupported responses.

The guardrail layer can handle scenarios such as:

* Insufficient evidence
* Irrelevant queries
* Unsupported answers
* Retrieval failures
* Potential hallucinations

---

# 🔍 Grounded Answering

The system follows a grounded generation approach.

The answer should be supported by the retrieved context.

Conceptually:

```text
Retrieved Evidence
       ↓
     LLM
       ↓
Generated Answer
       ↓
Grounding Check
       ↓
Final Response
```

If the answer cannot be adequately supported, the system can avoid presenting it as a confident factual response.

---

# 🔄 11. Runtime Harness

The complete pipeline is controlled through a runtime harness.

The harness manages:

* Input validation
* Structured inputs and outputs
* Pipeline orchestration
* Retries
* Error handling
* Recovery
* Logging
* Benchmarking

Conceptually:

```text
Request
   ↓
Validate
   ↓
Execute Pipeline
   ↓
Failure?
 ┌─┴─┐
YES  NO
 │    │
Retry Continue
 │    │
 └─┬──┘
   ↓
Response
```

This makes the system more reliable than a simple chain of API calls.

---

# ⚡ 12. Performance Benchmarking

Performance is measured across multiple queries rather than relying on a single successful run.

The benchmark records pipeline execution times and calculates latency percentiles.

### P50

The median latency.

Approximately half of the requests complete faster than this value.

### P70

The latency at which approximately 70% of requests complete.

### P100

The maximum observed latency in the benchmark set.

The benchmark therefore provides a more realistic picture of system performance.

---

# 📊 Benchmark Pipeline

```text
Test Queries
     ↓
Run Complete Pipeline
     ↓
Record Latency
     ↓
Aggregate Results
     ↓
Calculate
 ┌──────┬──────┬──────┐
 │ P50  │ P70  │ P100 │
 └──────┴──────┴──────┘
```

Component-level timings can also be measured:

```text
Speech-to-Text
      ↓
Retrieval
      ↓
Generation
      ↓
End-to-End
```

---

# 📂 Project Structure

```text
rag-o-rama/
│
├── app.py
│
├── data/
│   ├── load_data.py
│   └── ...
│
├── chunking/
│   ├── fixed.py
│   ├── sentence.py
│   ├── semantic.py
│   └── metadata.py
│
├── retrieval/
│   ├── vector.py
│   ├── bm25.py
│   └── hybrid.py
│
├── speech/
│   └── ...
│
├── generation/
│   └── ...
│
├── guardrails/
│   ├── relevance.py
│   └── grounding.py
│
├── benchmark/
│   └── benchmark.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🧰 Technology Stack

| Layer                | Technology                      |
| -------------------- | ------------------------------- |
| Programming Language | Python                          |
| Dataset              | AI4Bharat / MS MARCO-based data |
| Speech-to-Text       | Sarvam AI                       |
| Embeddings           | Sentence Transformers           |
| Vector Search        | FAISS                           |
| Lexical Search       | BM25                            |
| Retrieval            | Hybrid Retrieval                |
| Generation           | Large Language Model            |
| Interface            | Streamlit                       |
| Benchmarking         | Custom Python Benchmark Harness |
| Version Control      | Git / GitHub                    |

---

# 🖥️ Application Interface

The application provides a voice-based interface through which users can interact with the RAG system.

The intended interaction is:

```text
🎤 Click / Speak
      ↓
Question Transcribed
      ↓
Relevant Evidence Retrieved
      ↓
Guardrails Evaluated
      ↓
Answer Generated
      ↓
Response Displayed
```

The interface also exposes useful information about the response and system execution where applicable.

---

# 📈 Evaluation

RAG-O-RAMA evaluates the system across multiple dimensions.

## Retrieval Quality

* Relevance of retrieved chunks
* Vector retrieval performance
* BM25 retrieval performance
* Hybrid retrieval performance

## Answer Quality

* Groundedness
* Evidence utilization
* Unsupported-answer detection

## Performance

* P50 latency
* P70 latency
* P100 latency
* Component-level latency

## Reliability

* API failures
* Retry behavior
* Invalid inputs
* Retrieval failures
* Graceful refusal

---

# 🔐 Security

API credentials are stored using environment variables and are not committed to the repository.

Example:

```env
SARVAM_API_KEY=your_api_key
LLM_API_KEY=your_api_key
```

The `.env` file should be included in `.gitignore`.

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# 🚀 Running the Project Locally

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd rag-o-rama
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file and add the required API keys.

```env
SARVAM_API_KEY=your_api_key
LLM_API_KEY=your_api_key
```

## 5. Start the application

```bash
streamlit run app.py
```

---

# 🧪 Running the Benchmark

The benchmark can be executed using:

```bash
python benchmark/benchmark.py
```

The benchmark runs the pipeline across multiple queries and calculates latency statistics.

Example:

```text
========================================
          RAG-O-RAMA BENCHMARK
========================================

Number of Queries: 100

P50 Latency:   XX ms
P70 Latency:   XX ms
P100 Latency:  XX ms

Retrieval:     XX ms
Generation:    XX ms
End-to-End:    XX ms

========================================
```

Replace the placeholder values with the actual benchmark results from the project.

---

# 🏆 What Makes RAG-O-RAMA Different?

RAG-O-RAMA is not simply a voice interface connected to an LLM.

The system is engineered as a complete retrieval pipeline:

```text
             🎤 Voice
                ↓
        Speech-to-Text
                ↓
             Query
                ↓
        ┌───────────────┐
        │   Retrieval   │
        │               │
        │ Vector + BM25 │
        └───────┬───────┘
                ↓
       Relevant Evidence
                ↓
          Guardrails
                ↓
       ┌────────┴────────┐
       │                 │
   Sufficient         Insufficient
   Evidence             Evidence
       │                 │
       ▼                 ▼
      LLM              Refuse
       │
       ▼
 Grounded Answer
       │
       ▼
   Benchmark
```

The emphasis is on:

**Retrieval quality + Groundedness + Reliability + Performance**

rather than simply generating a fluent response.

---

# 💻 Technical Concepts Demonstrated

RAG-O-RAMA demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Speech-to-Text
* Natural Language Processing
* Document Chunking
* Semantic Search
* Text Embeddings
* Vector Databases / Vector Search
* FAISS
* BM25
* Hybrid Retrieval
* Context Retrieval
* Prompt Engineering
* LLM Integration
* Grounded Generation
* Hallucination Mitigation
* Guardrails
* Error Handling
* Retry Mechanisms
* Structured I/O
* Latency Benchmarking
* Percentile Analysis
* Streamlit Application Development

---

# 🧠 Engineering Philosophy

RAG-O-RAMA was built with the goal of understanding and engineering the complete RAG pipeline rather than treating the system as a black box.

The architecture follows:

```text
Understand
    ↓
Implement
    ↓
Integrate
    ↓
Benchmark
    ↓
Improve
```

Every major component contributes to the overall system rather than existing as an isolated demonstration.

---

# 📌 Current Project Status

| Component              | Status     |
| ---------------------- | ---------- |
| Project Architecture   | ✅ Complete |
| Data Pipeline          | ✅ Complete |
| Chunking               | ✅ Complete |
| Embeddings             | ✅ Complete |
| Vector Retrieval       | ✅ Complete |
| BM25 Retrieval         | ✅ Complete |
| Hybrid Retrieval       | ✅ Complete |
| Speech-to-Text         | ✅ Complete |
| LLM Generation         | ✅ Complete |
| Guardrails             | ✅ Complete |
| Error Handling         | ✅ Complete |
| Runtime Harness        | ✅ Complete |
| Benchmarking           | ✅ Complete |
| Streamlit Interface    | ✅ Complete |
| End-to-End Integration | ✅ Complete |
| Deployment             | 🚧 Pending |

---

# 🚧 Deployment

The complete RAG-O-RAMA pipeline has been implemented and integrated locally.

The remaining step is deployment.

The deployment phase will make the application available through a public URL and allow users to interact with the voice-enabled RAG system remotely.

Potential deployment platforms include:

* Render
* Streamlit Community Cloud
* Hugging Face Spaces
* Other cloud platforms

---

# 🔮 Future Enhancements

Future versions of RAG-O-RAMA could include:

* Multilingual voice interaction
* Streaming speech recognition
* Streaming LLM responses
* Query rewriting
* Retrieval reranking
* Adaptive retrieval
* More advanced semantic chunking
* Continuous evaluation
* Production monitoring
* Distributed vector databases
* Authentication
* User-specific knowledge bases
* Cloud deployment
* Scalable production infrastructure

---

# 📚 References

The project builds upon concepts and technologies from the broader Retrieval-Augmented Generation and information retrieval ecosystem, including:

* AI4Bharat
* Hugging Face
* FAISS
* Sentence Transformers
* BM25
* Sarvam AI
* Streamlit
* Retrieval-Augmented Generation research

---

# 👥 Team

## RAG-O-RAMA

An end-to-end engineering project focused on building a **voice-enabled, retrieval-grounded, measurable, and reliable RAG system**.

---

# 🌟 Vision

RAG-O-RAMA aims to make knowledge retrieval as natural as having a conversation.

Instead of typing:

> *"Search through the knowledge base and tell me what you found."*

the user simply speaks.

```text
🎤 Speak
   ↓
🔎 Retrieve
   ↓
🛡️ Verify
   ↓
🤖 Answer
```

And when the system doesn't have enough evidence:

```text
🎤 Question
   ↓
🔎 No reliable evidence
   ↓
🛡️ Don't hallucinate
   ↓
❌ "I don't have enough information to answer that."
```

---

# 🎙️ RAG-O-RAMA

### **Speak. Retrieve. Verify. Answer.**

> **Voice in. Evidence retrieved. Answers grounded.**

```
