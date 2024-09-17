import os
import time
import json

from openai import OpenAI

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/v1/")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")


es_client = Elasticsearch(ELASTIC_URL)
ollama_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


def elastic_search_text(query, subject=None, index_name="course-questions"):

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    if subject and subject in ["isw_general_faq", "qt_rebirth_faq"]:
        search_query["query"]["bool"]["filter"] = {
            "term": {"subject": subject}
        }

    response = es_client.search(index=index_name, body=search_query)
    
    return [hit['_source'] for hit in response['hits']['hits']]
    

# def elastic_search_text(query, course, index_name="course-questions"):
#     search_query = {
#         "size": 5,
#         "query": {
#             "bool": {
#                 "must": {
#                     "multi_match": {
#                         "query": query,
#                         "fields": ["question^3", "text", "section"],
#                         "type": "best_fields",
#                     }
#                 },
#                 "filter": {"term": {"course": course}},
#             }
#         },
#     }

#     response = es_client.search(index=index_name, body=search_query)
#     return [hit["_source"] for hit in response["hits"]["hits"]]


def elastic_search_knn(field,vector, subject=None, index_name="course-questions"):
    # search_term =query
    # vector_search_term=model.encode(search_term)
    knn_query = {
        "field": field,
        "query_vector": vector,
        "k": 5,
        "num_candidates": 100
    }

    
    knn_query = {
        "field": "text",
        "query_vector": vector,
        "k": 5,
        "num_candidates": 100
    }
    
    if subject and subject in ["isw_general_faq", "qt_rebirth_faq"]:
        response = es_client.search(
            index=index_name,
            query={
                "match": {"subject": f"{subject}"},
            },
            knn=knn_query,
            size=5,
            explain=True
        )
    else:
        response = es_client.search(
            index=index_name,
            knn=knn_query,
            size=5,
            explain=True
        )
    return [hit['_source'] for hit in response['hits']['hits']]

# def elastic_search_knn(field, vector, course, index_name="course-questions"):
#     knn = {
#         "field": field,
#         "query_vector": vector,
#         "k": 5,
#         "num_candidates": 10000,
#         "filter": {"term": {"course": course}},
#     }

#     search_query = {
#         "knn": knn,
#         "_source": ["text", "subject", "question", "course", "id"],
#     }

#     es_results = es_client.search(index=index_name, body=search_query)

#     return [hit["_source"] for hit in es_results["hits"]["hits"]]


def build_prompt(query, search_results):
    prompt_template = """
You're a Financial Services application assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.
If the CONTEXT doesn't contain the answer , output Hmmn , I'm not sure kindly reach out 
to the Quickteller team on WhatsApp - 07009065000

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = "\n\n".join(
        [
            f"question: {doc['question']}\nanswer: {doc['text']}"
            for doc in search_results
        ]
    )
    return prompt_template.format(question=query, context=context).strip()


def llm(prompt, model_choice):
    start_time = time.time()
    if model_choice.startswith('ollama/'):
        response = ollama_client.chat.completions.create(
            model=model_choice.split('/')[-1],
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        tokens = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
    elif model_choice.startswith('openai/'):
        response = openai_client.chat.completions.create(
            model=model_choice.split('/')[-1],
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        tokens = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
    else:
        raise ValueError(f"Unknown model choice: {model_choice}")
    
    end_time = time.time()
    response_time = end_time - start_time
    
    return answer, tokens, response_time


# def evaluate_relevance(question, answer):
#     prompt_template = """
#     You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
#     Your task is to analyze the relevance of the generated answer to the given question.
#     Based on the relevance of the generated answer, you will classify it
#     as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

#     Here is the data for evaluation:

#     Question: {question}
#     Generated Answer: {answer}

#     Please analyze the content and context of the generated answer in relation to the question
#     and provide your evaluation in parsable JSON without using code blocks:

#     {{
#       "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
#       "Explanation": "[Provide a brief explanation for your evaluation]"
#     }}
#     """.strip()

#     prompt = prompt_template.format(question=question, answer=answer)
#     evaluation, tokens, _ = llm(prompt, 'openai/gpt-4o-mini')
    
#     try:
#         json_eval = json.loads(evaluation)
#         return json_eval['Relevance'], json_eval['Explanation'], tokens
#     except json.JSONDecodeError:
#         return "UNKNOWN", "Failed to parse evaluation", tokens


def calculate_openai_cost(model_choice, tokens):
    openai_cost = 0

    if model_choice == 'openai/gpt-3.5-turbo':
        openai_cost = (tokens['prompt_tokens'] * 0.0015 + tokens['completion_tokens'] * 0.002) / 1000
    elif model_choice ==  'openai/gpt-4o-mini':
        openai_cost = (tokens['prompt_tokens'] * 0.15 + tokens['completion_tokens'] * 0.6) / 1000000

    return openai_cost


def get_answer(query,model_choice, search_type, subject=None):
    if search_type == 'Vector':
        vector = model.encode(query)
        search_results = elastic_search_knn('question_text_vector', vector, subject=subject)
    else:
        search_results = elastic_search_text(query, subject=subject)

    prompt = build_prompt(query, search_results)
    answer, tokens, response_time = llm(prompt, model_choice)
    
    #relevance, explanation, eval_tokens = evaluate_relevance(query, answer)

    openai_cost = calculate_openai_cost(model_choice, tokens)
 
    return {
        'answer': answer,
        'response_time': response_time,
        'model_used': model_choice,
        'prompt_tokens': tokens['prompt_tokens'],
        'completion_tokens': tokens['completion_tokens'],
        'total_tokens': tokens['total_tokens'],
        'openai_cost': openai_cost
    }