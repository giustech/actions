#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import re
from pathlib import Path


def get_namespace(root):
    m = re.match(r"\{(.*)\}", root.tag)
    return m.group(1) if m else ""


def ns_tag(ns, tag):
    return f'{{{ns}}}{tag}' if ns else tag


def get_text(elem):
    return elem.text.strip() if elem is not None and elem.text else None


def resolve_property(value, props, project_version_candidates):
    pattern = re.compile(r"\$\{([^}]+)\}")
    max_iter = 20
    for _ in range(max_iter):
        m = pattern.search(value)
        if not m:
            break
        prop = m.group(1)
        replacement = None
        if prop in props:
            replacement = props[prop]
        else:
            if prop in ("project.version", "pom.version"):
                replacement = project_version_candidates.get('project') or project_version_candidates.get(
                    'parent') or ''
            elif prop == 'revision':
                replacement = props.get('revision', '')
            else:
                last = prop.split('.')[-1]
                replacement = props.get(last, None)
        if replacement is None:
            replacement = ''
        value = pattern.sub(replacement, value, count=1)
    return value


def extract_properties(project, ns):
    props = {}
    props_elem = project.find(ns_tag(ns, 'properties'))
    if props_elem is None:
        return props
    for child in list(props_elem):
        tag = child.tag
        if ns and tag.startswith('{' + ns + '}'):
            tag = tag[len(ns) + 2:]
        props[tag] = child.text.strip() if child.text else ''
    return props


def main(pom_path):
    pom_path = Path(pom_path)
    if not pom_path.exists():
        print(f'POM_NOT_FOUND: {pom_path}', file=sys.stderr)
        return 2

    tree = ET.parse(str(pom_path))
    root = tree.getroot()
    ns = get_namespace(root)
    project = root

    version_elem = project.find(ns_tag(ns, 'version'))


    version = get_text(version_elem)

    parent = project.find(ns_tag(ns, 'parent'))
    parent_version = None
    if parent is not None:
        parent_version = get_text(parent.find(ns_tag(ns, 'version')))
        if version is None:
            version = parent_version

    props = extract_properties(project, ns)
    project_candidates = {'project': version, 'parent': parent_version}

    if version:
        version = resolve_property(version, props, project_candidates)

    if not version:
        for key in ('revision', 'project.version', 'pom.version'):
            if key in props and props[key]:
                version = resolve_property(props[key], props, project_candidates)
                break

    if not version:
        print('VERSION_NOT_FOUND', file=sys.stderr)
        return 1

    print(version)
    return 0

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'pom.xml'
    sys.exit(main(path))