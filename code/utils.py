

visible_ascii = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
# print(visible_ascii)

class CharTokenizer:
    def __init__(self):
        self.c2i = {}
        self.i2c = {}

        self.cls_token = '<CLS>'
        self.cls_token_id = 0
        self.pad_token = '<PAD>'
        self.pad_token_id = 1
        self.sep_token = '<SEP>'
        self.sep_token_id = 2
        self.unk_token = '<UNK>'
        self.unk_token_id = 3

        for i, c in enumerate(['<CLS>', '<PAD>','<SEP>',  '<UNK>']):
            self.c2i[c] = i
            self.i2c[i] = c
        for i, c in enumerate(visible_ascii):
            i = i + 4
            self.c2i[c] = i
            self.i2c[i] = c
        
        self.vocab_size = len(visible_ascii) + 4

        
    def tokenize(self, seq):
        return [c for c in seq]

    def convert_tokens_to_ids(self, seq):
        return [self.c2i[c] for c in seq]

    def decode(self, seq, clean_up_tokenization_spaces=True):
        seq = [self.i2c[i] for i in seq]
        return ''.join(seq)


class CustomTokenizer:
    def __init__(self):
        self.c2i = {}
        self.i2c = {}

        self.cls_token = '<CLS>'
        self.cls_token_id = 0
        self.pad_token = '<PAD>'
        self.pad_token_id = 1
        self.sep_token = '<SEP>'
        self.sep_token_id = 2
        self.unk_token = '<UNK>'
        self.unk_token_id = 3

        for i, c in enumerate(['<CLS>', '<PAD>','<SEP>',  '<UNK>']):
            self.c2i[c] = i
            self.i2c[i] = c
        for i, c in enumerate(visible_ascii):
            i = i + 4
            self.c2i[c] = i
            self.i2c[i] = c
        
        self.vocab_size = len(visible_ascii) + 4

        for c in ['<VOW>', '<NUM>', '<LET>', '<CAP>', '<LOW>', 
            '<M0>', '<M1>', '<M2>', '<M3>', 'None']:
            self.c2i[c] = self.vocab_size
            self.i2c[self.vocab_size] = c
            self.vocab_size += 1

        
    def tokenize(self, seq):
        return seq.split(' ')

    def convert_tokens_to_ids(self, seq):
        return [self.c2i[c] for c in seq]

    def decode(self, seq, clean_up_tokenization_spaces=True):
        seq = [self.i2c[i] for i in seq]
        return ' '.join(seq)


def reorder(original, gold, output):
    "reorder the `.output` to align to the target order (map gold index to original index)"
    with open(original, 'r') as f:
        original = f.readlines()
    with open(gold, 'r') as f:
        gold = f.readlines()
    with open(output, 'r') as f:
        output = f.readlines()
    indexes = []
    for line in original:
        if line[-1] != '\n':    # the last line does not have a '\n'
            line += '\n'
        indexes.append(gold.index(line))
    return [output[i] for i in indexes]


if __name__ == '__main__':
    # ctok = CharTokenizer()
    # s = ctok.tokenize("None")
    # print(s)
    # s = ctok.convert_tokens_to_ids(['<CLS>'] + s + ['<SEP>'])
    # print(s)

    # ctok = CustomTokenizer()
    # s = '~ ( ( [ <VOW> ] ) & ( [ <CAP> ] ) & ( [ <LOW> ] ) )'
    # print(ctok.vocab_size)
    # ids = ctok.convert_tokens_to_ids(ctok.tokenize(s))
    # print(ctok.decode(ids))

    # reorder
    reordered_output = reorder('../data/data-eval-turk/src-val.txt', 'output-cb3ld-back/dev.gold', 'output-cb3ld-back/dev.output')
    with open('output-cb3ld-back/dev-r.output', 'w') as f:
        f.writelines(reordered_output)