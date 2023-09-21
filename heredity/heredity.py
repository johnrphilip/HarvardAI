import csv
import itertools
import sys

# dictionary holding probabilitis
PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # 
    if len(sys.argv) != 2:  # two arguments are needed to execute the code, probably needing the csv along with the python code
        sys.exit("Usage: python heredity.py data.csv")\
    # this is taking the second argument of people from the csv and putting it into this variable. It has basic info from csv
    people = load_data(sys.argv[1])  

    # Keep track of gene and trait probabilities for each person through the iterations. Looks like they are set to zero for now
    probabilities = {
        person: {  # only names input into the dictionary. Mother/father/trait used in join probability
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait. The next twenty lines make the different trait sets
    # this is the loop where all the action & iterations are happening
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene. This creates the one_gene set
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):  # this is the rest of the people who have two genes because zero was already taken out

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)  #this calculates the joint as "p"
                update(probabilities, one_gene, two_genes, have_trait, p) # this updates all the values

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


# this whole bloody thing is just to make 'p'
def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    joint_prob = 1  # Initialize joint probability to 1 because of multiplication (instead of 0)

    # looping the dictionary
    for person, data in people.items():
        # Gives values for the Number of genes
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0

        # checks trait status
        trait = person in have_trait

        # set person probability t
        prob = 0

        # for those with two parents
        if data['mother'] and data['father']:
            mother = data['mother']
            father = data['father']

            # createes dictionary to store the probability 
            passing_prob = {name: (
                # PROBS values are all taken from the given code above
                1 - PROBS["mutation"] if name in two_genes else (  # prob if two genes is 1 - prob
                    0.5 if name in one_gene else PROBS["mutation"] # if one gene it is .5 else it is mutation rate
                )
            ) for name in [mother, father]}

            # Calculate probabilities based on the number of genes and parents passing them on
            if genes == 2:
                prob = passing_prob[mother] * passing_prob[father] # multiplication of probs
            elif genes == 1:
                prob = passing_prob[mother] * (1 - passing_prob[father]) + (1 - passing_prob[mother]) * passing_prob[father]
            else:
                prob = (1 - passing_prob[mother]) * (1 - passing_prob[father])

        # If no parents
        else:
            prob = PROBS["gene"][genes]  # taken straight from the table

        # Multiply by the conditional probability of trait
        prob *= PROBS["trait"][genes][trait]

        # Multiply this person's probability to the joint probability
        joint_prob *= prob

    return joint_prob


# five parameters!! This one has the new joint probability trait calculated in the earilier function
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # this one is more straightforward than the joint function. just updates the dicitonary with the genes depending on where th eprson i s located
    # this gets called in the main after joint probability
    for person in probabilities:
        # this looks at sets made during the main and updates them. It creates new keys with values to be added from joint 
        genes = 2 if person in two_genes else 1 if person in one_gene else 0  
        trait = person in have_trait  # sets the trait key value for the person

        probabilities[person]['gene'][genes] += p  # updates the p value for the genes
        probabilities[person]['trait'][trait] += p  # updates with p value fro the trait


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # normalizes the probabilities so they can add to 1
    for person in probabilities:  # loops through each person
        for field in ['gene', 'trait']:  # loops through each subfield
            total = sum(probabilities[person][field].values()) # calculates the sum of the values
            # take each value and divide by total value to get values adding up to 1. iF they were already normal then it would be the same
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total  


if __name__ == "__main__":
    main()
    """
    "data/family0.csv"
    "data/family1.csv"
    "data/family2.csv"
    """