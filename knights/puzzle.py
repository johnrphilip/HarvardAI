from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledgeAll = And(
    Or(AKnight,AKnave),  # the first part says that they can be either
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),  # this part says they cannot be both AND
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave))
)
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # the statement is represented as And(AKnight, AKnave)
    knowledgeAll,
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledgeAll,
    # if true it would imply A is a knight(for telling truth) and B is a knave(because statement says so)
    # if false it would imply that A is a knave and B is not a knave
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # If A is true it implies that A is both knight and B is a knight. If false it implies that A is knave and b is knight. Aknight and B knight. Aknave
    # if B is true it implies that B is knight (for telling truth) and A is a knave. Or it implies that B is knave and A is knave
    knowledgeAll,
    Implication(AKnight, Or(And(AKnight,BKnight),And(AKnave,BKnave))),
    Implication(AKnave, Not(Or(And(AKnight,BKnight),And(AKnave,BKnave)))),
    Implication(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight))),
    Implication(BKnave, Not(Or(And(BKnight, AKnave), And(AKnight, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    knowledgeAll,
    # A's statement is ambiguous and makes me wonder if I need anything for it but.......
    #if a knight , either of the statements could be true
    Implication(AKnight,Or(AKnight, AKnave)),
    # If a knave, it would mean the opposite of above
    Implication(AKnave,Not(Or(AKnight,AKnave))),

    # I had a few really crazy versions of this down below but simplified them
    # I combined the two statements here and went with A's statement about B being a bunch of useless
    # fluff. So instead went with if B a knight then A is knight or knave and cknave. Then opposite
    # the bottom approach works as well if needed
    Implication(BKnight, And(Implication(AKnight, AKnave), CKnave)),
    Implication(BKnave, Or(Implication(AKnight, Not(AKnave)), Not(CKnave))),
    # C says....
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))

    # Crazy first attempt at B1/2
    # IF B is a knight then A is knight and A is knave OR A is a knave and A not Aknave)
    # If B is a knave then not the above
    # Implication(BKnight, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    #Implication(BKnave, Not(Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))))
    # 3 - If B is a knight then C Knave or if B is a Knave then not C Knave
    #Implication(BKnight, CKnave),
    #Implication(BKnave, Not(CKnave)),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
