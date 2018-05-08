# Copyright (C) 2016-2018 Virgil Security Inc.
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
import json
from base64 import b64encode, b64decode

from virgil_sdk.raw_card_content import RawCardContent


class RawSignedModel(object):

    def __init__(
        self,
        content_snapshot
    ):
        self._content_snapshot = content_snapshot
        self._signatures = None

    def to_json(self):
        return self._content_snapshot.decode()

    def to_string(self):
        return b64encode(self._content_snapshot)

    def add_signature(self, signature):
        if signature in self._signatures:
            raise ValueError("Attempt to add an existing signature")
        else:
            self._signatures.append(signature)

    @property
    def content_snapshot(self):
        return self._content_snapshot

    @property
    def signatures(self):
        return self._signatures

    @classmethod
    def generate(cls, public_key, identity, created_at, previous_card_id=None):
        raw_card = RawCardContent(identity, public_key, created_at, previous_card_id)
        return RawSignedModel(raw_card.content_snapshot)

    @classmethod
    def from_string(cls, raw_signed_model_string):
        return RawSignedModel(b64decode(raw_signed_model_string))

    @classmethod
    def from_json(cls, raw_signed_model_json):
        return RawSignedModel(json.dumps(raw_signed_model_json).encode())