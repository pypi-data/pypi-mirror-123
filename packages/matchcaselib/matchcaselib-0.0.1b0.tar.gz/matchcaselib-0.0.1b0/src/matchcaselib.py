"""
MIT License

Copyright (c) 2021 minecraftpr03

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class match:
  """
  The main class for pattern matching.

  Args:
   - `attrs`: List - The variables you match against with the `case` method.
  
  """
  def __init__(self, *attrs):
    self._attrs = attrs
    self._default = True

  def __enter__(self):
    return self

  def __exit__(self, typ, val, tb):
    return self

  def case(self, *_objects):
    """
    Tries to match objects against objects given during initialization

    Args:
     - `_objects`: List - The objects to attempt to match

    """
    if len(_objects) != len(self._attrs):
      raise ValueError(f"The amount of objects passed in ({len(_objects)}) does not match the amount of objects used to initialize the match in context ({len(self._attrs)}).")

    if _objects == self._attrs:
      self._default = False
      return True

  @property
  def default(self):
    return self._default

  def exit(self):
    return self.__exit__(None, None, None)
