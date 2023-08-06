# CoverageToImg

## Introduction
To convert from coverage.json - that is made by [coverage](https://pypi.org/project/coverage/) library of pypi - to image

- Example of structure of coverage.json
```json
{
    "meta": {
        "version": "6.0.2",
        "timestamp": "2021-10-15T10:56:02.804556",
        "branch_coverage": false,
        "show_contexts": false
    }
    "files": {
        "path/file_name.py": {
            "executed_lines": [],
            "summary": {
                "covered_lines": 0,
                "num_statements": 0,
                "percent_covered": 100.0,
                "percent_covered_display": "100",
                "missing_lines": 0,
                "excluded_lines": 0
            },
            "missing_lines": [],
            "excluded_lines": []
        },
        ...
    }
    "totals": {
        "covered_lines": 100,
        "num_statements": 200,
        "percent_covered": 80.0,
        "percent_covered_display": "80",
        "missing_lines": 19,
        "excluded_lines": 1,
    }
}
```

## Example
- coverage.json -> png
```bash
coverage2img -i coverage.json -o result.png
```