# Copyright 2013-2019 Donald Stufft and individual contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

from rbcl.bindings.crypto_core import (
    crypto_core_ristretto255_BYTES,
    crypto_core_ristretto255_NONREDUCEDSCALARBYTES,
    crypto_core_ristretto255_SCALARBYTES,
    crypto_core_ristretto255_HASHBYTES,
    crypto_core_ristretto255_is_valid_point,
    crypto_core_ristretto255_add,
    crypto_core_ristretto255_sub,
    crypto_core_ristretto255_from_hash,
    crypto_core_ristretto255_random,
    crypto_core_ristretto255_scalar_random,
    crypto_core_ristretto255_scalar_invert,
    crypto_core_ristretto255_scalar_negate,
    crypto_core_ristretto255_scalar_complement,
    crypto_core_ristretto255_scalar_add,
    crypto_core_ristretto255_scalar_sub,
    crypto_core_ristretto255_scalar_mul,
    crypto_core_ristretto255_scalar_reduce,
    has_crypto_core_ristretto255,
)
from rbcl.bindings.crypto_scalarmult import (
    crypto_scalarmult_ristretto255,
    crypto_scalarmult_ristretto255_BYTES,
    crypto_scalarmult_ristretto255_SCALARBYTES,
    crypto_scalarmult_ristretto255_base,
    has_crypto_scalarmult_ristretto255,
)
from rbcl.bindings.randombytes import (
    randombytes,
    randombytes_buf_deterministic,
)
from rbcl.bindings.sodium_core import sodium_init
from rbcl.bindings.utils import (
    sodium_add,
    sodium_increment,
    sodium_memcmp,
    sodium_pad,
    sodium_unpad,
)


__all__ = [
    "crypto_core_ristretto255_random",
    "crypto_core_ristretto255_from_hash",
    "crypto_core_ristretto255_is_valid_point",
    "crypto_core_ristretto255_scalar_add",
    "crypto_core_ristretto255_scalar_sub",
    "crypto_core_ristretto255_scalar_mul",
    "crypto_core_ristretto255_scalar_complement",
    "crypto_core_ristretto255_scalar_invert",
    "crypto_core_ristretto255_scalar_negate",
    "crypto_core_ristretto255_scalar_reduce",
    "crypto_core_ristretto255_scalar_random",
    "crypto_core_ristretto255_add",
    "crypto_core_ristretto255_sub",
    "crypto_scalarmult_ristretto255",
    "crypto_scalarmult_ristretto255_base",
    "crypto_scalarmult_ristretto255_bytes",
    "crypto_scalarmult_ristretto255_scalarbytes",
    "crypto_core_ristretto255_bytes",
    "crypto_core_ristretto255_scalarbytes",
    "crypto_core_ristretto255_hashbytes",
    "crypto_core_ristretto255_nonreducedscalarbytes",
    "randombytes",
    "randombytes_buf_deterministic",
    "sodium_init",
    "sodium_add",
    "sodium_increment",
    "sodium_memcmp",
    "sodium_pad",
    "sodium_unpad",
]


# Initialize Sodium
sodium_init()
