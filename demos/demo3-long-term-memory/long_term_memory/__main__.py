"""Command-line interface for Demo 3."""

import argparse
import json
from pathlib import Path
import sqlite3
import sys

from .model import DynamicsConfig
from .providers import APIProvider, OfflineProvider
from .runtime import Runtime


def _read_json(path):
    with open(path, "r", encoding="utf-8") as source:
        return json.load(source)


def _write_json(path, value):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Emotion-free long-term conversational memory agent (Python 3.10+)"
    )
    parser.add_argument("--mode", choices=("offline", "api"), default="offline")
    parser.add_argument("--db", default="data/demo3.sqlite3")
    parser.add_argument("--conversation", default="default")
    parser.add_argument("--dynamics", choices=("weight-only", "two-state"), default="two-state")
    parser.add_argument("--decay-rate", type=float, default=0.12)
    parser.add_argument("--stability-protection", type=float, default=0.85)
    parser.add_argument("--recovery-rate", type=float, default=0.65)
    parser.add_argument("--stability-gain", type=float, default=0.12)
    parser.add_argument("--top-k", type=int, default=5)
    sub = parser.add_subparsers(dest="command", required=True)

    turn = sub.add_parser("turn", help="Send one user message")
    turn.add_argument("text")

    sub.add_parser("chat", help="Start an interactive conversation")
    sub.add_parser("history", help="Show the ordered conversation history")

    retrieve = sub.add_parser("retrieve", help="Inspect long-term memory retrieval")
    retrieve.add_argument("text")

    run = sub.add_parser("run", help="Run a scripted multi-turn conversation")
    run.add_argument("scenario")
    run.add_argument("--output", help="Optional JSON result path")

    sub.add_parser("state", help="Show memories, conversations and recent traces")

    args = parser.parse_args()
    try:
        provider = APIProvider() if args.mode == "api" else OfflineProvider()
        config = DynamicsConfig(
            mode=args.dynamics,
            decay_rate=args.decay_rate,
            stability_protection=args.stability_protection,
            recovery_rate=args.recovery_rate,
            stability_gain=args.stability_gain,
            top_k=args.top_k,
        )
        runtime = Runtime(args.db, provider, config)

        if args.command == "turn":
            result = runtime.turn(args.text, args.conversation)
        elif args.command == "chat":
            print("Chat started. Enter /exit or /quit to leave.")
            while True:
                try:
                    text = input("you> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if text in ("/exit", "/quit"):
                    break
                if not text:
                    continue
                result = runtime.turn(text, args.conversation)
                print("agent> " + result["answer"])
            return
        elif args.command == "history":
            result = runtime.history(args.conversation)
        elif args.command == "retrieve":
            result = runtime.retrieve(args.text)
        elif args.command == "run":
            scenario = _read_json(args.scenario)
            if not isinstance(scenario, dict) or not isinstance(scenario.get("turns"), list):
                raise ValueError("Scenario must be an object containing a turns list")
            conversation_id = scenario.get("conversation_id", args.conversation)
            traces = []
            for item in scenario["turns"]:
                if isinstance(item, str):
                    text = item
                elif isinstance(item, dict):
                    text = item.get("input")
                    conversation_id = item.get("conversation_id", conversation_id)
                else:
                    raise ValueError("Each scenario turn must be text or an object with input")
                traces.append(runtime.turn(text, conversation_id))
            result = {
                "scenario": scenario.get("name", Path(args.scenario).stem),
                "mode": provider.mode,
                "provider": {
                    "chat": getattr(provider, "chat_profile", None),
                    "embedding": provider.profile,
                },
                "config": config.to_dict(),
                "traces": traces,
                "final": runtime.inspect(conversation_id),
            }
            if args.output:
                _write_json(args.output, result)
        else:
            result = runtime.inspect(args.conversation)

        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, OSError, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
