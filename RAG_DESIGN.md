
## 1) What problem RAG solves?
- An LLM can't solve some issues reliably and so RAG exists because:
-- LLMs hallucinate
-- LLMs don't have access to private and up-to-date data
-- LLMs answer for the sake of it even when unsure!

***(failure prevention > performance.)***

## 2) How your system retrieves context?
- Documents --> chunks --> vectors --> similarity search --> top-k context

## 3) What happens when context is missing?
When retrieval fails, RAG:
- Detect low similarity
- Refuse to answer
- Ask for clarification or,
- return “insufficient context

Unlike LLMs, they hallucinate regardless of unsure context. 

## 4) How grounding is enforced?

We force the model to only use ***retrieved context*** by:
- Prompt constraints
- “If not in context, say you don’t know”
- Answer format rules
- Citations

**LLM reliability > ML accuracy**