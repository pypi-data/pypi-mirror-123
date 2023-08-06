from typing import Dict, List


class MetaModel(object):
    def __init__(
            self,
            version: str,
            timestamp: str,
            branch_coverage: bool,
            show_contexts: bool
    ):
        self.version = version
        self.timestamp = timestamp
        self.branch_coverage = branch_coverage
        self.show_contexts = show_contexts

    def to_dict(self):
        return {
            'version': self.version,
            'timestamp': self.timestamp,
            'branch_coverage': self.branch_coverage,
            'show_contexts': self.show_contexts,
        }


class SummaryModel(object):
    def __init__(
            self,
            covered_lines: int,
            num_statements: int,
            percent_covered: float,
            percent_covered_display: str,
            missing_lines: int,
            excluded_lines: int,
    ):
        self.covered_lines = covered_lines
        self.num_statements = num_statements
        self.percent_covered = percent_covered
        self.percent_covered_display = percent_covered_display
        self.missing_lines = missing_lines
        self.excluded_lines = excluded_lines

    def to_dict(self):
        return {
            'covered_lines': self.covered_lines,
            'num_statements': self.num_statements,
            'percent_covered': self.percent_covered,
            'percent_covered_display': self.percent_covered_display,
            'missing_lines': self.missing_lines,
            'excluded_lines': self.excluded_lines,
        }


class FileModel(object):
    def __init__(
            self,
            executed_lines: List[int],
            summary: Dict,
            missing_lines: List[int],
            excluded_lines: List[int],
    ):
        self.executed_lines = executed_lines
        self.summary = SummaryModel(**summary)
        self.missing_lines = missing_lines
        self.excluded_lines = excluded_lines

    def to_dict(self):
        return {
            'executed_lines': self.executed_lines,
            'summary': self.summary.to_dict(),
            'missing_lines': self.missing_lines,
            'excluded_lines': self.excluded_lines,
        }


class FilesModel(object):
    def __init__(self, files_data: Dict):
        self.coverage_of_files = self._render(files_data)

    def _render(self, data: Dict):
        result = {}
        for key in data.keys():
            result[key] = FileModel(**data[key])
        return result

    def to_dict(self):
        return {k: v.to_dict() for k, v in self.coverage_of_files.items()}


class CoverageModel(object):
    def __init__(
            self,
            meta: Dict,
            files: Dict,
            totals: Dict,
    ):
        self.meta = MetaModel(**meta)
        self.files = FilesModel(files)
        self.totals = SummaryModel(**totals)

    def to_dict(self):
        return {
            'meta': self.meta.to_dict(),
            'files': self.files.to_dict(),
            'totals': self.totals.to_dict(),
        }
