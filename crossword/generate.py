import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):  # constructor and parameter for crossword
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword  # assigns the crossword to the variable
        self.domains = {  # sets up a dictionary with keys as spots and values as words to fill them
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        # calls the function for enforcement
        self.enforce_node_consistency()  
        # calls the arc function
        self.ac3()   
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # calls that dictionary setup in the creator
        for var in self.domains:
            for word in set(self.domains[var]):
                # checks that the length of hte word is the same as the variable length
                if len(word) != var.length:  
                    # if it is not the same it is removed
                    self.domains[var].remove(word)  


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #initialize revised variable
        revised = False  
        # using the crossowrd module to check if words (x and y) overlap
        overlap = self.crossword.overlaps[x,y]  
        # if they don't then arc consistency maintained
        if overlap is None: 
            return False
        
        # iterating over the words in the dictionary
        for x_word in set(self.domains[x]): 
            # any function to look for conditions
            if not any(  
                # check for overlap
                y_word[overlap[1]] == x_word[overlap[0]]  
                for y_word in self.domains[y]
            ):
                # if the words do not overlap then they are removed 
                self.domains[x].remove(x_word) 
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # will start with None and then start processign them with the following list for x with all neighbors y
        if arcs is None:  
            arcs = [(x,y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]

        # processing the arcs
        while arcs: 
            # takes first arc and unpacks the variables
            x, y = arcs.pop(0) 
            # calls the revise method. It it returns False then the problem cannot be solved with arc consistency 
            if self.revise(x, y): 
                if not self.domains[x]:
                    return False
                # if true then the x values are added without the 'y' values as this can affect other neigbours
                for neighbor in (self.crossword.neighbors(x) - {y}):  
                    arcs.append((neighbor, x))
        return True
                                                          
                                                        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
         # checks assignment dictionary for keys if var has been assigned or not
        return all(var in assignment for var in self.crossword.variables) 


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # creates a set to remove duplicates and store unique values
        unique_words = set(assignment.values())  
        # if this new length is greater than old length then there are duplicate words
        if len(unique_words) < len((assignment)):  
            return False

        #iterating over the assignment dictionary
        for var, value in assignment.items():  
            # if the length of the assigned word (vale) is not the length of the space (var) return false
            if var.length != len(value):  
                return False
            # get neighoring values using crossword neighbors method
            neighbors = self.crossword.neighbors(var) 
            for neighbor in neighbors:
                # get  overlaps with overlaps method
                overlap = self.crossword.overlaps[var, neighbor]  
                # check if characters match neighbors for position
                if neighbor in assignment and value[overlap[0]] != assignment[neighbor][overlap[1]]: 
                    return False
        return True  # consistent if any of the above conditions not met

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # helper function to calculate the number of ruled out values
        def count_eliminated_values(value):  
            # used to store the ruled-out values
            count = 0  
            # iterates over neighbors using crossword method
            for neighbor in self.crossword.neighbors(var): 
                # checks if in the dictionary with value
                if neighbor not in assignment:  
                    count += sum(
                        1 for neighbor_value in self.domains[neighbor]
                        # if the character does not match then count increases
                        if neighbor_value[self.crossword.overlaps[var, neighbor][1]] != value[self.crossword.overlaps[var, neighbor][0]] 
                    )
            # returns value count
            return count  # returns value count

        # returns sorted list based on the eliminated values in the domain of var
        return sorted(self.domains[var], key=count_eliminated_values) 

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # creates unassigned variable . takes parameter assignment and using the crossword method for variables
        unassigned = [v for v in self.crossword.variables if v not in assignment] 

        #returns variable from unassigned with the smallest domain, or highest degree, or any of hte tied variables
        return min(unassigned, key= lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # calls self_assignment to check if complete
        if self.assignment_complete(assignment):  
            return assignment

        # calls unassigned variable from the crossword
        var = self.select_unassigned_variable(assignment)

        
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value 

            if self.consistent(new_assignment):
                # inferences = self.inference(var, value)
                if self.ac3([(var, neighbor) for neighbor in self.crossword.neighbors(var) if neighbor not in new_assignment]):
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
