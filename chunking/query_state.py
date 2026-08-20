class QueryState:

    def __init__(self):
        self.partial_query = ""
        self.predictions = []
        self.speculative_results = {}
        self.final_query = None

    def update(self, text):
        self.partial_query = text

def predict_queries(partial_query):

    partial = partial_query.lower()

    if "collapse of the" in partial:
        return [
            partial + " Roman Empire",
            partial + " Soviet Union",
            partial + " Ottoman Empire"
        ]

    return [partial]