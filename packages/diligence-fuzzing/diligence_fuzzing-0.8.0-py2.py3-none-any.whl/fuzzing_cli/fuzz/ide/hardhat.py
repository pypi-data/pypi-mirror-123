import json
from os.path import abspath, commonpath, relpath
from pathlib import Path
from typing import List

from fuzzing_cli.fuzz.exceptions import BuildArtifactsError
from fuzzing_cli.fuzz.ide.generic import IDEArtifacts, JobBuilder

from ...util import get_content_from_file, sol_files_by_directory


class HardhatArtifacts(IDEArtifacts):
    def __init__(self, build_dir=None, targets=None, map_to_original_source=False):
        self._include = []
        if targets:
            include = []
            for target in targets:
                include.extend(
                    [abspath(file_path) for file_path in sol_files_by_directory(target)]
                )
            self._include = include
        self._build_dir = Path(build_dir).absolute() or Path("./artifacts").absolute()
        self._contracts, self._sources = self.fetch_data(map_to_original_source)

    @property
    def contracts(self):
        return self._contracts

    @property
    def sources(self):
        return self._sources

    def fetch_data(self, map_to_original_source=False):
        result_contracts = {}
        result_sources = {}

        for file_path in self._include:
            cp = commonpath([self._build_dir, file_path])
            relative_file_path = relpath(file_path, cp)

            if relative_file_path in result_contracts:
                continue

            file_name = Path(file_path).stem
            file_artifact_path: Path = self._build_dir.joinpath(
                relative_file_path
            ).joinpath(f"{file_name}.json")
            file_debug_path: Path = self._build_dir.joinpath(
                relative_file_path
            ).joinpath(f"{file_name}.dbg.json")
            if not file_artifact_path.exists() or not file_debug_path.exists():
                raise BuildArtifactsError("Could not find target artifacts")

            with file_artifact_path.open("r") as file:
                file_artifact = json.load(file)
            with file_debug_path.open("r") as file:
                file_debug_artifact = json.load(file)
            build_info_name = Path(file_debug_artifact["buildInfo"]).name
            with self._build_dir.joinpath(f"build-info/{build_info_name}").open(
                "r"
            ) as file:
                build_info = json.load(file)

            result_contracts[relative_file_path] = []

            contracts = build_info["output"]["contracts"][relative_file_path]

            for contract, data in contracts.items():
                if data["evm"]["bytecode"]["object"] == "":
                    continue
                result_contracts[relative_file_path] += [
                    {
                        "sourcePaths": {
                            i: k
                            for i, k in enumerate(
                                build_info["output"]["contracts"].keys()
                            )
                        },
                        "deployedSourceMap": data["evm"]["deployedBytecode"][
                            "sourceMap"
                        ],
                        "deployedBytecode": data["evm"]["deployedBytecode"]["object"],
                        "sourceMap": data["evm"]["bytecode"]["sourceMap"],
                        "bytecode": data["evm"]["bytecode"]["object"],
                        "contractName": file_artifact["contractName"],
                        "mainSourceFile": file_artifact["sourceName"],
                    }
                ]

            for source_file_dep, data in build_info["output"]["sources"].items():
                if source_file_dep in result_sources.keys():
                    continue

                result_sources[source_file_dep] = {
                    "fileIndex": data["id"],
                    "source": build_info["input"]["sources"][source_file_dep][
                        "content"
                    ],
                    "ast": data["ast"],
                }

                if (
                    map_to_original_source
                    and Path(source_file_dep + ".original").is_file()
                ):
                    # we check if the current source file has a non instrumented version
                    # if it does, we include that one as the source code
                    result_sources[source_file_dep]["source"] = get_content_from_file(
                        source_file_dep + ".original"
                    )

        return result_contracts, result_sources


class HardhatJob:
    def __init__(
        self, target: List[str], build_dir: Path, map_to_original_source: bool
    ):
        artifacts = HardhatArtifacts(
            build_dir, targets=target, map_to_original_source=map_to_original_source
        )
        self._jb = JobBuilder(artifacts)
        self.payload = None

    def generate_payload(self):
        self.payload = self._jb.payload()
