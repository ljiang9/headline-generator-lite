"""命令行：python3 cli.py "正文文本" """
import argparse
import json
import sys

from generator import generate_headlines, generate_rule_based


def main(argv=None):
    p = argparse.ArgumentParser(description="headline-generator-lite 标题生成")
    p.add_argument("text", nargs="?", help="正文")
    p.add_argument("-n", type=int, default=3, help="候选个数")
    p.add_argument("--no-llm", action="store_true", help="强制只用规则")
    args = p.parse_args(argv)

    text = args.text or sys.stdin.read()
    if not text.strip():
        print("错误：未提供正文", file=sys.stderr)
        return 2

    result = generate_headlines(text, n=args.n, use_llm=not args.no_llm)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
