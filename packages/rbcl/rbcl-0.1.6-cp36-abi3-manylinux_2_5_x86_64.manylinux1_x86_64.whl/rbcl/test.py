import rbcl.bindings as lib

x = lib.crypto_core_ristretto255_random()
assert lib.crypto_core_ristretto255_is_valid_point(x)

y = lib.crypto_core_ristretto255_from_hash(b'\xF0'*64)
assert lib.crypto_core_ristretto255_is_valid_point(y)

def test_addition():
  z1 = lib.crypto_core_ristretto255_add(x, y)
  z2 = lib.crypto_core_ristretto255_add(y, x)
  assert z1 == z2  # Assert that point addition commutes (in L)

def test_multiplication():
  s1 = lib.crypto_core_ristretto255_scalar_random()
  s2 = lib.crypto_core_ristretto255_scalar_random()
  w1 = lib.crypto_scalarmult_ristretto255(s1, lib.crypto_scalarmult_ristretto255(s2, x))
  w2 = lib.crypto_scalarmult_ristretto255(s2, lib.crypto_scalarmult_ristretto255(s1, x))
  assert w1 == w2  # Assert that point multiplication (by a scalar) is repeated addition (in L)
