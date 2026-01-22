# PRANA — AI-Based Disaster Impact Assessment & Relief Prioritization

PRANA is a modular, offline-capable decision-support system designed to help disaster response authorities **decide where to act first, why, and with what kind of help** in the critical hours following a natural disaster.

Rather than replacing human judgment, PRANA augments it by combining **machine perception (ML)** with **explainable, human-centric decision logic**.

---

## Problem

After floods, cyclones, or earthquakes, relief is delayed because:

* Damage assessment is manual and slow
* Field reports are incomplete or inconsistent
* Prioritization decisions are opaque and hard to justify

In disasters, **delay itself becomes a risk**.

---

## Solution

PRANA reduces assessment time from days to minutes by:

* Estimating damage severity directly from imagery using ML
* Combining damage with population vulnerability and access constraints
* Producing ranked, explainable priorities
* Recommending **actionable relief types**, not just scores

The system is designed to work **offline-first**, with modular data layers that can be swapped or upgraded without changing the core logic.

---

## Core Design Philosophy

* **ML for perception, not decisions**
* **Explainability over black-box outputs**
* **Human vulnerability over infrastructure-only metrics**
* **Graceful degradation in low-connectivity environments**

PRANA assists decisions — it does not replace responders.

---

## System Architecture

```
Perception Layer (ML)
  └─ Image → Damage Severity

Decision Engine (Core)
  ├─ Damage Severity
  ├─ Population Vulnerability
  ├─ Healthcare Access Risk
  └─ Time-Based Urgency

Action Layer
  └─ Relief Recommendation
```

Each layer is modular and independently testable.

---

## Machine Learning Model

PRANA uses a **pretrained convolutional neural network (ResNet-18)** as a feature extractor:

* No task-specific retraining required
* Robust across unseen disaster scenarios
* Fast inference suitable for edge or offline deployment

The model outputs a **normalized damage severity score (0–1)** which feeds into the decision engine.

ML provides *visual perception* — final prioritization remains explainable and rule-driven.

---

## Decision Logic (Explainable)

Priority scores are computed using a weighted combination of:

* Damage severity
* Population density
* Elderly and child vulnerability
* Distance to medical infrastructure
* Time since disaster

Each decision includes a clear **"Why this zone?"** explanation.

---

## Relief Recommendation

PRANA does not stop at ranking zones.

For each high-priority area, it recommends:

* Rescue & evacuation
* Medical aid or mobile clinics
* Food, shelter, and sanitation support

This closes the gap between **assessment and action**.

---

## User Interface

A lightweight Streamlit UI allows responders to:

* Upload disaster imagery
* Adjust time since disaster
* View ranked zones
* See recommended actions and explanations

The UI is a visualization layer — all intelligence lives in the engine.

---

## Offline & Deployment Readiness

* Models and data load locally
* No cloud dependency
* Works with partial or simulated inputs
* Designed for laptops or edge servers in disaster zones

---

## Hackathon Demo Strategy

**Round 1**: Decision intelligence with limited data

* Ranked zones
* Explainable priorities

**Round 2**: Adaptive intelligence

* ML-based damage perception
* Time-aware priority evolution
* Relief recommendations

Same system. Deeper intelligence.

---

## Technology Stack

* Python
* PyTorch & Torchvision
* Streamlit
* Modular script-based architecture

---

## Disclaimer

This prototype demonstrates **decision-support logic**, not final operational accuracy.
Real-world deployment requires region-specific calibration and official data sources.

---

## Impact

PRANA aligns with **AI for Social Good** by enabling:

* Faster emergency response
* Better allocation of limited resources
* Transparent and justifiable decision-making

In disasters, clarity saves time. Time saves lives.
