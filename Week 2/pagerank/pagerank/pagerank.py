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
    result = dict().fromkeys(corpus.keys(), 0.0)
    if not corpus[page]:
        for key in corpus:
            result[key] = 1.0 / len(corpus)
            return result

    for key in corpus:
        result[key] += (1 - damping_factor) / len(corpus)

    for link in corpus[page]:
        result[link] += damping_factor / len(corpus[page])

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict().fromkeys(corpus.keys(), 0.0)
    for i in range(1, n ):
        if i == 1:
            random_page = random.choices(list(result.keys()))[0]
        else:
            random_page = random.choices(list(result.keys()), weights=list(result.values()), k=1)[0]
        sample_transition_model = transition_model(corpus, random_page, damping_factor)
        for page in result:
            result[page] = ((i - 1) * result[page] + sample_transition_model[page]) / i

    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dist = dict().fromkeys(corpus.keys(), 1.0 / len(corpus))
    while True:
        prev_dist = dist.copy()
        for page in corpus:
            page_sum = 0
            for p in corpus:
                if len(corpus[p]) == 0:
                    page_sum += dist[p] / len(corpus)
                elif page in corpus[p]:
                    page_sum += dist[p] / len(corpus[p])
            dist[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * page_sum)
        norm = sum(dist.values())
        dist = {page: (rank / norm) for page, rank in dist.items()}
        for page in corpus:
            if abs(prev_dist[page] - dist[page]) <= 0.001:
                return dist


if __name__ == "__main__":
    main()
