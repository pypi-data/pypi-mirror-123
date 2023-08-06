from .feature_extraction import DEFAULT_EXTRACTORS, DEFAULT_LAYERS


class CRFConfig:

    def __init__(
        self,
        labels: list = ["GPE", "ORG", "PER", "LOC"],
        num_iter: int = 100,
        test_size: int = 0.3,
        verbose: bool = False,
        c1: float = 1.0,
        c2: float = 1.0,
        bias: bool = True,
        window_size: int = 2,
        suffix_len: tuple = (2,2),
        context_feature_layers: list = DEFAULT_LAYERS,
        context_feature_extractors: list = DEFAULT_EXTRACTORS,
        feature_layers: list = DEFAULT_LAYERS,
        feature_extractors: list = DEFAULT_EXTRACTORS
    ):
        self.labels = labels
        self.test_size = test_size
        self.verbose = verbose

        self.num_iter = num_iter
        self.c1 = c1
        self.c2 = c2

        self.feature_layers = feature_layers
        self.context_feature_layers = context_feature_layers
        self.feature_extractors = feature_extractors
        self.context_feature_extractors = context_feature_extractors
        self.bias = bias
        self.window_size = window_size
        self.suffix_len = suffix_len
