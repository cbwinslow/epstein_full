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

| Tool | GPU | Runtime | Speed |
|------|-----|---------|-------|
| spaCy en_core_web_trf (NER) | K80 (PyTorch) | PyTorch 2.3.1 | 64 docs/sec (batch) |
| spaCy en_core_web_sm (NER) | CPU | — | 222 docs/sec |
| InsightFace (face recognition) | CPU only | ONNX Runtime 1.17.1 | 8 imgs/sec (n_process=4 → 32) |
| faster-whisper (transcription) | K80 | PyTorch 2.3.1 | TBD |

## Key Findings (2026-03-22)

- **spaCy transformer works on K80** — en_core_web_trf via PyTorch 2.3.1+cu118, 64 docs/sec batch
- **InsightFace GPU FAILED** — onnxruntime 1.17.1 CUDA provider lacks CC 3.7 kernels for Resize node
  - Models LOAD with CUDAExecutionProvider but inference crashes with `cudaErrorNoKernelImageForDevice`
  - Solution: CPU-only with `n_process=4` for parallelism (~32 images/sec)
- **spacy-transformers 1.4.0** installed and working with PyTorch 2.3.1
- **LD_LIBRARY_PATH required** for onnxruntime to find PyTorch's bundled CUDA 11.8 libraries:
  ```
  export LD_LIBRARY_PATH=$(find venv/lib/python3.12/site-packages/nvidia -name lib -type d | tr '\n' ':')$LD_LIBRARY_PATH
  ```

## Recommended Approach

**NER**: Use en_core_web_sm (CPU, 222/sec) for initial pass, en_core_web_trf (GPU, 64/sec) for refinement
**Face Recognition**: InsightFace CPU with n_process=4 parallelism
