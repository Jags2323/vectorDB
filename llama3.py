import json
import transformers
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

system_context = {
    "role": "system",
    "content": "You are a model that explains workflows from a given JSON. The JSON consists of objects that represent nodes and their children in a hierarchical structure. Each node has a unique name and can be linked to other nodes. Your task is to describe the chain of nodes from start to end for a given node."
}

json_workflow = """
[
    {
        "node": "Windows Server",
        "children": ["Linux Server", "Database Server"]
    },
    {
        "node": "Linux Server",
        "children": ["Application Server"]
    },
    {
        "node": "Database Server",
        "children": ["Backup Server"]
    },
    {
        "node": "Application Server",
        "children": ["Frontend Server", "Cache Server"]
    },
    {
        "node": "Frontend Server",
        "children": ["User Interface"]
    },
    {
        "node": "Cache Server",
        "children": []
    },
    {
        "node": "Backup Server",
        "children": []
    },
    {
        "node": "User Interface",
        "children": ["End"]
    },
    {
        "node": "End",
        "children": []
    }
]
"""

messages = [
    system_context,
    {"role": "user", "content": "Explain the workflow starting from the Windows Server to End."},
    {"role": "user", "content": f"Here is the JSON: {json_workflow}"}
]

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = pipeline(
    messages,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)

print(json.dumps(outputs[0]["generated_text"][-1], indent=2))
# print(outputs[0]["generated_text"][-1])
