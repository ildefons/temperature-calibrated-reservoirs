# v18.3 - safe-region metric consistency

This update resolves inconsistencies uncovered by the repaired M21 audit.

Changes:
- restored each study's native absolute safe-region tolerance: `epsilon_abs=0.005` for the controlled synthetic/path study and `epsilon_abs=0.002` for the two real-world sensor studies;
- corrected the synthetic M21 safe-region width from `2.40/13` to `3.23/13` and the matched containment enrichment from `3.73x` to `3.12x`;
- replaced mixed window-level/full-test "best-safe gain" values with a common full-test `safe_best_gain_vs_default` definition in the path-comparison, real-data, and M21 summary tables;
- updated the path-comparison full-test gains to temperature `0.00230`, gain `0.00241`, leak-rate `0.00422`, and sparsity `0.00015`;
- updated the Appliances Energy full-test temperature best-safe gain to `0.00014`; Air Quality remains `0.01635`;
- regenerated Figure 7 using the same full-test best-safe gain definition for the synthetic and Appliances comparisons;
- restricted the explicit epsilon-sensitivity claim to the fully regenerated synthetic M20a audit, while retaining the native real-data summaries.

No theoretical equations or distribution-shift results were changed.
