# STADIUMAI RAG

The backend `StadiumAIService` retrieves live rows from gates, crowd, parking, transport, and food court tables before composing an answer. In production, replace the deterministic composer with LangChain retrieval over FAISS plus OpenAI streaming:

1. Embed venue maps, SOPs, transit schedules, accessibility guides, and emergency playbooks.
2. Store vectors in FAISS with document metadata.
3. At request time, retrieve vector documents and structured SQL facts.
4. Generate a grounded answer in the user's language.
5. Persist `ai_conversations` with sources for auditability.
