# GPU Benchmark Collector

This repository collects benchmarking results of various AI models (e.g., YOLOv5, YOLOv9) across different GPU instances.

## 📂 Structure
- `run_benchmark.py`: Benchmark execution script
- `results/summary`: Aggregated benchmark results (e.g., FPS, latency, cost-performance)
- `results/per_instance`: Per-GPU raw results
- `env_info`: Hardware specs and OS information
- `notebooks`: Optional Jupyter notebooks for analysis

## 🚀 How to Run
```bash
python run_benchmark.py --gpu A5000 --model yolov5m
