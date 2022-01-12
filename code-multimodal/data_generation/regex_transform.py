from threading import current_thread
from typing import Tuple, List
import numpy as np
import random


# StReg DSL
NON_TERMINALS = {'startwith':1, 'endwith':1, 'contain':1, 'not':1, 'optional':1, 'star':1, 'notcc':1,
                 'concat':2, 'and':2, 'or':2, 'repeat':2, 'repeatatleast':2,
                 'repeatrange':3}
TERMINALS = ['<let>', '<cap>', '<low>', '<num>', '<any>', '<spec>']  # <null> (not found in datasets)


class Node:

    def __init__(self, content) -> None:
        self.content: str = content
        self.children: tuple = []
    
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.content)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

class Tree:

    def __init__(self) -> None:
        self.root: Node = None

    def from_string(self, string: str):
        # NOTE: essential preprocessing to remove '<,>' from the string
        string_clean = string.replace('<,>', '<comma>')

        self.root, _ = self.__from_string(string_clean)
        
    def __from_string(self, string: str) -> Tuple[Node, int]:
        i = 0
        while i < len(string):
            c = string[i]
            if c == '(' or c == ',' or c == ')':
                break
            i += 1
        node = Node(string[:i])
        # print(node.content)
        
        if string[i] == '(':
            while i < len(string):
                child, offset = self.__from_string(string[i+1:])
                node.children.append(child)
                i += offset + 1
                assert string[i] in '(),'
                if string[i] == ')':
                    return node, i+1    # finish as a node, so move an extra offset
        else:   # leaf
            return node, i

    def to_string(self, tokenize: bool) -> str:
        assert(self.root)

        # NOTE: restore '<,>'
        return self.__to_string(self.root, tokenize).replace('<comma>', '<,>')

    def __to_string(self, node: Node, tokenize=False) -> str:
        if not node.children:
            return node.content
        if tokenize:
            return '{} ( {} )'.format(node.content, ' , '.join([self.__to_string(child, tokenize) for child in node.children]))
        else:
            return '{}({})'.format(node.content, ','.join([self.__to_string(child, tokenize) for child in node.children]))
    
    def traverse_and_modify(self, func=None) -> None:
        self.root = self.__traverse_and_modify(self.root, func)

    def __traverse_and_modify(self, node, func=None) -> None:
        "pre-order traversal"
        node = func(node)
        for i, child_node in enumerate(node.children):
            node.children[i] = self.__traverse_and_modify(child_node, func)
        return node
    
    def __str__(self):
        return self.root.__str__()


class RegexTransfom(object):
    "Allow multiple transformations to an existing regular expression in NL-RX form"

    def __init__(self) -> None:
        self.candidates = []
        self.final = None

    def transform(self, regex: str, args):
        """
        The input string is essentially
        """
        tree = Tree()
        tree.from_string(regex)


    def __permutation(self, node: Node):
        pass

    def __constant(self, node: Node, mode='terminals'):
        """
        Exchangable: <Mx>, <VOW>, <CAP>, <LOW>, ...
        """
        pass

    def __number(self, node: Node):
        pass


