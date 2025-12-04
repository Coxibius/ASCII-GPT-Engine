# 🧠 ASCII-GPT: Self-Correction and Structural Generation Research

> An empirical study on training Small Language Models (GPT-2) to understand visual structures (ASCII Art) through iterative refinement assisted by AI agents.

## 📊 Project Abstract
This project documents the evolution of a language model trained to "draw" with characters. The process was driven 100% by prompt engineering and collaboration between multiple AI agents to correct hallucination and coding errors.

- **Development Time:** 48 hours.
- **Hardware:** Google Colab (T4) -> Kaggle (T4 x2).
- **Architecture:** GPT-2 Small (Fine-tuned).

## 🧬 Model Evolution Log

### 👶 Phase 1-2: Texture Learning
- **Dataset:** Small Travian dataset (Manual curation).
- **Outcome:** The model learned basic textures but lacked geometry.
- **Failure Mode:** Incoherent shapes.

### 🕷️ Phase 3: The "White Canvas" Problem
- **Dataset:** Massive scraping from `asciiart.eu`.
- **Outcome:** Model overfitted to whitespace (the most common token).
- **Failure Mode:** Empty outputs due to greedy decoding.

### 💪 Phase 4-5: Hardcore Training (Current Stable)
- **Strategy:** High-epoch training with low learning rate.
- **Outcome:** Perfect structure, replication of complex shapes (castles, swords).
- **Interesting Artifact:** The model learned to replicate famous ASCII artist signatures (e.g., `jgs`, `vk`).

### 🧼 Phase 6: Data Sanitization (Current)
- **Action:** Developed a Python Regex script to remove 2,000+ artist signatures from the training data.
- **Goal:** Reduce hallucinations and force the model to close visual structures instead of writing text.

## 📂 Repository Structure
- `/docs`: Daily logs and iteration contexts (Research Diaries).
- `/scripts`: Custom Python tools for data mining and cleaning.
- `/notebooks`: Reproducible training code (Jupyter).

## 💾 Model Downloads
Pre-trained models (.zip) are available in the [Releases Section](https://github.com/Coxibius/ASCII-GPT-Engine/releases).
