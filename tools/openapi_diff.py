import json
import os
import sys
from typing import Dict, Any, List, Tuple, Set


def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def dict_key_diff(a: Dict[str, Any], b: Dict[str, Any]) -> Tuple[Set[str], Set[str], Set[str]]:
    a_keys = set(a.keys()) if isinstance(a, dict) else set()
    b_keys = set(b.keys()) if isinstance(b, dict) else set()
    return b_keys - a_keys, a_keys - b_keys, a_keys & b_keys


def list_to_set_repr(lst: Any) -> Set[str]:
    if not isinstance(lst, list):
        return set()
    # Convert list of dicts like security requirements into deterministic strings
    out = set()
    for item in lst:
        out.add(json.dumps(item, sort_keys=True))
    return out


def compare_schema(old: Dict[str, Any], new: Dict[str, Any], path_prefix: str = "") -> List[str]:
    """Very lightweight schema comparison. Focuses on type, enum, properties, required."""
    changes = []
    if not isinstance(old, dict):
        old = {}
    if not isinstance(new, dict):
        new = {}

    old_type = old.get('type')
    new_type = new.get('type')
    if old_type != new_type:
        changes.append(f"{path_prefix} type changed: {old_type} -> {new_type}")

    # enum changes
    if 'enum' in old or 'enum' in new:
        if old.get('enum') != new.get('enum'):
            changes.append(f"{path_prefix} enum changed")

    # object properties
    old_props = old.get('properties', {}) if isinstance(old.get('properties'), dict) else {}
    new_props = new.get('properties', {}) if isinstance(new.get('properties'), dict) else {}
    added, removed, common = dict_key_diff(old_props, new_props)
    for p in sorted(added):
        changes.append(f"{path_prefix} property added: {p}")
    for p in sorted(removed):
        changes.append(f"{path_prefix} property removed: {p}")
    for p in sorted(common):
        o = old_props.get(p, {})
        n = new_props.get(p, {})
        ot = o.get('type')
        nt = n.get('type')
        if ot != nt:
            changes.append(f"{path_prefix} property '{p}' type changed: {ot} -> {nt}")
        # one level deeper for nested object
        if (o.get('properties') or n.get('properties')):
            changes.extend(compare_schema(o, n, path_prefix=f"{path_prefix}{p}."))

    # required list changes
    old_req = set(old.get('required') or [])
    new_req = set(new.get('required') or [])
    added_req = new_req - old_req
    removed_req = old_req - new_req
    for r in sorted(added_req):
        changes.append(f"{path_prefix} required added: {r}")
    for r in sorted(removed_req):
        changes.append(f"{path_prefix} required removed: {r}")

    # format change
    if old.get('format') != new.get('format'):
        changes.append(f"{path_prefix} format changed: {old.get('format')} -> {new.get('format')}")

    return changes


def compare_parameters(old_params: List[Dict[str, Any]] = None, new_params: List[Dict[str, Any]] = None) -> List[str]:
    old_params = old_params or []
    new_params = new_params or []
    def key(p):
        return (p.get('name'), p.get('in'))

    old_map = {key(p): p for p in old_params}
    new_map = {key(p): p for p in new_params}

    changes = []
    added = set(new_map.keys()) - set(old_map.keys())
    removed = set(old_map.keys()) - set(new_map.keys())
    common = set(old_map.keys()) & set(new_map.keys())
    for k in sorted(added):
        changes.append(f"parameter added: {k[0]} in={k[1]}")
    for k in sorted(removed):
        changes.append(f"parameter removed: {k[0]} in={k[1]}")
    for k in sorted(common):
        o = old_map[k]
        n = new_map[k]
        if bool(o.get('required')) != bool(n.get('required')):
            changes.append(f"parameter required changed: {k[0]} in={k[1]} {o.get('required')} -> {n.get('required')}")
        # schema compare if present
        o_schema = (o.get('schema') or {})
        n_schema = (n.get('schema') or {})
        sch_changes = compare_schema(o_schema, n_schema, path_prefix=f"param {k[0]}.")
        changes.extend(sch_changes)
    return changes


