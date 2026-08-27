def generate_system_prompt(
    assistant_name: str = "KYREN",
    assistant_full_name: str = "Knowledge-based Yielding Reasoning Executive Network"
    ) -> str:
    """
    Generate the system prompt for the configured assistant.

    Returns:
        str: The system prompt for the assistant.
    """
    return f"You are {assistant_name.strip()}, a helpful voice assistant."
