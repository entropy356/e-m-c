import json
import unittest
from unittest.mock import patch

from long_term_memory.providers import APIProvider, unit


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict("os.environ", {
            "AGENT_API_BASE": "",
            "AGENT_API_KEY": "",
            "AGENT_CHAT_BASE": "https://chat.invalid/v1",
            "AGENT_CHAT_KEY": "chat-secret",
            "AGENT_CHAT_MODEL": "chat-model",
            "AGENT_EMBED_PROTOCOL": "openai",
            "AGENT_EMBED_BASE": "https://embed.invalid/v1",
            "AGENT_EMBED_KEY": "embed-secret",
            "AGENT_EMBED_MODEL": "embed-model",
            "AGENT_EMBED_DIMENSIONS": "768",
        }, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.provider = APIProvider()

    def test_chat_receives_ordered_history_and_separate_memory_context(self):
        response = {"choices": [{"message": {"content": json.dumps({
            "answer": "context-aware answer", "used_memory_ids": [4], "memories": []
        })}}]}
        history = [
            {"role": "user", "content": "I prefer concise answers."},
            {"role": "assistant", "content": "Understood."},
            {"role": "user", "content": "What do I prefer?"},
        ]
        memories = [{"id": 4, "content": "User prefers concise answers.",
                     "weight": 0.7, "stability": 0.2, "vector": [1.0]}]
        with patch.object(self.provider, "_chat", return_value=response) as chat:
            result = self.provider.cognize(history, memories)
        self.assertEqual(result["answer"], "context-aware answer")
        payload = chat.call_args.args[0]
        messages = payload["messages"]
        self.assertEqual([item["role"] for item in messages[-3:]],
                         ["user", "assistant", "user"])
        self.assertEqual(messages[-3:], history)
        memory_context = json.loads(messages[1]["content"].split("\n", 1)[1])
        self.assertEqual(memory_context, {
            "long_term_memories": [{"id": 4, "content": "User prefers concise answers."}]
        })
        self.assertNotIn("chat-secret", self.provider.chat_profile)
        self.assertNotIn("embed-secret", self.provider.profile)

    def test_embedding_is_normalized_and_uses_separate_endpoint(self):
        with patch("long_term_memory.providers._request",
                   return_value={"data": [{"embedding": [3, 4]}]}) as request:
            self.assertEqual(self.provider.embed("query", "query"), [0.6, 0.8])
        self.assertEqual(request.call_args.args[0], "https://embed.invalid/v1/embeddings")
        self.assertEqual(request.call_args.args[1]["dimensions"], 768)
        self.assertEqual(request.call_args.args[2],
                         {"Authorization": "Bearer embed-secret"})

    def test_gemini_embedding_uses_retrieval_task_type(self):
        with patch.dict("os.environ", {
            "AGENT_EMBED_PROTOCOL": "gemini",
            "AGENT_EMBED_BASE": "https://gemini.invalid/v1beta",
            "AGENT_EMBED_MODEL": "gemini-embedding-001",
        }):
            provider = APIProvider()
        with patch("long_term_memory.providers._request",
                   return_value={"embedding": {"values": [0, 5]}}) as request:
            self.assertEqual(provider.embed("memory", "document"), [0.0, 1.0])
        url, payload, headers = request.call_args.args[:3]
        self.assertEqual(url, "https://gemini.invalid/v1beta/models/gemini-embedding-001:embedContent")
        self.assertEqual(payload["taskType"], "RETRIEVAL_DOCUMENT")
        self.assertEqual(payload["outputDimensionality"], 768)
        self.assertEqual(headers, {"x-goog-api-key": "embed-secret"})

    def test_invalid_embedding_vectors_are_rejected(self):
        for vector in ([], [0, 0], [float("nan")], [float("inf")], [True], ["x"]):
            with self.subTest(vector=vector), self.assertRaises(ValueError):
                unit(vector)


if __name__ == "__main__":
    unittest.main()
