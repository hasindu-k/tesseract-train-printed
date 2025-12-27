refer this chat
https://chatgpt.com/share/6942ab02-523c-8001-925e-83c2b6cf4dc0

make training MODEL_NAME=sin_eng_custom START_MODEL=sin TESSDATA=../tessdata/ DATA_DIR=../data/ MAX_ITERATIONS=500 LEARNING_RATE=0.001 LANG_TYPE=Indic

make training MODEL_NAME=sin_eng_custom \
START_MODEL=../data/sin_eng_custom/checkpoints/sin_eng_custom_19.784_441_500.checkpoint \
TESSDATA=../tessdata \
DATA_DIR=../data \
MAX_ITERATIONS=500 \
LEARNING_RATE=0.001 \
LANG_TYPE=Indic
