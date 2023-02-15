import json
import argparse
from itertools import chain


def main():
    args = get_args()
    filter_jsonlines_file(
        args.infile, args.output, {w.strip() for w in args.include_words.split(",")}
    )


def filter_jsonlines_file(infile, outfile, include_words):
    docs = []
    for doc in get_docs(infile):
        filter_doc(doc, include_words)
        docs.append(doc)
    write_jsonlines(outfile, docs)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", metavar="input file", help="input file")
    parser.add_argument(
        "-o", "--output", metavar="PATH", help="output file", required=True
    )
    parser.add_argument(
        "--include",
        dest="include_words",
        metavar="WORD",
        required=True,
        help="chains with mentions that contains that words will be included, other will be excluded. "
        "Comma separated list of words",
    )
    return parser.parse_args()


def get_docs(path):
    with open(path) as fh:
        for line in fh.readlines():
            yield json.loads(line)


def write_jsonlines(path, docs):
    with open(path, "w") as fh:
        for doc in docs:
            fh.write(json.dumps(doc) + "\n")


def filter_doc(doc, include_words):
    words = list(chain(*doc["sentences"]))
    new_clusters = []
    for cluster in doc["clusters"]:
        found = False
        for start, end in cluster:
            for i in range(start, end + 1):
                if words[i] in include_words:
                    new_clusters.append(cluster)
                    found = True
                    break
            if found:
                break
    doc["clusters"] = new_clusters


if __name__ == "__main__":
    main()
