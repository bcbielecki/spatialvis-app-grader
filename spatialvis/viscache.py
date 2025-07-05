import json
import os
from pathlib import Path


class StartupCache:

    cache_file_path = Path(".cache")

    def __init__(self):
        raise ValueError("StartupCache is not an instantiable class")

    def save(excel_file_path: Path, student_id: str) -> None:
        '''
        Saves data that will be used for the next program startup in a cache file
        in the current working directory
        '''

        if StartupCache.cache_file_path.exists():
            os.remove(StartupCache.cache_file_path)

        data = dict()
        data["excel_file_path"] = str(excel_file_path)
        data["student_id"] = student_id

        try:
            with open(StartupCache.cache_file_path, 'w', encoding='utf-8') as cache_file:
                json.dump(data, cache_file)
        except IOError as e:
            print(f"Error saving cache: {e}")

    def load() -> (Path, str):
        '''
        Loads and returns data that will be used during program startup.
        '''
        excel_file_path = None
        student_id = None

        if StartupCache.cache_file_path.exists():

            try:
                with open(StartupCache.cache_file_path, 'r', encoding='utf-8') as cache_file:
                    data = json.load(cache_file)
                    excel_file_path = Path(data["excel_file_path"])
                    student_id = str(data["student_id"])
            except:
                print(f"Error loading cache.")

        return excel_file_path, student_id