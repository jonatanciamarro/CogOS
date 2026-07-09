class EmergentProtocol:
    """
    EmergentProtocol translates long concept URIs to compressed symbol tokens.
    """
    def __init__(self):
        self.uri_to_symbol = {}
        self.symbol_to_uri = {}
        self.counter = 0

    def translate_to_symbol(self, concept_uri):
        """
        Translates a URI into a symbol, generating a new token if unmapped.
        """
        if concept_uri not in self.uri_to_symbol:
            self.counter += 1
            symbol = f"SYM_{self.counter:03d}"
            self.uri_to_symbol[concept_uri] = symbol
            self.symbol_to_uri[symbol] = concept_uri
        return self.uri_to_symbol[concept_uri]

    def translate_to_uri(self, symbol):
        """
        Resolves a symbol back to its full conceptual URI.
        """
        return self.symbol_to_uri.get(symbol, symbol)
