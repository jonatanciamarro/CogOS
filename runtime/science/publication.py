class ScientificPaper:
    """
    ScientificPaper holds published claims, author details, and citation metrics.
    """
    def __init__(self, paper_id, title, author_id, claim_concept, replications=1):
        self.id = paper_id
        self.title = title
        self.author = author_id
        self.claim = claim_concept
        self.replications = replications
        self.citations = 0

    def increment_citations(self):
        self.citations += 1
        return self.citations
