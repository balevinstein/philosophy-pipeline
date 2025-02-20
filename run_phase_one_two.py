# run_phase_one.py

import json
import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
import requests

from tavily import TavilyClient
import markdownify


def load_final_selection() -> Dict[str, Any]:
    """Load final selection from Phase I.1"""
    try:
        with open("./outputs/final_selection.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find final_selection.json. Run Phase I.1 first.")


def check_rivet_life() -> Dict[str, Any]:
    """Check if Rivet server is up"""
    try:
        result = requests.get("http://localhost:4040/life", timeout=5000)
        if result.ok:
            print("Rivet alive")
    except ConnectionError:
        raise ValueError(
            "Could not connect to the Rivet server. Please run `node ./rivet/app.js --watch` in another terminal process"
        )


def get_lit_search_queries(final_selection):

    try:
        load_dotenv()
        request_data = {
            "final_selection": final_selection,
            "openAiKey": os.getenv("OPENAI_API_KEY"),
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            "http://localhost:4040/litResearch",
            data=json.dumps(request_data),
            timeout=5000,
            headers=headers,
        )

        if response.status_code == 200:
            try:
                return response.json()["queries"]
            except ValueError:
                print("Failed to decode JSON")

        print("Finished generating search queries")

    except Exception as e:
        print(f"\nError in Phase I pipeline: {str(e)}")
        sys.exit(1)


def get_lit_papers(search_results, final_selection):

    try:
        load_dotenv()
        request_data = {
            "search_results": search_results,
            "final_selection": final_selection,
            "openAiKey": os.getenv("OPENAI_API_KEY"),
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            "http://localhost:4040/litResearch/papers",
            data=json.dumps(request_data),
            timeout=5000,
            headers=headers,
        )

        if response.status_code == 200:
            try:
                return response.content
            except ValueError:
                print("Failed to decode JSON")

        print("Finished generating search queries")

    except Exception as e:
        print(f"\nError in Phase I pipeline: {str(e)}")
        sys.exit(1)


def run_phase_one_two():
    """Run stage 2 of Phase I in sequence"""

    try:
        print("\nStarting Phase I.2 pipeline...")
        print("\nPlease make sure you started the rivet node server...")

        load_dotenv()
        tavily_key = os.getenv("TAVILY_API_KEY")

        # Load Phase I.1 output
        final_selection = load_final_selection()

        check_rivet_life()

        queries = get_lit_search_queries(final_selection=final_selection)
        print("\nGenerated queries for web search")

        search_results = []
        tavily_client = TavilyClient(api_key=tavily_key)

        for query in queries:
            print("\nExecuting web search for:", query)
            response = tavily_client.search(
                query=query,
                search_depth="advanced",
                include_raw_content=False,
                max_results=5,
            )
            search_results.extend(response["results"])

        print("\nCompleted Web Search")

        papers = get_lit_papers(search_results, final_selection)
        papers = str(markdownify.markdownify(papers))

        print("\nPhase I.2 completed successfully!")
        print(
            "\n\nPlease download the following papers and add them to the src/papers directory"
        )
        print(papers)

        with open("./outputs/literature_research_papers.md", "w") as f:
            f.write(papers)

        return papers

    except Exception as e:
        print(f"\nError in Phase I.2 pipeline: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_phase_one_two()
