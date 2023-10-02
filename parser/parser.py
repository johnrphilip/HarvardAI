import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Sentence 10 took a while!!! Needed some rules to handle all the adjectives
NONTERMINALS = """
S -> NP VP | S Conj S
NP -> Det N | N | NP PP | NP Conj NP | Det AdjP N | NP RelClause
AdjP -> Adj | Adj AdjP
VP -> V | Adv V | V NP | VP PP | VP Conj VP | V NP PP | VP AdvP | VP RelClause
PP -> P NP | P NP PP
AdvP -> Adv | AdvP Conj AdvP
RelClause -> P S | P NP VP | NP VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence.lower()) # tokenize and convert to lower-case
    return [word for word in words if word.isalpha()] # filter out non-alphabetic characters


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            if not any(sub.label() == 'NP' for sub in subtree.subtrees(lambda t: t != subtree)):
                np_chunks.append(subtree)
    return np_chunks


if __name__ == "__main__":
    main()



    """
    1. Holmes sat.  (NP VP)

    2. Holmes lit a pipe. (NP VP)->Holmes(N)  VP(a(Det) pipe(N))
    3. We arrived the day before Thursday. (NP, VP(V, NP(Det, N, PP(P, NP)))
    4. Holmes sat in the red armchair and he chuckled. (NP VP(VP(V PP(P NP(Det Adj N))) Con VP(Det N V)))
    5. My companion smiled an enigmatical smile. (NP(Det N) VP(V NP(Det Adj N)))
    6. Holmes chuckled to himself. (NP(N) VP(V PP(P NP(N))))
    7. She never said a word until we were at the door here. (NP(N) VP(Adv V NP(Det N) Conj S(NP VP(V PP(P NP(Det N))))) )
    8. Holmes sat down and lit his pipe. (NP(N) VP(VP(V Adv) Conj VP(V NP(Det N))))
    9. I had a country walk on Thursday and came home in a dreadful mess. (NP(N) VP(VP(V NP(Det N) PP(P NP)) Conj VP(V NP(N) PP(P NP(Det Adj N)))))
    10. I had a little moist red paint in the palm of my hand.  (NP(N) VP(V NP(Det Adj Adj Adj N) PP(P NP(Det N PP(P NP(Det N))))))

    * 7 & 10 were the hardest and needed rules to handle adverbs relative clauses, and nested prepositions

    python3 parser.py /Users/jp/Documents/EdX/parser/sentences/1.txt &


    """