# PandaChat-RAG Benchmark

Benchmark for evaluation of the retrieval-augmented generation (RAG) systems.

Currently, the benchmark consists of a Slovenian dataset:
- [PandaChat-RAG-sl dataset](data/eval_datasets/PandaChat-RAG-si/pandachat-rag-si-dataset.json): 206 questions from 160 texts with various topics, extracted from the Slovenian web corpus [CLASSLA-web.sl 1.0](
http://hdl.handle.net/11356/1882).

Currently the benchmark consists of the following task, but we plan to extend the list of tasks in the near future:
- Attributed Question-Answering (AQA): extension of the question-answering task, adapted for the needs of evaluation of the indexing and retrieval components of the RAG system. In this task, the input to the pipeline is a question, and the output is a pair of an answer and the relevant source text. The model is evaluated in retrieval accuracy - the percentage of questions for which the retriever identified the correct source text.

## Results

The results are available in the `results` directory which consists of:
- `results-aqa-sl.md` - table with the results of the AQA task on Slovenian test dataset, automatically updated once the `evaluate.py` script is ran
- `results.json` - results of all evaluated systems

### Retrieval accuracy (AQA task) on Slovenian test dataset

The models are evaluated on top 2 retrieved sources, and chunk_size = 128. We use the default (local) llama-index vector store, except for those, where the vector store is included in the name of the system (e.g., `qdrant-openai-embedding-3-small`)

| eval_scenario   | system                                 |   evaluated-top-k |   time_per_question (s) |   correct_retrieval_count |   correct_retrieval_per |
|:----------------|:---------------------------------------|------------------:|------------------------:|--------------------------:|------------------------:|
| aqa-sl          | bge-m3                                 |                 2 |                0.579386 |                       206 |                100      |
| aqa-sl          | multilingual-e5-large                  |                 2 |                0.583859 |                       206 |                100      |
| aqa-sl          | multilingual-e5-base                   |                 2 |                0.285738 |                       205 |                 99.5146 |
| aqa-sl          | text-embedding-3-small                 |                 2 |                0.692316 |                       205 |                 99.5146 |
| aqa-sl          | local-storage-text-embedding-3-small   |                 2 |                0.641238 |                       205 |                 99.5146 |
| aqa-sl          | qdrant-docker-openai-embedding-3-small |                 2 |                0.395684 |                       205 |                 99.5146 |
| aqa-sl          | gte-multilingual-base                  |                 2 |                0.310006 |                       204 |                 99.0291 |
| aqa-sl          | text-embedding-3-large                 |                 2 |                1.19002  |                       204 |                 99.0291 |
| aqa-sl          | multilingual-e5-small                  |                 2 |                0.15392  |                       203 |                 98.5437 |
| aqa-sl          | text-embedding-ada-002                 |                 2 |                0.631284 |                       203 |                 98.5437 |
| aqa-sl          | qdrant-openai-embedding-3-small        |                 2 |                0.42931  |                       199 |                 96.6019 |

## Benchmark Dataset

The PandaChat-RAG-sl is in a JSON format. Each instance is a dictionary with the following values:
- `query`: the question for which the system needs to provide an answer
- `answer`: true answer
- `document`: path to the document which should be retrieved to provide a correct answer to the query
- `text`: original text from which the query and answer were extracted
- `text_without_Q`: original text from which the query is removed - to be used for indexing and retrieval
- `multi_questions_doc`: NaN or "x" - whether the same text is the source of multiple questions and answers.


Example:
```json
  {
    "query": "Ali je no\u0161enje maske na UM obvezno?",
    "answer": "Obvezna je uporaba za\u0161\u010ditne maske ali druge oblike za\u0161\u010dite ustnega in nosnega predela obraza v zaprtem javnem prostoru. Obvezno je tudi razku\u017eevanje rok.",
    "document": "CLASSLA-web.sl.4006",
    "text": "Pomembne informacije v zvezi s koronavirusom za zaposlene UM<p>Datum objave: 20. 11. 2020<p>Vpra\u0161anja v zvezi s koronavirusom SARS-CoV-2 za zaposlene<p>Ali je no\u0161enje maske na UM obvezno?<p>Obvezna je uporaba za\u0161\u010ditne maske ali druge oblike za\u0161\u010dite ustnega in nosnega predela obraza v zaprtem javnem prostoru. Obvezno je tudi razku\u017eevanje rok.<p>OBRAZLO\u017dITEV:<p>Obveza no\u0161enja za\u0161\u010ditnih mask je dolo\u010dena Odlok o za\u010dasnih ukrepih za zmanj\u0161anje tveganja oku\u017ebe in \u0161irjenja oku\u017ebe z virusom SARS-CoV-2 (Uradni list RS, \u0161t. 124/20, 135/20 in 143/20). [...]",
    "text_without_Q": "Pomembne informacije v zvezi s koronavirusom za zaposlene UM<p>Datum objave: 20. 11. 2020<p>Vpra\u0161anja v zvezi s koronavirusom SARS-CoV-2 za zaposlene<p><p>Obvezna je uporaba za\u0161\u010ditne maske ali druge oblike za\u0161\u010dite ustnega in nosnega predela obraza v zaprtem javnem prostoru. Obvezno je tudi razku\u017eevanje rok.<p>OBRAZLO\u017dITEV:<p>Obveza no\u0161enja za\u0161\u010ditnih mask je dolo\u010dena Odlok o za\u010dasnih ukrepih za zmanj\u0161anje tveganja oku\u017ebe in \u0161irjenja oku\u017ebe z virusom SARS-CoV-2 (Uradni list RS, \u0161t. 124/20, 135/20 in 143/20).[...]",
    "multi_questions_doc": NaN
  },
```

## Contributing to the benchmark

See entries in the `systems` directory as examples of how the submission should be structured.

To contribute to the benchmark, submit an entry in a form of a directory to the `systems` directory (see existing examples there). Your directory should consist of:
- a README file which provides some details on the code and the embeddings that were used, 
- a submission file in a JSON format.

The submission JSON file should be structured like this:
```python
{
  "eval_scenario": "aqa-sl", 
  "system": "bge-m3", #provide a name for your system, ideally, it should be the same as the name of your submission folder
  "time_per_question": 3.619775378704071, # provide also time required for the system to provide an answer (in seconds, per question)
  "df": [ # the dataframe with the results - it should be based on the benchmark dataframe, with the following column added: "sources": list of retrieved sources
    {
      "query": "Ali se lahko strokovni naslovi tvorijo po \u0161tudijskih smereh/usmeritvah?",
      "answer": "Zakon o strokovnih in znanstvenih naslovih (ZSZN-1) dolo\u010da, da se lahko strokovni naslov tvori tudi po smereh/usmeritvah.",
      "document": "CLASSLA-web.sl.3086",
      "text": "FAQ<p>[...]",
      "text_without_Q": "FAQ<p>[...]",
      "multi_questions_doc": null,
      "sources": [
        "CLASSLA-web.sl.3086",
        "CLASSLA-web.sl.3086",
        "CLASSLA-web.sl.3086",
        "CLASSLA-web.sl.3086",
        "CLASSLA-web.sl.2764242"
      ]
    },
	[...]
  ]
}
```

## Evaluation

The submissions are evaluated with the `evaluate.py` script. The script evaluates solely the indexing and retrieval components of the pipeline by providing the retrieval accuracy (percentage of queries for which the correct text source was retrieved).

The submissions are evaluated using the following code with the following arguments: - relative path to the submission directory (e.g., `systems/embedding-models-evaluation`)
- number of top retrieved sources to be evaluated (e.g., "1")

```python
python evaluate.py "systems/embedding-models-evaluation" "2"
```