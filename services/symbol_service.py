"""
VolatilityForge

Symbol discovery service.

This module is responsible for discovering available trading symbols
from the configured data directory.
"""

from __future__ import annotations

from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SymbolService:
    """
    Service responsible for discovering available symbols.

    Supported file types:
        *.csv
        *.parquet
    """

    SUPPORTED_EXTENSIONS = {".csv", ".parquet"}

    def __init__(self, data_directory: Path):
        self._data_directory = Path(data_directory)
        self._symbols: list[str] = []

        self.refresh()

    @property
    def data_directory(self) -> Path:
        return self._data_directory

    def refresh(self) -> None:
        """
        Reload symbols from disk.
        """

        if not self._data_directory.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self._data_directory}"
            )

        symbols: set[str] = set()

        for item in self._data_directory.iterdir():

            if not item.is_file():
                continue

            if item.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            symbols.add(item.stem.upper())

        self._symbols = sorted(symbols)

        if self._symbols:
            logger.info("Loaded %d symbols.", len(self._symbols))
        else:
            logger.warning(
                "No symbol files found in %s",
                self._data_directory,
            )

    def get_symbols(self) -> list[str]:
        """
        Return all available symbols.
        """

        return list(self._symbols)

    def symbol_exists(self, symbol: str) -> bool:
        """
        Return True if symbol exists.
        """

        return symbol.upper() in self._symbols

    def __len__(self) -> int:
        return len(self._symbols)

    def __contains__(self, symbol: str) -> bool:
        return self.symbol_exists(symbol)