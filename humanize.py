#!/usr/bin/env python3
"""
humanize-text v1.0
Transform AI-generated text into natural, human-sounding writing.
https://github.com/Koi725/humanize-text

Usage:
    humanize "Your AI-generated text here"
    humanize -f input.txt
    humanize -f input.md -o output.md
    cat essay.txt | humanize
    humanize -f input.txt --level heavy

Author: Kousha Rezaei — github.com/Koi725
License: MIT
"""

import sys
import re
import random
import argparse
import os

VERSION = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# AI Detection Patterns — words and patterns that scream "AI"
# ═══════════════════════════════════════════════════════════════

# Overused AI words → more natural replacements
AI_WORDS = {
    "utilize": ["use", "work with", "rely on"],
    "utilized": ["used", "worked with", "relied on"],
    "utilizing": ["using", "working with"],
    "leverage": ["use", "take advantage of", "build on"],
    "leveraging": ["using", "building on", "taking advantage of"],
    "leveraged": ["used", "built on", "took advantage of"],
    "facilitate": ["help", "make easier", "support"],
    "facilitating": ["helping", "supporting", "enabling"],
    "facilitated": ["helped", "supported", "made possible"],
    "comprehensive": ["complete", "full", "thorough", "detailed"],
    "furthermore": ["also", "on top of that", "plus"],
    "moreover": ["also", "besides", "on top of that"],
    "additionally": ["also", "plus", "and"],
    "subsequently": ["then", "after that", "next"],
    "consequently": ["so", "because of this", "as a result"],
    "nevertheless": ["still", "but", "even so"],
    "notwithstanding": ["despite", "even though", "regardless"],
    "aforementioned": ["mentioned", "previous", "earlier"],
    "henceforth": ["from now on", "going forward"],
    "thereby": ["by doing this", "which"],
    "wherein": ["where", "in which"],
    "thereof": ["of it", "of this"],
    "whilst": ["while"],
    "amongst": ["among"],
    "endeavor": ["try", "attempt", "work hard"],
    "endeavors": ["tries", "attempts", "efforts"],
    "commencing": ["starting", "beginning"],
    "commenced": ["started", "began"],
    "ascertain": ["find out", "figure out", "determine"],
    "paramount": ["crucial", "key", "really important"],
    "plethora": ["a lot of", "many", "plenty of"],
    "myriad": ["many", "a ton of", "countless"],
    "multifaceted": ["complex", "varied"],
    "groundbreaking": ["new", "innovative", "game-changing"],
    "cutting-edge": ["modern", "latest", "advanced"],
    "state-of-the-art": ["modern", "latest", "top-tier"],
    "robust": ["strong", "solid", "reliable"],
    "seamless": ["smooth", "easy", "clean"],
    "seamlessly": ["smoothly", "easily", "cleanly"],
    "streamline": ["simplify", "speed up", "clean up"],
    "streamlined": ["simplified", "cleaned up", "faster"],
    "optimize": ["improve", "speed up", "fine-tune"],
    "optimized": ["improved", "faster", "fine-tuned"],
    "pivotal": ["key", "important", "critical"],
    "foster": ["encourage", "build", "grow"],
    "fostering": ["encouraging", "building", "growing"],
    "delve": ["dig into", "explore", "look at"],
    "delving": ["digging into", "exploring", "looking at"],
    "delved": ["dug into", "explored", "looked at"],
    "intricate": ["complex", "detailed", "tricky"],
    "intricacies": ["details", "complexities", "ins and outs"],
    "meticulous": ["careful", "detailed", "thorough"],
    "meticulously": ["carefully", "thoroughly"],
    "encompasses": ["includes", "covers"],
    "pertaining": ["about", "related to", "regarding"],
    "juxtaposition": ["contrast", "comparison"],
    "synergy": ["teamwork", "combination", "working together"],
    "paradigm": ["model", "approach", "way of thinking"],
    "holistic": ["complete", "full", "overall"],
    "nuanced": ["subtle", "detailed", "layered"],
    "overarching": ["main", "big-picture", "overall"],
    "underscores": ["shows", "highlights", "proves"],
    "underscore": ["show", "highlight", "prove"],
    "elucidate": ["explain", "clarify", "spell out"],
    "elucidating": ["explaining", "clarifying"],
    "bolster": ["strengthen", "support", "boost"],
    "bolstering": ["strengthening", "supporting", "boosting"],
    "augment": ["add to", "expand", "boost"],
    "augmenting": ["adding to", "expanding", "boosting"],
    "mitigate": ["reduce", "lessen", "handle"],
    "mitigating": ["reducing", "handling"],
    "navigate": ["handle", "deal with", "work through"],
    "navigating": ["handling", "dealing with", "working through"],
    "spearhead": ["lead", "drive", "kick off"],
    "spearheading": ["leading", "driving"],
    "revolutionize": ["change", "transform", "shake up"],
    "revolutionizing": ["changing", "transforming"],
    "empower": ["help", "enable", "give power to"],
    "empowering": ["helping", "enabling"],
    "embark": ["start", "begin", "kick off"],
    "embarking": ["starting", "beginning"],
    "realm": ["area", "field", "world"],
    "landscape": ["scene", "field", "space"],
    "ecosystem": ["system", "space", "world"],
    "tapestry": ["mix", "blend", "collection"],
    "cornerstone": ["foundation", "base", "key part"],
    "catalyst": ["driver", "trigger", "spark"],
    "testament": ["proof", "sign", "evidence"],
    "beacon": ["example", "guide", "symbol"],
    "aligns with": ["matches", "fits", "goes with"],
    "in conjunction with": ["with", "along with", "together with"],
    "it is important to note": ["worth noting", "keep in mind"],
    "it's worth mentioning": ["also", "on that note"],
    "in today's digital age": ["these days", "nowadays", "right now"],
    "in today's world": ["these days", "nowadays", "right now"],
    "at the end of the day": ["ultimately", "in the end"],
    "in conclusion": ["to wrap up", "bottom line"],
    "in summary": ["to sum up", "in short"],
    "as a matter of fact": ["actually", "in fact"],
    "without a doubt": ["definitely", "clearly", "for sure"],
    "it goes without saying": ["obviously", "clearly"],
    "needless to say": ["obviously", "of course"],
    "in the realm of": ["in", "when it comes to"],
    "serves as a": ["is a", "works as a", "acts as a"],
    "plays a crucial role": ["matters a lot", "is key", "is important"],
    "is of paramount importance": ["really matters", "is critical"],
}

