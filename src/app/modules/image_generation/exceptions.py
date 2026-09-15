class ImageGenerationRateLimitError(Exception):
    """Raised when the configured image provider has no available quota."""
