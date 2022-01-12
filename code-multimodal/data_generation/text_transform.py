from typing import *
import sys

NUMBER_MAP = {'one':1,'two':2,'three':3,'four':4,'five':5,
            'six':6,'seven':7,'eight':8,'nine':9,'zero':0}
RNUM_MAP = {x[1]:x[0] for x in NUMBER_MAP.items()}

def __is_numeric(string):
    return string.isnumeric() or string in NUMBER_MAP

def text_entity_normalize(text: List[str])-> Tuple[List[Union[str, int]], List[int]]:
    """
    * convert all string numbers to decimals
    * convert terminals to their name
    * also get all the locations of numbers and special tokens like `-`
    """
    entity_list = []
    location_list = []
    previous_low_or_cap = False
    for i, token in enumerate(text):
        add_location = True
        if token.isnumeric():
            entity_list.append(int(token))
        elif token in NUMBER_MAP:
            entity_list.append(NUMBER_MAP[token])
        elif token in ['-', 'to']:
            if __is_numeric(text[i-1]) and __is_numeric(text[i + 1]):
                entity_list.append(token)
            else:
                continue
        elif token.startswith('const'):
            entity_list.append(token)
        elif token in ['letter', 'letters']:
            if previous_low_or_cap:
                previous_low_or_cap = False
                continue
            else:
                entity_list.append('<let>')
        elif token == 'lowercase':
            entity_list.append('<low>')
            previous_low_or_cap = True
        elif token == 'capital':
            entity_list.append('<cap>')
            previous_low_or_cap = True
        elif token in ['digit', 'numeral']:
            entity_list.append('<num>')
        elif token == 'special':    # TODO: `special` is often followed by `characters` but it does not actually matters if we want to replace it
            entity_list.append('<spec>')
        else:
            add_location = False
        if add_location:
            location_list.append(i)
    if len(entity_list) != len(location_list):
        print(entity_list)
        print(location_list)
        print([text[i] for i in location_list])
    assert len(entity_list) == len(location_list)
    return entity_list, location_list


def entity_denormalize(val, previous_token):
    # assume val is `str`
    if val == '<let>':
        return 'letters'
    elif val == '<cap>':
        return 'capital'
    elif val == '<low>':
        return 'lowercase'
    elif val == '<num>':
        return 'digit'
    elif val == '<any>':
        return 'any'
    elif val == '<spec>':
        return 'special'
    elif val.isnumeric():
        if previous_token.isnumeric():
            return val
        else:
            return RNUM_MAP[int(val)]
    else:
        return val


def __regex_entity(token: str):
    "return None or entity"
    if token.isnumeric():
        return int(token)
    elif token in NUMBER_MAP:
        return NUMBER_MAP[token]
    elif token in ['<let>', '<cap>', '<low>', '<num>', '<any>', '<spec>']:
        return token
    elif token.startswith('const'):
        return token
    else:
        return None


def regex_entity_normalize(regex: List[str]) -> list:
    ret = []
    for tok in regex:
        ent = __regex_entity(tok)
        if ent:
            ret.append(ent)
    return ret

def remove_summary_first_sentence(text: List[str]) -> Tuple[str, str]:
    """
    - "A list of ..."
    - "there are ..."
    """
    hit = False
    state = 0
    for i, token in enumerate(text):
        if token == '.':
            if hit:
                return text[:i+1], text[i+1:]
            else:
                return [], text
        if token == 'list':
            hit = True
        if token.lower() == 'there' and state == 0:
            state = 1
        if token.lower() == 'are' and state == 1:
            hit = True
    return [], text


