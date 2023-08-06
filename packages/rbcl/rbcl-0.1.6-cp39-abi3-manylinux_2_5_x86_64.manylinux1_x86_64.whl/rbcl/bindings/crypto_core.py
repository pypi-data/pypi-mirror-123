# Copyright 2018 Donald Stufft and individual contributors
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

from rbcl import exceptions as exc
from rbcl._sodium import ffi, lib
from rbcl.exceptions import ensure


has_crypto_core_ristretto255 = bool(lib.PYNACL_HAS_CRYPTO_CORE_RISTRETTO255)

crypto_core_ristretto255_BYTES = 0
crypto_core_ristretto255_SCALARBYTES = 0
crypto_core_ristretto255_NONREDUCEDSCALARBYTES = 0

if has_crypto_core_ristretto255:
    crypto_core_ristretto255_BYTES = lib.crypto_core_ristretto255_bytes()
    crypto_core_ristretto255_SCALARBYTES = lib.crypto_core_ristretto255_scalarbytes()
    crypto_core_ristretto255_NONREDUCEDSCALARBYTES = (
        lib.crypto_core_ristretto255_nonreducedscalarbytes()
    )
    crypto_core_ristretto255_HASHBYTES = lib.crypto_core_ristretto255_hashbytes()


def crypto_core_ristretto255_is_valid_point(p):  # (const unsigned char *p);
    """
    Check if ``p`` represents a point on the ristretto255 curve, in canonical
    form, on the main subgroup, and that the point doesn't have a small order.

    :param p: a :py:data:`.crypto_core_ristretto255_BYTES` long bytes sequence
              representing a point on the ristretto255 curve
    :type p: bytes
    :return: point validity
    :rtype: bool
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes) and len(p) == crypto_core_ristretto255_BYTES,
        "Point must be a " + str(crypto_core_ristretto255_BYTES) + "long bytes sequence",
        raising=exc.TypeError,
    )

    rc = lib.crypto_core_ristretto255_is_valid_point(p)
    return rc == 1


def crypto_core_ristretto255_add(p, q):  # (unsigned char *r, const unsigned char *p, const unsigned char *q);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and isinstance(q, bytes)
        and len(p) == crypto_core_ristretto255_BYTES
        and len(q) == crypto_core_ristretto255_BYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_BYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_BYTES)

    lib.crypto_core_ristretto255_add(r, p, q)

    return ffi.buffer(r, crypto_core_ristretto255_BYTES)[:]


def crypto_core_ristretto255_sub(p, q):  # (unsigned char *r, const unsigned char *p, const unsigned char *q);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and isinstance(q, bytes)
        and len(p) == crypto_core_ristretto255_BYTES
        and len(q) == crypto_core_ristretto255_BYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_BYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_BYTES)

    lib.crypto_core_ristretto255_sub(r, p, q)

    return ffi.buffer(r, crypto_core_ristretto255_BYTES)[:]


def crypto_core_ristretto255_from_hash(h):  # (unsigned char *p, const unsigned char *r);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(h, bytes)
        and len(h) == crypto_core_ristretto255_HASHBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_HASHBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_BYTES)

    lib.crypto_core_ristretto255_from_hash(r, h)

    return ffi.buffer(r, crypto_core_ristretto255_BYTES)[:]


def crypto_core_ristretto255_random():  # (unsigned char *p);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_random(r)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_random():  # (unsigned char *r);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_random(r)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_invert(p):  # (unsigned char *recip, const unsigned char *s);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_invert(r, p)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_negate(p):  # (unsigned char *neg, const unsigned char *s);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_negate(r, p)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_complement(p):  # (unsigned char *comp, const unsigned char *s);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_complement(r, p)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_add(p, q):  # (unsigned char *z, const unsigned char *x, const unsigned char *y);
    
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and isinstance(q, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES
        and len(q) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_add(r, p, q)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_sub(p, q):  # (unsigned char *z, const unsigned char *x, const unsigned char *y);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and isinstance(q, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES
        and len(q) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_sub(r, p, q)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_mul(p, q):  # (unsigned char *z, const unsigned char *x, const unsigned char *y);
    
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and isinstance(q, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES
        and len(q) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_mul(r, p, q)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]


def crypto_core_ristretto255_scalar_reduce(p):  # (unsigned char *r, const unsigned char *s);
    """
    Add integers ``p`` and ``q`` modulo ``L``, where ``L`` is the order of
    the main subgroup.

    :param p: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type p: bytes
    :param q: a :py:data:`.crypto_core_ristretto255_SCALARBYTES`
              long bytes sequence representing an integer
    :type q: bytes
    :return: an integer represented as a
              :py:data:`.crypto_core_ristretto255_SCALARBYTES` long bytes sequence
    :rtype: bytes
    :raises rbcl.exceptions.UnavailableError: If called when using a
        minimal build of libsodium.
    """

    ensure(
        isinstance(p, bytes)
        and len(p) == crypto_core_ristretto255_SCALARBYTES,
        "Each integer must be a {} long bytes sequence".format(
            crypto_core_ristretto255_SCALARBYTES
        ),
        raising=exc.TypeError,
    )

    r = ffi.new("unsigned char[]", crypto_core_ristretto255_SCALARBYTES)

    lib.crypto_core_ristretto255_scalar_reduce(r, p)

    return ffi.buffer(r, crypto_core_ristretto255_SCALARBYTES)[:]
