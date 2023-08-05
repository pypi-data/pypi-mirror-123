"""The core approval testing algorithm.

This is where we check the latest *received* data with the latest *accepted* data.
"""


def verify(vault, comparator, test_id, data, mime_type, encoding):
    """Check if `received` matches the current accepted value for the test_id.

    If `received` doesn't match the accepted value, this will raise MismatchError§.

    Args:
        vault: A Vault instance.
        comparator: A Comparator instance.
        test_id: The ID of the test that produced `received`.
        data: The received data (bytes).
        mime_type: The mime-type of the received data.
        encoding: The encoding of the received data, if it represents encoded text.

    Raises:
        MismatchError: Received data doesn't compare as equal to the accepted data, or there
            is no accepted data.
    """
    try:
        accepted = vault.accepted(test_id)
    except KeyError:
        accepted = None
        message = "There is no accepted data"
    else:
        # If received and accepted compare as equal, we don't need to change anything.
        accepted_data = accepted.path.read_bytes()
        if comparator(accepted_data, data):
            # Clear any received data that exist from earlier.
            vault.clear_received(test_id)
            return

        message = "Received data does not match accepted"

    vault.receive(test_id, data, mime_type, encoding)

    raise MismatchError(message, data, accepted)


class MismatchError(Exception):
    def __init__(self, message, received_data, accepted):
        super().__init__(message)
        self._received = received_data
        self._accepted = accepted

    @property
    def message(self):
        return self.args[0]

    @property
    def received(self):
        "Received data (bytes)."
        return self._received

    @property
    def accepted(self):
        "Accepted data (Artifact)."
        return self._accepted