# Phrases AI loves to start sentences with
AI_STARTERS = {
    "It is worth noting that ": "",
    "It's important to understand that ": "",
    "It should be noted that ": "",
    "It is essential to ": "You need to ",
    "It is crucial to ": "You should ",
    "It is imperative to ": "Make sure to ",
    "In order to ": "To ",
    "For the purpose of ": "To ",
    "With respect to ": "About ",
    "With regard to ": "About ",
    "In light of ": "Given ",
    "In terms of ": "For ",
    "On the other hand, ": "But ",
    "Having said that, ": "That said, ",
    "That being said, ": "That said, ",
    "As previously mentioned, ": "",
    "As stated earlier, ": "",
    "As we have seen, ": "",
    "Moving forward, ": "",
    "Going forward, ": "",
    "In this article, we will ": "We'll ",
    "In this guide, we will ": "Let's ",
    "Let's dive in": "Here's the deal",
    "Let's delve into": "Let's look at",
    "Let's explore": "Let's look at",
}

# Overly formal connectors → casual ones
AI_CONNECTORS = {
    "However, ": ["But ", "Though ", "That said, "],
    "Therefore, ": ["So ", "That's why ", "Because of that, "],
    "Thus, ": ["So ", "That's why "],
    "Hence, ": ["So ", "That's why "],
    "Nonetheless, ": ["Still, ", "Even so, ", "But "],
    "Conversely, ": ["On the flip side, ", "But "],
    "Specifically, ": ["In particular, ", "More exactly, "],
    "Essentially, ": ["Basically, ", "Really, "],
    "Fundamentally, ": ["At its core, ", "Basically, "],
    "Undoubtedly, ": ["Clearly, ", "No question, "],
    "Evidently, ": ["Clearly, ", "Obviously, "],
    "Remarkably, ": ["Interestingly, ", "Surprisingly, "],
    "Notably, ": ["Interestingly, ", "Worth noting, "],
    "Significantly, ": ["More importantly, ", "A big deal — "],
    "Importantly, ": ["Key thing — ", "What matters is "],
}

