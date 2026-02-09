.PHONY: lambda-commands

create-hf-dataset:
	echo "Creating HF dataset"
	python3 src/dataset.py

generate-ssh-key:
	python3 src/lambda/commands.py generate-ssh-key

list-ssh-keys:
	python3 src/lambda/commands.py list-ssh-keys

list-instances:
	python3 src/lambda/commands.py list-instances

list-instance-types:
	python3 src/lambda/commands.py list-types

get-lambda-ip:
	python3 src/lambda/commands.py get-ip

launch-lambda-instance:
	python3 src/lambda/commands.py launch

lambda-help:
	python3 src/lambda/commands.py

lambda-setup:
	sudo apt update && sudo apt upgrade -y
	sudo apt install -y build-essential cmake ninja-build\
	                    python3.11 python3.11-venv python3.11-dev python3.11-distutils

	python3.11 -m venv myenv

	./myenv/bin/python3.11 -m pip install --upgrade pip setuptools wheel packaging

# 	python3.11 -m pip install torch==2.2.2+cu121 --index-url https://download.pytorch.org/whl/cu121
# 	python3.11 -m pip install torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cu121
#	python3.11 -m pip install torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121
	./myenv/bin/python3.11 -m pip install torch==2.8.0+cu128 \
		torchvision==0.23.0+cu128 \
		torchaudio==2.8.0+cu128 \
		--index-url https://download.pytorch.org/whl/cu128

	./myenv/bin/python3.11 -m pip install axolotl==0.14.0
#	./myenv/bin/python3.11 -m pip install flash-attn==2.6.3 --no-build-isolation
	./myenv/bin/python3.11 -m pip install deepspeed

# 	python3.11 -c "import torch; print('Torch CUDA available:', torch.cuda.is_available())"
# 	python3.11 -c "import axolotl; print('Axolotl version:', axolotl.__version__)"
# 	python3.11 -c "import flash_attn; print('Flash-Attn imported successfully')"

finetune-example:
	echo "Finetuning Michael LLM"
	bash -c "source myenv/bin/activate && export AXOLOTL_DO_NOT_TRACK=1 && axolotl train src/lora-1b.yml"

finetune:
	echo "Finetuning Michael LLM"
	bash -c "source myenv/bin/activate && export AXOLOTL_DO_NOT_TRACK=1 && axolotl train src/michael_finetune.yaml"

inference:
	echo "Running inference"
	bash -c "source myenv/bin/activate && export AXOLOTL_DO_NOT_TRACK=1 && accelerate launch -m axolotl.cli.inference src/michael_finetune.yaml --lora_model_dir="./outputs/michael-scott-llama-3.2-1b" --gradio"

terminate-instance:
	python3 src/lambda/commands.py terminate

# download-model:
# 	echo "Downloading model files"
# 	python3 src/download_model.py