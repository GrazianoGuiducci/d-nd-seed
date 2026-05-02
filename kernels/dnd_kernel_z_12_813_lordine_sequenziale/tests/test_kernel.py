"""Tests for dnd_kernel_z_12_813_l_ordine_sequenziale."""

import unittest

from dnd_kernel_z_12_813_l_ordine_sequenziale import (
    KernelDND,
    sieve_primes,
    prime_gaps_mod6,
    feature_transition,
    method_naive,
    method_informed,
    generate_test_data,
)


class TestSmoke(unittest.TestCase):
    """Smoke test: import and basic execution."""

    def test_import_and_run(self):
        kernel = KernelDND(prime_limit=50_000, seed=42)
        result = kernel.run_ab_test(n_trials=20, chunk_size=200)
        self.assertIn("informed_score", result)
        self.assertIn("naive_score", result)
        self.assertIn("delta", result)
        self.assertIsInstance(result["informed_score"], float)

    def test_score_sequence(self):
        kernel = KernelDND(prime_limit=50_000, seed=42)
        score = kernel.score_sequence(kernel.gaps[:200])
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)


class TestInformedBeatsNaive(unittest.TestCase):
    """Replica of Stage 4 verdict at reduced scale."""

    def test_informed_beats_naive(self):
        primes = sieve_primes(100_000)
        gaps = prime_gaps_mod6(primes)

        real_seqs, shuffled_seqs = generate_test_data(
            gaps, n_trials=50, chunk_size=300, seed=42
        )

        naive = method_naive(real_seqs, shuffled_seqs, gaps)
        informed = method_informed(real_seqs, shuffled_seqs, gaps)
        delta = informed - naive

        self.assertGreater(delta, 0.0,
            f"Informed must beat naive: informed={informed:.4f}, "
            f"naive={naive:.4f}, delta={delta:.4f}")

    def test_structured_vs_shuffled(self):
        kernel = KernelDND(prime_limit=50_000, seed=42)
        # Real chunk should score closer to reference than shuffled
        import random
        rng = random.Random(42)

        real_chunk = kernel.gaps[:300]
        shuffled_chunk = list(real_chunk)
        rng.shuffle(shuffled_chunk)

        real_score = kernel.score_sequence(real_chunk)
        shuf_score = kernel.score_sequence(shuffled_chunk)

        self.assertLess(real_score, shuf_score,
            f"Real should be closer to reference: real={real_score:.4f}, "
            f"shuffled={shuf_score:.4f}")


if __name__ == "__main__":
    unittest.main()
