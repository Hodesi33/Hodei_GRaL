import argparse
import sys
import distutils.util
import re
import os

##need a file with a wordform and predicted SES as input

def _apply_lemma_rule(form, lemma_rule):
    if ';' not in lemma_rule:
        raise ValueError('lemma_rule %r for form %r missing semicolon' % (lemma_rule, form))
    casing, rule = lemma_rule.split(";", 1)
    if rule.startswith("a"):
        lemma = rule[1:]
    else:
        form = form.lower()
        rules, rule_sources = rule[1:].split("¦"), []
        assert len(rules) == 2
        for rule in rules:
            source, i = 0, 0
            while i < len(rule):
                if rule[i] == "→" or rule[i] == "-":
                    source += 1
                else:
                    assert rule[i] == "+"
                    i += 1
                i += 1
            rule_sources.append(source)

        try:
            lemma, form_offset = "", 0
            for i in range(2):
                j, offset = 0, (0 if i == 0 else len(form) - rule_sources[1])
                while j < len(rules[i]):
                    if rules[i][j] == "→":
                        lemma += form[offset]
                        offset += 1
                    elif rules[i][j] == "-":
                        offset += 1
                    else:
                        assert (rules[i][j] == "+")
                        lemma += rules[i][j + 1]
                        j += 1
                    j += 1
                    # print(lemma)
                if i == 0:
                    lemma += form[rule_sources[0]: len(form) - rule_sources[1]]
        except:
            lemma = lemma

    for rule in casing.split("¦"):
        if rule == "↓0": continue  # The lemma is lowercased initially
        if not rule: continue  # Empty lemma might generate empty casing rule
        case, offset = rule[0], int(rule[1:])
        lemma = lemma[:offset] + (lemma[offset:].upper() if case == "↑" else lemma[offset:].lower())
    return lemma
