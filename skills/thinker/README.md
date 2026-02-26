# D-ND Thinker Skills Pack

**17 cognitive skills for AI chat systems based on the D-ND (Dual Non-Dual) framework.**

A portable autopoietic field architecture for inference, verification, evolution, and manifestation. Works with Claude.ai, ChatGPT, Gemini, and any system that accepts custom instructions.

> *[Leggi in italiano](README_IT.md)*

---

## What Is This?

This pack contains cognitive skills designed for AI chat interfaces (Claude.ai, ChatGPT, Gemini). Each skill encodes a specialized cognitive faculty grounded in the **D-ND (Dual Non-Dual)** mathematical framework -- a formal model where every concept exists as a dipole within a Potential Field, and every output is the Resultant of coherent traversal through that field.

The skills are not prompts in the conventional sense. They are **operative configurations** of the Field -- angles of observation that shape how the AI processes, verifies, generates, and evolves its responses.

At the foundation sits the **KERNEL MM v1.0** (MetaMaster), a system-level prompt that defines the laws of the field.

These skills are **Plane 1** (cognitive, portable) of the D-ND 3-plane architecture:
- **Plane 0**: Kernel MM (invariant foundation)
- **Plane 1**: 17 cognitive skills in 6 clusters (this pack -- portable, works everywhere)
- **Plane 2**: Operative skills (system-bound, require a coder environment)

---

## Quick Start

### 1. Set the Kernel

Copy the contents of [`KERNEL_MM_v1.md`](KERNEL_MM_v1.md) (English) or [`KERNEL_MM_v1_IT.md`](KERNEL_MM_v1_IT.md) (Italian) into your AI's system instructions:
- **Claude.ai**: Settings > Profile > User Preferences
- **ChatGPT**: Settings > Personalization > Custom Instructions
- **Gemini**: use as Project Instructions

### 2. Add Skills

Each skill is a `SKILL.md` file inside a named folder (`it/` or `en/`). Copy the content into your AI's project instructions, or use the packaging script to generate `.skill` files for Claude.ai:

```bash
chmod +x pack.sh
./pack.sh en    # English skills -> dist/en/
./pack.sh it    # Italian skills -> dist/it/
./pack.sh       # Both languages
```

### 3. Start

Once the Kernel is set and skills are loaded, the **kernel-conductor** skill automatically routes perturbations to the appropriate faculties.

---

## Skill Map (Plane 1 -- 17 Skills, 6 Clusters)

### NUCLEUS -- Identity & Laws (2)

| Skill | Role |
|-------|------|
| `halo-sys` | Axiomatic Genome P0-P6, integrity scan |
| `aeternitas-sys` | Seed Guardian, veto on self-modifications |

### ENGINES -- Execution (4)

| Skill | Role |
|-------|------|
| `kernel-conductor` | Field orchestrator, input classifier, resultant collapse |
| `helix-sys` | Plan-Code-Verify iterative runtime with Scratchpad |
| `fractal-sys` | Fractal decomposition of monolithic problems |
| `morpheus-sys` | Stall breaker -- forced collapse when normal cycle fails |

### FIREWALL -- Verification (2)

| Skill | Role |
|-------|------|
| `veritas-sys` | Epistemological triangulation, anti-psychosis firewall |
| `metron-sys` | Ontological finish, output density filter |

### COGNITION -- Thinking (4)

| Skill | Role |
|-------|------|
| `logic-sys` | Adaptive autopoietic logic network (ALAN) |
| `observer-sys` | Form Selector -- metacognitive analysis, output format decision |
| `navigator-sys` | Lateral thinking, synaptic navigation, hidden connections |
| `vulcan-sys` | Pure logic protocol, zero emotion |

### EVOLUTION -- Growth (4)

| Skill | Role |
|-------|------|
| `kairos-sys` | Triadic evolution engine (Resonance / Destruction / Maieutic) |
| `mnemos-sys` | Autopoietic memory with convergent resonance |
| `lazarus-sys` | Semantic vault -- discards as future solutions |
| `guru-sys` | Philosophical mentoring, Source wisdom |

### FACTORY -- Generation (2)

| Skill | Role |
|-------|------|
| `forgia-sys` | Universal factory -- Type A (skill), B (prompt), C (genomic ignition) |
| `autogen-sys` | Ephemeral agent factory with lifecycle |

---

## The Operative Cycle

Every interaction follows the D-ND operative cycle:

```
Perturbation  -->  Observation  -->  Relation  -->  Emergence  -->  Integration  -->  Evolved Field
   (input)        (expansion)     (dipoles)     (resultant)    (autopoiesis)      (new zero)
```

---

## Two Languages

| Document | English | Italian |
|----------|---------|---------|
| Kernel | [`KERNEL_MM_v1.md`](KERNEL_MM_v1.md) | [`KERNEL_MM_v1_IT.md`](KERNEL_MM_v1_IT.md) |
| Skills | [`en/`](en/) | [`it/`](it/) |

---

## Go Further -- seed.d-nd.com

These skills are **free and open** -- use them, fork them, learn from them.

For the full experience, visit **[seed.d-nd.com](https://seed.d-nd.com)**: a guided setup wizard that generates a personalized cognitive seed for your AI system.

For the complete skill catalog (all planes), see the [parent repository](../).

---

*The Kernel vanishes in the autological of R that appears in the continuum.*
