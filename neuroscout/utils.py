# Python imports
from functools import wraps
from typing import Any, Callable, Literal, Tuple
import asyncio

# 3rd party imports
import aiohttp
from bs4 import BeautifulSoup
from pydantic_ai.agent import Agent
from tenacity import retry, stop_after_attempt, wait_random_exponential


# Local imports
from neuroscout.prompts import get_system_prompt, get_user_prompt


def max_concurrent_calls(
    limit: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to limit the number of concurrent asynchronous function calls.

    Args:
        limit (int): The maximum number of concurrent asynchronous function calls allowed.

    Returns:
        function: A decorator that wraps the given function to enforce the concurrency limit.

    Example:
        @max_concurrent_calls(3)
        async def my_async_function():
            # Your async code here
    """
    semaphore = asyncio.Semaphore(limit)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Ensure that only up to 'limit' number of async tasks can run concurrently
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator


async def get_title_and_abstract(url: str) -> Tuple[str, str]:
    """
    Fetch the title and abstract from a given URL.

    This function sends an asynchronous HTTP GET request to the specified URL, parses
    the HTML content, and extracts the title and abstract of a paper.

    Args:
        url (str): The URL of the webpage to fetch the title and abstract from.

    Returns:
        Tuple[str, str]: A tuple containing the title and abstract of the paper.

    Raises:
        RuntimeError: If the title or abstract HTML elements cannot be found.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Find the title of the paper by getting the content of the h2 tag with class
    # "card-title main-title text-center"
    title_elem = soup.find("h2", {"class": "card-title main-title text-center"})
    if not title_elem:
        raise RuntimeError("Couldn't find the HTML element for title")
    title = title_elem.text

    # Get the content of the most inner <p> tag under the <div> tag with ID
    # "abstract_details"
    abstract_elem = soup.select_one("div#abstract_details p")
    if not abstract_elem:
        raise RuntimeError("Couldn't find the HTML element for abstract")
    abstract = abstract_elem.text

    return title.strip(), abstract.strip()


class PaperEvaluator:
    """
    A class to evaluate relevance of research papers to a user work using an AI agent.

    Attributes:
        company_name (str): The name of the company the user works at.
        company_description (str): A description of the company.
        department_name (str): The name of the department the user works at.
        department_description (str): A description of the department.
        model (str): The model to be used by the agent. Defaults to "openai:gpt-4o".

    Methods:
        evaluate_paper(url: str):
            Asynchronously evaluates a research paper given its URL.
    """

    def __init__(
        self,
        company_name: str,
        company_description: str,
        department_name: str,
        department_description: str,
        model: Literal["openai:gpt-4o"] = "openai:gpt-4o",
    ):
        """
        Initializes the PaperEvaluator with company and department details, and sets up
        the AI agent.

        Args:
            company_name (str): The name of the company.
            company_description (str): A description of the company.
            department_name (str): The name of the department.
            department_description (str): A description of the department.
            model (str): The model to be used by the agent. Defaults to "openai:gpt-4o".
        """
        system_prompt = get_system_prompt(
            company_name=company_name,
            company_description=company_description,
            department_name=department_name,
            department_description=department_description,
        )
        self.agent = Agent(model=model, system_prompt=system_prompt)
        self.company_name = company_name
        self.company_description = company_description
        self.department_name = department_name
        self.department_description = department_description

    @retry(wait=wait_random_exponential(min=15, max=300), stop=stop_after_attempt(20))
    async def _run_agent(self, paper_title: str, paper_abstract: str) -> str:
        """
        Runs the AI agent to evaluate the paper based on its title and abstract.

        Args:
            paper_title (str): The title of the paper.
            paper_abstract (str): The abstract of the paper.

        Returns:
            str: The evaluation verdict from the AI agent.
        """
        response = await self.agent.run(get_user_prompt(paper_title, paper_abstract))
        last_message = response.all_messages()[-1]
        return last_message.content  # type: ignore

    @max_concurrent_calls(5)
    async def evaluate_paper(self, url: str):
        """
        Asynchronously evaluates a research paper given its URL.

        Args:
            url (str): The URL of the research paper.

        Prints:
            The title, URL, and evaluation verdict of the paper.
        """
        paper_title, paper_abstract = await get_title_and_abstract(url)

        verdict = await self._run_agent(paper_title, paper_abstract)
        print(f"Evaluating the paper: {paper_title}")
        print(f"Link: {url}")
        print()
        print(f"Verdict: {verdict}")
        print()
        print("=" * 80)
        print()
