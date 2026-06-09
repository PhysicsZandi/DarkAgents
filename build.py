import argparse
import json
import shutil
from pathlib import Path

LLM_TARGETS = {
    "claude": {
        "orchestrator": "CLAUDE.md",
        "agent_instructions": ".claude",
    },
    "codex": {
        "orchestrator": "AGENTS.md",
        "agent_instructions": ".codex",
    },
    "vibe": {
        "orchestrator": "AGENTS.md",
        "agent_instructions": ".vibe",
    },
    "ollama": {
        "orchestrator": "CLAUDE.md",
        "agent_instructions": ".claude",
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="Build an LLM-specific workspace.")
    parser.add_argument(
        "--llm",
        required=True,
        choices=sorted(LLM_TARGETS),
        help="Target LLM. Options: %s." % ", ".join(sorted(LLM_TARGETS)),
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path("src"),
        help="Source folder to copy.",
    )
    return parser.parse_args()


def rename(root: Path, old_name: str, new_name: str) -> None:
    old_path = root / old_name
    new_path = root / new_name
    if not old_path.exists():
        return
    if new_path.exists():
        if new_path.is_dir():
            shutil.rmtree(new_path)
        else:
            new_path.unlink()
    old_path.rename(new_path)


def is_frontmatter_fence(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped) == {"-"} and len(stripped) >= 3


def parse_frontmatter_agent(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text()
    lines = text.splitlines()

    if not lines or not is_frontmatter_fence(lines[0]):
        return {}, text.strip()

    end = next(
        (i for i, line in enumerate(lines[1:], 1) if is_frontmatter_fence(line)),
        -1,
    )
    if end < 0:
        return {}, text.strip()

    metadata: dict[str, str] = {}
    current_key = ""

    for line in lines[1:end]:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("-") and current_key:
            item = stripped[1:].strip().strip('"').strip("'")
            if item:
                previous = metadata.get(current_key, "")
                metadata[current_key] = ", ".join(
                    value for value in [previous, item] if value
                )
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        current_key = key.strip()
        metadata[current_key] = value.strip().strip('"').strip("'")

    body = "\n".join(lines[end + 1 :]).strip()
    return metadata, body


def toml_string(value: str) -> str:
    return json.dumps(value)


def agent_display_name(metadata: dict[str, str], fallback: str) -> str:
    name = metadata.get("display_name") or metadata.get("name") or fallback
    name = name.replace("-", "_").replace("_", " ").strip()
    return name[:1].upper() + name[1:] if name else fallback


def parse_tool_names(raw_tools: str) -> set[str]:
    normalized = raw_tools.replace("[", "").replace("]", "")
    return {
        tool.strip().strip('"').strip("'").lower()
        for tool in normalized.split(",")
        if tool.strip()
    }


def vibe_tool_config(metadata: dict[str, str]) -> list[str]:
    claude_tools = parse_tool_names(metadata.get("tools", ""))
    if not claude_tools:
        return []

    tool_map = {
        "read": "read_file",
        "grep": "grep",
        "glob": "grep",
        "bash": "bash",
        "edit": "search_replace",
        "multiedit": "search_replace",
        "write": "write_file",
        "task": "task",
        # These are only valid if exposed by Vibe custom tools or MCP servers.
        "websearch": "web_search",
        "webfetch": "web_fetch",
    }
    enabled_tools = sorted(
        {tool_map[tool] for tool in claude_tools if tool in tool_map}
    )
    unknown_tools = sorted(tool for tool in claude_tools if tool not in tool_map)

    lines: list[str] = []

    if enabled_tools:
        lines.append(f"enabled_tools = {json.dumps(enabled_tools)}")

    if {"websearch", "webfetch"} & claude_tools:
        lines.extend(
            [
                "",
                "# NOTE: Claude WebSearch/WebFetch were mapped to web_search/web_fetch.",
                "# These names must exist as Vibe custom tools or MCP-provided tools.",
            ]
        )

    if unknown_tools:
        lines.extend(
            [
                "",
                f"# NOTE: Unmapped Claude tools: {', '.join(unknown_tools)}.",
                "# Add them manually if equivalent Vibe custom tools exist.",
            ]
        )

    if "bash" in enabled_tools:
        lines.extend(["", "[tools.bash]", 'permission = "ask"'])

    return lines


def fix_vibe_agents(root: Path) -> None:
    agents = root / ".vibe" / "agents"
    if not agents.exists():
        return

    for md_path in agents.glob("*.md"):
        toml_path = md_path.with_suffix(".toml")
        metadata, body = parse_frontmatter_agent(md_path)

        description = metadata.get(
            "description", f"Agent generated from {md_path.name}."
        )
        display_name = agent_display_name(metadata, md_path.stem)
        model = metadata.get("model", "").strip()

        toml_lines = [
            "# This file is generated from the sibling Markdown agent file.",
            "# Modify the .md file and regenerate the workspace.",
            'agent_type = "subagent"',
            f"display_name = {toml_string(display_name)}",
            f"description = {toml_string(description)}",
            'safety = "safe"',
        ]

        if model and model != "inherit":
            toml_lines.append(f"active_model = {toml_string(model)}")

        tool_config = vibe_tool_config(metadata)
        if tool_config:
            toml_lines.extend(["", *tool_config])

        toml_lines.extend(["", f"system_prompt = {toml_string(body)}"])
        toml_path.write_text("\n".join(toml_lines) + "\n")


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    target_root = Path(f"{args.llm}_workspace").resolve()
    target = LLM_TARGETS[args.llm]

    if not source_root.exists():
        raise SystemExit(f"missing source root: {source_root}")

    if target_root.exists():
        shutil.rmtree(target_root)

    shutil.copytree(source_root, target_root, symlinks=True)

    orchestrator_path = target_root / "ORCHESTRATOR.md"
    if orchestrator_path.exists():
        content = orchestrator_path.read_text()
        content = content.replace("ORCHESTRATOR.md", target["orchestrator"])
        content = content.replace(
            "agent_instructions/", target["agent_instructions"] + "/"
        )
        orchestrator_path.write_text(content)

    rename(target_root, "ORCHESTRATOR.md", target["orchestrator"])
    rename(target_root, "agent_instructions", target["agent_instructions"])

    if args.llm == "vibe":
        fix_vibe_agents(target_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
