import os
from enum import Enum, auto
from typing import Optional


class SecretNotFound(Exception):
    """
    Exception raised when a secret is not found.
    """
    pass


class Secrets(Enum):
    """
    Enum for managing secrets required by the service.
    """

    # Define secrets needed for the service
    CALCULATION_DB_USERNAME = auto()
    CALCULATION_DB_PASSWORD = auto()

    @staticmethod
    def _get_from_folder(secret_name: str, folder: str = '/run/secrets') -> Optional[str]:
        """
        Reads the secret file from a specified folder and returns the value.

        params:
        - secret_name (str): The name of the secret file.
        - folder (str): The folder containing the secret files.

        return:
        - Optional[str]: The secret value if found, else None.
        """
        file_path = os.path.join(folder, secret_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        return None

    def get_value(self) -> str:
        """
        Retrieves the secret value from various sources.

        return:
        - str: The secret value.

        raises:
        - SecretNotFound: If the secret is not found in any source.
        """
        # 1. Check default secret folder /run/secrets (prod)
        secret_value = self._get_from_folder(secret_name=self.name)
        if secret_value is not None:
            return secret_value

        # 2. Check folder /run/secrets/eds-pseudo (dev)
        secret_value = self._get_from_folder(secret_name=self.name, folder='/run/secrets/rpn-calculator')
        if secret_value is not None:
            return secret_value

        # 4. Check folder /etc/secrets/eds-pseudo (dev on MacOS)
        secret_value = self._get_from_folder(secret_name=self.name, folder='/etc/secrets/rpn-calculator')
        if secret_value is not None:
            return secret_value

        # Raise exception if secret is not found
        raise SecretNotFound(f"The secret `{self.name}` is not found in the secrets folder")
