# humanize-text# ✍️ humanize-text

**Transform AI-generated text into natural, human-sounding writing. From your terminal.**

AI detectors flag your text? Your writing sounds like ChatGPT? This tool fixes that.

```bash
humanize "It is important to note that utilizing robust methodologies facilitates seamless collaboration."
# Output: "Worth knowing — using solid methods makes collaboration smooth."
```

No API keys. No cloud service. Runs 100% locally. Zero dependencies.

---

## Install

```bash
# Option 1: pip
pip install humanize-text

# Option 2: Clone and run directly
git clone https://github.com/Koi725/humanize-text.git
cd humanize-text
python humanize.py "your text here"
```

---

## Usage

```bash
# Direct text
humanize "Your AI-generated text here"

# From file
humanize -f essay.txt

# File to file
humanize -f input.md -o output.md

# Pipe from stdin
cat article.txt | humanize

# With stats
humanize -f input.txt --stats

# Before/after comparison
humanize -f input.txt --diff

# Heavy mode (more casual)
humanize -f input.txt --level heavy
```

---

## What It Fixes

### 1. AI Vocabulary

Words that AI loves but humans rarely use:

| AI Says        | Humanized          |
| -------------- | ------------------ |
| utilize        | use                |
| leverage       | take advantage of  |
| facilitate     | help               |
| comprehensive  | complete, thorough |
| furthermore    | also, plus         |
| delve into     | dig into, explore  |
| robust         | solid, reliable    |
| seamless       | smooth, clean      |
| groundbreaking | new, innovative    |
| paramount      | really important   |
| plethora       | a lot of           |

**200+ word replacements** built in.

### 2. AI Sentence Starters

Removes the filler phrases AI puts at the start of sentences:

| AI Starts With                          | Humanized                     |
| --------------------------------------- | ----------------------------- |
| "It is worth noting that..."            | (removed — gets to the point) |
| "It is important to understand that..." | (removed)                     |
| "In order to..."                        | "To..."                       |
| "In today's digital age..."             | "These days..."               |
| "Let's delve into..."                   | "Let's look at..."            |

### 3. Formal Connectors

Replaces stiff transitions with natural ones:

| AI Connector  | Humanized              |
| ------------- | ---------------------- |
| However,      | But, / Though,         |
| Therefore,    | So, / That's why,      |
| Furthermore,  | Also, / Plus,          |
| Nevertheless, | Still, / Even so,      |
| Consequently, | So, / Because of this, |

### 4. AI Sentence Patterns

Restructures sentences that follow AI templates:

| AI Pattern                               | Humanized              |
| ---------------------------------------- | ---------------------- |
| "This approach enables us to..."         | "This lets you..."     |
| "It is widely recognized that..."        | "Most people agree..." |
| "One of the most significant factors..." | "A big part of..."     |

### 5. Formatting Cleanup

- Removes excessive bold/emphasis
- Converts overly long bullet lists to prose
- Fixes paragraph starters that all begin the same way
- Varies sentence length for natural rhythm

---

## Levels

```bash
humanize -f input.txt --level light    # AI words only
humanize -f input.txt --level medium   # Words + structure + formatting (default)
humanize -f input.txt --level heavy    # Full rewrite, casual tone
```

| Level    | What It Changes                              |
| -------- | -------------------------------------------- |
| `light`  | Replaces obvious AI vocabulary               |
| `medium` | Vocabulary + sentence structure + formatting |
| `heavy`  | Everything + adds casual tone markers        |

---

## Example

**Input (AI-generated):**

```
It is important to note that utilizing robust methodologies is paramount
for facilitating seamless collaboration in today's digital age. Furthermore,
leveraging cutting-edge technologies enables organizations to streamline
their comprehensive workflows. Nevertheless, it is crucial to understand
that this multifaceted approach encompasses various intricate components.
```

**Output (humanized, medium level):**

```
Using solid methods is really important for making collaboration smooth
these days. Also, taking advantage of modern tech helps organizations
simplify their full workflows. Still, keep in mind that this complex
approach covers a lot of detailed parts.
```

---

## Stats Mode

```bash
humanize -f essay.txt --stats

── Stats ──
  Words replaced:     23
  Starters fixed:     4
  Connectors fixed:   7
  Structures fixed:   2
  Formatting fixed:   3
  Total changes:      39
```

---

## How It Works

No AI, no API calls, no cloud. Just pattern matching and replacement rules built from analyzing thousands of AI-generated texts. The tool identifies:

1. **Vocabulary patterns** — words AI overuses that humans rarely say
2. **Structural patterns** — sentence templates AI defaults to
3. **Formatting patterns** — excessive lists, bold, and repetitive starters
4. **Flow patterns** — same-length sentences, formal connectors

Each pattern has multiple replacement options chosen randomly, so running the tool twice on the same text produces slightly different results — just like a human would write it differently each time.

---

## Contributing

Found an AI word or pattern that should be added? PRs are welcome.

1. Fork the repo
2. Add patterns to the dictionaries in `humanize.py`
3. Test with `python humanize.py --diff -f test.txt`
4. Open a Pull Request

---

## License

MIT — do whatever you want with it.

---

**Built by [Kousha Rezaei](https://kousharezaei.dev)** — because AI-generated text shouldn't sound like AI-generated text.

If this saved you time, give it a ⭐
