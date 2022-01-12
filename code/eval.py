from regexDFAEquals import regex_equiv, regex_equiv_from_raw

def dfa_eq_eval(data_path, gold, output):
    acc = 0
    total = 0
    with open(data_path+gold, 'r') as f_gold, open(data_path+output, 'r') as f_pred:
        for gold, pred in zip(f_gold.readlines(), f_pred.readlines()):
            if regex_equiv_from_raw(gold.strip(), pred.strip()):
                acc += 1
            total += 1
    print('DFA-equivalence-acc:', acc/total)


# TODO: output inaccurate parts

if __name__ == '__main__':
    dfa_eq_eval('output-test-sampling-bt/', 'test_0.gold', 'test_0.output')
