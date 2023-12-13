# Simple Accuracy Benchmark for Optimized LLMs

Simple and quick accuracy test for compressed, quantized, pruned, distilled LLMs. It works with any model that suppors HuggingFace Transformers text generation API including:
* HuggingFace Transformers compressed models via [Bitsandbytes](https://huggingface.co/docs/transformers/main_classes/quantization#transformers.BitsAndBytesConfig)
* [GPTQ](https://huggingface.co/docs/transformers/main_classes/quantization#transformers.GPTQConfig) via HuggingFace API
* Llama.cpp via [BigDL-LLM](https://github.com/intel-analytics/BigDL/tree/main/python/llm)
* [OpenVINO](https://github.com/openvinotoolkit/openvino) and [NNCF](https://github.com/openvinotoolkit/nncf) via [Optimum-Intel](https://github.com/huggingface/optimum-intel)

The main idea is to compare similarity of text generation between baseline and optimized LLMs.

The API provides a way to access to investigate the worst generated text examples.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import whowhatbench

model_id = "facebook/opt-1.3b"
base_small = AutoModelForCausalLM.from_pretrained(model_id)
optimized_model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id)

evaluator = whowhatbench.Evaluator(base_model=base_small, tokenizer=tokenizer)
metrics_per_prompt, metrics = evaluator.score(optimized_model)

metric_of_interest = "similarity"
print(metric_of_interest, ": ", metrics["similarity"][0])

worst_examples = evaluator.worst_examples(top_k=5, metric=metric_of_interest)
print("Metric: ", metric_of_interest)
for e in worst_examples:
    print("\t=========================")
    print("\tPrompt: ", e["prompt"])
    print("\tBaseline Model:\n ", "\t" + e["source_model"])
    print("\tOptimized Model:\n ", "\t" + e["optimized_model"])

```

Use your own list of prompts to compare (e.g. from a dataset):
```python
from datasets import load_dataset
val = load_dataset("lambada", split="validation[20:40]")
prompts = val["text"]
...
metrics_per_prompt, metrics = evaluator.score(optimized_model, test_data=prompts)
```

### Installing

* git clone https://github.com/andreyanufr/who_what_benchmark.git
* python -m venv eval_env
* source eval_env/bin/activate
* pip install -r requirements.txt

### CLI example

* Step-by-step bullets
```
# run text generation for original model
python3 generate.py --modeltype causal --model meta-llama/Llama-2-7b-chat-hf --save_generations_path gold_llama-2-7b-chat-hf.csv --csv simple.csv --trust_remote_code

# convert and compress llama with optimum-intel and nncf and save it to some folder
...

#run text generation for compressed models
python3 generate.py --modeltype ov_causal --model /home/user/models/meta-llama/Llama-2-7b-chat-hf-int8 --save_generations_path predict_llama-2-7b-chat-hf_int8.csv --csv simple.csv --trust_remote_code

python3 generate.py --modeltype ov_causal --model /home/user/models/meta-llama/Llama-2-7b-chat-hf-int4_sym --save_generations_path predict_llama-2-7b-chat-hf_int4_sym.csv --csv simple.csv --trust_remote_code

python3 generate.py --modeltype ov_causal --model /home/user/models/meta-llama/Llama-2-7b-chat-hf-int4_asym --save_generations_path predict_llama-2-7b-chat-hf_int4_asym.csv --csv simple.csv --trust_remote_code


for file in predict_llama-2-7b*; do
python3 evaluate.py --gold gold_llama-2-7b-chat-hf.csv --prediction $file --save_evaluation_path eval_$file 2>&1 | tee -a eval.log
done
```

### Notes

* In the file save_evaluation_path you can see per sample similarity metrics.
* Input CSV file for generation must contain column with name `questions`. For example see simple.csv
* You can see example of generation in file generations.csv
* evaluate.py uses for similarity measurement [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) but you can use other similar network.