# Repetitive AI sentence structures
AI_STRUCTURES = [
    (
        r"This (?:approach|method|technique|strategy) (?:allows|enables|permits) (?:us|you|one) to",
        lambda m: random.choice(
            ["This lets you", "This way you can", "With this you can"]
        ),
    ),
    (
        r"By (\w+ing) (.+?), (?:you|we|one) can",
        lambda m: f"If you {m.group(1).lower()} {m.group(2)}, you can",
    ),
    (
        r"(?:This|It) (?:is|has been) (?:widely|broadly|generally) (?:recognized|acknowledged|accepted) that",
        lambda m: random.choice(
            ["Most people agree that", "It's well known that", "Everyone knows"]
        ),
    ),
    (
        r"One of the (?:most|key|primary|main) (?:significant|important|crucial|critical) (?:aspects|elements|factors|components) (?:of|in)",
        lambda m: random.choice(
            ["A big part of", "What really matters in", "The key thing about"]
        ),
    ),
    (
        r"(?:It is|It's) (?:important|crucial|essential|vital|imperative) to (?:note|understand|recognize|acknowledge) that",
        lambda m: random.choice(
            ["Keep in mind that", "Worth knowing —", "Here's the thing —"]
        ),
    ),
]


# ═══════════════════════════════════════════════════════════════
# Humanizer Engine
# ═══════════════════════════════════════════════════════════════