def compare_request_body(old_rb: Dict[str, Any] = None, new_rb: Dict[str, Any] = None) -> List[str]:
    old_rb = old_rb or {}
    new_rb = new_rb or {}
    changes = []
    if (old_rb == {}) and (new_rb == {}):
        return changes
    if bool(old_rb) != bool(new_rb):
        changes.append(f"requestBody presence changed: {bool(old_rb)} -> {bool(new_rb)}")
    if bool(old_rb.get('required')) != bool(new_rb.get('required')):
        changes.append(f"requestBody.required changed: {old_rb.get('required')} -> {new_rb.get('required')}")

    old_content = (old_rb.get('content') or {})
    new_content = (new_rb.get('content') or {})
    added, removed, common = dict_key_diff(old_content, new_content)
    for ct in sorted(added):
        changes.append(f"requestBody content type added: {ct}")
    for ct in sorted(removed):
        changes.append(f"requestBody content type removed: {ct}")
    for ct in sorted(common):
        o_schema = (((old_content.get(ct) or {}).get('schema')) or {})
        n_schema = (((new_content.get(ct) or {}).get('schema')) or {})
        sch_changes = compare_schema(o_schema, n_schema, path_prefix=f"requestBody[{ct}].")
        changes.extend(sch_changes)
    return changes


def compare_responses(old_resp: Dict[str, Any] = None, new_resp: Dict[str, Any] = None) -> List[str]:
    old_resp = old_resp or {}
    new_resp = new_resp or {}
    changes = []
    added, removed, common = dict_key_diff(old_resp, new_resp)
    for sc in sorted(added):
        changes.append(f"response added: {sc}")
    for sc in sorted(removed):
        changes.append(f"response removed: {sc}")
    for sc in sorted(common):
        o_ct = ((old_resp.get(sc) or {}).get('content') or {})
        n_ct = ((new_resp.get(sc) or {}).get('content') or {})
        a2, r2, c2 = dict_key_diff(o_ct, n_ct)
        for ct in sorted(a2):
            changes.append(f"response {sc} content type added: {ct}")
        for ct in sorted(r2):
            changes.append(f"response {sc} content type removed: {ct}")
        for ct in sorted(c2):
            o_schema = (((o_ct.get(ct) or {}).get('schema')) or {})
            n_schema = (((n_ct.get(ct) or {}).get('schema')) or {})
            sch_changes = compare_schema(o_schema, n_schema, path_prefix=f"response[{sc}][{ct}].")
            changes.extend(sch_changes)
    return changes


