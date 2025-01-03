import os
import argparse
from typing import List, Set
import pathlib


def find_files(
    directories: List[str],
    files: List[str],
    ignore_dirs: Set[str],
    extensions: Set[str],
) -> List[tuple[str, str]]:
    """指定されたディレクトリとファイルから、条件に一致するファイルを探し、ファイルパスと内容のタプルをリストで返す

    Args:
        directories (List[str]): 検索対象のディレクトリパスのリスト
        files (List[str]): 検索対象のファイルパスのリスト
        ignore_dirs (Set[str]): 除外するディレクトリ名のセット
        extensions (Set[str]): 検索対象の拡張子のセット

    Returns:
        List[tuple[str, str]]: ファイルパスとファイル内容のタプルのリスト
    """
    found_files: List[tuple[str, str]] = []

    # ディレクトリ内のファイルを検索
    for directory in directories:
        abs_dir = pathlib.Path(directory).resolve()
        for root, dirs, files_in_dir in os.walk(abs_dir):
            # 除外ディレクトリをフィルタリング
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files_in_dir:
                if not extensions or pathlib.Path(file).suffix in extensions:
                    file_path = pathlib.Path(root) / file
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            relative_path = file_path.relative_to(pathlib.Path.cwd())
                            found_files.append((str(relative_path), content))
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")

    # 個別ファイルを検索
    for file in files:
        file_path = pathlib.Path(file).resolve()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                relative_path = file_path.relative_to(pathlib.Path.cwd())
                found_files.append((str(relative_path), content))
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return found_files


def generate_tree_structure(
    found_files: List[tuple[str, str]],
) -> str:
    """
    ファイルリストからディレクトリ構造を生成する

    Args:
        found_files (List[tuple[str, str]]): ファイルパスと内容のタプルのリスト

    Returns:
        str: ディレクトリ構造を表す文字列
    """

    tree = {}
    for file_path, _ in found_files:
        parts = file_path.split(os.sep)
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = None

    def _format_tree(tree, prefix=""):
        output = ""
        items = sorted(tree.items())
        for i, (key, value) in enumerate(items):
            is_last = i == len(items) - 1
            output += prefix
            if is_last:
                output += "└── "
            else:
                output += "├── "
            output += key + "\n"

            if isinstance(value, dict):
                if is_last:
                    output += _format_tree(value, prefix + "    ")
                else:
                    output += _format_tree(value, prefix + "│   ")
        return output

    return _format_tree(tree)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--directories",
        nargs="+",
        default=[],
        help="検索対象のディレクトリパス (複数指定可能)",
    )
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        default=[],
        help="検索対象のファイルパス (複数指定可能)",
    )
    parser.add_argument(
        "-i",
        "--ignore-dirs",
        nargs="+",
        default=[".git", ".venv", "venv", "node_modules"],
        help="除外するディレクトリ名 (複数指定可能)",
    )
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=[".ts", ".tsx"],
        help="検索対象の拡張子 (複数指定可能)",
    )

    args = parser.parse_args()

    found_files = find_files(
        args.directories, args.files, set(args.ignore_dirs), set(args.extensions)
    )

    print("Directory Structure:")
    print("```")
    print(".")
    print(generate_tree_structure(found_files))
    print("```")
    print()

    for file_path, content in found_files:
        print(f"File: {file_path}")
        print(content)
        print("---")


if __name__ == "__main__":
    main()
