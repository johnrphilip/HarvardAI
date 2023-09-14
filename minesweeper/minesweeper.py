import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    
    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
            based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
            if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
            if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell) # add to moves made (1)
        self.mark_safe(cell)  # mark as safe (2)...the easy bit

        unknown_cells = []  # list for unknown cell coordinates
        countMines = 0   # integer to count the mines 

        for i in range(cell[0] - 1, cell[0] + 2):  # similar looping as nearby mines
            for j in range(cell[1] - 1, cell[1] + 2):
                # this line checks if on the game board (height, width) and not itself
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) != cell:
                    if (i, j) in self.mines: # if already known to be a mine add to mine
                        countMines += 1
                    elif (i, j) not in self.safes:  # otherwise add to the maybe
                        unknown_cells.append((i, j))

        # this will make the new knowledge sentence based on subtracting known mines from total mines
        newKnowledgeSentence = Sentence(unknown_cells, count - countMines)
        self.knowledge.append(newKnowledgeSentence)

        # had lots of loop problems before using sets here to store the marked knowledge
        mine_cells_to_mark = set()
        safe_cells_to_mark = set()

        # looping over each sentence and updating safes and mines. calls known_mine/safes methods
        for sentence in self.knowledge:
            mine_cells_to_mark.update(sentence.known_mines())
            safe_cells_to_mark.update(sentence.known_safes())

        # these mark on the identified mines and safes. again these were used to prevent loops
        for mine_cell in mine_cells_to_mark:
            self.mark_mine(mine_cell)

        for safe_cell in safe_cells_to_mark:
            self.mark_safe(safe_cell)

        new_inferences = [] # this stores the inference/implication
        for sentence1 in self.knowledge: # this will compare all the sentences against one another
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells): # not comparing the same sentence. seeing if subset as well
                    new_cells = sentence2.cells - sentence1.cells  # this makes the new cell inference
                    new_count = sentence2.count - sentence1.count # change the minecount
                    new_sentence = Sentence(new_cells, new_count) # making new knowledge
                    if new_sentence not in self.knowledge and new_sentence not in new_inferences:
                        new_inferences.append(new_sentence)
        self.knowledge.extend(new_inferences)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        valid_moves = [
        (i, j) for i in range(self.height)
        for j in range(self.width)
        if (i, j) not in self.moves_made and (i, j) not in self.mines
    ]
    
        return random.choice(valid_moves) if valid_moves else None
