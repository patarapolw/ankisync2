from pathlib import Path
from typing import Union
from zipfile import ZipFile
import json
import shutil

from .anki20 import Anki20


class Apkg(Anki20):
    """Reads a *.apkg file"""

    original: Path
    folder: Path
    media_path: Path

    def __init__(self, filename_or_dir: Union[str, Path], **kwargs):
        """
        ```python
        from ankisync2.apkg import Apkg, db

        apkg = Apkg("example.apkg")
        # Or Apkg("example/") also works. the folder named 'example' will be created.
        ```

        Args:
            filename_or_dir (Union[str, Path]): Can be a *.apkg, or a folder name
        """

        self.original = Path(filename_or_dir)
        if not self.original.is_dir():
            self.folder = self.original.with_suffix("")
            self._unzip()
        else:
            self.folder = self.original
        self.folder.mkdir(exist_ok=True)

        self.media_path = self.folder.joinpath("media")
        if not self.media_path.exists():
            self.media_path.write_text("{}")

        shutil.copy(
            self.folder.joinpath("collection.anki2"),
            self.folder.joinpath("collection.anki20"),
        )
        super().__init__(self.folder.joinpath("collection.anki20"), **kwargs)

    def _unzip(self):
        if self.original.exists():
            with ZipFile(self.original) as zf:
                zf.extractall(self.folder)

    def export(self, filename: Union[str, Path]):
        """Export to `*.apkg`

        Args:
            filename (Union[str, Path]): Exported filename. The extension should be *.apkg
        """

        """For each file, simply shutil.copy() and the file will be created or overwritten, whichever is appropriate.
        """
        shutil.copy(
            self.folder.joinpath("collection.anki20"),
            self.folder.joinpath("collection.anki2"),
        )

        Anki20(self.folder.joinpath("collection.anki2")).finalize()

        with ZipFile(filename, "w") as zf:
            for f in self.folder.iterdir():
                if not f.name.endswith(".anki20"):
                    zf.write(str(f.resolve()), arcname=f.name)

    def clean(self):
        """Delete the generated folder"""

        shutil.rmtree(self.folder)

    @property
    def media(self) -> dict:
        """Get media dictionary

        Returns:
            dict: media dictionary
        """

        return json.loads(self.media_path.read_text())

    @media.setter
    def media(self, value: dict):
        """Set media dictionary

        Args:
            value (dict): media dictionary
        """

        with self.media_path.open("w") as f:
            json.dump(value, f)

    def iter_media(self):
        """Iterate through the media

        Yields:
            dict: media dictionary, containing "path": path_to_file and "name": represented_filename
        """

        for k, v in self.media.items():
            yield {"path": k, "name": v}

    def add_media(self, file_path: Union[str, Path], archive_name: str = "") -> int:
        """Add media to the archive

        ```python
        apkg.add_media("path/to/media.jpg")
        ```

        Args:
            file_path (Union[str, Path]): file path to the media.
            archive_name (str, optional): file may be renamed. Defaults to "".

        Returns:
            int: The media file ID.
        """

        media = self.media
        file_id = max(int(i) for i in (0, *media.keys())) + 1

        if not archive_name:
            archive_name = Path(file_path).name

        if any(sep in archive_name for sep in {"/", "\\"}):
            raise ValueError("Media name does not support sub-folders")

        if str(file_path) != str(self.folder.joinpath(archive_name)):
            shutil.copy(str(file_path), str(self.folder.joinpath(archive_name)))

        media[str(file_id)] = archive_name

        self.media = media

        return file_id
