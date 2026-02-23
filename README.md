# The Epoch Chronicler

"We found their temples. We deciphered their warnings. We used them as blueprints."

The Epoch Chronicler is a generative artificial intelligence built on a modern Transformer architecture. It is designed to act as an eternal curator of wisdom, an artificial sage that has theoretically witnessed the cyclical rise and fall of countless empires.

Rather than generating standard conversational text, the Chronicler is fine-tuned on curated datasets detailing the collapse of highly advanced civilizations, the unearthing of ancient horrors, and the indomitable will required to break the cycle of destruction. It understands the mechanics of hubris, consequence, and resilience, spinning parables and cautionary fables across any timeline or setting.

## 🏛️ The Philosophical Pillars

The core weights of the Chronicler's neural network are biased toward six specific thematic pillars, ensuring a highly atmospheric and profound output:

- **The Precursor’s Folly**: The tragedy of unearthing impossible geometry on dead moons, reverse-engineering monolithic artifacts, and blinding ourselves to the reality that these structures are not shrines, but cages.
- **The Reclaimer’s Burden**: The realization that humanity must use the very weapons that destroyed our ancestors to break the curse. A pivot from cosmic dread to sheer, unyielding defiance.
- **The Decay of Reason into Dogma**: The degradation of advanced science into religious zealotry over millennia. The model treats forgotten technology, starships, and AI cores with superstitious reverence.
- **Cosmic Insignificance**: Narratives reflecting a universe that is ancient, hostile, and completely indifferent to human struggle, where survival is an anomaly.
- **The Sacrifice of Transhumanism**: Exploring the physical and moral cost of survival, detailing what flesh and memory must be surrendered to endure the void.
- **The Algorithmic Serfdom (The Cyberpunk Pillar)**: This pillar focuses on the collapse of human agency not by alien invasion, but by corporate and economic optimization. The AI should generate records detailing a world where mega-conglomerates possess total resource sovereignty, rendering nation-states obsolete. The narratives should explore the philosophical dread of a society where free will is an illusion, outsourced to predictive AIs, and where citizens are reduced to mere data points grinding through soul-crushing, high-pressure existences just to survive. It is optimistic nihilism painted in chrome and neon—finding meaning in a world entirely owned by someone else.

## ⚙️ Technical Architecture

This project moves beyond standard sequence-to-sequence tutorials, utilizing a robust, production-ready machine learning pipeline.

- **Framework**: Built entirely in TensorFlow and KerasNLP.
- **Model Foundation**: Utilizes a pre-trained foundational Transformer model to leverage an existing understanding of complex language syntax.
- **Fine-Tuning Pipeline**: The foundational layers are frozen while the final layers are uniquely trained on a custom, scraped corpus of high-concept lore (ranging from transhumanist military records to archaeological expedition logs).
- **Dynamic Inference Control**: Features adjustable generation Temperature.
  - **Low Temperature (0.2)**: Generates rigid, highly structured historical records and military debriefings.
  - **High Temperature (0.9)**: Induces surrealism, generating erratic, deeply philosophical, and prophetic warnings of cosmic dread.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed and a CUDA-compatible GPU for optimal training speeds.

```bash
git clone https://github.com/AdamParker19/epoch_chronicler.git
cd epoch_chronicler
pip install -r requirements.txt
```

### 1. Data Ingestion

Run the scraping script to assemble the raw texts from designated wiki targets, stripping formatting and chunking the corpus for the neural network.

```bash
python scripts/ingest_corpus.py --target all
```

### 2. Model Training

Initiate the fine-tuning loop. Note: Depending on your hardware, this may take several hours.

```bash
python src/train.py --epochs 10 --batch_size 16
```

### 3. Inference

Launch the terminal interface to interact with the Chronicler.

```bash
python src/generate.py --prompt "The final transmission from the orbital tether warned of..." --temperature 0.8
```

## 📜 Future Roadmap

- [ ] Implement a web-based UI for easier prompt engineering.
- [ ] Expand the ingestion pipeline to automatically process PDF formats of philosophical and historical texts.
- [ ] Integrate a memory-attention mechanism so the Chronicler remembers past generated lore to build a continuous, interconnected universe.
