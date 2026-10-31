import unittest
from titles import topic_title, display_title as make_title

def display_title(topic, session_id, existing):
    return make_title(topic, session_id, existing, "飞书")


class TopicTitleTests(unittest.TestCase):
    def session(self, *texts, name="default"):
        return {"name": name, "history": [{"role": "user", "content": text} for text in texts]}

    def test_skip_greetings_and_use_task(self):
        topic, meaningful = topic_title(
            self.session("在", "你知道我从哪给你发消息吗？", "帮我检查登录回调失败的问题。")
        )
        self.assertEqual(topic, "检查登录回调失败的问题")
        self.assertTrue(meaningful)

    def test_action_is_not_mistaken_for_small_talk(self):
        self.assertEqual(topic_title(self.session("测试登录流程")), ("测试登录流程", True))
        self.assertEqual(topic_title(self.session("修复登录")), ("修复登录", True))

    def test_later_replies_do_not_rename_topic(self):
        self.assertEqual(topic_title(self.session("好了，再试"), "登录流程测试"), ("登录流程测试", True))

    def test_explicit_session_name_wins(self):
        self.assertEqual(topic_title(self.session(name="邮件登录修复"), "旧话题"), ("邮件登录修复", True))

    def test_distinct_topics_and_duplicate_suffix(self):
        first = display_title("登录测试", "s1", set())
        self.assertEqual(first, "飞书｜登录测试")
        self.assertEqual(display_title("登录测试", "s2", {first}), "飞书｜登录测试 · s2")
        self.assertNotEqual(display_title("提交代码", "s3", {first}), first)

    def test_greeting_only_has_unique_provisional_title(self):
        topic, meaningful = topic_title(self.session("你好", "在吗"))
        self.assertFalse(meaningful)
        self.assertEqual(display_title(topic, "s4", set()), "飞书｜待确定话题 · s4")


if __name__ == "__main__":
    unittest.main()
