# process_domain_mixins.py

from pathlib import Path
from typing import Optional


class DomainFileToolMixin:
    """
    Standard contract for tools that operate on dataset_file (+ optional dictionary_file).
    """

    def process_domain(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[Path],
        output_path: Path,
        **kwargs
    ) -> None:
        """
        Contract:
        - dataset_file MUST be used via self.load_data_file or equivalent
        - dictionary_file may be required depending on tool
        """

        if dataset_file is None:
            raise ValueError(f"{self.__class__.__name__} requires dataset_file")

        # enforce explicit intent clarity
        _ = dictionary_file

        return self._process_domain_impl(
            domain=domain,
            dataset_file=dataset_file,
            dictionary_file=dictionary_file,
            output_path=output_path,
            **kwargs
        )

    def _process_domain_impl(self, *args, **kwargs):
        raise NotImplementedError


class DomainMappedToolMixin:
    """
    Tools where domain determines file resolution (NOT dataset_file driven).
    """

    def process_domain(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[Path],
        output_path: Path,
        **kwargs
    ) -> None:

        # dataset_file is intentionally unused in this pattern
        _ = dataset_file
        _ = dictionary_file

        return self._process_domain_impl(
            domain=domain,
            output_path=output_path,
            **kwargs
        )

    def _process_domain_impl(self, *args, **kwargs):
        raise NotImplementedError


class EngineWrapperToolMixin:
    """
    Tools that delegate processing to an internal engine.
    """

    def process_domain(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[Path],
        output_path: Path,
        **kwargs
    ) -> None:

        return self._process_domain_impl(
            domain=domain,
            dataset_file=dataset_file,
            output_path=output_path,
            **kwargs
        )

    def _process_domain_impl(self, *args, **kwargs):
        raise NotImplementedError