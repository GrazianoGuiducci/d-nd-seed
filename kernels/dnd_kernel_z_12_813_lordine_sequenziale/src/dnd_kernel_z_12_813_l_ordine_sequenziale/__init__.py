"""dnd_kernel_z_12_813_l_ordine_sequenziale — Informed predictor for hidden Markov structure."""

__version__ = "0.1.0"

from .kernel import (
    KernelDND,
    sieve_primes,
    prime_gaps_mod6,
    transition_matrix_3x3,
    det3,
    count_structural_zeros,
    feature_freq,
    feature_transition,
    method_naive,
    method_informed,
    generate_test_data,
)
