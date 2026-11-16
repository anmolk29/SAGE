# ResNet-18 ONNX weights

`resnet18-v1-7.onnx` is the ImageNet-pretrained ResNet-18 v1 model from the [ONNX Model Zoo Hugging Face repository](https://huggingface.co/onnxmodelzoo/resnet18-v1-7). Its model card identifies the license as Apache-2.0. The official model card describes 224 × 224 RGB input, ImageNet mean/std normalization, and 1,000 ImageNet output scores. This project uses those fixed scores as features for a separate class-balanced logistic head trained on weak/manual conveyor labels.

- Model file SHA-256: `4e8f8653e7a2222b3904cc3fe8e304cd8b339ce1d05fd24688162f86fb6df52c`
- Downloaded file size: 46,820,737 bytes
- Download URL: `https://huggingface.co/onnxmodelzoo/resnet18-v1-7/resolve/main/resnet18-v1-7.onnx`
- Local inference runtime: ONNX Runtime CPU provider

The ImageNet model is not itself trained to identify conveyor anomalies. The linear head and clip-held-out evaluation are project-specific, exploratory transfer learning over weak labels; do not describe the base weights alone as an anomaly detector.
