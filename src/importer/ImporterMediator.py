from src.entity.ExtractCollection import ExtractCollection
from src.importer import ErlekamImporter


def __extract_by__(dirname: str) -> ExtractCollection:
    if 'tri_tetra' == dirname:
        return __extract_man1355llbb25__()
    if 'deca_bi' == dirname:
        return __extract_man1010lacetate2__()


def __extract_man1355llbb25__() -> ExtractCollection:
    return ErlekamImporter.extract_collection('data/Man1355LLBB25.xlsx', False)


def __extract_man1010lacetate2__() -> ExtractCollection:
    return ErlekamImporter.extract_collection('data/Man1010Lacetate2.xlsx', False)
