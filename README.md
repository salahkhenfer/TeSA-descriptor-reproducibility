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

## Provenance note

The three descriptor sets were generated in separate, independent LLM sessions
using Gemini 2.5 Pro and GPT-5.6-Sol with the exact dataset-specific prompts
provided in this repository. The default settings of the corresponding
interfaces were used. Unavailable metadata are stated explicitly.

No dataset images, API keys, model checkpoints, or private data are included.
