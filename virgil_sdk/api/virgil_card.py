# Copyright (C) 2016 Virgil Security Inc.
#
# Lead Maintainer: Virgil Security Inc. <support@virgilsecurity.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#     (3) Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from virgil_sdk.api import VirgilBuffer
from virgil_sdk.client import RequestSigner
from virgil_sdk.client.requests import CreateCardRequest
from virgil_sdk.client.requests import CreateGlobalCardRequest


class VirgilCard(object):
    """A Virgil Card is the main entity of the Virgil Security services, it includes an information
    about the user and his public key. The Virgil Card identifies the user by one of his available
    types, such as an email, a phone number, etc."""

    def __init__(
        self,
        context,  # type: Context
        card  # type: Card
    ):
        # type: (...) -> None
        self.__context = context
        self.__card = card
        self._public_key = None
        self._id = None
        self._identity = None
        self._identity_type = None
        self._custom_fields = None

    def encrypt(self, buffer):
        # type: (VirgilBuffer) -> VirgilBuffer
        """Encrypts the specified data for current VirgilCard recipient.
        Args:
            buffer: The data to be encrypted.
        Returns:
            Encrypted data
        Raises:
            ValueError if VirgilBuffer empty
        """
        if not buffer:
            raise ValueError("VirgilBuffer empty")
        cipher_data = self.__context.crypto.encrypt(buffer.get_bytearray(), self.__public_key)
        return VirgilBuffer(cipher_data)

    def verify(self, buffer, signature):
        # type: (VirgilBuffer, VirgilBuffer) -> bool
        """Verifies the specified buffer and signature with current VirgilCard recipient.
        Args:
            buffer: The data to be verified.
            signature: The signature used to verify the data integrity.
        Returns:
            Boolean verification result
        Raises:
            ValueError is buffer or signature empty
        """
        if not buffer:
            raise ValueError("VirgilBuffer empty")
        if not signature:
            raise ValueError("Signatures empty")
        is_valid = self.__context.crypto.verify(
            buffer.get_bytearray(),
            signature.get_bytearray(),
            self.__public_key
        )
        return is_valid

    def export(self):
        # type: () -> str
        """Exports a current VirgilCard instance into base64 encoded string.
        Returns:
            A base64 string that represents a VirgilCard.
        """
        card_json = self.__card.__dict__
        return VirgilBuffer.from_string(str(card_json)).to_string("base64")

    def check_identity(self, time_to_live=3600, count_to_live=1):
        # type: (int, int) -> dict
        """Initiates an identity verification process for current Card indentity type. It is only working for
        Global identity types like Email.
        Args:
            time_to_live: Limit the lifetime of the token in econds (maximum value is 60 * 60 * 24 * 365 = 1 year).
            count_to_live: Restrict the number of validation token usages (maximum value is 100).
        Returns:
            Information about operation etc...
        """
        action_id = self.__context.client.verify_identity(self.identity, self.identity_type, self.custom_fields)
        attempt = {
            "action_id": action_id,
            "time_to_live": time_to_live,
            "count_to_live": count_to_live,
            "identity": self.identity,
            "identity_type": self.identity_type
        }
        return attempt

    def publish(self):
        # type: () -> None
        """Publishes a current VirgilCard to the Virgil Security services."""
        create_card_request = CreateCardRequest(
            self.identity,
            self.identity_type,
            self.__public_key,
            self.__card.data
        )
        create_card_request.signatures = self.__card.signatures
        create_card_request.snapshot = self.__card.snapshot
        request_signer = RequestSigner(self.__context.crypto)
        request_signer.authority_sign(
            create_card_request,
            self.__context.credentials.app_id,
            self.__context.credentials.get_app_key(self.__context.crypto)
        )
        self.__card = self.__context.client.create_card_from_request(create_card_request)

    def publish_global(self, identity_token):
        # type: (str) -> None
        """Publishes a current VirgilCard to the Virgil Security services into global scope.
        Args:
            identity_token: identity validation token
        Raises:
            ValueError if identity token empty
        """
        if not identity_token:
            raise ValueError("Identity validation token empty")

        create_global_card_request = CreateGlobalCardRequest(
            self.identity,
            self.identity_type,
            self.__public_key,
            identity_token,
            self.__card.data
        )
        create_global_card_request.signatures = self.__card.signatures
        create_global_card_request.snapshot = self.__card.snapshot
        print(create_global_card_request.request_model)
        self.__card = self.__context.client.create_global_card_from_request(create_global_card_request)

    @property
    def id(self):
        # type: () -> str
        """Gets the unique identifier for the Virgil Card."""
        return self.__card.id

    @property
    def identity(self):
        # type: () -> str
        """Gets the value of current Virgil Card identity."""
        return self.__card.identity

    @property
    def identity_type(self):
        # type: () -> str
        """Gets the identityType of current Virgil Card identity."""
        return self.__card.identity_type

    @property
    def custom_fields(self):
        # type: () -> dict
        """Gets the custom VirgilCard parameters."""
        return self.__card.data

    @property
    def __public_key(self):
        # type: () -> PublicKey
        """Gets a Public key that is assigned to current VirgilCard."""
        return self.__context.crypto.import_public_key(self.__card.public_key)