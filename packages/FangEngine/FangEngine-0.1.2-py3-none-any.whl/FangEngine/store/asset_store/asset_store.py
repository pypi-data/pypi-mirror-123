"""
This module contains the asset store
"""
import abc
import typing
import os
import random


class AssetStore(abc.ABC):
    """
    This class is the base class for all asset stores
    This class is a singleton so multiple instances will have no affect on performance
    """
    _instance = None
    asset_path = ""
    store = {}  # type: typing.Dict[str, object]
    restricted_extensions = None        # type: typing.List[str]

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AssetStore, cls).__new__(cls, *args, **kwargs)
            cls._instance.reload()

        return cls._instance

    def __repr__(self):
        return "<{} items={}>".format(self.__class__.__name__, len(self.store))

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.delete(key)

    def __len__(self):
        return self.count()

    def __iter__(self):
        for k, v in self.store.items():
            yield k, v

    def get(self, name: str):
        """
        Returns the asset with the specified name
        """
        return self.store[name]

    def get_all(self, search: str = "") -> list:
        """
        Returns everything in the asset store
        :param search: the text the names must start with (or blank for everything)
        :return: list of assets
        """
        result = []

        for k, v in self.store.items():
            if k.startswith(search):
                result.append(v)

        return result

    def get_random(self, search: str = ""):
        """
        Returns a random asset in the store
        :param search: the text the names must start with (or blank for everything)
        """
        return random.choice(
            [v for k, v in self.store.items() if k.startswith(search)]
        )

    def get_all_names(self, search: str = "") -> typing.List[str]:
        """
        Returns every name of every asset in the store
        :param search: the text the names must start with (or blank for everything)
        :return: list of names of assets
        """
        result = []

        for k in self.store:
            if k.startswith(search):
                result.append(k)

        return result

    def get_random_name(self, search: str = "") -> str:
        """
        Returns a random asset name in the store
        :param search: the text the names must start with (or blank for everything)
        """
        return random.choice(
            self.get_all_names(search)
        )

    def set(self, name: str, asset: str):
        """
        Adds/overwrites the asset at the specified name
        :param name:
        :param asset: the asset
        """
        self.store[name] = asset

    def delete(self, name: str):
        """
        Deletes and returns the asset with the specified name
        """
        return self.store.pop(name)

    def count(self) -> int:
        """
        Returns the number of assets in the store
        """
        return len(self.store)

    def reload(self, path: str = None):
        """
        Reloads the assets
        Note that this clears the current store and then loads everything
        If a file is missing when the reload happens the file will NOT be loaded
        :param path: optional path to reload from
        """
        self.store = {}
        self.overload(path=path)

    def overload(self, path: str = None):
        """
        Reloads the assets
        Note that this DOES NOT clear the current store. It simply overwrites whatever it finds
        If a file is missing when the reload happens the original file will remain loaded
        :param path: optional path to reload from
        """
        if path is None:
            path = self.asset_path

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if self.restricted_extensions is not None:
                    for e in self.restricted_extensions:
                        if name.endswith(e):
                            break
                    else:
                        continue

                self.store[
                    os.path.splitext(
                        os.path.relpath(os.path.join(root, name), path)
                    )[0].replace("/", ".").replace("\\\\", ".").replace("\\", ".")

                ] = self.load_asset(os.path.join(root, name))

    def get_ignore_path(self, name: str):
        name = os.path.splitext(os.path.basename(name))[0]
        for k, v in self.store.items():
            if k[k.rfind(".") + 1:] == name:
                return self.store[k]

    @abc.abstractmethod
    def load_asset(self, path: str):
        """
        Loads an asset into memory
        """
        pass
