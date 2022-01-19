#!/usr/bin/env python3
# coding: utf8

import re
import sys
import yaml
import argparse
from typing import Union, Tuple, Optional


def get_substitution(context: dict, entity: str, default: any = None) -> Optional[
    Union[str, list]]:
    split_entity = re.split(r'\s+', entity)
    entity = context
    for part in split_entity:
        if part not in entity:
            return default
        entity = entity[part]
    return entity


def is_entity(entity: str) -> bool:
    return entity.startswith('[[') and entity.endswith(']]')


def unpack_entity(entity: str) -> str:
    return entity[2:-2].strip()


def parse_loop(context: dict, entity: str) -> Optional[Tuple[str, list]]:
    loops = re.findall(
        r'for(?:\s+(even|odd))?\s+([a-zA-Z0-9_\-]+)\s+in\s+([a-zA-Z0-9_\-\s]+)', entity)
    if not loops:
        return None

    parity, variable, list_entity = loops[0]
    iterable = get_substitution(context, list_entity, default=[])

    if parity == 'even':
        iterable = list([iterable[i] for i in range(0, len(iterable)) if i % 2 == 0])
    elif parity == 'odd':
        iterable = list([iterable[i] for i in range(0, len(iterable)) if i % 2 == 1])

    return variable, iterable


def parse_substitution(context: dict, entity: str, default: any = '') -> Optional[str]:
    if not is_entity(entity):
        return None
    return get_substitution(context, unpack_entity(entity), default)


def apply_substitutions(context: dict, string: str) -> str:
    entities = re.split(r'(\[\[\s*.*?\s*]])', string)
    output = ''

    i = 0
    while i < len(entities):
        raw_entity = entities[i]

        if loop := parse_loop(context, raw_entity):
            binding, iterable = loop
            buffer = ''
            loop_level = 1
            for j in range(1 + i, len(entities)):
                raw_inner_entity = entities[j]
                if is_entity(raw_inner_entity):
                    inner_entity = unpack_entity(raw_inner_entity)
                    if inner_entity.startswith('for'):
                        loop_level += 1
                    elif inner_entity == 'end for':
                        loop_level -= 1
                i = j
                if loop_level == 0:
                    break
                buffer += raw_inner_entity
            for element in iterable:
                context[binding] = element
                output += apply_substitutions(context, buffer)
                del context[binding]
        elif (substitution := parse_substitution(context, raw_entity)) is not None:
            output += substitution
        else:
            output += raw_entity
        i += 1
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=argparse.FileType('r'),
                        help='YAML file containing the template data')
    parser.add_argument('template', type=argparse.FileType('r'),
                        help='Text file containing the template')
    parser.add_argument('-o', type=argparse.FileType('w'), metavar='output',
                        help='Output file. Defaults to stdout', default=sys.stdout)
    args = parser.parse_args()

    output_text = apply_substitutions(yaml.load(args.data), args.template.read())
    args.o.write(output_text)
    args.o.flush()
