#!/usr/bin/env python3
"""Archive explicit AI endorsements as annotated Git tags and remove stale ones.

Git tags are the versioned source of truth; Markdown comments are current-view labels.
The script intentionally fails closed on changed scopes and unknown old signatures.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PREFIX = "endorsements/v1/"
FORMAT = "e-m-c-endorsement/v1"
COMMENT = re.compile(
    r"^\s*<!--\s*(?:认可范围[：:]\s*(上一块|本节|全文)\s*；\s*)?认可[：:]\s*(.*?)\s*-->\s*$"
)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout if proc.returncode == 0 else ""


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Approval:
    line: int
    identity: str
    scope: str
    anchor: str
    digest: str


def strip_approval_lines(lines: list[str]) -> str:
    return "".join(line for line in lines if not COMMENT.fullmatch(line.rstrip("\r\n")))


def section_start(lines: list[str], line_number: int) -> tuple[int, int, str] | None:
    stack: list[tuple[int, str]] = []
    last: tuple[int, int, str] | None = None
    for n in range(line_number):
        match = HEADING.match(lines[n].rstrip("\r\n"))
        if not match:
            continue
        depth, title = len(match.group(1)), match.group(2)
        while stack and stack[-1][0] >= depth:
            stack.pop()
        stack.append((depth, title))
        last = (n, depth, "/".join(title for _, title in stack))
    return last


def approval_scope(lines: list[str], line_no: int, scope: str) -> tuple[str, str] | None:
    if scope == "全文":
        return "全文", strip_approval_lines(lines)
    section = section_start(lines, line_no)
    if scope == "本节":
        if section is None:
            return None
        start, depth, heading_path = section
        end = len(lines)
        for i in range(start + 1, len(lines)):
            match = HEADING.match(lines[i].rstrip("\r\n"))
            if match and len(match.group(1)) <= depth:
                end = i
                break
        return heading_path, strip_approval_lines(lines[start:end])
    # Default: the preceding nonempty block separated by blank lines.
    n = line_no - 1
    while n >= 0 and (not lines[n].strip() or COMMENT.fullmatch(lines[n].rstrip("\r\n"))):
        n -= 1
    if n < 0:
        return None
    end = n + 1
    while n >= 0 and lines[n].strip() and not COMMENT.fullmatch(lines[n].rstrip("\r\n")):
        n -= 1
    body = "".join(lines[n + 1:end])
    heading_path = section[2] if section else "(无标题)"
    return heading_path, body


def parse_approvals(content: str) -> list[Approval]:
    lines = content.splitlines(keepends=True)
    output: list[Approval] = []
    for line_number, line in enumerate(lines):
        match = COMMENT.fullmatch(line.rstrip("\r\n"))
        if not match:
            continue
        scope = match.group(1) or "上一块"
        bounds = approval_scope(lines, line_number, scope)
        if bounds is None:
            anchor, body = "", ""
        else:
            anchor, body = bounds
        for identity in match.group(2).split("；"):
            identity = identity.strip()
            if identity and len(identity) <= 128:
                output.append(Approval(line_number, identity, scope, anchor, fingerprint(body) if body else ""))
    return output


def encode_comment(scope: str, identities: list[str], newline: str) -> str:
    prefix = f"认可范围：{scope}；" if scope != "上一块" else ""
    return f"<!-- {prefix}认可：{'；'.join(identities)} -->{newline}"


def reconcile(
    old: str, new: str, path: str, records: set[tuple[str, str, str, str, str]]
) -> tuple[str, list[tuple[Approval, int]]]:
    """Return cleaned content and newly issued endorsements (with occurrence index)."""
    previous = parse_approvals(old)
    current = parse_approvals(new)
    old_counts = Counter((a.identity, a.scope) for a in previous)
    new_counts = Counter((a.identity, a.scope) for a in current)
    # Fail closed if any previously present signer lost a validated endorsement.
    verified_counts = Counter((a.identity, a.scope) for a in current
        if (path, a.identity, a.scope, a.anchor, a.digest) in records)
    allowances = {
        token: max(0, total - old_counts[token])
        if verified_counts[token] >= old_counts[token] else 0
        for token, total in new_counts.items()
    }
    approvals_by_line: dict[int, list[Approval]] = {}
    for item in current:
        approvals_by_line.setdefault(item.line, []).append(item)

    accepted: set[tuple[str, str, str, str, str]] = set()
    created: list[tuple[Approval, int]] = []
    lines = new.splitlines(keepends=True)
    for line_no, items in approvals_by_line.items():
        identities: list[str] = []
        scope = items[0].scope
        for item in items:
            key = (path, item.identity, item.scope, item.anchor, item.digest)
            if not item.digest:
                continue
            if key in accepted:
                continue  # A single identity must not count twice for the same scope content.
            if key in records:
                identities.append(item.identity)
                accepted.add(key)
                continue
            # An unchanged signature is NOT renewed merely because the body changed.
            token = (item.identity, item.scope)
            if allowances.get(token, 0) > 0:
                allowances[token] -= 1
                identities.append(item.identity)
                accepted.add(key)
                created.append((item, line_no))
        if identities:
            newline = "\r\n" if lines[line_no].endswith("\r\n") else "\n" if lines[line_no].endswith("\n") else ""
            lines[line_no] = encode_comment(scope, identities, newline)
        else:
            lines[line_no] = ""
    return "".join(lines), created


def load_records() -> set[tuple[str, str, str, str, str]]:
    records: set[tuple[str, str, str, str, str]] = set()
    tag_names = git("for-each-ref", "--format=%(refname)", f"refs/tags/{PREFIX}").splitlines()
    for ref in tag_names:
        annotated = git("cat-file", "-p", ref)
        _, separator, message = annotated.partition("\n\n")
        if not separator:
            continue
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            continue
        if data.get("format") == FORMAT:
            records.add(tuple(data[field] for field in ("path", "identity", "scope", "anchor", "digest")))
    return records


def is_first_push(commit: str) -> bool:
    return not commit or commit == "0" * 40


def reachable(commit: str) -> bool:
    return bool(git("rev-parse", "--verify", f"{commit}^{{commit}}", check=False))


def text_at(commit: str, path: str) -> str:
    return git("show", f"{commit}:{path}", check=False)


def markdown_paths(commit: str) -> list[str]:
    if is_first_push(commit):
        return []
    return [p for p in git("ls-tree", "-r", "--name-only", commit).splitlines()
            if p.lower().endswith(".md")]


def commit_tag(item: Approval, path: str, commit: str, index: int) -> str:
    metadata = {"format": FORMAT, "path": path, "identity": item.identity,
                "scope": item.scope, "anchor": item.anchor, "digest": item.digest}
    tag_key = fingerprint(json.dumps([commit, path, index, metadata], ensure_ascii=False, sort_keys=True))[:24]
    name = f"{PREFIX}{commit[:12]}/{tag_key}"
    if git("rev-parse", "--verify", f"refs/tags/{name}", check=False):
        return ""
    git("tag", "-a", name, commit, "-m", json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    return name


def run(before: str, head: str, manifest: Path) -> None:
    if git("rev-parse", "HEAD").strip() != head:
        raise RuntimeError("HEAD must match the triggering commit")
    # A missing prior tree makes every signature look new, which would certify
    # endorsements whose scope actually changed. Refuse instead of guessing.
    if not is_first_push(before) and not reachable(before):
        raise RuntimeError(
            f"prior commit {before} is not reachable in this clone; "
            "refusing to archive or remove endorsements without a prior tree"
        )
    records = load_records()
    generated: list[str] = []
    changed: list[str] = []
    for path in markdown_paths(head):
        after = text_at(head, path)
        prior = "" if is_first_push(before) else text_at(before, path)
        cleaned, additions = reconcile(prior, after, path, records)
        for item, index in additions:
            tag = commit_tag(item, path, head, index)
            if tag:
                generated.append(tag)
            records.add((path, item.identity, item.scope, item.anchor, item.digest))
        if cleaned != after:
            Path(path).write_text(cleaned, encoding="utf-8", newline="")
            changed.append(path)
    manifest.write_text("\n".join(generated) + ("\n" if generated else ""), encoding="utf-8")
    print(f"Archived {len(generated)} endorsements; cleaned {len(changed)} Markdown files")
    if changed:
        print("Changed:", ", ".join(changed))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--manifest", default=".git/endorsement-tags")
    args = parser.parse_args()
    run(args.before, args.head, Path(args.manifest))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        sys.exit(str(error))