def change_tokens_accordingly(text_entities, locations, tokens, regex_changes) -> List[str]:
    """
    Assumption:
    1. entities in most of the training data are aligned (actually not very correct, many 1 to more situations)
    2. NL entities should be less than regex entities (if not replicated)

    Other considerations:
    1. 'constX' can appear multiple times, yet we are clear that they can be replaced together 
    2. '-' / 'to' is left for further analysis
    3. handle numbers and terminals separately (because order is not always the same if combined)
    3. one to all mapping (extension of 'constX' mapping)
        (I) latest map
    """

    # `constX` replacement, then remove from list
    const_map = {}
    for i, changed in enumerate(regex_changes[2]):
        if changed and regex_changes[0][i].startswith('const'):
            const_map[regex_changes[0][i]] = regex_changes[1][i]
    for i, ent in enumerate(text_entities):
        if type(ent) == str:
            if ent.startswith('const') and ent in const_map:    # it's ok not to be in map (unchanged)
                tokens[locations[i]] = entity_denormalize(const_map[ent], ent)

    # handle numbers
    index = 0
    latest_map = {}
    for tok_old, tok_new, changed in zip(regex_changes[0], regex_changes[1], regex_changes[2]):

        # avoid index error
        if index >= len(text_entities):
            break

        # skip non-numbers
        while index < len(text_entities) and type(text_entities[index]) != int:
            index += 1
        if index >= len(text_entities):
            break
        if not tok_old.isnumeric():
            continue

        
        if changed:
            if tok_old == str(text_entities[index]):  # aligned
                tokens[locations[index]] = entity_denormalize(tok_new, tok_old)  # TODO: further convertion, e.g. 1 -> '1'/'one'
                latest_map[tok_old] = tok_new
                index += 1
            else:
                # print(tok_old, text_entities[index])
                # raise IndexError("Entities not aligned.")
                try:
                    tokens[locations[index]] = entity_denormalize(latest_map[tok_old], tok_old)  # TODO: further convertion, e.g. 1 -> '1'/'one'
                except KeyError:
                    # raise IndexError("Empty Latest Map")
                    continue
        else:
            regex_entity = __regex_entity(tok_old)
            if not regex_entity:
                continue
            else:
                if tok_old == str(text_entities[index]):
                    index += 1
                else:
                    print(tok_old, text_entities[index])
                    # raise IndexError("Entities not aligned.")
                    index += 1


    # handle non-numbers
    index = 0
    latest_map = {}
    for tok_old, tok_new, changed in zip(regex_changes[0], regex_changes[1], regex_changes[2]):

        # avoid index error
        if index >= len(text_entities):
            break

        # skip 'constX', '-'/'to'
        while index < len(text_entities) - 1 and type(text_entities[index]) != str:
            index += 1
        if type(text_entities[index]) == int:
            break

        if text_entities[index].startswith('const'):
            index += 1
        elif text_entities[index] == '-' or text_entities[index] == 'to':
            index += 1
        if tok_old.startswith('const'):
            continue
        if tok_old.isnumeric():
            continue

        if changed:
            if tok_old == str(text_entities[index]):  # aligned
                tokens[locations[index]] = entity_denormalize(tok_new, tok_old)  # TODO: further convertion, e.g. 1 -> '1'/'one'
                latest_map[tok_old] = tok_new
                index += 1
            else:
                # print(tok_old, text_entities[index])
                # raise IndexError("Entities not aligned.")
                try:
                    tokens[locations[index]] = entity_denormalize(latest_map[tok_old], tok_old)  # TODO: further convertion, e.g. 1 -> '1'/'one'
                except KeyError:
                    # raise IndexError("Empty Latest Map Non-Number")
                    # index += 1
                    continue
                # raise IndexError("Entities not aligned.")
        else:
            regex_entity = __regex_entity(tok_old)
            if not regex_entity:
                continue
            else:
                if tok_old == str(text_entities[index]):
                    index += 1
                else:
                    # print(tok_old, text_entities[index])
                    index += 1
                    # raise IndexError("Entities not aligned.")
    return tokens


class TextTransformBeta(object):

    def __init__(self) -> None:
        pass

    def transform_by_regex_changes(self, text: str, regex_changes: Tuple[List[str], List[str], List[bool]], verbose=False):
        # remove summary sentence if exist
        summary_sentence, rest = remove_summary_first_sentence(text.split(' '))

        # entity normalize
        entity_list, locations = text_entity_normalize(rest)

        # change NL according to regex changes
        try:
            new_rest = change_tokens_accordingly(entity_list, locations, rest, regex_changes)
        except IndexError as IE:
            if verbose:
                print(IE)
                print(entity_list)
                print(regex_entity_normalize(regex_changes[0]))
                print(rest)
                print(regex_changes[0])
                print(regex_changes[1])
                print([regex_changes[1][i] for i, x in enumerate(regex_changes[2]) if x])
                print('*' * 20)
            # exit()
            return None

        # restore summary sentence
        return ' '.join(summary_sentence + new_rest)