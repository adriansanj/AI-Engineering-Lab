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

	./myenv/bin/python3.11 -m pip install torch==2.8.0+cu128 \
		torchvision==0.23.0+cu128 \
		torchaudio==2.8.0+cu128 \
		--index-url https://download.pytorch.org/whl/cu128

	./myenv/bin/python3.11 -m pip install axolotl==0.14.0
	./myenv/bin/python3.11 -m pip install deepspeed

finetune-example:
	echo "Finetuning Michael LLM"
	bsource myenv/bin/activate && \
	export AXOLOTL_DO_NOT_TRACK=1 && \
	axolotl train src/lora-1b.yml

finetune:
	echo "Finetuning Michael LLM"
	source myenv/bin/activate && \
	export AXOLOTL_DO_NOT_TRACK=1 && \
	axolotl train src/michael_finetune.yaml && \
	axolotl merge-lora src/michael_finetune.yaml --lora-model-dir ./outputs/michael-scott-llama-3.2-1b && \
	sed -i 's/"tokenizer_class": "TokenizersBackend"/"tokenizer_class": "PreTrainedTokenizerFast"/' ./outputs/michael-scott-llama-3.2-1b/merged/tokenizer_config.json

create-hf-gguf-model:
	@export HUGGING_FACE_HUB_TOKEN=$$(grep HUGGING_FACE_HUB_TOKEN .env | cut -d'=' -f2 | tr -d '"') && \
	pip install --upgrade transformers && \
	if [ ! -d "llama.cpp" ]; then \
		echo "Cloning llama.cpp..."; \
		git clone https://github.com/ggerganov/llama.cpp; \
	else \
		echo "llama.cpp already exists, skipping clone"; \
	fi && \
	pip install -r llama.cpp/requirements.txt && \
	python llama.cpp/convert_hf_to_gguf.py \
		./outputs/michael-scott-llama-3.2-1b/merged \
		--outfile model-fp16.gguf \
		--outtype f16 && \
	huggingface-cli upload adrianse/michael-scott-llama-3.2-1b-GGUF model-fp16.gguf model-fp16.gguf

inference:
	echo "Running inference"
	bash -c "source myenv/bin/activate && export AXOLOTL_DO_NOT_TRACK=1 && accelerate launch -m axolotl.cli.inference src/michael_finetune.yaml --lora_model_dir="./outputs/michael-scott-llama-3.2-1b" --gradio"

terminate-instance:
	python3 src/lambda/commands.py terminate

ollama-setup:
	@echo "Setting up Ollama..."
	@if ! command -v ollama >/dev/null 2>&1; then \
		echo "→ Ollama not found, installing..."; \
		curl -fsSL https://ollama.com/install.sh | sh; \
		echo "✓ Ollama installed"; \
	else \
		echo "✓ Ollama already installed"; \
	fi
	@if [ ! -f /etc/systemd/system/ollama.service.d/override.conf ] || \
	   ! grep -q "OLLAMA_HOST=0.0.0.0:11434" /etc/systemd/system/ollama.service.d/override.conf 2>/dev/null; then \
		echo "→ Configuration needs update..."; \
		sudo mkdir -p /etc/systemd/system/ollama.service.d; \
		echo "[Service]" | sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null; \
		echo "Environment=\"OLLAMA_HOST=0.0.0.0:11434\"" | sudo tee -a /etc/systemd/system/ollama.service.d/override.conf > /dev/null; \
		sudo systemctl daemon-reload; \
		echo "✓ Configuration updated"; \
	else \
		echo "✓ Configuration already correct"; \
	fi
	@echo "→ Ensuring Ollama is running..."
	@sudo systemctl enable ollama 2>/dev/null || true
	@sudo systemctl is-active --quiet ollama && sudo systemctl restart ollama || sudo systemctl start ollama
	@sleep 2
	@curl -s http://localhost:11434/api/tags > /dev/null && \
		echo "✓ Ollama is running and accessible on 0.0.0.0:11434" || \
		echo "✗ Ollama failed to start"

ollama-create-model:
	@echo "Creating model 'michael-scott' from src/Modelfile..."
	@ollama create michael-scott -f src/Modelfile && \
		echo "✓ Model 'michael-scott' created successfully" || \
		echo "✗ Failed to create model"
	
start-web-ui:
	docker compose up -d

stop-web-ui:
	docker compose down