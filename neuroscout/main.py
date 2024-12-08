# Python imports
from pathlib import Path
import argparse
import asyncio

# Local imports
from neuroscout.data import NEURIPS_2024_PAPER_URLS
from neuroscout.utils import PaperEvaluator


def read_file(file_path: str):
    """Reads the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: The file '{file_path}' does not exist."
    except Exception as e:
        return f"Error: Unable to read file '{file_path}'. Reason: {e}"


async def main():
    parser = argparse.ArgumentParser(
        description="Read and combine content from multiple files."
    )
    parser.add_argument(
        "--company-name-file",
        type=Path,
        required=True,
        help="Path to the company name file",
    )
    parser.add_argument(
        "--company-description-file",
        type=Path,
        required=True,
        help="Path to the company description file",
    )
    parser.add_argument(
        "--department-name-file",
        type=Path,
        required=True,
        help="Path to the department name file",
    )
    parser.add_argument(
        "--department-description-file",
        type=Path,
        required=True,
        help="Path to the department description file",
    )

    args = parser.parse_args()

    # Read the content of each file
    company_name = read_file(args.company_name_file)
    company_description = read_file(args.company_description_file)
    department_name = read_file(args.department_name_file)
    department_description = read_file(args.department_description_file)

    evaluator = PaperEvaluator(
        company_name=company_name,
        company_description=company_description,
        department_name=department_name,
        department_description=department_description,
    )

    urls = NEURIPS_2024_PAPER_URLS
    tasks = [evaluator.evaluate_paper(url) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
