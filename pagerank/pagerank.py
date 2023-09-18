import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # check number of pages in coprus and number of links on current page
    total_pages = len(corpus)
    outgoing_links = len(corpus[page])

    # dictionary to store the transition probabilities
    probabilities = {}

    if outgoing_links == 0:  # if there are no links and equal distribution across all links (fourth condition)
        for pg in corpus: #iterates over the keys in the corpus
            probabilities[pg] = 1/total_pages

    else:
        #base probability for all pages
        for pg in corpus:
            probabilities[pg] = (1-damping_factor) / total_pages # basic probability with damping factor (condition 2). This would be .15 divided by the number of pages

        for link in corpus[page]: # iteraties over the values in the corpous
            probabilities[link] += damping_factor / outgoing_links  #here it updates the dictionary for each link with a probability value. This would be .85 divided by the number of outgoing links

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # this will build off the transition model probabilities to send the surfer off to new pages for 'n' samples
    samples = {page: 0 for page in corpus} # creates dictionary to keep track of the new pages visited set to zero
    current_page = random.choice(list(corpus.keys())) # this takes a random choice from the corpus to make jump
    samples[current_page] += 1  # this moves through the pages

    for i in range (1,n):  # here n is the number of jumps the surfer will  make and will n-1 times
        #grab the probabilities from the transition  model
        probabilities = transition_model(corpus, current_page, damping_factor)

        #choose next page based on transition prob. next page is assigned from the 
        next_page = random.choices(  # random module with multiple choices and weighted selection
            population=list(probabilities.keys()), # grabs keys and converst them to a list from we can pick
            weights=list(probabilities.values()),  # grabs values and converts them to a list from which we can pick values
            k=1  # we are only making one choice
        )[0]  # since k is one we are only taking the first item from the list

        samples[next_page] += 1 # incrementing the count and making new prob jumps until n-1
        current_page = next_page # reassigns the current page to get ready for next loop

    # dictionary comprehension. This will update the dictionary filled during the next_page for loop
    # calculates the probabilities or counts for each page by dividing by n
    samples = {page: count/n for page, count in samples.items()}

    return samples

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_number = len(corpus)  # (getting number of pages in the corpus)
    threshold = .01  # I have seen different levels but this seemed reasonable

    # intialize all pageranks to equal
    pageranks = {page: 1 / page_number for page in corpus}

    # set converge to false for loop
    converged = False
    iterations = 0 # curious how mnay iterations
    while not converged:
        new_pageranks = {}  # dictionary to hold pageranks in this loop before updating outer pageranks

        # set off trying to converge the Markov chain
        for page in corpus:
            pr_value = (1 - damping_factor) / page_number  # this pr will be the new value for each key. similar to transition model calculation
            for i in corpus:  # here we iterate through every other key in the corpus to see if it matches the current key 'page'
                if page in corpus[i]:  # checking the values of each key for page if it is there we need to calculate the new probability
                    pr_value += damping_factor * pageranks[i] / len(corpus[i]) # this is the meaty math. denominator is dividing by number of outbound links. numerator is previously calculated pageranks divided by all times damping factor
                elif not corpus[i]: # no outbound links
                    pr_value += damping_factor * pageranks[i] / page_number  # taking the initialized prob and considering the damping factor
            new_pageranks[page] = pr_value

        # check for convergence. if converged the loop will stop. otherwise it will update the pageranks and try again. 
        diff = sum(abs(new_pageranks[page] - pageranks[page]) for page in corpus)
        if diff < threshold:
            converged = True

        pageranks = new_pageranks
        iterations += 1
    
    print(f"Converged after {iterations} iterations.")
    return pageranks
                    

if __name__ == "__main__":
    main()
