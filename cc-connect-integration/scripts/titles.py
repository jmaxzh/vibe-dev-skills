"""Stable, local topic titles; no model calls or transcript uploads."""

import re

GENERIC_NAMES = {"", "default", "新会话", "新对话"}
SMALL_TALK = re.compile(
    r"^(?:(?:你好|您好|在吗|在不在|在|嗨|hello|hi|测试|好的?|可以|继续|开始|谢谢|再试)[，,。.!！?？\s]*$|你知道我从哪)",
    re.I,
)
PREFIX = re.compile(
    r"^(?:(?:请|麻烦|帮我|请帮我|能否|能不能|可以帮我|再|准备|我想|我需要|我们需要|现在需要|做一次|完整的)\s*)+"
)


def topic_title(session, saved_topic=None, generic_names=()):
    """Prefer an explicit session name, then a saved topic, then its first task."""
    name = str(session.get("name") or "").strip()
    if name.lower() not in GENERIC_NAMES | {str(n).lower() for n in generic_names}:
        return re.sub(r"\s+", " ", name)[:40], True
    if saved_topic:
        return saved_topic, True
    for message in session.get("history", []):
        if message.get("role") != "user":
            continue
        text = message.get("content", "").strip()
        if text.startswith("[Quoted message") or SMALL_TALK.match(text):
            continue
        text = re.sub(r"^(?:你好|您好|嗨|hello|hi)[，,！!\s]+", "", text, flags=re.I)
        text = re.sub(r"\s+", " ", text)
        # The opening request gives the conversation a stable, recognizable label.
        text = re.split(r"[。！？!?\n：:]", text, maxsplit=1)[0]
        text = PREFIX.sub("", text).strip(" ，,、。")
        if len(text) >= 4:
            return text[:36].rstrip(" ，,、") + ("…" if len(text) > 36 else ""), True
    return "待确定话题", False


def display_title(topic, session_id, existing, source_label):
    base = source_label + "｜" + topic
    if topic == "待确定话题" or base in existing:
        return base + " · " + session_id
    return base