class RegexTransformBeta(object):
    """
    Store some patterns

    Assumptions:
    (1) usually the first item of `concat` is a terminating subtree, which can be exchangable with other terminating subtrees
    """
    def __init__(self) -> None:
        self.subtree_patterns = []
    
    def build(self, corpus: List[str]) -> None:
        """
        learn patterns from datasets
        return statistics (non-terminal ratio)
        """
        for regex_string in corpus:
            rx_tree = Tree().__from_string(regex_string)


    def random_transform(self, regex: str) -> str :
        rx_tree = Tree()
        try:
            rx_tree.from_string(regex)
        except AssertionError:
            print(regex)
            assert 0
        
        def judge_and_mutate(node: Node, thres=0.6):
            # judge if is terminating subtree
            try:
                if node.content not in NON_TERMINALS:   # terminal
                    return node
            except AttributeError:
                print('Str:', node)
            for child in node.children:     # non terminating subtree
                if child.content in NON_TERMINALS:
                    return node
            # if 
            if random.random() < thres:
                m_node = self.__mutate_nonterminal(node)
                return m_node
            else:
                return node

        rx_tree.traverse_and_modify(judge_and_mutate)
        new_targ = rx_tree.to_string(tokenize=True).split(' ')

        # # NOTE: fix '<,>' from '< , >'
        # new_targ_fixed = []
        # state = 0
        # cat_tok = ''
        # for tok in new_targ:
        #     if tok == '<':
        #         state = 1
        #         cat_tok = '<'
        #     elif tok == '>':
        #         state = 0
        #         new_targ_fixed.append(cat_tok)
        #         cat_tok = ''
        #     else:
        #         if state == 1:
        #             cat_tok += tok
        #         else:
        #             new_targ_fixed.append(tok)
        # return ' '.join(new_targ_fixed)

        return ' '.join(new_targ)

    def __mutate_terminal(self, terminal: str) -> str:
        try:
            assert terminal not in NON_TERMINALS
        except AssertionError:
            print('Illegal terminal:', terminal)
            return terminal
        return TERMINALS[random.randint(0, len(TERMINALS)-1)]
    
    def __mutate_nonterminal(self, nonterminal: Node) -> Node:
        """
        Only consider "complexity one" non-terminals (which I call it terminating subtree), e.g. "not(contain(x))", "repeat(x, 4)"
        Why this setting? Won't affect regex string length distribution too much.

        Probability:
        P(N_m | N)

        """
        nt_thres = 1.0   # non-terminal change threshold
        # tm_thres = 0.5   # terminal change threshold
        if random.random() <= nt_thres:
            # print(nonterminal.content)
            if nonterminal.content in ['startwith', 'endwith', 'contain', 'not', 'optional', 'notcc', 'star']:
                nonterminal.children[0].content = self.__mutate_terminal(nonterminal.children[0].content)
                return nonterminal
            # elif nonterminal.content in ['concat', 'or']:  # switch order, NOTE: removed `and` because it is difficult to locate it in NL
            #     nonterminal.children[0], nonterminal.children[1] = nonterminal.children[1], nonterminal.children[0]
            elif nonterminal.content in ['repeat', 'repeatatleast']:
                nonterminal.children[0].content = self.__mutate_terminal(nonterminal.children[0].content)
                nonterminal.children[1].content = str(random.randint(1, 9))
            elif nonterminal.content == 'repeatrange':
                nonterminal.children[0].content = self.__mutate_terminal(nonterminal.children[0].content)
                k1 = random.randint(1, 9)
                k2 = random.randint(1, 9)
                if k1 < k2:
                    nonterminal.children[1].content = str(k1)
                    nonterminal.children[2].content = str(k2)
                else:
                    nonterminal.children[2].content = str(k1)
                    nonterminal.children[1].content = str(k2)
            else:
                # print('Non-Terminal Not Handled:', nonterminal.content)
                # raise NotImplementedError('---UNT---')
                pass
            return nonterminal
        else:   # increase or decrease complexity
            return nonterminal


def compare_streg(reg0: List[str], reg1: List[str]) -> List[bool]:
    if len(reg0) != len(reg1):
        print(reg0)
        print(reg1)
        exit()
    return reg0, reg1, [reg0[i] != reg1[i] for i in range(len(reg0))]


if __name__ == '__main__':
    # unit test
    import pandas as pd
    class Example:
        def __init__(self, idx, source, target, positive, negative):
            self.idx = idx
            self.source = source
            self.target = target
            self.positive = positive
            self.negative = negative

    def read_examples(filename):
        examples = []
        idx = 0
        num_without_neg = 0
        df = pd.read_csv(filename, delimiter='\t')
        for line1, line2, line3, line4 in zip(df['description'], df['regex'], df['pos_examples'], df['neg_examples']):
            if type(line4) == float:
                num_without_neg += 1
            examples.append(
                Example(
                    idx=idx,
                    source=line1.strip(),
                    target=line2.strip(),
                    positive=line3,
                    negative=line4  # NOTE: some examples in train doesn't have negative examples
                )
            )
            idx += 1
        print('Examples without negative examples:', num_without_neg)
        return examples

    rt = RegexTransformBeta()
    tree = Tree()
    string = 'concat(repeatatleast(<num>,1),concat(repeatrange(<let>,3,4),concat(repeat(<low>,4),concat(or(const0,const1),optional(or(const2,const3))))))'
    tree.from_string(string)
    print(tree.to_string())
    print(tree.to_string() == string)
    # print(str(tree))
    print(rt.random_transform(string))