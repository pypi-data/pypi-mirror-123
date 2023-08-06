import sys
from stwfsapy.automata.nfa import Nfa
from stwfsapy.automata.construction import ConstructionState
from stwfsapy.automata.conversion import NfaToDfaConverter
from stwfsapy.expansion import base_expansion
from stwfsapy.case_handlers import title_case_handler
import stwfsapy.thesaurus as t
from rdflib import Graph
from rdflib.namespace import SKOS
import logging
from math import ceil


def check(labels):
    nfa = Nfa()
    if len(labels) == 0:
        return True
    for concept, label in labels:
        ConstructionState(
            nfa,
            title_case_handler(
                base_expansion(label)),
            str(concept)
        ).construct()
    try:
        nfa.remove_empty_transitions()
        dfa = NfaToDfaConverter(nfa).start_conversion()
        return True
    except Exception as e:
        logging.warning(e, exc_info=True)
        return False


if __name__ == '__main__':
    in_pth = '/home/fuer/autoSE/stwfsapy/gnd_skos_20191013.ttl'  # sys.argv[1]
    print(in_pth)
    g = Graph()
    g.load(in_pth, format='ttl')
    all_deprecated = set(t.extract_deprecated(g))
    concepts = set(t.extract_by_type_uri(
        g,
        SKOS.Concept,
        remove=all_deprecated))
    #  deprecated??
    labels = t.retrieve_concept_labels(
        g,
        allowed=concepts,
        langs={'de'})
    labels = list(labels)
    step = ceil(len(labels) / 10)
    labelss = []
    start = 0
    while start < len(labels):
        end = start+step
        labelss.append(
            labels[start*step:min(end, len(labels))])
        start = end
    bad_labels = []
    while labelss:
        new_labelss = []
        for idx, labels in enumerate(labelss):
            print(idx)
            status = check(labels)
            if not status:
                if len(labels) == 1:
                    bad_labels.append(labels[0])
                mid = len(labels) % 2
                new_labelss = [labels[:mid], labels[mid:]]
                break
        labelss = new_labelss
    for label in bad_labels:
        print(bad_labels)
