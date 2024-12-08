# neuroscout

An LLM-powered tool to analyze NeurIPS paper abstracts and help researchers efficiently
discover relevant papers for the poster sessions.

## Overview

Attending NeurIPS can be overwhelming due to the vast number of paper posters presented.
`neuroscout` addresses this challenge by providing a streamlined approach to identify
papers of interest within the extensive collection of papers submitted to NeurIPS. This
tool enhances the conference experience by enabling attendees to focus on papers most
relevant to their interests.

## Installation

You can install `neuroscout` using `pip` or `pipx`, e.g.

```
pip install git+https://github.com/rafidka/neuroscout.git # Using pip
```

You can also clone the repository locally, which enables you to apply make tweaks to the
evaluation process to suit your needs:

```bash
git clone https://github.com/rafidka/neuroscout.git
cd neuroscout
poetry install
```

You can then run `neuroscout` with:

```
poetry run neuroscout
```

## Usage

> **Note**: Currently, `neuroscout` makes use of OpenAI models in the evaluation process.
> As such, you would need to have an OpenAI API key set in the `OPENAI_API_KEY`
> environment variable. Refer to the ["Create and export an API
> key"](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key) section
> of OpenAI's developer guide for more information.

After installation, you can use `neuroscout` via its command-line interface:

```
neuroscout [OPTIONS]
```

Below as an example use case:

```
poetry run python -m neuroscout.main \
    --company-name-file <path to a file containing the company name> \
    --company-description-file <path to a file containing a description about the company> \
    --department-name-file <path to a file containing the department name> \
    --department-description-file <path to a file containing a description about the department>
```

Needless to say, you need to create those 4 files and add information about your job.

Notice that by default, the script will evaluate all NeurIPS papers, which will take a long
time. So, to run a quick experiment, you can use the `--i-am-feeling-lucky` flag, which will
randomly select 10 papers and evaluate them:

```bash
poetry run python -m neuroscout.cli
    --company-name-file ./data/company_name.txt \
    --company-description-file ./data/company_description.txt \
    --department-name-file ./data/department_name.txt \
    --department-description-file ./data/department_description.txt \
    --i-am-feeling-lucky

```

Below is a sample execution output from my machine:

```
Evaluating the paper: Cardinality-Aware Set Prediction and Top-$k$ Classification
Link: https://nips.cc/virtual/2024/poster/94852

Verdict: Not relevant

================================================================================

Evaluating the paper: EGonc : Energy-based Open-Set Node Classification with substitute Unknowns
Link: https://nips.cc/virtual/2024/poster/96733

Verdict: Not relevant

================================================================================

Evaluating the paper: Uni-Med: A Unified Medical Generalist Foundation Model For Multi-Task Learning Via Connector-MoE
Link: https://nips.cc/virtual/2024/poster/93590

Verdict: Not relevant

================================================================================

Evaluating the paper: The Surprising Ineffectiveness of Pre-Trained Visual Representations for Model-Based Reinforcement Learning
Link: https://nips.cc/virtual/2024/poster/95560

Verdict: Not relevant

================================================================================

Evaluating the paper: EigenVI: score-based variational inference with orthogonal function expansions
Link: https://nips.cc/virtual/2024/poster/93317

Verdict: Not relevant

================================================================================

Evaluating the paper: A Swiss Army Knife for Heterogeneous Federated Learning: Flexible Coupling via Trace Norm
Link: https://nips.cc/virtual/2024/poster/96737

Verdict: Not relevant

================================================================================

Evaluating the paper: Slicing Vision Transformer for Flexibile Inference
Link: https://nips.cc/virtual/2024/poster/92963

Verdict: Not relevant

================================================================================

Evaluating the paper: ESPACE: Dimensionality Reduction of Activations for Model Compression
Link: https://nips.cc/virtual/2024/poster/95852

Verdict: Relevant to your company, but not your department

This paper is about model compression using a technique called ESPACE, which focuses on dimensionality reduction of activations for compressing Large Language Models (LLMs). Cohere, being a company that deals with large-scale language models, would be interested in advancements in model compression techniques to enhance efficiency and performance of their NLP models. However, specific focus on embeddings and search, such as the work of the Embeddings & Search organization at Cohere, does not directly align with the subject of this paper, which is more related to model compression rather than embedding or search technologies.

================================================================================

Evaluating the paper: Online Learning of Delayed Choices
Link: https://nips.cc/virtual/2024/poster/94160

Verdict: Not relevant

================================================================================

Evaluating the paper: LLM Circuit Analyses Are Consistent Across Training and Scale
Link: https://nips.cc/virtual/2024/poster/96762

Verdict: Relevant to your company, but not your department.

The paper discusses the internal mechanisms and circuit analyses of Large Language Models (LLMs) across training and scale. While these findings are important to the broader context of language model training and deployment, they do not specifically focus on embeddings and search technologies, which is your department's primary focus. However, understanding the consistent emergence and functionality of model components across different scales could be relevant to Cohere's work in maintaining and fine-tuning language models for various NLP tasks.

================================================================================
```

As you can see, most papers are not relevant to my work, which is expected since Machine Learning is a vast field. However, the model found 2 papers that it thought might be
relevant to the general work of my company. However, it didn't find any paper that is specifically relevant to my department. I guess I-wasn't-as-lucky-as-I-felt.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any
enhancements or bug fixes.
