# Text Embeddings CLI

This repository contains a simple command line interface (CLI) tool for creating and searching text embeddings. The motivation behind the tool is to provide a UNIX-like utility for contextual search: a program that does one thing and does it well.

The tool uses a local model for generating embeddings, contrary to querying models hosted on platforms like OpenAI. This design decision has two significant advantages:

1. **Cost-efficiency**: There's no need to pay for each query.
2. **Data privacy**: All your data stays on your local machine, so you have full control.

Please note that upon the first run of the application, it will download the `gtr-t5-large` model from the Hugging Face Model Hub to your local machine, which will take up approximately 670 MB of storage. This is a one-time operation, but it is worth considering the storage implications.

The `gtr-t5-large` model is a 768-dimensional vector space model specifically designed for contextual search. In benchmarks, it has proven itself to be close in performance to the commercial `text-embedding-ada-002` model.

## Usage

### Creating Embeddings

To create an embeddings file from all text files in a directory, use the `create` command:

```bash
python instant-contextual-search.py create dir_path output_file [--ext .txt,.csv,.docx]
```

This will walk through all text files in `dir_path`, calculate their embeddings, and save them to `output_file` in pickle format. You can optionally specify one or more file extensions to filter the files using the `--ext` argument.

### Searching Embeddings

To search the embeddings file for texts similar to a given input text, use the `find` command:

```bash
python instant-contextual-search.py find embed_file text [-t threshold] [-s]
```

This will calculate the embedding for `text` and find all texts in `embed_file` with a cosine similarity greater than `threshold` (default 0.7). The `-s` flag indicates that the text should be printed along with the path.

## Development Plans

The tool currently treats each file as a single text when creating embeddings. In the future, we plan to add support for breaking down files into chunks of text. This would enable more precise search through large files, as each chunk would have its own embedding.

## Contributions

Feel free to fork this repository and submit pull requests for any enhancements or bug fixes. Suggestions and feedback are always welcome!
