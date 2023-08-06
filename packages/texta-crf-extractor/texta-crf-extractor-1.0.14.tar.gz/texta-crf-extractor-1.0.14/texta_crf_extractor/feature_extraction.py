from typing import List, Tuple
from . import exceptions

# define token extractor names & defaults
EXTRACTOR_ISUPPER = "isupper"
EXTRACTOR_ISTITLE = "istitle"
EXTRACTOR_HASDIGIT = "hasdigit"

# define feature layers & defaults
FEATURE_LAYER_WORD = "text"
FEATURE_LAYER_LEMMA = "lemmas"
FEATURE_LAYER_POS = "pos_tags"
FEATURE_LAYER_GRAMMAR = "word_features"

DEFAULT_EXTRACTORS = [EXTRACTOR_ISUPPER, EXTRACTOR_ISTITLE, EXTRACTOR_HASDIGIT]
DEFAULT_LAYERS = [FEATURE_LAYER_WORD, FEATURE_LAYER_LEMMA, FEATURE_LAYER_POS, FEATURE_LAYER_GRAMMAR]


def has_digit(string: str):
    """
    Checks whether string contrains any numbers.
    """
    return any(chr.isdigit() for chr in string)


def check_blacklist(string: str):
    """
    Checks whether token should be used as a feature.
    Returns boolean.
    """

    # TODO: Implement

    return False



def extract_features(item: dict, layers_to_use: List[str], extractors_to_use: List[str], word_index: int, suffix_len: Tuple[int], embedding):
    """
    Extract features from token and surrounding tokens based on window size.
    """
    features = []
    # select features from selected layers
    for layer in layers_to_use:
        if layer not in item:
            raise exceptions.InvalidInputError(f"Layer {layer} not present in document!")
        # extract values from Grammar layer
        if layer == FEATURE_LAYER_GRAMMAR:
            for grammar_feature in item[layer].split("|"):
                feat_list = grammar_feature.split("=")
                # check if list contains key & val(otherwise it's useless)
                if len(feat_list) == 2:
                    features.append(f"{word_index}:{layer}:{feat_list[0]}={feat_list[1]}")
        # extract values from other (flat) layers
        else:
            value = item[layer].lower()
            if not check_blacklist(value):
                features.append(f"{word_index}:{layer}={value}")

        # add some suffixes from token
        if layer == FEATURE_LAYER_WORD:
            for i in range(suffix_len[0], suffix_len[1]+1):
                features.append(f"{word_index}:{layer}.suffix={value[-i:]}")

    if FEATURE_LAYER_WORD in item:
        # extract more features from token
        token = item[FEATURE_LAYER_WORD]
        for extractor in extractors_to_use:
            if extractor == EXTRACTOR_ISUPPER:
                feature_value = token.isupper()
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            elif extractor == EXTRACTOR_ISTITLE:
                feature_value = token.istitle()
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            elif extractor == EXTRACTOR_HASDIGIT:
                feature_value = has_digit(token)
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            # add more token-based extractors here!

    # get similar lemmas from embedding
    if embedding and FEATURE_LAYER_LEMMA in item:
        most_similar_lemmas = embedding.get_similar([item[FEATURE_LAYER_LEMMA]], n=1)
        if len(most_similar_lemmas):
            most_similar_lemma = most_similar_lemmas[0]["phrase"]
            features.append(f"{word_index}:{FEATURE_LAYER_LEMMA}.embedding={most_similar_lemma}")
        else:
            features.append(f"{word_index}:{FEATURE_LAYER_LEMMA}.embedding=NA")
    # replace newlines as it breaks taggerinfo()
    features = [f.replace("\n", "") for f in features]
    return features


def word2features(sent: List[tuple], i: int, config, embedding):
    """
    Transforms token with it's layers into features.
    I denotes the token ID in the list of tokens.
    """
    # empty list for all features
    features = []
    # add bias
    if config.bias:
        features.append("bias")
    # this is the current token
    item = {}
    for layer_name in config.feature_layers:
        item[layer_name] = sent[i][0][layer_name]
    features.extend(extract_features(item, config.feature_layers, config.feature_extractors, "0", config.suffix_len, embedding))
    # check if not the first token in sentence
    if i > 0:
        for window in range(1, config.window_size+1):
            try:
                item1 = {}
                for layer_name in config.context_feature_layers:
                    item1[layer_name] = sent[i-window][0][layer_name]
                features.extend(extract_features(item1, config.context_feature_layers, config.context_feature_extractors, f"-{window}", config.suffix_len, embedding))
            except IndexError:
                pass
    else:
        # beginning of sentence
        features.append("BOS")
    # check if not the last token in sentence
    if i < len(sent)-1:
        for window in range(1, config.window_size+1):
            try:
                item1 = {}
                for layer_name in config.context_feature_layers:
                    item1[layer_name] = sent[i+window][0][layer_name]
                features.extend(extract_features(item1, config.context_feature_layers, config.context_feature_extractors, f"+{window}", config.suffix_len, embedding))
            except IndexError:
                pass
    else:
        # end of sentence
        features.append("EOS")
    return features


def sent2features(sent: List[tuple], config, embedding):
    # featurize everything except labels
    return [word2features(sent, i, config, embedding) for i in range(len(sent))]

def sent2labels(sent: List[tuple]):
    # retrieve labels from tuple
    return [item[1] for item in sent]
