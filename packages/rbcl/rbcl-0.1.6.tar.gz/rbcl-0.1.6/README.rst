====
RbCl
====

Ristretto group Python binding to
`libsodium <https://github.com/jedisct1/libsodium>`__

RbCl supports Python 2.7 and 3.5+ as well as PyPy 2.6+.

.. code:: python

    import rbcl.bindings as lib

    x = lib.crypto_core_ristretto255_random()
    assert lib.crypto_core_ristretto255_is_valid_point(x)

    y = lib.crypto_core_ristretto255_from_hash(b'\xF0'*64)
    assert lib.crypto_core_ristretto255_is_valid_point(y)
    
    z1 = lib.crypto_core_ristretto255_add(x, y)
    z2 = lib.crypto_core_ristretto255_add(y, x)
    assert z1 == z2  # Assert that point addition commutes (in L)
    
    s1 = lib.crypto_core_ristretto255_scalar_random()
    s2 = lib.crypto_core_ristretto255_scalar_random()
    w1 = lib.crypto_scalarmult_ristretto255(s1, lib.crypto_scalarmult_ristretto255(s2, x))
    w2 = lib.crypto_scalarmult_ristretto255(s2, lib.crypto_scalarmult_ristretto255(s1, x))
    assert w1 == w2  # Assert that point multiplication (by a scalar) is repeated addition (in L)

The following bindings are made available:

`Constructors <https://libsodium.gitbook.io/doc/advanced/point-arithmetic/ristretto#encoded-element-validation>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    crypto_core_ristretto255_random()
    crypto_core_ristretto255_from_hash(h)
    crypto_core_ristretto255_is_valid_point(p)

`Scalar arithmetic <https://libsodium.gitbook.io/doc/advanced/point-arithmetic/ristretto#scalar-arithmetic-over-l>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    crypto_core_ristretto255_scalar_add(s1, s2)
    crypto_core_ristretto255_scalar_sub(s1, s2)
    crypto_core_ristretto255_scalar_mul(s1, s2)  # NOT scalar mulitplication of a point!
    crypto_core_ristretto255_scalar_complement(s)
    crypto_core_ristretto255_scalar_invert(s)
    crypto_core_ristretto255_scalar_negate(s)
    crypto_core_ristretto255_scalar_reduce(s)
    crypto_core_ristretto255_scalar_random()

`Point arithmetic <https://libsodium.gitbook.io/doc/advanced/point-arithmetic/ristretto#scalar-multiplication>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    crypto_core_ristretto255_add(p, q)
    crypto_core_ristretto255_sub(p, q)
    crypto_scalarmult_ristretto255(p, s)
    crypto_scalarmult_ristretto255_base(s)

Constants
~~~~~~~~~

::

    crypto_scalarmult_ristretto255_bytes
    crypto_scalarmult_ristretto255_scalarbytes
    crypto_core_ristretto255_bytes
    crypto_core_ristretto255_scalarbytes
    crypto_core_ristretto255_hashbytes
    crypto_core_ristretto255_nonreducedscalarbytes

Helpers
~~~~~~~

::

    randombytes
    randombytes_buf_deterministic
    sodium_bin2hex
    sodium_hex2bin
    sodium_base642bin
    sodium_base64_encoded_len
    sodium_bin2base64
    sodium_pad
    sodium_unpad

===================================
Manual installation
===================================

.. code:: shell

    # Build as a wheel and install
    python setup.py bdist_wheel
    python -m pip install -f wheelhouse --no-index rbcl
    python -m nose

===================================
Publishing [for Nth Party]
===================================

.. code:: shell
    
    # Package source distribution
    python setup.py sdist
    
    # Run wheel-builder.yml and save/download artifacts locally, e.g. in ./dist
    # Then, upload to PyPi
    twine upload dist/rbcl-0.1.1*