class Humanizer:
    def __init__(self, level="medium"):
        self.level = level
        self.stats = {
            "words_replaced": 0,
            "starters_fixed": 0,
            "connectors_fixed": 0,
            "structures_fixed": 0,
            "formatting_fixed": 0,
        }

    def humanize(self, text):
        """Main entry point — applies all transformations."""
        text = self._fix_ai_starters(text)
        text = self._replace_ai_words(text)
        text = self._fix_connectors(text)
        text = self._fix_structures(text)
        text = self._fix_excessive_formatting(text)
        text = self._vary_sentence_length(text)
        text = self._fix_paragraph_starters(text)

        if self.level == "heavy":
            text = self._add_casual_touches(text)

        text = self._clean_whitespace(text)
        return text

    def _replace_ai_words(self, text):
        for ai_word, replacements in AI_WORDS.items():
            pattern = re.compile(r"\b" + re.escape(ai_word) + r"\b", re.IGNORECASE)
            matches = pattern.findall(text)
            for match in matches:
                replacement = random.choice(replacements)
                # Preserve capitalization
                if match[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                text = text.replace(match, replacement, 1)
                self.stats["words_replaced"] += 1
        return text

    def _fix_ai_starters(self, text):
        for starter, replacement in AI_STARTERS.items():
            if starter in text:
                text = text.replace(starter, replacement)
                self.stats["starters_fixed"] += 1
        return text

    def _fix_connectors(self, text):
        for connector, replacements in AI_CONNECTORS.items():
            while connector in text:
                replacement = random.choice(replacements)
                text = text.replace(connector, replacement, 1)
                self.stats["connectors_fixed"] += 1
        return text

    def _fix_structures(self, text):
        for pattern, replacement_fn in AI_STRUCTURES:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for match in reversed(matches):
                replacement = replacement_fn(match)
                text = text[: match.start()] + replacement + text[match.end() :]
                self.stats["structures_fixed"] += 1
        return text

    def _fix_excessive_formatting(self, text):
        # Remove excessive bold markers in markdown
        bold_count = text.count("**")
        if bold_count > 10:
            # Keep some bold but remove excessive
            parts = text.split("**")
            result = []
            for i, part in enumerate(parts):
                if i % 2 == 1 and random.random() > 0.4:
                    result.append(part)  # Remove bold from this one
                else:
                    result.append(part)
                    if i < len(parts) - 1:
                        result.append("**" if i % 2 == 0 else "**")
            text = "".join(result)
            self.stats["formatting_fixed"] += 1

        # Remove excessive bullet points that could be prose
        lines = text.split("\n")
        bullet_streak = 0
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("- ", "• ", "* ")) and not stripped.startswith(
                "---"
            ):
                bullet_streak += 1
                if bullet_streak > 6 and self.level in ("medium", "heavy"):
                    # Convert to prose
                    content = stripped.lstrip("-•* ").strip()
                    if new_lines and not new_lines[-1].strip().endswith("."):
                        new_lines[-1] = new_lines[-1].rstrip() + ". " + content
                    else:
                        new_lines.append(content)
                    self.stats["formatting_fixed"] += 1
                    continue
            else:
                bullet_streak = 0
            new_lines.append(line)
        text = "\n".join(new_lines)

        return text

    def _vary_sentence_length(self, text):
        """Break up strings of same-length sentences."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        if len(sentences) < 3:
            return text

        result = []
        for i, sentence in enumerate(sentences):
            # Occasionally merge short sentences
            if (
                i > 0
                and len(sentence.split()) < 6
                and len(result[-1].split()) < 8
                and random.random() > 0.6
                and self.level in ("medium", "heavy")
            ):
                connector = random.choice([" — ", ", and ", ". Plus, "])
                sentence_lower = (
                    sentence[0].lower() + sentence[1:] if sentence else sentence
                )
                result[-1] = result[-1].rstrip(".!?") + connector + sentence_lower
            else:
                result.append(sentence)

        return " ".join(result)

    def _fix_paragraph_starters(self, text):
        """Fix AI's habit of starting every paragraph the same way."""
        paragraphs = text.split("\n\n")
        starters_seen = set()

        for i, para in enumerate(paragraphs):
            if not para.strip():
                continue
            first_word = para.strip().split()[0] if para.strip().split() else ""
            if first_word in starters_seen and first_word in (
                "The",
                "This",
                "These",
                "It",
                "In",
            ):
                alternatives = {
                    "The": ["One", "A", "What's interesting —"],
                    "This": ["That", "Here,", "What this means —"],
                    "These": ["Those", "All of these", "Each of these"],
                    "It": ["That", "What", "Here's the thing —"],
                    "In": ["When it comes to", "For", "Within"],
                }
                if first_word in alternatives:
                    replacement = random.choice(alternatives[first_word])
                    paragraphs[i] = replacement + para.strip()[len(first_word) :]
            starters_seen.add(first_word)

        return "\n\n".join(paragraphs)

    def _add_casual_touches(self, text):
        """Add subtle casual markers (heavy mode only)."""
        casual_insertions = {
            ". This is ": [". This is ", ". Look, this is ", ". Honestly, this is "],
            ". It is ": [". It's ", ". Really, it's ", ". Truth is, it's "],
            ". There is ": [". There's ", ". Turns out there's "],
            ". We can ": [". We can ", ". You can actually "],
            ". You should ": [". You should ", ". Seriously, you should "],
        }

        for formal, casual_options in casual_insertions.items():
            if formal in text and random.random() > 0.5:
                text = text.replace(formal, random.choice(casual_options), 1)

        return text

    def _clean_whitespace(self, text):
        """Clean up any double spaces or weird whitespace."""
        text = re.sub(r"  +", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()
        return text

    def get_stats(self):
        total = sum(self.stats.values())
        return self.stats, total


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="humanize-text — Transform AI-generated text into natural writing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  humanize "Your AI text here"
  humanize -f essay.txt
  humanize -f input.md -o output.md
  humanize -f input.txt --level heavy
  cat article.txt | humanize
  echo "Utilize this tool" | humanize

Levels:
  light    — Replace obvious AI words only
  medium   — Words + sentence structure + formatting (default)
  heavy    — Full rewrite with casual tone

https://github.com/Koi725/humanize-text
        """,
    )

    parser.add_argument("text", nargs="?", help="Text to humanize (or use -f for file)")
    parser.add_argument("-f", "--file", help="Input file path (.txt, .md)")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument(
        "--level",
        choices=["light", "medium", "heavy"],
        default="medium",
        help="Humanization level (default: medium)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show transformation stats"
    )
    parser.add_argument(
        "--version", action="version", version=f"humanize-text v{VERSION}"
    )
    parser.add_argument(
        "--diff", action="store_true", help="Show before/after comparison"
    )

    args = parser.parse_args()

    # Get input text
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print(
            "Error: No input provided. Use 'humanize --help' for usage.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not text.strip():
        print("Error: Empty input.", file=sys.stderr)
        sys.exit(1)

    # Humanize
    humanizer = Humanizer(level=args.level)
    original = text
    result = humanizer.humanize(text)

    # Output
    if args.diff:
        print("═══ BEFORE ═══")
        print(original[:500] + ("..." if len(original) > 500 else ""))
        print("\n═══ AFTER ═══")
        print(result[:500] + ("..." if len(result) > 500 else ""))
        print()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✓ Saved to {args.output}")
    elif not args.diff:
        print(result)

    # Stats
    if args.stats:
        stats, total = humanizer.get_stats()
        print(f"\n── Stats ──", file=sys.stderr)
        print(f"  Words replaced:     {stats['words_replaced']}", file=sys.stderr)
        print(f"  Starters fixed:     {stats['starters_fixed']}", file=sys.stderr)
        print(f"  Connectors fixed:   {stats['connectors_fixed']}", file=sys.stderr)
        print(f"  Structures fixed:   {stats['structures_fixed']}", file=sys.stderr)
        print(f"  Formatting fixed:   {stats['formatting_fixed']}", file=sys.stderr)
        print(f"  Total changes:      {total}", file=sys.stderr)


if __name__ == "__main__":
    main()
