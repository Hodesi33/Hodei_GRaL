#!/bin/bash
SEED=42
NUM_EPOCHS=20
BATCH_SIZE=8
GRADIENT_ACC_STEPS=2
BATCH_SIZE_PER_GPU=$(( $BATCH_SIZE*$GRADIENT_ACC_STEPS ))
LEARN_RATE=0.00005
WARMUP=0.06
WEIGHT_DECAY=0.01


MODEL='HiTZ/xlm-roberta-large-lemma-eu'
OUTPUT_DIR='./'
LOGGING_DIR='./logs/xlm-roberta-large.log'
DIR_NAME='eu_bdt_ses_udpipe'_${BATCH_SIZE_PER_GPU}_${WEIGHT_DECAY}_${LEARN_RATE}_${NUM_EPOCHS}_$(date +'%m-%d-%y_%H-%M')

python ./bsc_run_ner.py --model_name_or_path $MODEL --seed $SEED \
                                         --dataset_script_path ./eu-bdt-dataset.py \
                                         --task_name ner --do_predict \
                                         --num_train_epochs $NUM_EPOCHS --gradient_accumulation_steps $GRADIENT_ACC_STEPS --per_device_train_batch_size $BATCH_SIZE \
                                         --learning_rate $LEARN_RATE \
                                         --warmup_ratio $WARMUP --weight_decay $WEIGHT_DECAY \
                                         --output_dir $OUTPUT_DIR/$DIR_NAME --overwrite_output_dir \
                                         --logging_dir $LOGGING_DIR/$DIR_NAME --logging_strategy epoch \
                                         --overwrite_cache \
                                         --metric_for_best_model f1 --save_strategy epoch --evaluation_strategy epoch --load_best_model_at_end
rm -r -f $OUTPUT_DIR/$DIR_NAME/checkpoint*
#rm -r -f $OUTPUT_DIR/$DIR_NAME/pytorch_model.bin
                