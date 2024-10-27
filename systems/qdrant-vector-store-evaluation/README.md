# Qdrant Vector Store Evaluation

Evaluation of the Qdrant vector store - whether using this vector store instead of the default llama-index local vector store changes the results.

For the evaluation, we use the same settings that were used for text-embedding-3-small model in the benchmark:
- OpenAI's embedding model that was shown to be the best-performing out of their models: "text-embedding-3-small"
- chunk size of 128 and similarity_top_k set to 2

We evaluate two possibilities of using the client:
- `location=":memory:"` is used when defining the Qdrant client.
- the Docker qdrant/qdrant is used.