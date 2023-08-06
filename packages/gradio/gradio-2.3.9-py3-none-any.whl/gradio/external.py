import json
import tempfile
import requests
from gradio import inputs, outputs
import re


def get_huggingface_interface(model_name, api_key, alias):
    api_url = "https://api-inference.huggingface.co/models/{}".format(model_name)
    if api_key is not None:
        headers = {"Authorization": f"Bearer {api_key}"}
    else:
        headers = {}

    # Checking if model exists, and if so, it gets the pipeline
    response = requests.request("GET", api_url,  headers=headers)
    assert response.status_code == 200, "Invalid model name or src"
    p = response.json().get('pipeline_tag')

    def post_process_binary_body(r: requests.Response):
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(r.content)
            return fp.name

    pipelines = {
        'question-answering': {
            'inputs': [inputs.Textbox(label="Context", lines=7), inputs.Textbox(label="Question")],
            'outputs': [outputs.Textbox(label="Answer"), outputs.Label(label="Score")],
            'preprocess': lambda c, q: {"inputs": {"context": c, "question": q}},
            'postprocess': lambda r: (r["answer"], r["score"]),
            # 'examples': [['My name is Sarah and I live in London', 'Where do I live?']]
        },
        'text-generation': {
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Textbox(label="Output"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: r[0]["generated_text"],
            # 'examples': [['My name is Clara and I am']]
        },
        'summarization': {
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Textbox(label="Summary"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: r[0]["summary_text"]
        },
        'translation': {
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Textbox(label="Translation"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: r[0]["translation_text"]
        },
        'text2text-generation': {
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Textbox(label="Generated Text"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: r[0]["generated_text"]
        },
        'text-classification': {
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Label(label="Classification"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: {'Negative': r[0][0]["score"],
                                      'Positive': r[0][1]["score"]}
        },
        'fill-mask': {
            'inputs': inputs.Textbox(label="Input"),
            'outputs': "label",
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: {i["token_str"]: i["score"] for i in r}
        },
        'zero-shot-classification': {
            'inputs': [inputs.Textbox(label="Input"),
                       inputs.Textbox(label="Possible class names ("
                                            "comma-separated)"),
                       inputs.Checkbox(label="Allow multiple true classes")],
            'outputs': "label",
            'preprocess': lambda i, c, m: {"inputs": i, "parameters":
            {"candidate_labels": c, "multi_class": m}},
            'postprocess': lambda r: {r["labels"][i]: r["scores"][i] for i in
                                      range(len(r["labels"]))}
        },
        'automatic-speech-recognition': {
            'inputs': inputs.Audio(label="Input", source="upload",
                                   type="file"),
            'outputs': outputs.Textbox(label="Output"),
            'preprocess': lambda i: {"inputs": i},
            'postprocess': lambda r: r["text"]
        },
        'image-classification': {
            'inputs': inputs.Image(label="Input Image", type="file"),
            'outputs': outputs.Label(label="Classification"),
            'preprocess': lambda i: i,
            'postprocess': lambda r: {i["label"].split(", ")[0]: i["score"] for
                                      i in r}
        },
        'feature-extraction': {
            # example model: hf.co/julien-c/distilbert-feature-extraction
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Dataframe(label="Output"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': lambda r: r[0],
        },
        'sentence-similarity': {
            # example model: hf.co/sentence-transformers/distilbert-base-nli-stsb-mean-tokens
            'inputs': [
                inputs.Textbox(label="Source Sentence", default="That is a happy person"),
                inputs.Textbox(lines=7, label="Sentences to compare to", placeholder="Separate each sentence by a newline"),
            ],
            'outputs': outputs.Label(label="Classification"),
            'preprocess': lambda src, sentences: {"inputs": {
                "source_sentence": src,
                "sentences": [s for s in sentences.splitlines() if s != ""],
            }},
            'postprocess': lambda r: { f"sentence {i}": v for i, v in enumerate(r) },
        },
        'text-to-speech': {
            # example model: hf.co/julien-c/ljspeech_tts_train_tacotron2_raw_phn_tacotron_g2p_en_no_space_train
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Audio(label="Audio"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': post_process_binary_body,
        },
        'text-to-image': {
            # example model: hf.co/osanseviero/BigGAN-deep-128
            'inputs': inputs.Textbox(label="Input"),
            'outputs': outputs.Image(label="Output"),
            'preprocess': lambda x: {"inputs": x},
            'postprocess': post_process_binary_body,
        },
    }

    if p is None or not(p in pipelines):
        print("Warning: no interface information found")
    
    pipeline = pipelines[p]

    def query_huggingface_api(*input):
        payload = pipeline['preprocess'](*input)
        if p == 'automatic-speech-recognition' or p == 'image-classification':
            with open(input[0].name, "rb") as f:
                data = f.read()
        else:
            payload.update({'options': {'wait_for_model': True}})
            data = json.dumps(payload)
        response = requests.request("POST", api_url, headers=headers, data=data)
        if response.status_code == 200:
            if p == 'text-to-speech' or p == 'text-to-image':
                output = pipeline['postprocess'](response)
            else:
                result = response.json()
                output = pipeline['postprocess'](result)
        else:
            raise ValueError("Could not complete request to HuggingFace API, Error {}".format(response.status_code))
        return output
    
    if alias is None:
        query_huggingface_api.__name__ = model_name
    else:
        query_huggingface_api.__name__ = alias

    interface_info = {
        'fn': query_huggingface_api, 
        'inputs': pipeline['inputs'],
        'outputs': pipeline['outputs'],
        'title': model_name,
        # 'examples': pipeline['examples'],
    }

    return interface_info

def load_interface(name, src=None, api_key=None, alias=None):
    if src is None:
        tokens = name.split("/")
        assert len(tokens) > 1, "Either `src` parameter must be provided, or `name` must be formatted as \{src\}/\{repo name\}"
        src = tokens[0]
        name = "/".join(tokens[1:])
    assert src.lower() in repos, "parameter: src must be one of {}".format(repos.keys())
    interface_info = repos[src](name, api_key, alias)
    return interface_info

def interface_params_from_config(config_dict):
    ## instantiate input component and output component
    config_dict["inputs"] = [inputs.get_input_instance(component) for component in config_dict["input_components"]]
    config_dict["outputs"] = [outputs.get_output_instance(component) for component in config_dict["output_components"]]
    # remove preprocessing and postprocessing (since they'll be performed remotely)
    for component in config_dict["inputs"]:
        component.preprocess = lambda x:x
    for component in config_dict["outputs"]:
        component.postprocess = lambda x:x        
    # Remove keys that are not parameters to Interface() class
    not_parameters = ("allow_embedding", "allow_interpretation", "avg_durations", "function_count",
                      "queue", "input_components", "output_components", "examples")
    for key in not_parameters:
        if key in config_dict:
            del config_dict[key]
    return config_dict

def get_spaces_interface(model_name, api_key, alias):
    iframe_url = "https://huggingface.co/gradioiframe/{}/+".format(model_name)
    api_url = "https://huggingface.co/gradioiframe/{}/api/predict/".format(model_name)
    headers = {'Content-Type': 'application/json'}

    r = requests.get(iframe_url)
    result = re.search('window.config =(.*?);\n', r.text) # some basic regex to extract the config
    config = json.loads(result.group(1))
    interface_info = interface_params_from_config(config)
    
    # The function should call the API with preprocessed data
    def fn(*data):
        data = json.dumps({"data": data})
        response = requests.post(api_url, headers=headers, data=data)
        result = json.loads(response.content.decode("utf-8"))
        output = result["data"]
        if len(interface_info["outputs"])==1:  # if the fn is supposed to return a single value, pop it
            output = output[0]
        return output
     
    if alias is None:
        fn.__name__ = model_name
    else:
        fn.__name__ = alias
    interface_info["fn"] = fn

    return interface_info

repos = {
    # for each repo, we have a method that returns the Interface given the model name & optionally an api_key
    "huggingface": get_huggingface_interface,
    "spaces": get_spaces_interface,
}

