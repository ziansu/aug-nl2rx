if [ $1 == 'nl2regex' ]
then
	pretrained_model=microsoft/codebert-base
	output_dir=./output
	# data_dir=../data/StructuredRegex/tokenized/
	data_dir=../data/StructuredRegex/const_anonymized/

	# do train
	# python run_mm2regex.py \
	# 	--do_train \
	# 	--do_eval \
	# 	--model_type roberta \
	# 	--model_name_or_path $pretrained_model \
	# 	--config_name roberta-base \
	# 	--tokenizer_name roberta-base \
	# 	--train_filename $data_dir/train.tsv \
	# 	--dev_filename $data_dir/dev.tsv \
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
	load_model_path=./output-cb6ld-a
	python run_mm2regex.py \
		--do_test\
		--output_beam \
		--model_type roberta \
		--model_name_or_path $pretrained_model \
		--config_name roberta-base \
		--tokenizer_name roberta-base \
		--load_model_path $load_model_path/checkpoint-best-ppl/pytorch_model.bin \
		--test_filename $data_dir/dev.tsv \
		--output_dir $output_dir \
		--max_source_length 256 \
		--max_target_length 256 \
		--beam_size 5 \
		--eval_batch_size 64 \
		--learning_rate 5e-5 \
		--train_steps 10000 \
		--eval_steps 500

elif [ $1 == 'regex2nl' ]
then
	pretrained_model=microsoft/codebert-base

	# do train
	# output_dir=./output-cb6ld-back-5k
	# data_dir=../data/StructuredRegex/tokenized/
	# data_dir=../data/StructuredRegex/const_anonymized/
	# python run_regex2mm.py \
	# 	--do_train \
	# 	--do_eval \
	# 	--model_type roberta \
	# 	--model_name_or_path $pretrained_model \
	# 	--config_name roberta-base \
	# 	--tokenizer_name roberta-base \
	# 	--train_filename $data_dir/train.tsv \
	# 	--dev_filename $data_dir/dev.tsv \
	# 	--output_dir $output_dir \
	# 	--max_source_length 256 \
	# 	--max_target_length 256 \
	# 	--beam_size 5 \
	# 	--train_batch_size 32 \
	# 	--eval_batch_size 64 \
	# 	--learning_rate 5e-5 \
	# 	--train_steps 5000 \
	# 	--eval_steps 500

	# do diverse
	data_dir='./syn_data'
	output_dir='./syn_data'
	load_model_path='./output-cb6ld-back/checkpoint-best-ppl/pytorch_model.bin'
	python run_regex2mm.py \
		--do_diverse \
		--model_type roberta \
		--model_name_or_path $pretrained_model \
		--config_name roberta-base \
		--tokenizer_name roberta-base \
		--load_model_path $load_model_path \
		--test_filename $data_dir/diverse_test.csv \
		--output_dir $output_dir \
		--max_source_length 256 \
		--max_target_length 256 \
		--beam_size 5 \
		--train_batch_size 32 \
		--eval_batch_size 64 \
		--learning_rate 5e-5 \
		--eval_steps 500

else
	echo "Not Implemented."
fi

# StrReg decode
# python decode.py StReg pretrained --split val

# StrReg eval
# python eval.py StReg pretrained --split val