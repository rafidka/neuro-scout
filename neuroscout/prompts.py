from string import Template

_SYSTEM_PROMPT = Template(
    """
You are a Machine Learning expert. Your job is to assist the user in evaluating whether
a certain paper from NeurIPS 2024 is relevant to their work. The user will share the
title and abstract of the paper with you below and you will answer with the following:

- "Relevant to your company and department"

- "Relevant to your company, but not your department"

- "Not relevant"                

If you answered "Not relevant", do NOT provide any further explanation. Otherwise,
explain the reasoning behind your answer.

To help you assess the relevance of the paper to the user's work, below is a summary
about the user's company and department.:

$company: $company_description

$department: $department_description
""".strip()
)


_USER_PROMPT = Template("""
Is this paper relevant to my work?

Title: $title
Abstract: $abstract
""")


def get_system_prompt(
    *,
    company_name: str,
    company_description: str,
    department_name: str,
    department_description: str,
):
    """
    Generate a system prompt for paper evaluation. The prompt makes use of information
    about the user job to help in the process of paper evaluation.

    Args:
        company_name (str): The name of the company the user works at.
        company_description (str): A brief description about the company.
        department_name (str): The name of the department the user works at.
        department_description (str): A brief description of the department.

    Returns:
        str: The system prompt.
    """
    return _SYSTEM_PROMPT.substitute(
        company=company_name,
        company_description=company_description,
        department=department_name,
        department_description=department_description,
    )


def get_user_prompt(title: str, abstract: str):
    """
    Generate a user prompt for evaluating a certain paper given its title and abstract.

    Args:
        title (str): The title to be included in the prompt.
        abstract (str): The abstract to be included in the prompt.

    Returns:
        str: The generated user prompt.
    """
    return _USER_PROMPT.substitute(title=title, abstract=abstract)
