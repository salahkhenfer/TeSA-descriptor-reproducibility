# TeSA descriptor-generation reproducibility files

This repository contains the text resources used for the descriptor-generation
robustness experiment reported for **Training-Free Text-Subspace Alignment
(TeSA)**.

## Contents

- `prompts/`: the exact dataset-specific prompts, including every class name.
- `descriptors/generation_01_original/`: the original descriptors exported from
  `TAXONOMIES_RAW` in the TeSA experiment code. Two unused legacy NWPU keys
  (`residential` and `woodland`) are excluded because they are not among the 45
  NWPU-RESISC45 dataset classes and are never indexed by the evaluation loader.
- `descriptors/generation_02/` and `descriptors/generation_03/`: the two
  additional descriptor sets used in the robustness experiment.
- `metadata/generation_metadata.json`: the available provenance and generation
  information. Fields that were not recorded at generation time are explicitly
  marked as unavailable rather than reconstructed retrospectively.
- `results/descriptor_robustness_summary.csv`: the controlled CLIP/PE results
  reported in the manuscript, including means and standard deviations.
- `scripts/validate_descriptors.py`: a deterministic validator for class
  coverage, descriptor count, empty strings, and within-class duplicates.

Each JSON file maps an exact dataset class name to an array of ten concise,
visually observable descriptors. Within a descriptor set, the identical JSON
files were used by simple descriptor averaging, maximum similarity, CHiLS, and
TeSA. Therefore, the controlled comparison changes only the aggregation or
subspace-construction rule, not the descriptor vocabulary.

## Datasets

- UCM Land Use: 21 classes
- NWPU-RESISC45: 45 classes
- AID: 30 classes
- RSSCN7: 7 classes
- EuroSAT: 10 classes

## Validation

From the repository root, run:

```bash
python scripts/validate_descriptors.py
```

The validator expects ten unique, non-empty descriptor strings for every class
in every dataset and generation.

## Provenance note

The model/provider labels in `metadata/generation_metadata.json` reflect the
authors' reported provenance. Raw provider transcripts and exact sampling
values were not stored with all generations. The two additional sets were
preserved as distinct descriptor ensembles in the same Codex work session on
2026-09-25; consequently, this repository does not describe them as independent
stochastic API trials. Unavailable metadata are stated explicitly.

No dataset images, API keys, model checkpoints, or private data are included.
