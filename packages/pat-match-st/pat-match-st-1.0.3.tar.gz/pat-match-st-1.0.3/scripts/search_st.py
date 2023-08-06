import argparse

from scripts import utils


class Node:
    def __init__(self, label="", label_index=0):
        self.label = label
        self.label_index = label_index
        self.children = {}


class SuffixTree:
    def __init__(self, s):
        s += '$'
        self.root = Node()
        self.root.children[s[0]] = Node(s)

        for i in range(1, len(s)):
            curr_node = self.root
            j = i

            while j < len(s):
                if s[j] in curr_node.children:
                    child = curr_node.children[s[j]]
                    label = child.label
                    k = j + 1

                    while k - j < len(label) and s[k] == label[k - j]:
                        k = k + 1

                    if k - j == len(label):
                        curr_node = child
                        j = k
                    else:
                        existing_suffix = label[k - j]
                        new_suffix = s[k]
                        split = Node(label[:k - j], child.label_index)
                        split.children[new_suffix] = Node(s[k:], i + 1)
                        split.children[existing_suffix] = child
                        child.label = label[k - j:]
                        curr_node.children[s[j]] = split
                else:
                    curr_node.children[s[j]] = Node(s[j:], i + 1)

    def find(self, pattern):
        curr_node = self.root
        i = 0

        while i < len(pattern):
            curr_c = pattern[i]

            if curr_c not in curr_node.children:
                return None, None

            child = curr_node.children[pattern[i]]
            label = child.label
            j = i + 1

            while j - i < len(label) and j < len(pattern) and pattern[j] == label[j - i]:
                j += 1

            if j - i == len(label):
                curr_node = child
                i = j
            elif j == len(pattern):
                return child, j - i
            else:
                return None, None

        return curr_node, None

    def find_matches(self, node, matched_indices_set):
        matched_indices_set.add(node.label_index)

        values = node.children.values()
        for val in values:
            self.find_matches(val, matched_indices_set)


def run(fasta_file, fastq_file):
    fasta_seqs = utils.get_seq_from_file(fasta_file, "fasta")
    fastq_seqs = utils.get_seq_from_file(fastq_file, "fastq")

    for fasta_seq in fasta_seqs:
        tree = SuffixTree(fasta_seq.seq)

        for fastq_seq in fastq_seqs:
            node, idx = tree.find(fastq_seq.seq)

            if node is not None:
                matched_indices = set()
                tree.find_matches(node, matched_indices)
                utils.output_sam(matched_indices, fasta_seq, fastq_seq)


def main():
    parser = argparse.ArgumentParser(description="Matches a pattern using the naive suffix-tree implementation")
    required_parser = parser.add_argument_group('required arguments')
    required_parser.add_argument("-fa", "-fasta-file", dest="fasta_file", help="fasta file", required=True)
    required_parser.add_argument("-fq", "-fastq-file", dest="fastq_file", help="fastq file", required=True)
    args = parser.parse_args()

    run(args.fasta_file, args.fastq_file)


if __name__ == "__main__":
    main()
