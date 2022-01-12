from .regex_transform import RegexTransformBeta, compare_streg
from .text_transform import TextTransformBeta
import random


def parallel_augmentation(src, targ, mode: list = None):
    """
    augment parallel data, mainly content replacement

    NOTE: If this doesn't work for one time, try again ;)
    
    Limitations: 
    (1) cannot rephrase nl;
    (2) only deal with contents;

    Usage:
    (1) random augmentation during training
    (2) directly add to training dataset

    Implemented functionalities:
    (1) number change

    """
    def __number_aug(src, targ):
        debug = False
        def __isnumeric(token: str) -> bool:
            return token in '1234567890' or token in ['one','two','three','four','five','six','seven','eight','nine','zero']
        def __int(token: str) -> int:
            if token.isnumeric():
                return int(token)
            else:
                return {'one':1,'two':2,'three':3,'four':4,'five':5,
                    'six':6,'seven':7,'eight':8,'nine':9,'zero':0}[token]
        def __str(n: int, thres=0.3) -> str:
            if random.random() > thres:
                return str(n)
            else:
                return {1:'one',2:'two',3:'three',4:'four',5:'five',
                    6:'six',7:'seven',8:'eight',9:'nine',0:'zero'}[n]
        # maintain partial order
        number_set_src = set([tok for tok in src.split(' ') if __isnumeric(tok)])
        number_set_targ = set([tok for tok in targ.split(' ') if __isnumeric(tok)])
        skip_first = False  # first summary sentence does not count
        if len(number_set_src) == 0 or len(number_set_targ) == 0:   # no-number inputs
            return src, targ
        if number_set_src != number_set_targ:   # FIXME: hard to handle non-trivial mappings, maybe only with NNs
            # print('src:', src.strip())
            # print('targ:', targ.strip())
            print('len src num:', len(number_set_src), ', len targ num:', len(number_set_targ))
            if len(number_set_src) == len(number_set_targ) + 1:
                skip_first = True
                # print('src:', src.strip())
                # print('targ:', targ.strip())
                # print('***SKIP_FIRST***')
            # raise NotImplementedError
            return src, targ
        number_list = sorted(list(number_set_targ))
        number_map = {}
        number_map[number_list[0]] = max(__int(number_list[0]) + random.randint(-__int(number_list[0]) + 1, 2), 0)  # not less than 0
        for i, n in enumerate(number_list[1:]):
            n_val = __int(n)
            bound = number_map[number_list[i]]
            new_val = random.randint(bound, max(n_val, bound) + 2)
            number_map[n] = new_val
        
        # restrict max
        max_mapped_num = max(list(number_map.values()))
        if max_mapped_num >= 10:
            for key in number_map:
                number_map[key] -= (max_mapped_num - 9)

        if skip_first:  # FIXME: skip first
            src = ' '.join([__str(number_map[tok]) if tok in number_map else tok for tok in src.split(' ')])
        else:
            src = ' '.join([__str(number_map[tok]) if tok in number_map else tok for tok in src.split(' ')])
        targ = ' '.join([__str(number_map[tok], thres=0.0) if tok in number_map else tok for tok in targ.split(' ')])

    def __regex_aug(src, targ):
        """
        using `RegexTransformBeta` to augment target and then augment source accordingly
        """
        rxt = RegexTransformBeta()
        new_targ = rxt.random_transform(targ.replace(' ', ''))
        old_targ_tokens, new_targ_tokens, diff_locations = compare_streg(targ.split(' '), new_targ.split(' '))
        ttt = TextTransformBeta()
        new_src = ttt.transform_by_regex_changes(src, [old_targ_tokens, new_targ_tokens, diff_locations], verbose=True)
        return new_src, new_targ

    nsrc, ntarg = src, targ
    unchanged = 0
    if 'number' in mode:
        nsrc, ntarg = __number_aug(nsrc, ntarg)
    if 'regex2nl' in mode:
        nsrc, ntarg = __regex_aug(nsrc, ntarg)
    
    return nsrc, ntarg


if __name__ == '__main__':
    src = 'const0 list of 3 strings . first string consist 1 - 2 const0 . next string consist 3 - 4 capital that is optional . last string consist 1 - 2 const0 that is optional .'
    targ = 'concat ( repeatrange ( const0 , 1 , 2 ) , concat ( optional ( repeatrange ( <cap> , 3 , 4 ) ) , optional ( repeatrange ( const0 , 1 , 2 ) ) ) )'
    new_src, new_targ = parallel_augmentation(src, targ, ['number'])
    print('old src:', src)
    print('new src:', new_src)
    print('old targ:', targ)
    print('new targ:', new_targ)