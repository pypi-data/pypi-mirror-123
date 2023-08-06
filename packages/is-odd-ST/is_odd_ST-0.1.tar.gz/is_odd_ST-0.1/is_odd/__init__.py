def is_odd(value):
  try:
    int_value = int(value)
  except ValueError:
    return False
  if (int_value != value):
    return False
  return value % 2 == 0