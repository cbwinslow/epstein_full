# Tier 3: GPU Compatibility

> GPU-specific findings. Read when working with ML/NLP/vision.
> Rank: 3 (medium priority).

## GPU Inventory

| GPU | Device | Model | CC | VRAM | PyTorch? | ONNX? |
|-----|--------|-------|-----|------|----------|-------|
| 0 | cuda:0 | Tesla K40m | 3.5 | 11GB | ❌ NO | ✅ Yes |
| 1 | cuda:1 | Tesla K80 | 3.7 | 12GB | ✅ Yes | ✅ Yes |
| 2 | cuda:2 | Tesla K80 | 3.7 | 12GB | ✅ Yes | ✅ Yes |

## Critical Findings

- **Driver 470.256.02** is the LATEST for Kepler — cannot upgrade beyond this
- **PyTorch 2.3.1+cu118** works on K80 WITHOUT driver upgrade
- **PyTorch 2.10+cu128** does NOT work — requires CUDA 12.8 (needs driver 525+)
- **Tesla K40m (CC 3.5)** too old for PyTorch — "no kernel image available"
- **ONNX Runtime GPU** works on ALL GPUs (K80 + K40m)

## Configuration

```bash
export CUDA_VISIBLE_DEVICES=1,2  # Exclude K40m from PyTorch workloads
```

## Tool Assignments

| Tool | GPU | Runtime |
|------|-----|---------|
| InsightFace (face recognition) | K40m or K80 | ONNX Runtime |
| Surya OCR | K40m or K80 | ONNX Runtime |
| spaCy NER (transformer) | K80 | PyTorch 2.3.1 |
| faster-whisper (transcription) | K80 | PyTorch 2.3.1 |
| sentence-transformers (embeddings) | K80 | PyTorch 2.3.1 |
