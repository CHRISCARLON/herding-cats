import os
from typing import List, Dict, Any
from dataclasses import dataclass, field
import adalflow as adal
from adalflow.core import Generator
from adalflow.components.model_client.openai_client import OpenAIClient
from adalflow.optim.parameter import Parameter, ParameterType
from loguru import logger

from ..session.session import CatSession
from ..explorer.explore import (
    CkanCatExplorer,
    DataPressCatExplorer,
    OpenDataSoftCatExplorer,
    FrenchGouvCatExplorer,
    ONSNomisCatExplorer,
)
from ..config.sources import (
    CkanDataCatalogues,
    DataPressCatalogues,
    OpenDataSoftDataCatalogues,
    FrenchGouvCatalogue,
    ONSNomisAPI,
)


@dataclass
class DatasetSearchResult(adal.DataClass):
    """Data class for dataset search results."""

    dataset_title: str = field(
        default="",
        metadata={"desc": "The title of the most relevant dataset found"}
    )
    dataset_id: str = field(
        default="",
        metadata={"desc": "The ID or identifier of the dataset"}
    )
    catalog_source: str = field(
        default="",
        metadata={"desc": "The catalog where this dataset was found"}
    )
    relevance_score: float = field(
        default=0.0,
        metadata={"desc": "Score indicating relevance (0-1)"}
    )
    relevance_explanation: str = field(
        default="",
        metadata={"desc": "Explanation of why this dataset is relevant to the query"}
    )
    dataset_description: str = field(
        default="",
        metadata={"desc": "Brief description of the dataset content"}
    )
    access_instructions: str = field(
        default="",
        metadata={"desc": "Instructions on how to access the dataset"}
    )

    __output_fields__ = [
        "dataset_title",
        "dataset_id",
        "catalog_source",
        "relevance_score",
        "relevance_explanation",
        "dataset_description",
        "access_instructions"
    ]


