#!/bin/bash
set -e

##### NOTE
# This assumes that you have OpenFST and the Python bindings installed

DATA_DIR=en-de
SCRIPT_DIR=.
OUT_DIR=outputs
TRAIN_DATA=$DATA_DIR/train.en-de.low.filt
#TRAIN_DATA=$DATA_DIR/valid.en-de.low

mkdir -p $OUT_DIR

# *** Train n-gram language model and create an FST
echo "starting train-ngram..."
python $SCRIPT_DIR/train-ngram.py $TRAIN_DATA.en $OUT_DIR/ngram-fst.txt

# *** Implement 1: Train IBM Model 1 and find alignment
echo "train IBM model 2..."
python $SCRIPT_DIR/train-model2.py $TRAIN_DATA.de $TRAIN_DATA.en $OUT_DIR/alignment_train_f.txt
#
echo "train IBM model 2 reverse..."
python $SCRIPT_DIR/train-model2.py $TRAIN_DATA.en $TRAIN_DATA.de $OUT_DIR/alignment_train_e.txt
#
echo "intersection heuristic..."
python $SCRIPT_DIR/intersect.py $OUT_DIR/alignment_train_f.txt $OUT_DIR/alignment_train_e.txt $OUT_DIR/alignment_train_intersect.txt
#
echo "union heuristic..."
python $SCRIPT_DIR/union.py $OUT_DIR/alignment_train_f.txt $OUT_DIR/alignment_train_e.txt $OUT_DIR/alignment_train_union.txt
#
echo "grow-diag heuristic..."
python $SCRIPT_DIR/grow-diagonal.py $OUT_DIR/alignment_train_intersect.txt $OUT_DIR/alignment_train_union.txt $OUT_DIR/alignment_train_grow_diag.txt
#
# # *** Implement 2: Extract and score phrases
echo "phrase extraction..."
python $SCRIPT_DIR/phrase-extract.py $TRAIN_DATA.de $TRAIN_DATA.en $OUT_DIR/alignment_train_grow_diag.txt $OUT_DIR/phrase_train_grow_diag.txt

#*** Implement 3: Create WFSTs for phrases
echo "creating WFSTs..."
python $SCRIPT_DIR/create-phrase-fst.py $OUT_DIR/phrase_train_grow_diag.txt $OUT_DIR/phrase-fst.txt


echo "create word penalty pairs"
python $SCRIPT_DIR/word-penalty-fst.py $DATA_DIR/train.en-de.low.filt.en $OUT_DIR/wp-train-fst.txt

# # *** Compile WFSTs into a single model
 echo "compile WFSTs..."
python $SCRIPT_DIR/symbols.py 2 < $OUT_DIR/phrase-fst.txt > $OUT_DIR/phrase-fst.isym
python $SCRIPT_DIR/symbols.py 2 < $OUT_DIR/ngram-fst.txt > $OUT_DIR/ngram-fst.isym
python $SCRIPT_DIR/symbols.py 2 < $OUT_DIR/wp-train-fst.txt > $OUT_DIR/wp-train-fst.isym

fstcompile --isymbols=$OUT_DIR/ngram-fst.isym --osymbols=$OUT_DIR/ngram-fst.isym $OUT_DIR/ngram-fst.txt | fstarcsort > $OUT_DIR/ngram-fst.fst
fstcompile --isymbols=$OUT_DIR/wp-train-fst.isym --osymbols=$OUT_DIR/wp-train-fst.isym $OUT_DIR/wp-train-fst.txt | fstarcsort > $OUT_DIR/wp-train-fst.fst
fstcompile --isymbols=$OUT_DIR/phrase-fst.isym --osymbols=$OUT_DIR/ngram-fst.isym $OUT_DIR/phrase-fst.txt | fstarcsort > $OUT_DIR/phrase-fst.fst

# *** Normally we could do this for efficiency purposes, but it takes a lot of memory, so we keep the FSTs separate
# fstcompose $OUT_DIR/phrase-fst.fst $OUT_DIR/ngram-fst.fst | fstarcsort > $OUT_DIR/tm-fst.fst

# *** Compose and find the best path for each WFST
for f in valid test blind; do
  echo "python $SCRIPT_DIR/decode.py $OUT_DIR/phrase-fst.fst $OUT_DIR/ngram-fst.fst $OUT_DIR/phrase-fst.isym $OUT_DIR/ngram-fst.isym < $DATA_DIR/$f.en-de.low.de > $OUT_DIR/$f.baseline.en"
  python $SCRIPT_DIR/decode.py $OUT_DIR/phrase-fst.fst $OUT_DIR/ngram-fst.fst $OUT_DIR/wp-train-fst.fst $OUT_DIR/phrase-fst.isym $OUT_DIR/ngram-fst.isym < $DATA_DIR/$f.en-de.low.de > $OUT_DIR/$f.baseline.en
  if [[ -e $DATA_DIR/$f.en-de.low.en ]]; then
    perl $SCRIPT_DIR/multi-bleu.perl $DATA_DIR/$f.en-de.low.en < $OUT_DIR/$f.baseline.en
  fi
done
