# MichaelScottLLM

## Overview

A project exploring language model fine-tuning techniques.

**Disclaimer:** Most of the code in this project is copied and refactored from [neural-maze/neural-hub](https://github.com/neural-maze/neural-hub/tree/master/rick-llm). Specifically, the `src/lambda` code and most of the `Makefile` is a direct copy-paste, while the rest has been inspired and refactored to adapt it to a new use case.

**Note:** This README is a work in progress and will be updated with more details soon.

## Getting Started

### Dataset Creation

```bash
make create-hf-dataset
```

Executes the code in `dataset.py` to create the dataset in Hugging Face.

### Fine-Tuning

```bash
make generate-ssh-key
```

Generates an SSH key and stores the public key in your Lambda Labs account. Creates a `.pem` file in `src/lambda/ssh-key/`.

```bash
make launch-lambda-instance
```

Starts your Lambda instance. **⚠️ Charges apply once the instance is initiated.**

```bash
make get-lambda-ip
```

Retrieves your instance IP, necessary for file transfer and SSH connection.

```bash
rsync -av -e "ssh -i src/lambda/ssh-key/michael-private_key.pem -o IdentitiesOnly=yes" Makefile .env ubuntu@<INSTANCE_IP>:/home/ubuntu/
rsync -av -e "ssh -i src/lambda/ssh-key/michael-private_key.pem -o IdentitiesOnly=yes" src ubuntu@<INSTANCE_IP>:/home/ubuntu/src/
```

Transfers necessary files to your instance.

```bash
ssh -i src/lambda/ssh-key/michael-private_key.pem ubuntu@<INSTANCE_IP>
```

Connects to your instance via SSH.

```bash
make lambda-setup
```

Installs all necessary dependencies to run Axolotl on your instance.

```bash
make finetune
```

Executes the fine-tuning of the model using Axolotl.

### Inference

```bash
make inference
```

Creates a Gradio interface to test the model. Must run immediately after fine-tuning completes as it uses the `.outputs` folder.

### Cleanup

```bash
make terminate-instance
```

**🛑 Terminates the Lambda instance to avoid additional charges.**