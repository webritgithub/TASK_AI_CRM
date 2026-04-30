# AI-First CRM – HCP Interaction Module

An AI-powered Customer Relationship Management (CRM) system designed for Healthcare Professionals (HCPs).  
This system helps sales representatives log, analyze, and manage doctor interactions using AI.

---

## Features

### Log Interaction
- Add HCP interaction using:
  - Manual form
  - AI-powered chat input

### AI Autofill
- Converts natural language into structured CRM data

### AI Chat Assistant
- Generates:
  - Summary
  - Insights
  - Next Best Action

### AI Edit Interaction
- Modify existing data using natural language

### Dashboard Analytics
- Visualize sentiment (Positive / Neutral / Negative)

---

## AI Architecture (LangGraph)

The system uses **LangGraph** to create an AI workflow:

1. Extract structured data from input  
2. Analyze sentiment  
3. Log interaction  
4. Generate summary  
5. Generate insights  
6. Suggest next best action  

---

## AI Tools Used

- Log Interaction  
- Edit Interaction  
- Sentiment Analyzer  
- Summarizer  
- Insight Generator  
- Next Best Action  

---

## Tech Stack

### Frontend
- React.js
- Redux
- Recharts
- Google Inter Font

### Backend
- FastAPI (Python)
- LangGraph
- Groq LLM (Llama 3.3 / Gemma)

### Database
- PostgreSQL

---

**Use Case**

This system is designed for:

Pharma sales representatives
Medical field teams
CRM automation using AI

**Key Learnings**

Integration of LLM into real-world applications
Building AI workflows using LangGraph
Full-stack development (React + FastAPI)
CRM automation using AI
