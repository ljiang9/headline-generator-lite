"""headline-generator-lite — 标题生成。

规则模板：抽取核心关键词，按多种模板组合出多个候选标题。
若设置 OPENAI_API_KEY，则额外可选调用 OpenAI 兼容接口润色；无 key 自动降级为纯规则。
零第三方依赖（LLM 仅用标准库 urllib）。
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from collections import Counter

_EN_RE = re.compile(r"[a-zA-Z]+")
_STOP = {"the", "a", "an", "is", "are", "of", "and", "to", "in", "on",
         "的", "了", "和", "是", "在", "与", "及", "或", "这", "那"}


def extract_keywords(text: str, k: int = 3) -> list[str]:
    """抽取核心关键词：中文按连续汉字段、英文按词，去停用词后取高频前 k。"""
    toks = _EN_RE.findall(text.lower())
    toks += re.findall(r"[\u4e00-\u9fff]{2,}", text)
    toks = [t for t in toks if t not in _STOP]
    freq = Counter(toks)
    return [w for w, _ in freq.most_common(k)]


TEMPLATES = [
    "{kw0}：一文读懂{kw1}",
    "关于{kw0}，你需要知道这些",
    "{kw0}与{kw1}：深度解析",
    "三分钟看懂{kw0}",
    "{kw0}来袭，{kw1}将如何改变",
]


def generate_rule_based(text: str, n: int = 3) -> list[str]:
    """用模板组合候选标题。"""
    kws = extract_keywords(text, k=3)
    if not kws:
        return []
    kw0 = kws[0]
    kw1 = kws[1] if len(kws) > 1 else kws[0]
    out = []
    for tpl in TEMPLATES:
        try:
            out.append(tpl.format(kw0=kw0, kw1=kw1))
        except KeyError:
            continue
    return out[:n]


def generate_with_llm(text: str, n: int = 3) -> list[str] | None:
    """有 key 时调用 OpenAI 兼容接口；无 key / 失败返回 None。"""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你是标题生成器，输出多个候选标题。"},
            {"role": "user", "content": f"为下面内容生成 {n} 个吸引人的标题，每行一个：\n{text[:800]}"},
        ],
        "max_tokens": 200,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        return [ln.strip("-•0123456789. ") for ln in content.splitlines() if ln.strip()][:n]
    except Exception:
        return None


def generate_headlines(text: str, n: int = 3, use_llm: bool = True) -> list[dict]:
    """对外主接口：返回 [{title, source}]，source 为 'llm' 或 'rule'。"""
    if use_llm:
        llm_titles = generate_with_llm(text, n=n)
        if llm_titles:
            return [{"title": t, "source": "llm"} for t in llm_titles]
    rules = generate_rule_based(text, n=n)
    return [{"title": t, "source": "rule"} for t in rules]
