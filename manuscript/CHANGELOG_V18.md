# CHANGELOG V18 - Human-reader and reproducibility consolidation

Version 18 is a presentation and reproducibility consolidation based on a full author reread and an external review. It keeps the established theory, experimental outputs, and numerical conclusions, while making the scientific narrative substantially more self-contained and easier to read without opening notebooks.

## Scientific framing

- Foregrounds allocation temperature as the main contribution: a distinct structural reservoir configuration axis controlling continuous recurrent-weight concentration while recurrent scale is normalized separately.
- Clarifies effective support as the entropy-equivalent number of equally weighted recurrent inputs. It is a continuous concentration measure, not a count of nonzero edges and not hard sparsity.
- Uses `allocation temperature` when needed to distinguish the recurrent control from output/logit temperature in ordinary machine-learning calibration.
- Adds a concise paper roadmap at the end of the Introduction.

## Theory and state evolution

- Retains the v17 clarification of the allocation-weighted mean score and the expanded entropy derivation.
- Explains reservoir-state generation explicitly: sequential recurrence from a zero initial state, followed by washout; no fixed-point solve is performed for each sample.
- Clarifies the difference between smooth allocation concentration and top-k edge removal.

## Methods and reproducibility

- Reorganizes the Methods around five scientific validation questions and links each question to the corresponding manuscript section, table, and figure.
- Moves notebook/module identifiers out of the main scientific narrative. They now appear only in Appendix C as a reproducibility map.
- Describes uncertainty positively in terms of the independent resampling unit and cluster bootstrap.
- Expands the distribution-shift protocol into short subsections for the candidate bank, pre-deployment conditions, held-out shifts, four compared policies, and the pre-deployment certified subset.
- States the random-substrate construction used in the robustness study: standard-normal off-diagonal scores, independent recurrent signs, excluded self-connections, and fixed substrates across temperature candidates.
- Derives the dense computational scaling for reservoir simulation and ridge-readout fitting directly from matrix-vector and normal-equation costs.

## Results presentation

- Rewrites the core validation around experimental questions rather than notebook names.
- Explicitly explains why the two reported containment summaries come from independent run panels and therefore have different denominators.
- Adds direct references to the relevant tables and figures throughout the validation sections.
- Replaces notebook-centric and checkpoint/revision language with experiment-centric descriptions.
- Renames the former revision-audit material as `Additional Validation of Sensitivity and Structural Confounds`.
- Simplifies the grid-density/reservoir-size robustness interpretation and explains singleton safe regions directly.
- Presents task-level distribution-shift means without emphasizing bootstrap confidence intervals based on only three substrates; shift-type intervals continue to resample nine task-substrate clusters.
- Adds a clear bridge between the one-dimensional temperature-path studies and the final two-dimensional temperature-leak distribution-shift study.
- Adds an operational-interpretation table explaining conservative responses to low/high path sensitivity and information-removing shifts.

## Related work

- Adds and differentiates Singh and Raman (2026), an entropic optimal-transport ESN with dynamic input-conditioned routing.
- Adds Bendi-Ouis and Hinaut (2025), Echo State Transformer, as adjacent work on learned/adaptive reservoir dynamics.
- Clarifies the distinction from graph attention and output-probability temperature scaling.

## Discussion, limitations, and conclusion

- Opens the Discussion by emphasizing the two main contributions: the structural parameterization and its empirical characterization.
- Keeps a concise dedicated Limitations section because the negative/null results materially delimit the claim.
- Rewrites the Conclusion to foreground allocation temperature as a reservoir-design coordinate and to separate structural sensitivity, available improvement, and label-free model choice.

## Reproducibility status

- The manuscript is self-contained with respect to the experimental design and interpretation.
- Appendix C maps manuscript claims to computational notebooks.
- The public archival repository URL remains the only submission-time placeholder and must be inserted once the repository release is created.

## Figure consolidation

- Recreated the primary path-sensitivity figure with plain practitioner-facing labels and only the two primary indicators.
- Recreated the robustness containment figure with descriptive configuration labels instead of internal experiment identifiers.
- Removed two redundant figures whose information was already carried by the tables and text, reducing figure overlap and eliminating notebook/checkpoint terminology embedded in old plot titles.
