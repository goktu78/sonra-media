#!/bin/sh
# Ses hattı kurulumu: seslendirme modelleri + gerçek enstrüman soundfont
set -e
cd "$(dirname "$0")"
apt-get update -q >/dev/null 2>&1 || true
apt-get install -y -q fluidsynth fluid-soundfont-gm >/dev/null
pip install -q piper-tts kokoro-onnx soundfile mido --break-system-packages
mkdir -p models && cd models
[ -f kokoro.onnx ] || curl -sL -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices.bin ] || curl -sL -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
[ -d vits-piper-tr_TR-fahrettin-medium ] || (curl -sL https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fahrettin-medium.tar.bz2 | tar xj)
echo "ses hattı hazır"
