# -*- coding: utf-8 -*-

import math as pm

from brainpy import errors
from brainpy import math as bm
from brainpy.simulation.brainobjects.base import DynamicalSystem
from brainpy.simulation.utils import size2len

__all__ = [
  'Delay',
  'ConstantDelay',
]


class Delay(DynamicalSystem):
  """Base class to model delay variables.

  Parameters
  ----------

  steps : tuple of str, tuple of function, dict of (str, function), optional
      The callable function, or a list of callable functions.
  monitors : None, list, tuple, datastructures.Monitor
      Variables to monitor.
  name : str, optional
      The name of the dynamic system.
  """

  def __init__(self, steps=('update',), name=None, monitors=None):
    super(Delay, self).__init__(steps=steps, monitors=monitors, name=name)

  def update(self, _t, _dt, **kwargs):
    raise NotImplementedError


class ConstantDelay(Delay):
  """Class used to model constant delay variables.

  For examples:

  >>> import brainpy as bp
  >>>
  >>> bp.ConstantDelay(size=10, delay=10.)
  >>> bp.ConstantDelay(size=100, delay=lambda: bp.math.random.randint(5, 10))
  >>> bp.ConstantDelay(size=100, delay=bp.math.random.random(100) * 4 + 10)

  Parameters
  ----------
  size : int, list of int, tuple of int
    The delay data size.
  delay : int, float, function, ndarray
    The delay time. With the unit of `dt`.
  num_batch : optional, int
    The batch size.
  steps : optional, tuple of str, tuple of function, dict of (str, function)
    The callable function, or a list of callable functions.
  monitors : optional, list, tuple, datastructures.Monitor
    Variables to monitor.
  name : optional, str
    The name of the dynamic system.
  """

  def __init__(self, size, delay, num_batch=None, dtype=None, dt=None, **kwargs):
    # dt
    self.dt = bm.get_dt() if dt is None else dt

    # num_batch
    self.num_batch = num_batch
    if num_batch is None:
      batch_size = ()
    else:
      assert isinstance(num_batch, int), 'Only support int for "num_batch"'
      batch_size = (num_batch,)

    # data size
    if isinstance(size, int): size = (size,)
    if not isinstance(size, (tuple, list)):
      raise errors.BrainPyError(f'"size" must a tuple/list of int, but we got {type(size)}: {size}')
    self.size = tuple(size)

    # data shape
    self.shape = self.size + batch_size

    # delay time length
    self.delay = delay

    # data and operations
    if isinstance(delay, (int, float)):  # uniform delay
      self.uniform_delay = True
      self.num_step = int(pm.ceil(delay / self.dt)) + 1
      self.out_idx = bm.Variable(bm.array([0]))
      self.in_idx = bm.Variable(bm.array([self.num_step - 1]))
      self.data = bm.Variable(bm.zeros((self.num_step,) + self.size + batch_size, dtype=dtype))

      self.push = self._push_for_uniform_delay
      self.pull = self._pull_for_uniform_delay

    else:  # non-uniform delay
      self.uniform_delay = False
      if not len(self.size) == 1:
        raise NotImplementedError(f'Currently, BrainPy only supports 1D heterogeneous '
                                  f'delays, while we got the heterogeneous delay with '
                                  f'{len(self.size)}-dimensions.')
      self.num = size2len(size)
      if callable(delay):  # like: "delay=lambda: np.random.randint(5, 10)"
        temp = bm.zeros(size)
        for i in range(size[0]): temp[i] = delay()
        delay = temp
      else:
        if bm.shape(delay) != self.size:
          raise errors.BrainPyError(f"The shape of the delay time size must be "
                                    f"the same with the delay data size. But we "
                                    f"got {bm.shape(delay)} != {self.size}")
      delay = bm.around(delay / self.dt)
      self.diag = bm.array(bm.arange(self.num), dtype=bm.int_)
      self.num_step = bm.array(delay, dtype=bm.int_) + 1
      self.in_idx = bm.Variable(self.num_step - 1)
      self.out_idx = bm.Variable(bm.zeros(self.num, dtype=bm.int_))
      self.data = bm.Variable(bm.zeros((self.num_step.max(),) + size + batch_size, dtype=dtype))

      self.push = self._push_for_nonuniform_delay
      self.pull = self._pull_for_nonuniform_delay

    super(ConstantDelay, self).__init__(**kwargs)

  def _pull_for_uniform_delay(self):
    """Pull delayed data for variables with the uniform delay."""
    return self.data[self.out_idx[0]]

  # def _pull_for_uniform_delay_batch(self):
  #   """Pull delayed data for variables with the uniform delay."""
  #   return self.data[:, self.out_idx[0]]

  def _push_for_uniform_delay(self, value):
    """Push the latest data to the delay bottom."""
    self.data[self.in_idx[0]] = value

  # def _push_for_uniform_delay_batch(self, value):
  #   """Push the latest data to the delay bottom."""
  #   self.data[:, self.in_idx[0]] = value

  def _pull_for_nonuniform_delay(self):
    """Pull delayed data for variables with the non-uniform delay."""
    return self.data[self.out_idx, self.diag]

  # def _pull_for_nonuniform_delay_batch(self):
  #   """Pull delayed data for variables with the non-uniform delay."""
  #   return self.data[:, self.out_idx, self.diag]

  def _push_for_nonuniform_delay(self, value):
    """Push the latest data to the delay bottom."""
    self.data[self.in_idx, self.diag] = value

  # def _push_for_nonuniform_delay_batch(self, value):
  #   """Push the latest data to the delay bottom."""
  #   self.data[:, self.in_idx, self.diag] = value

  def update(self, _t, _dt, **kwargs):
    """Update the delay index."""
    self.in_idx[:] = (self.in_idx + 1) % self.num_step
    self.out_idx[:] = (self.out_idx + 1) % self.num_step

  def reset(self):
    """Reset the variables."""
    self.in_idx[:] = self.num_step - 1
    self.out_idx[:] = 0
    self.data[:] = 0.