class DatasetDiscoveryAgent:
    """Agent for discovering datasets across multiple catalogues based on user queries."""

    def __init__(self, temperature=0.2, model="gpt-4o-mini"):
        """
        Initialise the dataset discovery agent.

        Args:
            temperature: Controls randomness in the LLM response (lower = more deterministic)
            model: The LLM model to use for reasoning
        """
        # Initialize the LLM-based agent
        self.temperature = temperature
        self.model = model

        # Create the system prompt for dataset search
        self.search_system_prompt = Parameter(
            data="""
            You are a data discovery agent that helps users find the most relevant datasets for their needs.
            Your task is to analyse dataset metadata and identify the single most relevant dataset that best matches the user's query.

            Consider the following when assessing dataset relevance:
            1. Subject matter relevance to the query
            2. Data completeness and quality
            3. Recency of the data
            4. Format accessibility
            5. Geographic coverage if relevant

            Provide a clear explanation of why the chosen dataset is the best match for the query and how it can be used.
            """,
            role_desc="System instructions for the dataset discovery agent",
            requires_opt=False,
            param_type=ParameterType.PROMPT,
        )

        self.parser = adal.DataClassParser(
            data_class=DatasetSearchResult,  # type: ignore
            return_data_class=True,
            format_type="json",
        )

        # Define the template for dataset discovery
        self.template = r"""<START_OF_SYSTEM_PROMPT>
            {{search_system_prompt}}
            <OUTPUT_FORMAT>
            {{output_format_str}}
            </OUTPUT_FORMAT>
            <END_OF_SYSTEM_PROMPT>
            <START_OF_USER>
            I need to find a dataset about: {{search_topic}}

            Here are potential datasets I found across different catalogs:

            {{dataset_candidates}}

            Please analyse these datasets and recommend the single most relevant one that best matches my search topic.
            Provide a relevance score between 0-1 (where 1 is perfectly relevant) and explain your reasoning.
            <END_OF_USER>
        """

        self.generator = Generator(
            model_client=OpenAIClient(),
            model_kwargs={
                "model": self.model,
                "temperature": self.temperature,  # type: ignore
            },
            template=self.template,
            prompt_kwargs={
                "search_system_prompt": self.search_system_prompt,
                "output_format_str": self.parser.get_output_format_str(),
            },
            output_processors=self.parser,
        )

    def find_dataset(self, search_topic: str, max_datasets_per_catalog: int = 5) -> DatasetSearchResult:
        """
        Search across multiple catalogues to find the most relevant dataset for the given topic.

        Args:
            search_topic: The user's search query
            max_datasets_per_catalog: Maximum number of datasets to retrieve from each catalog

        Returns:
            DatasetSearchResult with the most relevant dataset
        """
        # Check for API key
        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Get candidate datasets from different catalogs
        logger.info(f"Searching for datasets about: {search_topic}")
        candidate_datasets = self._gather_candidate_datasets(search_topic, max_datasets_per_catalog)

        if not candidate_datasets:
            logger.warning("No datasets found matching the search criteria.")
            return DatasetSearchResult(
                dataset_title="No matching datasets found",
                relevance_explanation="No datasets were found matching your search criteria."
            )

        # Format the candidate datasets for the LLM
        dataset_candidates_text = self._format_candidates_for_llm(candidate_datasets)
        print(dataset_candidates_text)

        # Analyse and select the best dataset
        logger.info(f"Analysing {len(candidate_datasets)} candidate datasets")
        response = self.generator(
            prompt_kwargs={
                "search_topic": search_topic,
                "dataset_candidates": dataset_candidates_text
            }
        )

        if response.error:
            raise Exception(f"Error analyzing datasets: {response.error}")

        # Get the structured output
        result = response.data
        if not isinstance(result, DatasetSearchResult):
            raise TypeError(f"Expected DatasetSearchResult, got {type(result)}")

        logger.success(f"Found best matching dataset: {result.dataset_title}")
        return result

    def _gather_candidate_datasets(self, search_topic: str, max_per_catalog: int) -> List[Dict[str, Any]]:
        """
        Gather candidate datasets from multiple catalogs.

        Args:
            search_topic: The search query
            max_per_catalog: Maximum datasets to retrieve per catalog

        Returns:
            List of candidate datasets with metadata
        """
        all_candidates = []

        # Get datasets from CKAN catalogs
        ckan_candidates = self._search_ckan_catalogs(search_topic, max_per_catalog)
        all_candidates.extend(ckan_candidates)

        # Get datasets from DataPress catalogs
        datapress_candidates = self._search_datapress_catalogs(search_topic, max_per_catalog)
        all_candidates.extend(datapress_candidates)

        # Get datasets from OpenDataSoft catalogs
        opendata_candidates = self._search_opendata_catalogs(search_topic, max_per_catalog)
        all_candidates.extend(opendata_candidates)

        # Get datasets from French Gov catalog
        french_gov_candidates = self._search_french_gov_catalogs(search_topic, max_per_catalog)
        all_candidates.extend(french_gov_candidates)

        # Get datasets from ONS Nomis catalog
        ons_candidates = self._search_ons_catalogs(search_topic, max_per_catalog)
        all_candidates.extend(ons_candidates)

        return all_candidates

    def _search_ckan_catalogs(self, search_topic: str, max_per_catalog: int) -> List[Dict[str, Any]]:
        """Search through CKAN catalogs for relevant datasets."""
        candidates = []

        for catalog in CkanDataCatalogues:
            try:
                with CatSession(catalog) as session:
                    explorer = CkanCatExplorer(session)

                    # Search for datasets using the explorer's package_search method
                    logger.info(f"Searching {catalog.name} for '{search_topic}'")
                    search_results = explorer.package_search_condense(search_topic, max_per_catalog)

                    if search_results:  # Make sure search_results is not None
                        # Process and add each result to candidates
                        for dataset in search_results:
                            candidates.append({
                                "title": dataset.get("name", "Unknown"),
                                "description": dataset.get("notes_markdown", "No description available"),
                                "catalog": catalog.name,
                                "catalog_type": "CKAN",
                                "id": dataset.get("name", ""),
                                "resources": dataset.get("resources", []),
                                "resource_count": len(dataset.get("resources", [])),
                            })
            except Exception as e:
                logger.warning(f"Error searching {catalog.name}: {str(e)}")

        return candidates

    def _search_datapress_catalogs(self, search_topic: str, max_per_catalog: int) -> List[Dict[str, Any]]:
        """Search through DataPress catalogs for relevant datasets."""
        candidates = []

        for catalog in DataPressCatalogues:
            try:
                with CatSession(catalog) as session:
                    explorer = DataPressCatExplorer(session)

                    # Get all datasets since DataPress doesn't have a direct search method
                    logger.info(f"Searching {catalog.name} for '{search_topic}'")
                    all_datasets = explorer.get_all_datasets()

                    # Filter datasets by checking if search terms appear in title
                    # This is a simple approach - in a real implementation, you might want to use
                    # more sophisticated text matching
                    search_terms = search_topic.lower().split()
                    matched_datasets = []

                    for title, dataset_id in all_datasets.items():
                        title_lower = title.lower()
                        if any(term in title_lower for term in search_terms):
                            matched_datasets.append((title, dataset_id))

                    # Limit the number of datasets
                    matched_datasets = matched_datasets[:max_per_catalog]

                    # Get more details for each matched dataset
                    for title, dataset_id in matched_datasets:
                        try:
                            dataset_info = explorer.get_dataset_by_id(dataset_id)
                            resources = explorer.get_resource_by_dataset_id(dataset_id)

                            candidates.append({
                                "title": title,
                                "description": dataset_info.get("notes", "No description available"),
                                "catalog": catalog.name,
                                "catalog_type": "DataPress",
                                "id": dataset_id,
                                "resources": resources,
                                "resource_count": len(resources) if resources else 0,
                            })
                        except Exception as e:
                            logger.warning(f"Error getting details for {title}: {str(e)}")
            except Exception as e:
                logger.warning(f"Error searching {catalog.name}: {str(e)}")

        return candidates

    def _search_opendata_catalogs(self, search_topic: str, max_per_catalog: int) -> List[Dict[str, Any]]:
        """Search through OpenDataSoft catalogs for relevant datasets."""
        candidates = []

        for catalog in OpenDataSoftDataCatalogues:
            try:
                with CatSession(catalog) as session:
                    explorer = OpenDataSoftCatExplorer(session)

                    # Get all datasets
                    logger.info(f"Searching {catalog.name} for '{search_topic}'")
                    all_datasets = explorer.fetch_all_datasets()

                    if not all_datasets:
                        continue

                    # Filter datasets by checking if search terms appear in title
                    search_terms = search_topic.lower().split()
                    matched_datasets = []

                    for title, dataset_id in all_datasets.items():
                        title_lower = title.lower()
                        if any(term in title_lower for term in search_terms):
                            matched_datasets.append((title, dataset_id))

                    # Limit the number of datasets
                    matched_datasets = matched_datasets[:max_per_catalog]

                    # Get more details for each matched dataset
                    for title, dataset_id in matched_datasets:
                        try:
                            dataset_info = explorer.show_dataset_info(dataset_id)
                            export_options = explorer.show_dataset_export_options(dataset_id)

                            description = "No description available"
                            if "dataset" in dataset_info and "metas" in dataset_info["dataset"] and "default" in dataset_info["dataset"]["metas"]:
                                description = dataset_info["dataset"]["metas"]["default"].get("description", description)

                            candidates.append({
                                "title": title,
                                "description": description,
                                "catalog": catalog.name,
                                "catalog_type": "OpenDataSoft",
                                "id": dataset_id,
                                "resources": export_options,
                                "resource_count": len(export_options) if export_options else 0,
                            })
                        except Exception as e:
                            logger.warning(f"Error getting details for {title}: {str(e)}")
            except Exception as e:
                logger.warning(f"Error searching {catalog.name}: {str(e)}")

        return candidates

    def _search_french_gov_catalogs(self, search_topic: str, max_per_catalog: int) -> List[Dict[str, Any]]:
        """Search through French Government catalogs for relevant datasets."""
        candidates = []

        for catalog in FrenchGouvCatalogue:
            try:
                with CatSession(catalog) as session:
                    explorer = FrenchGouvCatExplorer(session)

                    # Use the search_datasets method directly
                    logger.info(f"Searching {catalog.name} for '{search_topic}'")
                    search_results = explorer.search_datasets(search_topic)

                    # Limit the number of results
                    limited_results = search_results[:max_per_catalog]

                    # Process each result
                    for dataset in limited_results:
                        dataset_id = dataset.get("id", "")

                        # Get detailed info for the dataset
                        try:
                            dataset_meta = explorer.get_dataset_meta(dataset_id)
                            resources = explorer.get_dataset_resource_meta(dataset_meta) if dataset_meta else []

                            candidates.append({
                                "title": dataset.get("title", "Unknown"),
                                "description": dataset.get("description", "No description available"),
                                "catalog": catalog.name,
                                "catalog_type": "FrenchGouv",
                                "id": dataset_id,
                                "resources": resources,
                                "resource_count": len(resources) if resources else 0,
                            })
                        except Exception as e:
                            logger.warning(f"Error getting details for dataset {dataset_id}: {str(e)}")
            except Exception as e:
                logger.warning(f"Error searching {catalog.name}: {str(e)}")

        return candidates

    def _search_ons_catalogs(self, search_topic: str, max_per_catalog: int) -> List[Dict[str, Any]]:
        """Search through ONS Nomis catalogs for relevant datasets."""
        candidates = []

        for catalog in ONSNomisAPI:
            try:
                with CatSession(catalog) as session:
                    explorer = ONSNomisCatExplorer(session)

                    # Get all datasets
                    logger.info(f"Searching {catalog.name} for '{search_topic}'")
                    all_datasets = explorer.get_all_datasets()

                    # Filter datasets by checking if search terms appear in name
                    search_terms = search_topic.lower().split()
                    matched_datasets = []

                    for dataset in all_datasets:
                        name_lower = dataset.get("name", "").lower()
                        if any(term in name_lower for term in search_terms):
                            matched_datasets.append(dataset)

                    # Limit the number of datasets
                    matched_datasets = matched_datasets[:max_per_catalog]

                    # Get more details for each matched dataset
                    for dataset in matched_datasets:
                        dataset_id = dataset.get("id")
                        try:
                            dataset_info = explorer.get_dataset_info(dataset_id)

                            candidates.append({
                                "title": dataset.get("name", "Unknown"),
                                "description": "ONS Nomis dataset",
                                "catalog": catalog.name,
                                "catalog_type": "ONSNomis",
                                "id": dataset_id,
                                "resources": dataset_info,
                                "resource_count": len(dataset_info) if dataset_info else 0,
                            })
                        except Exception as e:
                            logger.warning(f"Error getting details for {dataset.get('name')}: {str(e)}")
            except Exception as e:
                logger.warning(f"Error searching {catalog.name}: {str(e)}")

        return candidates

    def _format_candidates_for_llm(self, candidates: List[Dict[str, Any]]) -> str:
        """
        Format the candidate datasets for the LLM to analyze.

        Args:
            candidates: List of candidate datasets

        Returns:
            Formatted text for the LLM prompt
        """
        formatted_text = ""

        for i, dataset in enumerate(candidates):
            formatted_text += f"DATASET {i+1}:\n"
            formatted_text += f"Title: {dataset['title']}\n"
            formatted_text += f"Description: {dataset['description']}\n"
            formatted_text += f"Catalog: {dataset['catalog']} ({dataset['catalog_type']})\n"
            formatted_text += f"Dataset ID: {dataset['id']}\n"
            formatted_text += f"Number of resources: {dataset['resource_count']}\n"

            # Add resource information if available
            if dataset['resource_count'] > 0 and isinstance(dataset['resources'], list):
                formatted_text += "Resource formats: "
                # Try to extract formats from resources (handling different catalog structures)
                formats = []
                for resource in dataset['resources'][:3]:
                    if isinstance(resource, dict):
                        if 'format' in resource:
                            formats.append(resource['format'])
                        elif 'resource_format' in resource:
                            formats.append(resource['resource_format'])
                formatted_text += ", ".join(formats) if formats else "Unknown"
                formatted_text += "\n"

            formatted_text += "\n"

        return formatted_text

    def _check_context_length(self, text: str, max_tokens: int = 16000) -> str:
        """
        Check if the context is too long for the LLM and truncate if necessary.

        Args:
            text: The text to check
            max_tokens: Maximum token count allowed

        Returns:
            Truncated text if necessary
        """
        # Rough approximation: 1 token ≈ 4 characters for English text
        estimated_tokens = len(text) / 4

        if estimated_tokens > max_tokens:
            ratio = max_tokens / estimated_tokens
            safe_ratio = ratio * 0.8
            chars_to_keep = int(len(text) * safe_ratio)

            # Find the last newline before our cutoff to avoid cutting mid-dataset
            last_newline = text[:chars_to_keep].rfind("\n\n")
            if last_newline == -1:
                last_newline = text[:chars_to_keep].rfind("\n")

            truncated_text = text[:last_newline] if last_newline != -1 else text[:chars_to_keep]

            truncated_text += "\n\n[Note: Dataset list was truncated due to length constraints. Analysis is based on the datasets shown above.]"

            logger.warning(f"Dataset list truncated from {len(text)} chars to {len(truncated_text)} chars due to token limit")
            return truncated_text

        return text
