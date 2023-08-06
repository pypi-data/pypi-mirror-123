import pathlib
from yoyo import step


def migration_steps(migration_dir: pathlib.Path = None, suffix: str = "*.sql.txt"):
    def read_content(file: pathlib.Path = None):
        with open(file) as f:
            return f.read()

    def alphabetically_sorted_files(migration_dir: pathlib.Path = None):
        files = [str(f) for f in list(pathlib.Path(migration_dir).glob(suffix))]
        return sorted(files)

    return [
        step(read_content(file=file))
        for file in alphabetically_sorted_files(migration_dir=migration_dir)
    ]