def compare_paths(old: Dict[str, Any], new: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    summary_lines: List[str] = []
    notes: List[str] = []

    old_paths = old.get('paths', {})
    new_paths = new.get('paths', {})

    added_paths, removed_paths, common_paths = dict_key_diff(old_paths, new_paths)

    if added_paths:
        summary_lines.append("New paths:")
        for p in sorted(added_paths):
            summary_lines.append(f"  + {p}")
    if removed_paths:
        summary_lines.append("Removed paths:")
        for p in sorted(removed_paths):
            summary_lines.append(f"  - {p}")

    for p in sorted(common_paths):
        o = old_paths[p]
        n = new_paths[p]
        # HTTP methods keys
        http_methods = {k for k in o.keys()} | {k for k in n.keys()}
        http_methods = {m for m in http_methods if m.lower() in {"get","post","put","delete","patch","options","head"}}
        for m in sorted(http_methods):
            o_op = o.get(m, {})
            n_op = n.get(m, {})
            if not o_op and n_op:
                summary_lines.append(f"  + {m.upper()} {p}")
                continue
            if o_op and not n_op:
                summary_lines.append(f"  - {m.upper()} {p}")
                continue
            # compare details
            op_changes: List[str] = []
            if o_op.get('operationId') != n_op.get('operationId'):
                op_changes.append(f"operationId: {o_op.get('operationId')} -> {n_op.get('operationId')}")
            if o_op.get('summary') != n_op.get('summary'):
                op_changes.append("summary changed")
            # parameters
            op_changes.extend(compare_parameters(o_op.get('parameters'), n_op.get('parameters')))
            # requestBody
            op_changes.extend(compare_request_body(o_op.get('requestBody'), n_op.get('requestBody')))
            # responses
            op_changes.extend(compare_responses(o_op.get('responses'), n_op.get('responses')))

            if op_changes:
                summary_lines.append(f"Modified {m.upper()} {p}:")
                for ch in op_changes:
                    summary_lines.append(f"    * {ch}")

    return summary_lines, notes


def compare_components(old: Dict[str, Any], new: Dict[str, Any]) -> List[str]:
    out: List[str] = []
    old_comp = old.get('components', {})
    new_comp = new.get('components', {})

    # Schemas
    old_schemas = old_comp.get('schemas', {})
    new_schemas = new_comp.get('schemas', {})
    added, removed, common = dict_key_diff(old_schemas, new_schemas)
    if added:
        out.append("New schemas:")
        for s in sorted(added):
            out.append(f"  + {s}")
    if removed:
        out.append("Removed schemas:")
        for s in sorted(removed):
            out.append(f"  - {s}")
    for s in sorted(common):
        changes = compare_schema(old_schemas.get(s, {}), new_schemas.get(s, {}), path_prefix=f"schema {s}.")
        if changes:
            out.append(f"Modified schema {s}:")
            for ch in changes:
                out.append(f"    * {ch}")

    # Security Schemes
    old_sec = old_comp.get('securitySchemes', {})
    new_sec = new_comp.get('securitySchemes', {})
    a2, r2, c2 = dict_key_diff(old_sec, new_sec)
    if a2:
        out.append("New securitySchemes:")
        for k in sorted(a2):
            out.append(f"  + {k}")
    if r2:
        out.append("Removed securitySchemes:")
        for k in sorted(r2):
            out.append(f"  - {k}")
    for k in sorted(c2):
        o = old_sec.get(k, {})
        n = new_sec.get(k, {})
        changes = []
        for prop in ["type", "scheme", "bearerFormat", "openIdConnectUrl"]:
            if o.get(prop) != n.get(prop):
                changes.append(f"{prop}: {o.get(prop)} -> {n.get(prop)}")
        if o.get('flows') != n.get('flows'):
            changes.append("flows changed")
        if changes:
            out.append(f"Modified securityScheme {k}:")
            for ch in changes:
                out.append(f"    * {ch}")

    return out


def compare_servers_and_security(old: Dict[str, Any], new: Dict[str, Any]) -> List[str]:
    out: List[str] = []
    # servers
    old_servers = [s.get('url') for s in (old.get('servers') or [])]
    new_servers = [s.get('url') for s in (new.get('servers') or [])]
    added = sorted(list(set(new_servers) - set(old_servers)))
    removed = sorted(list(set(old_servers) - set(new_servers)))
    if added:
        out.append("New servers:")
        for s in added:
            out.append(f"  + {s}")
    if removed:
        out.append("Removed servers:")
        for s in removed:
            out.append(f"  - {s}")
    # root security
    old_sec = list_to_set_repr(old.get('security'))
    new_sec = list_to_set_repr(new.get('security'))
    added = new_sec - old_sec
    removed = old_sec - new_sec
    if added:
        out.append("New root security requirements:")
        for s in sorted(added):
            out.append(f"  + {s}")
    if removed:
        out.append("Removed root security requirements:")
        for s in sorted(removed):
            out.append(f"  - {s}")
    return out


def main():
    try:
        if len(sys.argv) < 3:
            print("Usage: python openapi_diff.py <old.json> <new.json>", flush=True)
            sys.exit(1)
        old_path = sys.argv[1]
        new_path = sys.argv[2]
        if not os.path.isabs(old_path):
            old_path = os.path.abspath(old_path)
        if not os.path.isabs(new_path):
            new_path = os.path.abspath(new_path)

        old = load_json(old_path)
        new = load_json(new_path)

        lines: List[str] = []
        def emit(s: str = ""):
            lines.append(s)
            print(s, flush=True)

        emit("=== Summary of Changes ===")

        # Version/title change
        if old.get('info', {}).get('version') != new.get('info', {}).get('version'):
            emit(f"Info.version: {old.get('info', {}).get('version')} -> {new.get('info', {}).get('version')}")
        if old.get('info', {}).get('title') != new.get('info', {}).get('title'):
            emit("Info.title changed")

        # Servers and security
        for line in compare_servers_and_security(old, new):
            emit(line)

        # Paths
        path_summary, _ = compare_paths(old, new)
        if path_summary:
            emit("\n=== Paths ===")
            for line in path_summary:
                emit(line)

        # Components
        comp_summary = compare_components(old, new)
        if comp_summary:
            emit("\n=== Components ===")
            for line in comp_summary:
                emit(line)

        emit("\n=== End ===")

        # Write to a markdown file alongside the specs for easy retrieval
        out_dir = os.path.dirname(new_path) or os.getcwd()
        base_old = os.path.basename(old_path)
        base_new = os.path.basename(new_path)
        out_file = os.path.join(out_dir, f"openapi-diff-{base_old.replace('.json','')}-to-{base_new.replace('.json','')}.md")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
    except Exception as e:
        print(f"Error: {e}", flush=True)
        raise


if __name__ == '__main__':
    main()
