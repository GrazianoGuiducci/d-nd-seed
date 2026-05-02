# dnd_kernel_z_12_813_l_ordine_sequenziale

Informed predictor for sequences with hidden Markov structure. Exploits the
finding that the Markov transition matrix of prime gap residues mod 6 carries
massive structural information (z=12,813 vs shuffle baseline), while frequency
distributions alone are blind to sequential order. The kernel discriminates
structured sequences from shuffled ones using transition matrix fingerprints:
determinant, structural zeros, and full matrix distance.

**Operational limit**: verified on 400 trials with prime gaps mod 6 up to 200k.
Generalization to different domains requires re-verification.

## Use case

Kernel cognitivo D-ND installabile per agenti LLM: predittore informato per
sequenze con struttura Markov nascosta. Plugin riusabile per anti-loop guardrail
e compressione context strutturata.

## Install

```bash
pip install -e .
```

## Quick start

```python
from dnd_kernel_z_12_813_l_ordine_sequenziale import KernelDND

kernel = KernelDND(prime_limit=200_000)
result = kernel.run_ab_test(n_trials=200, chunk_size=500)
print(f"Informed: {result['informed_score']:.4f}")
print(f"Naive:    {result['naive_score']:.4f}")
print(f"Delta:    {result['delta']:.4f}")
```

## Verification

Stage 4 verdict: **PASS**

| Metric         | Value   |
|----------------|---------|
| naive_score    | 0.3117  |
| informed_score | 0.9975  |
| delta          | +0.6858 |
| n_trials       | 400     |

## License

MIT — see [LICENSE](LICENSE).

## Lineage

- Discovery cycle: `20260501_1256`
- Finding: z=12,813 — sequential order carries massive information
- Product ID: `20260501_1256_finding2_kernel_z-12813-lordine-sequenziale-porta-informazione`
- Lab: [D-ND_LAB](https://github.com/GrazianoGuiducci/D-ND_LAB)
