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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any
enhancements or bug fixes.
