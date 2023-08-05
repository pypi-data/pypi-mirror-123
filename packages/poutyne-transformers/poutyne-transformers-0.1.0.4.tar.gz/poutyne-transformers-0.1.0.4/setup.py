# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poutyne_transformers']

package_data = \
{'': ['*']}

install_requires = \
['Poutyne>=1.6,<2.0', 'torch>=1.9.0,<2.0.0', 'transformers>=4.11.3,<5.0.0']

setup_kwargs = {
    'name': 'poutyne-transformers',
    'version': '0.1.0.4',
    'description': 'Train 🤗-transformers models with Poutyne.',
    'long_description': '# poutyne-transformers\n\nTrain [🤗-transformers](https://huggingface.co/transformers/) models with [Poutyne](https://poutyne.org).\n\n## Installation\n\n```bash\npip install poutyne-transformers\n```\n\n## Example\n\n```python\nimport torch\nfrom transformers import AutoModelForSequenceClassification, AutoTokenizer\nfrom datasets import load_dataset\nfrom torch.utils.data import DataLoader\nfrom torch import optim\nfrom poutyne import Model, Accuracy\nfrom poutyne_transformers import (\n    TransformerCollator,\n    model_loss,\n    ModelWrapper,\n    MetricWrapper,\n)\n\nprint("Loading model & tokenizer.")\ntransformer = AutoModelForSequenceClassification.from_pretrained(\n    "distilbert-base-cased", num_labels=2, return_dict=True\n)\ntokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")\n\nprint("Loading & preparing dataset.")\ndataset = load_dataset("imdb")\ndataset = dataset.map(\n    lambda entry: tokenizer(\n        entry["text"], add_special_tokens=True, padding="max_length", truncation=True\n    ),\n    batched=True,\n)\ndataset = dataset.remove_columns(["text"])\ndataset = dataset.shuffle()\ndataset.set_format("torch")\n\ncollate_fn = TransformerCollator(y_keys="labels")\ntrain_dataloader = DataLoader(dataset["train"], batch_size=16, collate_fn=collate_fn)\ntest_dataloader = DataLoader(dataset["test"], batch_size=16, collate_fn=collate_fn)\n\nprint("Preparing training.")\nwrapped_transformer = ModelWrapper(transformer)\noptimizer = optim.AdamW(wrapped_transformer.parameters(), lr=5e-5)\ndevice = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")\naccuracy = MetricWrapper(Accuracy(), pred_key="logits")\nmodel = Model(\n    wrapped_transformer,\n    optimizer,\n    loss_function=model_loss,\n    batch_metrics=[accuracy],\n    device=device,\n)\n\nprint("Starting training.")\nmodel.fit_generator(train_dataloader, test_dataloader, epochs=1)\n```\n\nYou can also create models with a custom architecture using `torch.nn.Sequential` class:\n\n```python\nfrom torch import nn\nfrom transformers import AutoModel\nfrom poutyne import Lambda\nfrom poutyne_transformers import ModelWrapper\n\n...\n\ntransformer = AutoModel.from_pretrained(\n    "distilbert-base-cased", output_hidden_states=True\n)\n\ncustom_model = nn.Sequential(\n    ModelWrapper(transformer),\n    # Use distilberts [CLS] token for classification.\n    Lambda(lambda outputs: outputs["last_hidden_state"][:, 0, :]),\n    nn.Linear(in_features=transformer.config.hidden_size, out_features=1),\n    Lambda(lambda out: out.reshape(-1)),\n)\n\n...\n```\n',
    'author': 'Lennart Keller',
    'author_email': 'lennart.keller@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LennartKeller/poutyne-transformers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
