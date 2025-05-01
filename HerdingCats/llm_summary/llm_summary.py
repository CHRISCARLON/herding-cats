from dataclasses import dataclass, field
import json

# Import adalflow components
import adalflow as adal
from adalflow.core import Generator
from adalflow.components.model_client.openai_client import OpenAIClient
from adalflow.optim.parameter import Parameter, ParameterType
from HerdingCats.llm_summary.llm_config import LLMCatalogueSummary


@dataclass
class CkanPackageSummary(adal.DataClass):
    """Data class for structured CKAN package summary output."""

    title: str = field(
        default="", metadata={"desc": "The title or name of the dataset/package"}
    )
    description: str = field(
        default="",
        metadata={"desc": "A concise description of the dataset (100-200 words)"},
    )
    key_resources: list[dict] = field(
        default_factory=list,
        metadata={"desc": "List of key resources with name, format, and description"},
    )
    metadata_summary: dict = field(
        default_factory=dict,
        metadata={
            "desc": "Summary of important metadata like update frequency, license, etc."
        },
    )
    data_highlights: list[str] = field(
        default_factory=list,
        metadata={"desc": "List of key highlights or insights about the data"},
    )
    potential_uses: list[str] = field(
        default_factory=list,
        metadata={"desc": "List of potential use cases for this dataset"},
    )

    __output_fields__ = [
        "title",
        "description",
        "key_resources",
        "metadata_summary",
        "data_highlights",
        "potential_uses",
    ]


class CkanCatalogueSummariser(LLMCatalogueSummary):
    """Implementation of the LLMCatalogueSummary protocol for CKAN package information."""

    def __init__(self, temperature=0.2):
        """
        Initialize the CKAN catalogue summarizer with AdalFlow components.
        Uses GPT-4o-mini as specified.

        Args:
            temperature: The temperature parameter for generation
        """
        # Define the system prompt as a parameter
        self.system_prompt = Parameter(
            data="""You are a data catalogue specialist who helps users understand and extract value from open data packages in CKAN catalogues.
Your task is to analyze and summarize dataset metadata in a clear, structured format that highlights the most important aspects of the dataset.
Focus on providing information that would help a data analyst or data scientist quickly understand:
1. What the dataset contains
2. The key available resources and their formats
3. Important metadata like update frequency and license
4. Potential uses for the dataset""",
            role_desc="To provide task instructions to the language model",
            requires_opt=False,
            param_type=ParameterType.PROMPT,
        )

        # Create a parser for structured output
        self.parser = adal.DataClassParser(
            data_class=CkanPackageSummary, # type: ignore
            return_data_class=True,
            format_type="json",
        )

        # Define the template with output format
        self.template = r"""<START_OF_SYSTEM_PROMPT>
            {{system_prompt}}
            <OUTPUT_FORMAT>
            {{output_format_str}}
            </OUTPUT_FORMAT>
            <END_OF_SYSTEM_PROMPT>
            <START_OF_USER>
            Please analyze and summarize the following CKAN dataset information:

            DATASET METADATA:
            {{package_json}}

            {% if context is not none %}
            ADDITIONAL CONTEXT:
            {{context}}
            {% endif %}

            Please provide a concise, structured summary of this dataset that would help users understand its contents, potential uses, and key characteristics.
            <END_OF_USER>
        """

        # Initialise the Generator with GPT-4o-mini
        self.generator = Generator(
            model_client=OpenAIClient(),
            model_kwargs={
                "model": "gpt-4o-mini",
                "temperature": temperature,  # type: ignore
            },
            template=self.template,
            prompt_kwargs={
                "system_prompt": self.system_prompt,
                "output_format_str": self.parser.get_output_format_str(),
            },
            output_processors=self.parser,
        )

    def summarise_catalogue(self, catalogue_data) -> dict:
        """
        Summarise the provided CKAN package information.

        Args:
            catalogue_data: A dictionary or list of dictionaries containing the package information

        Returns:
            A dictionary containing the structured summary
        """
        # Convert to JSON for the prompt
        package_json = json.dumps(catalogue_data, indent=2)

        # Generate the summary using AdalFlow
        response = self.generator(
            prompt_kwargs={"package_json": package_json, "context": None}
        )

        if response.error:
            raise Exception(f"Error generating summary: {response.error}")

        # Get the structured output and ensure proper typing
        summary = response.data
        if not isinstance(summary, CkanPackageSummary):
            raise TypeError(f"Expected CkanPackageSummary, got {type(summary)}")

        # Return as a dictionary
        return {
            "title": summary.title,
            "description": summary.description,
            "key_resources": summary.key_resources,
            "metadata_summary": summary.metadata_summary,
            "data_highlights": summary.data_highlights,
            "potential_uses": summary.potential_uses,
        }
