"""kw-skills command line interface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, discover_skills, find_root, frontmatter

EPILOG = """examples:
  Linux/macOS:  kw-skills validate requirement-analysis --json
  Windows:      kw-skills package --platform claude-code --verbose
  either:       python -m kw_skills compatibility        (when not installed)
"""


def _emit(args, data, text: str) -> None:
    print(json.dumps(data, indent=2) if args.json else text)


def _log(args, msg: str) -> None:
    if args.verbose:
        print(msg, file=sys.stderr)


def cmd_list(args, root):
    rows = []
    for s in discover_skills(root):
        fm, _, _ = frontmatter.parse((s / "SKILL.md").read_text(encoding="utf-8"))
        m = fm.get("metadata", {})
        rows.append({"name": s.name, "category": m.get("category", ""), "version": m.get("version", ""),
                     "tier": m.get("tier", "paid"), "path": s.relative_to(root).as_posix()})
    _emit(args, rows, "\n".join(f"{r['name']:<34} {r['category']:<14} {r['version']:<12} {r['path']}" for r in rows) or "no skills found")
    return 0


def cmd_validate(args, root):
    from .validator import summarize, validate_skill

    skills = discover_skills(root)
    if args.skill:
        skills = [s for s in skills if s.name == args.skill]
        if not skills:
            print(f"error: unknown skill '{args.skill}'. Run 'kw-skills list'.", file=sys.stderr)
            return 2
    results = {}
    for s in skills:
        _log(args, f"validating {s.name}")
        results[s.name] = validate_skill(s)
    summ = summarize(results)
    if args.json:
        print(json.dumps({"summary": summ, "findings": {k: [f.to_dict() for f in v] for k, v in results.items()}}, indent=2))
    else:
        for k, v in results.items():
            for f in v:
                print(f"{f.severity.upper():7} {f.code} {k}: {f.message}" + (f"  [{Path(f.path).name}]" if args.verbose and f.path else ""))
        print(f"\n{summ['skills']} skill(s): {summ['errors']} error(s), {summ['warnings']} warning(s). Structural validation only.")
    return 1 if summ["errors"] else 0


def cmd_package(args, root):
    from .packager import PLATFORMS, package

    plats = list(PLATFORMS) if not args.platform else [("generic" if p == "generic-agent" else p) for p in args.platform]
    try:
        res = package(root, plats, only=args.skill or None, dist=Path(args.out) if args.out else None)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    _emit(args, res, "\n".join(f"[{p}] {a['file']}  {a['sha256'][:12]}  {a['bytes']}B" for p, v in res.items() for a in v))
    return 0


def cmd_compat(args, root):
    from . import compatibility

    plats = args.platform or [p for p in compatibility.MATRIX]
    res = compatibility.run(root, plats)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        for p, r in res.items():
            print(f"{'PASS' if r['passed'] else 'FAIL'}  {p:<15} structural, {r['skills_checked']} skills, live-tested: {r['live_tested']}")
            for e in r["errors"]:
                print(f"      - {e}")
        print("\nStructural checks only. A pass does not prove a live assistant discovers the skill.")
    return 0 if all(r["passed"] for r in res.values()) else 1


def cmd_docs(args, root):
    from . import docsgen

    if args.check:
        ok = docsgen.check(root)
        _emit(args, {"catalogue_current": ok}, "catalogue is current" if ok else "docs/SKILL_CATALOGUE.md is stale: run 'kw-skills docs'")
        return 0 if ok else 1
    p = docsgen.write(root)
    _emit(args, {"written": str(p)}, f"wrote {p}")
    return 0


def cmd_release(args, root):
    from . import release

    try:
        if args.action == "history":
            h = release.load_history(root)
            _emit(args, h, "\n".join(f"{e['version']:<14} {e['status']:<12} published={e['published']}  {e['built_at']}" for e in h) or "no releases")
        elif args.action == "rollback":
            if not args.version:
                raise ValueError("rollback needs --version")
            r = release.rollback(root, args.version)
            _emit(args, r, f"rolled back {r['version']}")
        else:
            r = release.build_release(root, args.version)
            _emit(args, r, f"built release {r['version']} ({r['artifacts']} artifacts) in {r['dir']}\nNot published. Publishing needs owner approval.")
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


def cmd_marketplace(args, root):
    from . import marketplace

    try:
        if args.action == "prepare":
            if args.target != "agensi":
                raise ValueError("only 'agensi' is supported")
            r = marketplace.prepare(root)
            _emit(args, r, f"prepared {r['listings']} listings and {r['packages']} packages in {r['dir']}\nNothing was published or submitted.")
        else:
            r = marketplace.report(root)
            lines = [f"submission assets ready: {r['submission_assets_ready']}  |  skills with real-world evaluation: {r['evaluated_in_real_world']}"]
            lines += [f"  {x['skill']:<34} valid={x['structurally_valid']} listing={x['listing']} package={x['package']}" for x in r["skills"]]
            lines += ["pending human gates:"] + [f"  - {g}" for g in r["pending_human_gates"]]
            _emit(args, r, "\n".join(lines))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


def cmd_eval(args, root):
    from . import evals

    try:
        r = evals.score(Path(args.rubric), Path(args.scores))
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    _emit(args, r, f"{r['rubric']}: {r['total']}/100 (evaluator {r['evaluator']}, {r['run_date']})\n" +
          "\n".join(f"  {c['id']:<22} {c['points']:>5}/{c['weight']}  {c['rationale']}" for c in r["criteria"]))
    return 0


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="machine-readable output")
    common.add_argument("--verbose", action="store_true", default=argparse.SUPPRESS, help="progress on stderr")
    p = argparse.ArgumentParser(prog="kw-skills", description="KnowledgeWala AI Engineering Skills tooling",
                                epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"kw-skills {__version__}")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--verbose", action="store_true", help="progress on stderr")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("list", parents=[common], help="list skills").set_defaults(fn=cmd_list)
    v = sub.add_parser("validate", parents=[common], help="structurally validate skills")
    v.add_argument("skill", nargs="?")
    v.set_defaults(fn=cmd_validate)
    k = sub.add_parser("package", parents=[common], help="build platform packages")
    k.add_argument("--platform", action="append", choices=["claude-code", "cursor", "github-copilot", "codex", "generic", "generic-agent", "agensi"])
    k.add_argument("--skill", action="append")
    k.add_argument("--out")
    k.set_defaults(fn=cmd_package)
    c = sub.add_parser("compatibility", parents=[common], help="structural platform compatibility checks")
    c.add_argument("--platform", action="append")
    c.set_defaults(fn=cmd_compat)
    d = sub.add_parser("docs", parents=[common], help="generate/check the skill catalogue")
    d.add_argument("--check", action="store_true")
    d.set_defaults(fn=cmd_docs)
    r = sub.add_parser("release", parents=[common], help="build a release locally (never publishes)")
    r.add_argument("action", nargs="?", choices=["build", "history", "rollback"], default="build")
    r.add_argument("--version")
    r.set_defaults(fn=cmd_release)
    m = sub.add_parser("marketplace", parents=[common], help="marketplace submission assets (never submits)")
    m.add_argument("action", choices=["prepare", "report"])
    m.add_argument("target", nargs="?", default="agensi")
    m.set_defaults(fn=cmd_marketplace)
    e = sub.add_parser("eval", parents=[common], help="score a recorded skill evaluation against a rubric")
    e.add_argument("action", choices=["score"])
    e.add_argument("rubric")
    e.add_argument("scores")
    e.set_defaults(fn=cmd_eval)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.json = getattr(args, "json", False)
    args.verbose = getattr(args, "verbose", False)
    return args.fn(args, find_root())


if __name__ == "__main__":
    sys.exit(main())
