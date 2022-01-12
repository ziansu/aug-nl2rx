if [ $1 = 'nl2regex' ]; then
	echo "nl2regex"

	pretrained_model=microsoft/codebert-base
	output_dir=./output-test-sampling-bt
	data_dir=../data/data-eval-turk
	load_model_path=./output-cb3ld-sampling-bt/checkpoint-best-bleu/

	# # do train
	# python run_nl2regex.py \
	# 	--do_train \
	# 	--do_eval \
	# 	--model_type roberta \
	# 	--model_name_or_path $pretrained_model \
	# 	--config_name roberta-base \
	# 	--tokenizer_name roberta-base \
	# 	--train_filename $data_dir/src-train-merged.txt,$data_dir/targ-train-merged.txt \
	# 	--dev_filename $data_dir/src-val.txt,$data_dir/targ-val.txt \
	# 	--output_dir $output_dir \
	# 	--max_source_length 256 \
	# 	--max_target_length 256 \
	# 	--beam_size 5 \
	# 	--train_batch_size 48 \
	# 	--eval_batch_size 64 \
	# 	--learning_rate 5e-5 \
	# 	--train_steps 20000 \
	# 	--eval_steps 500

	# do test
	python run_nl2regex.py \
		--do_test\
		--model_type roberta \
		--model_name_or_path $pretrained_model \
		--config_name roberta-base \
		--tokenizer_name roberta-base \
	    --load_model_path $load_model_path/pytorch_model.bin \
		--test_filename $data_dir/src-test.txt,$data_dir/targ-test.txt \
		--output_dir $output_dir \
		--max_source_length 256 \
		--max_target_length 256 \
		--beam_size 5 \
		--eval_batch_size 64 \
		--learning_rate 5e-5 \
		--train_steps 10000 \
		--eval_steps 500

elif [ $1 = 'regex2nl' ]; then
	echo "regex2nl"

	pretrained_model=microsoft/codebert-base
	output_dir=./output
	# data_dir=../data/data-eval-turk
	data_dir=../data/data-synthesized
	load_model_path=./output-cb3ld-back/checkpoint-best-ppl

	# do train
	# python run_regex2nl.py \
	# 	--do_train \
	# 	--do_eval \
	# 	--model_type roberta \
	# 	--model_name_or_path $pretrained_model \
	# 	--config_name roberta-base \
	# 	--tokenizer_name roberta-base \
	# 	--train_filename $data_dir/targ-train.txt,$data_dir/src-train.txt \
	# 	--dev_filename $data_dir/targ-val.txt,$data_dir/src-val.txt \
	# 	--output_dir $output_dir \
	# 	--max_source_length 256 \
	# 	--max_target_length 256 \
	# 	--beam_size 5 \
	# 	--train_batch_size 32 \
	# 	--eval_batch_size 64 \
	# 	--learning_rate 5e-5 \
	# 	--train_steps 20000 \
	# 	--eval_steps 500


	# do test
	# python run_nl2regex.py \
	# 	--do_test\
	# 	--model_type roberta \
	# 	--model_name_or_path $pretrained_model \
	# 	--config_name roberta-base \
	# 	--tokenizer_name roberta-base \
	#     --load_model_path ./output/checkpoint-best-ppl/pytorch_model.bin \
	# 	--test_filename $data_dir/NL-RX-Turk.test.X.txt,$data_dir/NL-RX-Turk.test.Y.txt \
	# 	--output_dir $output_dir \
	# 	--max_source_length 256 \
	# 	--max_target_length 256 \
	# 	--beam_size 5 \
	# 	--eval_batch_size 64 \
	# 	--learning_rate 5e-5 \
	# 	--train_steps 10000 \
	# 	--eval_steps 500

	# diverse generation
	python run_regex2nl.py \
		--do_diverse\
		--model_type roberta \
		--model_name_or_path $pretrained_model \
		--config_name roberta-base \
		--tokenizer_name roberta-base \
	    --load_model_path $load_model_path/pytorch_model.bin \
		--test_filename $data_dir/targ-anonymized.txt,$data_dir/src-anonymized.txt \
		--output_dir $output_dir \
		--max_source_length 256 \
		--max_target_length 256 \
		--beam_size 5 \
		--eval_batch_size 64 \
		--learning_rate 5e-5 \
		--train_steps 10000 \
		--eval_steps 500

else
	echo $1
	echo "back-translation"

fi