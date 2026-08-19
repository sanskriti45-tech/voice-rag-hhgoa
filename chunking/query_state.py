class QueryState:
    def __init__(self):
        self.partial_query = ""
        self.predictions = []
        self.speculative_results = {}
        self.final_query = None

    def update(self, text):
        self.partial_query = text

    def set_predictions(self, predictions):
        self.predictions = predictions

    def set_speculative_results(self, results):
        self.speculative_results = results

    def set_final_query(self, text):
        self.final_query = text