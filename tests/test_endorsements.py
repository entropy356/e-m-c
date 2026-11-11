import importlib.util
from pathlib import Path
import sys
import unittest

script = Path(__file__).resolve().parents[1] / 'scripts' / 'endorsements.py'
spec = importlib.util.spec_from_file_location('endorsements', script)
e = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = e
spec.loader.exec_module(e)


class EndorsementTests(unittest.TestCase):
    def test_no_preceding_block_cannot_be_endorsed(self):
        body = '<!-- 认可：ChatGPT GPT-6 -->\n'
        cleaned, added = e.reconcile('', body, 'docs/a.md', set())
        self.assertEqual(cleaned, '')
        self.assertEqual(added, [])

    def test_new_block_endorsement_archives(self):
        original = 'hello world\n'
        new = 'hello world\n<!-- 认可：ChatGPT GPT-6 Chat -->\n'
        cleaned, added = e.reconcile(original, new, 'docs/a.md', set())
        self.assertEqual(cleaned, new)
        self.assertEqual(len(added), 1)
        self.assertEqual(added[0][0].identity, 'ChatGPT GPT-6 Chat')

    def test_old_comment_edited_content_is_removed(self):
        before = 'hello world\n<!-- 认可：ChatGPT GPT-6 -->\n'
        after = 'hello worlds\n<!-- 认可：ChatGPT GPT-6 -->\n'
        item = e.parse_approvals(before)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        cleaned, added = e.reconcile(before, after, 'docs/a.md', records)
        self.assertEqual(cleaned, 'hello worlds\n')
        self.assertFalse(added)

    def test_no_record_no_new_signature_is_removed(self):
        content = 'hello\n<!-- 认可：ChatGPT GPT-6 -->\n'
        cleaned, added = e.reconcile(content, content, 'docs/a.md', set())
        self.assertEqual(cleaned, 'hello\n')
        self.assertEqual(added, [])

    def test_new_signer_to_existing_approval(self):
        before = 'hi\n<!-- 认可：ChatGPT GPT-6 -->\n'
        after = 'hi\n<!-- 认可：ChatGPT GPT-6；Claude Opus 4.6 -->\n'
        item = e.parse_approvals(before)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        cleaned, added = e.reconcile(before, after, 'docs/a.md', records)
        self.assertEqual(cleaned, after)
        self.assertEqual(len(added), 1)
        self.assertEqual(added[0][0].identity, 'Claude Opus 4.6')

    def test_multiple_comments_do_not_change_hash(self):
        single = 'hi\n<!-- 认可：ChatGPT GPT-6 -->\n'
        both = 'hi\n<!-- 认可：ChatGPT GPT-6 -->\n<!-- 认可：Claude Opus 4.6 -->\n'
        self.assertEqual(e.parse_approvals(single)[0].digest, e.parse_approvals(both)[0].digest)

    def test_section_scope_changes_invalidate(self):
        before = '# A\ntext\n<!-- 认可范围：本节；认可：ChatGPT GPT-6 -->\n# B\nother\n'
        after = before.replace('text\n', 'text!\n')
        item = e.parse_approvals(before)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        cleaned, added = e.reconcile(before, after, 'docs/a.md', records)
        self.assertNotIn('认可', cleaned)
        self.assertFalse(added)

    def test_other_section_does_not_invalidate(self):
        before = '# A\ntext\n<!-- 认可范围：本节；认可：ChatGPT GPT-6 -->\n# B\nother\n'
        after = before.replace('other\n', 'new other\n')
        item = e.parse_approvals(before)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        cleaned, _ = e.reconcile(before, after, 'docs/a.md', records)
        self.assertEqual(cleaned, after)

    def test_unchanged_existing_signature_preserved(self):
        content = 'hello\n<!-- 认可：ChatGPT GPT-6 -->\n'
        item = e.parse_approvals(content)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        self.assertEqual(e.reconcile(content, content, 'docs/a.md', records)[0], content)

    def test_full_document_range(self):
        content = '# A\nbody\n<!-- 认可范围：全文；认可：ChatGPT GPT-6 -->\n'
        item = e.parse_approvals(content)[0]
        self.assertEqual(item.digest, e.fingerprint('# A\nbody\n'))

    def test_changed_body_does_not_create_false_new_approval(self):
        before = 'old\n<!-- 认可：GPT X -->\n'
        after = 'new\n<!-- 认可：GPT X -->\n'
        cleaned, additions = e.reconcile(before, after, 'docs/a.md', set())
        self.assertNotIn('认可', cleaned)
        self.assertEqual(additions, [])

    def test_new_signature_does_not_revive_stale_prior_approval(self):
        before = '# A\nold\n<!-- 认可：ChatGPT GPT-6 -->\n# B\nother\n'
        after = '# A\nnew\n<!-- 认可：ChatGPT GPT-6 -->\n# B\nother\n<!-- 认可：ChatGPT GPT-6 -->\n'
        item = e.parse_approvals(before)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        cleaned, added = e.reconcile(before, after, 'docs/a.md', records)
        self.assertEqual(added, [])
        self.assertNotIn('认可', cleaned)

    def test_same_signer_can_endorse_another_block_if_old_still_valid(self):
        before = '# A\nold\n<!-- 认可：ChatGPT GPT-6 -->\n# B\nother\n'
        after = '# A\nold\n<!-- 认可：ChatGPT GPT-6 -->\n# B\nother\n<!-- 认可：ChatGPT GPT-6 -->\n'
        item = e.parse_approvals(before)[0]
        records = {('docs/a.md', item.identity, item.scope, item.anchor, item.digest)}
        cleaned, added = e.reconcile(before, after, 'docs/a.md', records)
        self.assertEqual(cleaned, after)
        self.assertEqual(len(added), 1)


if __name__ == '__main__':
    unittest.main()
