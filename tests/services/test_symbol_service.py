from pathlib import Path

import pytest

from services.symbol_service import SymbolService


def test_empty_directory(tmp_path: Path):
    service = SymbolService(tmp_path)
    assert service.get_symbols() == []


def test_csv_discovery(tmp_path: Path):
    (tmp_path / "NIFTY.csv").touch()

    service = SymbolService(tmp_path)

    assert service.get_symbols() == ["NIFTY"]


def test_parquet_discovery(tmp_path: Path):
    (tmp_path / "BANKNIFTY.parquet").touch()

    service = SymbolService(tmp_path)

    assert service.get_symbols() == ["BANKNIFTY"]


def test_ignore_other_files(tmp_path: Path):
    (tmp_path / "README.md").touch()
    (tmp_path / "notes.txt").touch()
    (tmp_path / "NIFTY.csv").touch()

    service = SymbolService(tmp_path)

    assert service.get_symbols() == ["NIFTY"]


def test_sorted_symbols(tmp_path: Path):
    (tmp_path / "SBIN.csv").touch()
    (tmp_path / "INFY.csv").touch()
    (tmp_path / "RELIANCE.csv").touch()

    service = SymbolService(tmp_path)

    assert service.get_symbols() == [
        "INFY",
        "RELIANCE",
        "SBIN",
    ]


def test_symbol_exists(tmp_path: Path):
    (tmp_path / "TCS.csv").touch()

    service = SymbolService(tmp_path)

    assert service.symbol_exists("TCS")
    assert service.symbol_exists("tcs")
    assert not service.symbol_exists("INFY")


def test_missing_directory():
    with pytest.raises(FileNotFoundError):
        SymbolService(Path("directory_does_not_exist"))