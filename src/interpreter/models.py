"""Shared utilities for model downloading and recovery."""

import shutil
from pathlib import Path

from huggingface_hub.constants import HF_HUB_CACHE

from . import log

logger = log.get_logger()

# Custom models directory; None means use the default HuggingFace cache.
_custom_models_dir: Path | None = None


def set_models_dir(path: Path | str) -> None:
    """Override the directory where models are stored.

    Must be called before any model is loaded or downloaded.

    Args:
        path: Directory to use instead of the default HuggingFace cache
              (~/.cache/huggingface/hub/).
    """
    global _custom_models_dir
    _custom_models_dir = Path(path)
    _custom_models_dir.mkdir(parents=True, exist_ok=True)
    logger.info("custom models directory set", path=str(_custom_models_dir))


def get_models_dir() -> Path:
    """Return the active models directory.

    Returns:
        The custom directory if set via set_models_dir(), otherwise the
        default HuggingFace hub cache directory.
    """
    if _custom_models_dir is not None:
        return _custom_models_dir
    return Path(HF_HUB_CACHE)


def get_hf_cache_path(repo_id: str) -> Path:
    """Get the cache directory for a HuggingFace repository.

    Args:
        repo_id: Repository ID (e.g., "org/model-name").

    Returns:
        Path to the cache directory for this repo.
    """
    # HuggingFace stores repos as: <cache>/models--org--repo/
    repo_folder = "models--" + repo_id.replace("/", "--")
    return get_models_dir() / repo_folder


def delete_model_cache(repo_id: str) -> bool:
    """Delete cached model to force re-download.

    Args:
        repo_id: Repository ID (e.g., "org/model-name").

    Returns:
        True if cache was deleted, False if it didn't exist.
    """
    cache_path = get_hf_cache_path(repo_id)
    if cache_path.exists():
        logger.info("deleting model cache", repo=repo_id)
        shutil.rmtree(cache_path)
        return True
    return False


class ModelLoadError(Exception):
    """Raised when a model fails to load."""

    pass
