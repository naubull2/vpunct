# coding: utf-8
import argparse
import codecs
import json
import pdb
import re
import os
import sys
import time
from tqdm import tqdm
from configs import Config as cfg

import spacy


tqdm.monitor_interval = 0

# Take the least neccessary components from the NLU pipeline
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
rules = json.load(codecs.open(os.path.join(cfg.home_path, 'res/pattern.json'), 'r', 'utf-8'))


def qmark_restore(message):
    if message:
        doc = nlp(message)
        mark = _pattern_tag(message, doc)
        return '{}{}'.format(message, mark)
    return message


def check_rule(rule, doc):
    if doc:
        keys = [','.join([doc[0].lemma_, doc[0].pos_, doc[0].tag_]),
                ','.join([doc[0].pos_, doc[0].tag_]),
                ','.join([doc[0].lemma_, doc[0].pos_]),
                doc[0].tag_]
        for k in keys:
            if not k in rule:
                continue
            val = rule.get(k, False)
            if isinstance(val, bool):
                return val
            elif isinstance(val, dict):
                # traverse sub rules
                return check_rule(val, doc[1:])
    return False
        

def _pattern_tag(message, doc):
    """
    """
    # check for beginning pattern
    qmark = check_rule(rules, doc[:3])

    if not qmark:
        # ending pattern
        if len(doc) > 1:
            for offset in range(1,4):
                qmark = check_rule(rules, doc[-1*offset:])
                if qmark:
                    break

    if qmark:
        return '?'
    return '.'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--eval', action='store_true', help='Evaluate on the dialogue dataset')
    args = parser.parse_args()
    if args.eval:
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        with codecs.open(os.path.join(cfg.home_path, 'dataset/train.en.in'), 'r', 'utf-8') as ifp:
            tests = ifp.read().split('\n')
            for t in tqdm(tests, ncols=70):
                try:
                    origin = t.endswith('?')
                    result = qmark_restore(t).endswith('?')

                    if origin and result:
                        tp += 1
                    elif origin and not result:
                        fn += 1
                    elif not origin and not result:
                        tn += 1
                    elif not origin and result:
                        fp += 1
                except Exception as e:
                    print(str(e))
                    print(t)
                    exit()

            total = sum([tp, tn, fp, fn])
            precision = float(tp)/sum([tp, fp])
            recall = float(tp)/sum([tp, fn])
            print('accuracy :\t{}'.format(float(sum([tp, tn]))/total))
            print('precision :\t{}'.format(precision)) 
            print('recall :\t{}'.format(recall))
            print('F1 :\t{}'.format(2*(precision*recall)/float(precision+recall)))
    else:
        while True:
            try:
                msg = sys.stdin.readline().rstrip('\n')
            except KeyboardInterrupt:
                break

            print(' '.join(['{}/{}/{}'.format(t.lemma_, t.pos_, t.tag_) for t in nlp(msg)]))

            tm= time.time()
            print(qmark_restore(msg))
            print('{} ms'.format(1000*(time.time()-tm)))

