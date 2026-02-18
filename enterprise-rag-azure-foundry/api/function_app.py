
import azure.functions as func
import json
import logging
import os
import time

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
import openai

app = func.FunctionApp()

# ─── Clients ───────────────────────────────────────────────────────────────

def get_search_client():
    return SearchClient(
        endpoint=os.environ["SEARCH_ENDPOINT"],
        index_name=os.environ["INDEX_NAME"],
        credential=AzureKeyCredential(os.environ["SEARCH_KEY"])
    )

def get_openai_client():
    return openai.AzureOpenAI(
        azure_endpoint=os.environ["OPENAI_ENDPOINT"],
        api_key=os.environ["OPENAI_KEY"],
        api_version="2024-02-01"
    )

# ─── Helpers ───────────────────────────────────────────────────────────────

def embed_question(question: str) -> list:
    client = get_openai_client()
    response = client.embeddings.create(
        model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
        input=question
    )
    return response.data[0].embedding


def hybrid_search(question: str, user_groups: list, top_k: int = 5) -> list:
    client = get_search_client()
    vector = embed_question(question)

    security_filter = None
    if user_groups:
        groups_str = ",".join(user_groups)
        security_filter = f"access_groups/any(g: search.in(g, '{groups_str}', ','))"

    results = client.search(
        search_text=question,
        vector_queries=[
            VectorizedQuery(
                vector=vector,
                k_nearest_neighbors=top_k,
                fields="content_vector"
            )
        ],
        filter=security_filter,
        select=["chunk", "title", "parent_id", "department", "source_path"],
        top=top_k,
        query_type="semantic",
        semantic_configuration_name="semantic-config"
    )
    return [doc for doc in results]


def build_context(results: list) -> str:
    parts = []
    for i, doc in enumerate(results, 1):
        heading = doc.get("title", "Source")
        chunk = doc.get("chunk", "")
        parts.append(f"[{i}] {heading}\n{chunk}")
    return "\n\n".join(parts)


def extract_citations(results: list) -> list:
    return [
        {
            "id": i + 1,
            "title": doc.get("title", "Untitled"),
            "source_path": doc.get("source_path", ""),
            "department": doc.get("department", "")
        }
        for i, doc in enumerate(results)
    ]


def validate_token(token: str) -> dict:
    # Simplified – wire in MSAL/jwt validation in production
    return {
        "user_id": "demo_user",
        "groups": ["general", "hr-general"]
    }


# ─── Chat endpoint ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a helpful enterprise knowledge assistant.

Rules:
- Answer ONLY using the provided Context chunks.
- Do NOT use external knowledge or training data.
- Cite sources inline: [1], [2], etc.
- If the answer is not in the context, say: "I don't have that information in the knowledge base."
- Be concise. Use bullet points for lists. Professional, precise tone.
- For legal, HR disputes, or personnel matters, direct to appropriate human expert.
"""

@app.route(route="chat", methods=["POST"])
def chat(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    correlation_id = req.headers.get("x-correlation-id", "none")

    try:
        data = req.get_json()
        question = data.get("question", "").strip()
        if not question:
            return func.HttpResponse(
                json.dumps({"error": "Question is required"}),
                status_code=400,
                mimetype="application/json"
            )

        # 1. Auth
        token = req.headers.get("Authorization", "").replace("Bearer ", "")
        user_info = validate_token(token)
        logging.info(f"[{correlation_id}] User: {user_info['user_id']} | Q: {question[:80]}")

        # 2. Hybrid search
        search_start = time.time()
        results = hybrid_search(question, user_info["groups"])
        search_ms = round((time.time() - search_start) * 1000)
        logging.info(f"[{correlation_id}] Search: {len(results)} chunks in {search_ms}ms")

        # 3. Build prompt
        context = build_context(results)
        user_message = f"Context:\n{context}\n\nQuestion: {question}"

        # 4. Generate
        gen_start = time.time()
        client = get_openai_client()
        response = client.chat.completions.create(
            model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=800,
            temperature=0.1
        )
        gen_ms = round((time.time() - gen_start) * 1000)
        answer = response.choices[0].message.content
        logging.info(f"[{correlation_id}] Generation: {gen_ms}ms | tokens: {response.usage.total_tokens}")

        total_ms = round((time.time() - start) * 1000)

        return func.HttpResponse(
            json.dumps({
                "answer": answer,
                "citations": extract_citations(results),
                "telemetry": {
                    "search_ms": search_ms,
                    "generation_ms": gen_ms,
                    "total_ms": total_ms,
                    "tokens_used": response.usage.total_tokens,
                    "chunks_retrieved": len(results),
                    "correlation_id": correlation_id
                }
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"[{correlation_id}] Error: {str(e)}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "An error occurred. Please try again."}),
            status_code=500,
            mimetype="application/json"
        )
