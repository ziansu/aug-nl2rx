
import enum
import pickle


visible_ascii = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
print(visible_ascii)

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

        # structured-regex DSL (rep->repeat, repatleast->repeatatleast)
        reserved = ['startwith', 'endwith', 'contain', 'not', 'optional', 'star', 'concat', 'and', 'or', 
                    'repeat', 'repeatatleast', 'repeatrange', 'const', 'notcc',
                    '<let>', '<cap>', '<low>', '<num>', '<any>', '<spec>', '<null>',
                    '10', 'None']
        for c in reserved:
            self.c2i[c] = self.vocab_size
            self.i2c[self.vocab_size] = c
            self.vocab_size += 1
        
    def tokenize(self, line):
        s = line.split()
        tokenized = []
        for token in s:
            if token[0] == '<' and token[-1] == '>' and token not in ['<let>', '<cap>', '<low>', '<num>', '<any>', '<spec>', '<null>']:
                # print(token)
                tokenized += [c for c in token]
            else:
                tokenized.append(token)
        return tokenized

    def convert_tokens_to_ids(self, seq):
        return [self.c2i[c] for c in seq]

    def decode(self, seq, clean_up_tokenization_spaces=True):
        seq = [self.i2c[i] for i in seq]
        return ''.join(seq)


class ConstAnonymizedCustomTokenizer:
    "Store const{0-5}"

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

        # structured-regex DSL (rep->repeat, repatleast->repeatatleast)
        reserved = ['startwith', 'endwith', 'contain', 'not', 'optional', 'star', 'concat', 'and', 'or', 
                    'repeat', 'repeatatleast', 'repeatrange', 'const', 'notcc',
                    '<let>', '<cap>', '<low>', '<num>', '<any>', '<spec>', '<null>',
                    '10', 'None']
        for c in reserved:
            self.c2i[c] = self.vocab_size
            self.i2c[self.vocab_size] = c
            self.vocab_size += 1
        
    def tokenize(self, line):
        s = line.split()
        tokenized = []
        for token in s:
            if token[0] == '<' and token[-1] == '>' and token not in ['<let>', '<cap>', '<low>', '<num>', '<any>', '<spec>', '<null>']:
                # print(token)
                tokenized += [c for c in token]
            else:
                tokenized.append(token)
        return tokenized

    def convert_tokens_to_ids(self, seq):
        return [self.c2i[c] for c in seq]

    def decode(self, seq, clean_up_tokenization_spaces=True):
        seq = [self.i2c[i] for i in seq]
        return ''.join(seq)


def restore_gold(tokenized_gold):
    return tokenized_gold.replace(' ', '')

if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('../data/StructuredRegex/tokenized/train.tsv', delimiter='\t')
    ctok = CustomTokenizer()
    for line in df['regex'][:10]:
        # print(ctok.tokenize(line))
        print(restore_gold(line))
    