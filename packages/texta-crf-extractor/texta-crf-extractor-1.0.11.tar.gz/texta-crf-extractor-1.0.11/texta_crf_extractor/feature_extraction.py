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

DEFAULT_EXTRACTORS = [EXTRACTOR_ISUPPER, EXTRACTOR_ISTITLE, EXTRACTOR_HASDIGIT]
DEFAULT_LAYERS = [FEATURE_LAYER_WORD, FEATURE_LAYER_LEMMA, FEATURE_LAYER_POS]


def has_digit(string: str):
    """
    Checks whether string contrains any numbers.
    """
    return any(chr.isdigit() for chr in string)


def extract_features(item: dict, layers_to_use: List[str], extractors_to_use: List[str], word_index: int, suffix_len: Tuple[int], embedding):
    """
    Extract features from token and surrounding tokens based on window size.
    """
    features = []
    # select features from selected layers
    for layer in layers_to_use:
        if layer not in item:
            raise exceptions.InvalidInputError(f"Layer {layer} not present in document!")
        value = item[layer].lower()
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


def word2features(sent: list, i: int, config, embedding):
    # empty list for all features
    features = []
    # add bias
    if config.bias:
        features.append("bias")
    # this is the current token
    item = {}
    if FEATURE_LAYER_WORD in config.feature_layers:
        item[FEATURE_LAYER_WORD] = sent[i][0]
    if FEATURE_LAYER_LEMMA in config.feature_layers:
        item[FEATURE_LAYER_LEMMA] = sent[i][1]
    if FEATURE_LAYER_POS in config.feature_layers:
        item[FEATURE_LAYER_POS] = sent[i][2]

    features.extend(extract_features(item, config.feature_layers, config.feature_extractors, "0", config.suffix_len, embedding))
    # check if not the first token in sentence
    if i > 0:
        for window in range(1, config.window_size+1):
            try:
                item1 = {}
                if FEATURE_LAYER_WORD in config.context_feature_layers:
                    item1[FEATURE_LAYER_WORD] = sent[i-window][0]
                if FEATURE_LAYER_LEMMA in config.context_feature_layers:
                    item1[FEATURE_LAYER_LEMMA] = sent[i-window][1]
                if FEATURE_LAYER_POS in config.context_feature_layers:
                    item1[FEATURE_LAYER_POS] = sent[i-window][2]
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
                if FEATURE_LAYER_WORD in config.context_feature_layers:
                    item1[FEATURE_LAYER_WORD] = sent[i+window][0]
                if FEATURE_LAYER_LEMMA in config.context_feature_layers:
                    item1[FEATURE_LAYER_LEMMA] = sent[i+window][1]
                if FEATURE_LAYER_POS in config.context_feature_layers:
                    item1[FEATURE_LAYER_POS] = sent[i+window][2]
                features.extend(extract_features(item1, config.context_feature_layers, config.context_feature_extractors, f"+{window}", config.suffix_len, embedding))
            except IndexError:
                pass
    else:
        # end of sentence
        features.append("EOS")
    return features


def sent2features(sent: list, config, embedding):
    return [word2features(sent, i, config, embedding) for i in range(len(sent))]

def sent2labels(sent: list):
    return [label for token, lemma, postag, label in sent]
