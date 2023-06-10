import os
import argparse
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def create_embeddings(model, dir_path, output_file, ext):
    texts = []
    paths = []

    # If extensions are provided, split them into a list
    if ext is not None:
        ext = ext.split(",")

    # Walk through all files in the directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if ext is None or any(file.endswith(e) for e in ext):
                try:
                    # Open each file and read the text
                    with open(os.path.join(root, file), "r") as f:
                        texts.append(f.read())
                    paths.append(os.path.join(root, file))
                except Exception as e:
                    print(f"Error reading file {os.path.join(root, file)}: {e}")

    print("Calculating embeddings, it may take some time...")
    embeddings = model.encode(texts)

    # Create a structured array
    data = [
        {"path": p, "text": t, "embedding": e}
        for p, t, e in zip(paths, texts, embeddings)
    ]

    # Save the array to a file
    with open(output_file, "wb") as f:
        pickle.dump(data, f)
    print(f"Embeddings saved to {output_file}")


def find_nearest(model, embed_file, text, similarity_threshold, show_text):
    try:
        with open(embed_file, "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"Error loading file {embed_file}: {e}")
        return

    # Calculate the embedding for the input text
    text_embedding = model.encode([text])[0]

    # Calculate the cosine similarity between the input text embedding and all other embeddings
    similarities = cosine_similarity([text_embedding], [x["embedding"] for x in data])

    # Get the indices of the most similar texts
    nearest_indices = np.where(similarities[0] > similarity_threshold)[0]

    if nearest_indices.size == 0:
        print("No matching results found.")
    else:
        for idx in nearest_indices:
            if show_text:
                print(f"{data[idx]['path']}\n{data[idx]['text']}")
            else:
                print(data[idx]["path"])


def main():
    parser = argparse.ArgumentParser(description="Text embeddings CLI")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create text embeddings")
    create_parser.add_argument("dir_path", help="Path to directory of text files")
    create_parser.add_argument("output_file", help="Output pickle file for embeddings")
    create_parser.add_argument(
        "--ext", help="Comma-separated extension filter for files"
    )

    find_parser = subparsers.add_parser("find", help="Find nearest text")
    find_parser.add_argument("embed_file", help="Input pickle file with embeddings")
    find_parser.add_argument("text", help="Text to find nearest")
    find_parser.add_argument(
        "-t", "--threshold", type=float, default=0.7, help="Similarity threshold"
    )
    find_parser.add_argument(
        "-s", "--show-text", action="store_true", help="Show text in output"
    )

    args = parser.parse_args()

    if args.command is not None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("sentence-transformers/gtr-t5-large")

        if args.command == "create":
            create_embeddings(model, args.dir_path, args.output_file, args.ext)
        elif args.command == "find":
            find_nearest(
                model, args.embed_file, args.text, args.threshold, args.show_text
            )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
