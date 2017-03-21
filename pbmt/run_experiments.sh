#!/bin/bash
set -e

##### NOTE
# This assumes that you have OpenFST and the Python bindings installed

DATA_DIR=en-de
SCRIPT_DIR=.
OUT_DIR=outputs
TRAIN_DATA=$DATA_DIR/valid.en-de.low
mkdir -p $OUT_DIR

# *** Train n-gram language model and create an FST
python $SCRIPT_DIR/train-ngram.py $TRAIN_DATA.en $OUT_DIR/ngram-exp-fst.txt

# *** Implement 1: Train IBM Model 1 and find alignment
#
python $SCRIPT_DIR/train-model2.py $TRAIN_DATA.de $TRAIN_DATA.en $OUT_DIR/alignment_exp_f.txt

# python $SCRIPT_DIR/train-model2.py $TRAIN_DATA.en $TRAIN_DATA.de $OUT_DIR/alignment_exp_e.txt
#
# #
# python $SCRIPT_DIR/intersect.py $OUT_DIR/alignment_exp_f.txt $OUT_DIR/alignment_exp_e.txt $OUT_DIR/alignment_exp_intersect.txt
#
# python $SCRIPT_DIR/union.py $OUT_DIR/alignment_exp_f.txt $OUT_DIR/alignment_exp_e.txt $OUT_DIR/alignment_exp_union.txt
#
# python $SCRIPT_DIR/grow-diagonal.py $OUT_DIR/alignment_exp_intersect.txt $OUT_DIR/alignment_exp_union.txt $OUT_DIR/alignment_exp_grow_diag.txt

# *** Implement 2: Extract and score phrases
python $SCRIPT_DIR/phrase-extract.py $TRAIN_DATA.de $TRAIN_DATA.en $OUT_DIR/alignment_exp_f.txt $OUT_DIR/phrase_exp_f.txt

# *** Implement 3: Create WFSTs for phrases
python $SCRIPT_DIR/create-phrase-fst.py $OUT_DIR/phrase_exp_f.txt $OUT_DIR/phrase-exp-fst.txt

# *** Compile WFSTs into a single model
python $SCRIPT_DIR/symbols.py 2 < $OUT_DIR/phrase-exp-fst.txt > $OUT_DIR/phrase-exp-fst.isym
python $SCRIPT_DIR/symbols.py 2 < $OUT_DIR/ngram-exp-fst.txt > $OUT_DIR/ngram-exp-fst.isym
python $SCRIPT_DIR/symbols.py 2 < $OUT_DIR/wp-exp-fst.txt > $OUT_DIR/wp-exp-fst.isym
fstcompile --isymbols=$OUT_DIR/ngram-exp-fst.isym --osymbols=$OUT_DIR/ngram-exp-fst.isym $OUT_DIR/ngram-exp-fst.txt | fstarcsort > $OUT_DIR/ngram-exp-fst.fst
fstcompile --isymbols=$OUT_DIR/wp-exp-fst.isym --osymbols=$OUT_DIR/wp-exp-fst.isym $OUT_DIR/wp-exp-fst.txt | fstarcsort > $OUT_DIR/wp-exp-fst.fst
fstcompile --isymbols=$OUT_DIR/phrase-exp-fst.isym --osymbols=$OUT_DIR/ngram-exp-fst.isym $OUT_DIR/phrase-exp-fst.txt | fstarcsort > $OUT_DIR/phrase-exp-fst.fst

# *** Normally we could do this for efficiency purposes, but it takes a lot of memory, so we keep the FSTs separate
#fstcompose $OUT_DIR/phrase-exp-fst.fst $OUT_DIR/ngram-exp-fst.fst | fstarcsort > $OUT_DIR/tm-fst.fst

# *** Compose and find the best path for each WFST
for f in valid test; do
  echo "python $SCRIPT_DIR/decode.py $OUT_DIR/phrase-exp-fst.fst $OUT_DIR/ngram-exp-fst.fst $OUT_DIR/phrase-exp-fst.isym $OUT_DIR/ngram-exp-fst.isym < $DATA_DIR/$f.en-de.low.de > $OUT_DIR/$f.baseline.exp.en"
  python $SCRIPT_DIR/decode.py $OUT_DIR/phrase-exp-fst.fst $OUT_DIR/ngram-exp-fst.fst $OUT_DIR/wp-exp-fst.fst $OUT_DIR/phrase-exp-fst.isym $OUT_DIR/ngram-exp-fst.isym < $DATA_DIR/$f.en-de.low.de > $OUT_DIR/$f.baseline.exp.en
  if [[ -e $DATA_DIR/$f.en-de.low.en ]]; then
    perl $SCRIPT_DIR/multi-bleu.perl $DATA_DIR/$f.en-de.low.en < $OUT_DIR/$f.baseline.exp.en
  fi
done
