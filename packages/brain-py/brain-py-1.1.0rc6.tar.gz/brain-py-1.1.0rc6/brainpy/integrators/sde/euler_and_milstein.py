# -*- coding: utf-8 -*-

import inspect

from brainpy import errors, math
from brainpy.integrators import constants
from brainpy.integrators.analysis_by_ast import separate_variables
from . import common

__all__ = [
  'euler',
  'heun',
  'milstein',
  'exponential_euler',
]


class Tools(object):

  @staticmethod
  def df_and_dg(code_lines, variables, parameters):
    # 1. df
    # df = f(x, t, *args)
    all_df = [f'{var}_df' for var in variables]
    code_lines.append(f'  {", ".join(all_df)} = f({", ".join(variables + parameters)})')

    # 2. dg
    # dg = g(x, t, *args)
    all_dg = [f'{var}_dg' for var in variables]
    code_lines.append(f'  {", ".join(all_dg)} = g({", ".join(variables + parameters)})')
    code_lines.append('  ')

  @staticmethod
  def dfdt(code_lines, variables, vdt):
    for var in variables:
      code_lines.append(f'  {var}_dfdt = {var}_df * {vdt}')
    code_lines.append('  ')

  @staticmethod
  def noise_terms(code_lines, variables):
    # num_vars = len(variables)
    # if num_vars > 1:
    #     code_lines.append(f'  all_dW = math.normal(0.0, dt_sqrt, ({num_vars},)+math.shape({variables[0]}_dg))')
    #     for i, var in enumerate(variables):
    #         code_lines.append(f'  {var}_dW = all_dW[{i}]')
    # else:
    #     var = variables[0]
    #     code_lines.append(f'  {var}_dW = math.normal(0.0, dt_sqrt, math.shape({var}))')
    # code_lines.append('  ')

    for var in variables:
      code_lines.append(f'  {var}_dW = math.random.normal(0.000, dt_sqrt, math.shape({var}))')
    code_lines.append('  ')


class Wrapper(object):

  @staticmethod
  def wrap(wrapper, f, g, dt, intg_type, var_type, wiener_type, show_code):
    """The base function to format a SRK method.

    Parameters
    ----------
    f : callable
        The drift function of the SDE_INT.
    g : callable
        The diffusion function of the SDE_INT.
    dt : float
        The numerical precision.
    intg_type : str
        "utils.ITO_SDE" : Ito's Stochastic Calculus.
        "utils.STRA_SDE" : Stratonovich's Stochastic Calculus.
    wiener_type : str
    var_type : str
        "scalar" : with the shape of ().
        "population" : with the shape of (N,) or (N1, N2) or (N1, N2, ...).
        "system": with the shape of (d, ), (d, N), or (d, N1, N2).
    show_code : bool
        Whether show the formatted code.

    Returns
    -------
    numerical_func : callable
        The numerical function.
    """

    intg_type = constants.ITO_SDE if intg_type is None else intg_type
    var_type = constants.SCALAR_VAR if var_type is None else var_type
    wiener_type = constants.SCALAR_WIENER if wiener_type is None else wiener_type
    if intg_type not in constants.SUPPORTED_INTG_TYPE:
      raise errors.IntegratorError(f'Currently, BrainPy only support SDE_INT types: '
                                   f'{constants.SUPPORTED_INTG_TYPE}. But we got {intg_type}.')
    if var_type not in constants.SUPPORTED_VAR_TYPE:
      raise errors.IntegratorError(f'Currently, BrainPy only supports variable types: '
                                   f'{constants.SUPPORTED_VAR_TYPE}. But we got {var_type}.')
    if wiener_type not in constants.SUPPORTED_WIENER_TYPE:
      raise errors.IntegratorError(f'Currently, BrainPy only supports Wiener '
                                   f'Process types: {constants.SUPPORTED_WIENER_TYPE}. '
                                   f'But we got {wiener_type}.')

    show_code = False if show_code is None else show_code
    dt = math.get_dt() if dt is None else dt

    if f is not None and g is not None:
      return wrapper(f=f, g=g, dt=dt, show_code=show_code, intg_type=intg_type,
                     var_type=var_type, wiener_type=wiener_type)

    elif f is not None:
      return lambda g: wrapper(f=f, g=g, dt=dt, show_code=show_code, intg_type=intg_type,
                               var_type=var_type, wiener_type=wiener_type)

    elif g is not None:
      return lambda f: wrapper(f=f, g=g, dt=dt, show_code=show_code, intg_type=intg_type,
                               var_type=var_type, wiener_type=wiener_type)

    else:
      raise ValueError('Must provide "f" or "g".')

  @staticmethod
  def exp_euler(f, g, dt, intg_type, var_type, wiener_type, show_code):
    try:
      import sympy
      from brainpy.integrators import analysis_by_sympy
    except ModuleNotFoundError:
      raise errors.PackageMissingError('SymPy must be installed when using exponential euler methods.')

    if var_type == constants.SYSTEM_VAR:
      raise errors.IntegratorError(f'Exponential Euler method do not support {var_type} variable type.')
    if intg_type != constants.ITO_SDE:
      raise errors.IntegratorError(f'Exponential Euler method only supports Ito integral, but we got {intg_type}.')

    vdt, variables, parameters, arguments, func_name = common.basic_info(f=f, g=g)
    arguments = list(arguments) + [f'{vdt}={dt}']

    # 1. code scope
    closure_vars = inspect.getclosurevars(f)
    code_scope = dict(closure_vars.nonlocals)
    code_scope.update(dict(closure_vars.globals))
    code_scope['f'] = f
    code_scope['g'] = g
    code_scope['math'] = math
    # code_scope['exp'] = math.exp

    # 2. code lines
    code_lines = [f'def {func_name}({", ".join(arguments)}):']
    code_lines.append(f'  {vdt}_sqrt = {vdt} ** 0.5')

    # 2.1 dg
    # dg = g(x, t, *args)
    all_dg = [f'{var}_dg' for var in variables]
    code_lines.append(f'  {", ".join(all_dg)} = g({", ".join(variables + parameters)})')
    code_lines.append('  ')

    # 2.2 dW
    Tools.noise_terms(code_lines, variables)

    # 2.3 dgdW
    # ----
    # SCALAR_WIENER : dg * dW
    # VECTOR_WIENER : math.sum(dg * dW, axis=-1)

    if wiener_type == constants.SCALAR_WIENER:
      for var in variables:
        code_lines.append(f'  {var}_dgdW = {var}_dg * {var}_dW')
    else:
      for var in variables:
        code_lines.append(f'  {var}_dgdW = math.sum({var}_dg * {var}_dW, axis=-1)')
    code_lines.append('  ')

    # 2.4 new var
    # ----
    analysis = separate_variables(f)
    variables_for_returns = analysis['variables_for_returns']
    expressions_for_returns = analysis['expressions_for_returns']
    for vi, (key, vars) in enumerate(variables_for_returns.items()):
      # separate variables
      sd_variables = []
      for v in vars:
        if len(v) > 1:
          raise ValueError('Cannot analyze multi-assignment code line.')
        sd_variables.append(v[0])
      expressions = expressions_for_returns[key]
      var_name = variables[vi]
      diff_eq = analysis_by_sympy.SingleDiffEq(var_name=var_name,
                                               variables=sd_variables,
                                               expressions=expressions,
                                               derivative_expr=key,
                                               scope=code_scope,
                                               func_name=func_name)

      f_expressions = diff_eq.get_f_expressions(substitute_vars=diff_eq.var_name)

      # code lines
      code_lines.extend([f"  {str(expr)}" for expr in f_expressions[:-1]])

      # get the linear system using sympy
      f_res = f_expressions[-1]
      df_expr = analysis_by_sympy.str2sympy(f_res.code).expr.expand()
      s_df = sympy.Symbol(f"{f_res.var_name}")
      code_lines.append(f'  {s_df.name} = {analysis_by_sympy.sympy2str(df_expr)}')
      var = sympy.Symbol(diff_eq.var_name, real=True)

      # get df part
      s_linear = sympy.Symbol(f'_{diff_eq.var_name}_linear')
      s_linear_exp = sympy.Symbol(f'_{diff_eq.var_name}_linear_exp')
      s_df_part = sympy.Symbol(f'_{diff_eq.var_name}_df_part')
      if df_expr.has(var):
        # linear
        linear = sympy.collect(df_expr, var, evaluate=False)[var]
        code_lines.append(f'  {s_linear.name} = {analysis_by_sympy.sympy2str(linear)}')
        # linear exponential
        code_lines.append(f'  {s_linear_exp.name} = math.exp({linear.name} * {vdt})')
        # df part
        df_part = (s_linear_exp - 1) / s_linear * s_df
        code_lines.append(f'  {s_df_part.name} = {analysis_by_sympy.sympy2str(df_part)}')

      else:
        # linear exponential
        code_lines.append(f'  {s_linear_exp.name} = {vdt}_sqrt')
        # df part
        code_lines.append(f'  {s_df_part.name} = {s_df.name} * {vdt}')

      # update expression
      update = var + s_df_part

      # The actual update step
      code_lines.append(f'  {diff_eq.var_name}_new = {analysis_by_sympy.sympy2str(update)} + {var_name}_dgdW')
      code_lines.append('')

    # returns
    new_vars = [f'{var}_new' for var in variables]
    code_lines.append(f'  return {", ".join(new_vars)}')

    # return and compile
    return common.compile_and_assign_attrs(
      code_lines=code_lines, code_scope=code_scope, show_code=show_code,
      variables=variables, parameters=parameters, func_name=func_name,
      intg_type=intg_type, var_type=var_type, wiener_type=wiener_type,
      dt=dt, method='exponential_euler', raw_func=dict(f=f, g=g)
    )

  @staticmethod
  def euler_and_heun(f, g, dt, intg_type, var_type, wiener_type, show_code):
    vdt, variables, parameters, arguments, func_name = common.basic_info(f=f, g=g)
    arguments = list(arguments) + [f'{vdt}={dt}']

    # 1. code scope
    code_scope = {'f': f, 'g': g, 'math': math}

    # 2. code lines
    code_lines = [f'def {func_name}({", ".join(arguments)}):']
    code_lines.append(f'  {vdt}_sqrt = {vdt} ** 0.5')

    # 2.1 df, dg
    Tools.df_and_dg(code_lines, variables, parameters)

    # 2.2 dfdt
    Tools.dfdt(code_lines, variables, vdt)

    # 2.3 dW
    Tools.noise_terms(code_lines, variables)

    # 2.3 dgdW
    # ----
    # SCALAR_WIENER : dg * dW
    # VECTOR_WIENER : math.sum(dg * dW, axis=-1)

    if wiener_type == constants.SCALAR_WIENER:
      for var in variables:
        code_lines.append(f'  {var}_dgdW = {var}_dg * {var}_dW')
    else:
      for var in variables:
        code_lines.append(f'  {var}_dgdW = math.sum({var}_dg * {var}_dW, axis=-1)')
    code_lines.append('  ')

    if intg_type == constants.ITO_SDE:
      method = 'euler'
      # 2.4 new var
      # ----
      # y = x + dfdt + dgdW
      for var in variables:
        code_lines.append(f'  {var}_new = {var} + {var}_dfdt + {var}_dgdW')
      code_lines.append('  ')

    elif intg_type == constants.STRA_SDE:
      method = 'heun'

      # 2.4  y_bar = x + math.sum(dgdW, axis=-1)
      all_bar = [f'{var}_bar' for var in variables]
      for var in variables:
        code_lines.append(f'  {var}_bar = {var} + {var}_dgdW')
      code_lines.append('  ')

      # 2.5  dg_bar = g(y_bar, t, *args)
      all_dg_bar = [f'{var}_dg_bar' for var in variables]
      code_lines.append(f'  {", ".join(all_dg_bar)} = g({", ".join(all_bar + parameters)})')

      # 2.6 dgdW2
      # ----
      # SCALAR_WIENER : dgdW2 = dg_bar * dW
      # VECTOR_WIENER : dgdW2 = math.sum(dg_bar * dW, axis=-1)
      if wiener_type == constants.SCALAR_WIENER:
        for var in variables:
          code_lines.append(f'  {var}_dgdW2 = {var}_dg_bar * {var}_dW')
      else:
        for var in variables:
          code_lines.append(f'  {var}_dgdW2 = math.sum({var}_dg_bar * {var}_dW, axis=-1)')
      code_lines.append('  ')

      # 2.7 new var
      # ----
      # y = x + dfdt + 0.5 * (dgdW + dgdW2)
      for var in variables:
        code_lines.append(f'  {var}_new = {var} + {var}_dfdt + 0.5 * ({var}_dgdW + {var}_dgdW2)')
      code_lines.append('  ')
    else:
      raise ValueError(f'Unknown SDE_INT type: {intg_type}. We only '
                       f'supports {constants.SUPPORTED_INTG_TYPE}.')

    # returns
    new_vars = [f'{var}_new' for var in variables]
    code_lines.append(f'  return {", ".join(new_vars)}')

    # return and compile
    return common.compile_and_assign_attrs(
      code_lines=code_lines, code_scope=code_scope, show_code=show_code,
      variables=variables, parameters=parameters, func_name=func_name,
      intg_type=intg_type, var_type=var_type, wiener_type=wiener_type,
      dt=dt, method=method, raw_func=dict(f=f, g=g))

  @staticmethod
  def milstein(f, g, dt, intg_type, var_type, wiener_type, show_code):
    vdt, variables, parameters, arguments, func_name = common.basic_info(f=f, g=g)
    arguments = list(arguments) + [f'{vdt}={dt}']

    # 1. code scope
    code_scope = {'f': f, 'g': g, 'math': math}

    # 2. code lines
    code_lines = [f'def {func_name}({", ".join(arguments)}):']
    code_lines.append(f'  {vdt}_sqrt = {vdt} ** 0.5')

    # 2.1 df, dg
    Tools.df_and_dg(code_lines, variables, parameters)

    # 2.2 dfdt
    Tools.dfdt(code_lines, variables, vdt)

    # 2.3 dW
    Tools.noise_terms(code_lines, variables)

    # 2.3 dgdW
    # ----
    # dg * dW
    for var in variables:
      code_lines.append(f'  {var}_dgdW = {var}_dg * {var}_dW')
    code_lines.append('  ')

    # 2.4  df_bar = x + dfdt + math.sum(dg * dt_sqrt, axis=-1)
    all_df_bar = [f'{var}_df_bar' for var in variables]
    if wiener_type == constants.SCALAR_WIENER:
      for var in variables:
        code_lines.append(f'  {var}_df_bar = {var} + {var}_dfdt + {var}_dg * {vdt}_sqrt')
    else:
      for var in variables:
        code_lines.append(f'  {var}_df_bar = {var} + {var}_dfdt + math.sum('
                          f'{var}_dg * {vdt}_sqrt, axis=-1)')

    # 2.5  dg_bar = g(y_bar, t, *args)
    all_dg_bar = [f'{var}_dg_bar' for var in variables]
    code_lines.append(f'  {", ".join(all_dg_bar)} = g({", ".join(all_df_bar + parameters)})')
    code_lines.append('  ')

    # 2.6 dgdW2
    # ----
    # dgdW2 = 0.5 * (dg_bar - dg) * (dW * dW / dt_sqrt - dt_sqrt)
    if intg_type == constants.ITO_SDE:
      for var in variables:
        code_lines.append(f'  {var}_dgdW2 = 0.5 * ({var}_dg_bar - {var}_dg) * '
                          f'({var}_dW * {var}_dW / {vdt}_sqrt - {vdt}_sqrt)')
    elif intg_type == constants.STRA_SDE:
      for var in variables:
        code_lines.append(f'  {var}_dgdW2 = 0.5 * ({var}_dg_bar - {var}_dg) * '
                          f'{var}_dW * {var}_dW / {vdt}_sqrt')
    else:
      raise ValueError(f'Unknown SDE_INT type: {intg_type}')
    code_lines.append('  ')

    # 2.7 new var
    # ----
    # SCALAR_WIENER : y = x + dfdt + dgdW + dgdW2
    # VECTOR_WIENER : y = x + dfdt + math.sum(dgdW + dgdW2, axis=-1)
    if wiener_type == constants.SCALAR_WIENER:
      for var in variables:
        code_lines.append(f'  {var}_new = {var} + {var}_dfdt + {var}_dgdW + {var}_dgdW2')
    elif wiener_type == constants.VECTOR_WIENER:
      for var in variables:
        code_lines.append(f'  {var}_new = {var} + {var}_dfdt + math.sum({var}_dgdW + {var}_dgdW2, axis=-1)')
    else:
      raise ValueError(f'Unknown Wiener Process : {wiener_type}')
    code_lines.append('  ')

    # returns
    new_vars = [f'{var}_new' for var in variables]
    code_lines.append(f'  return {", ".join(new_vars)}')

    # return and compile
    return common.compile_and_assign_attrs(
      code_lines=code_lines, code_scope=code_scope, show_code=show_code,
      variables=variables, parameters=parameters, func_name=func_name,
      intg_type=intg_type, var_type=var_type, wiener_type=wiener_type,
      dt=dt, method='milstein', raw_func=dict(f=f, g=g))


def euler(f=None, g=None, dt=None, intg_type=None, var_type=None, wiener_type=None, show_code=None):
  return Wrapper.wrap(Wrapper.euler_and_heun, f=f, g=g, dt=dt, intg_type=intg_type,
                      var_type=var_type, wiener_type=wiener_type, show_code=show_code)


def heun(f=None, g=None, dt=None, intg_type=None, var_type=None, wiener_type=None, show_code=None):
  if intg_type != constants.STRA_SDE:
    raise errors.IntegratorError(f'Heun method only supports Stranovich integral of SDEs, '
                                 f'but we got {intg_type} integral.')
  return Wrapper.wrap(Wrapper.euler_and_heun, f=f, g=g, dt=dt, intg_type=intg_type,
                      var_type=var_type, wiener_type=wiener_type, show_code=show_code)


def exponential_euler(f=None, g=None, dt=None, intg_type=None, var_type=None,
                      wiener_type=None, show_code=None):
  r"""First order, explicit exponential Euler method.

  For a SDE_INT equation of the form

  .. math::

      d y=(Ay+ F(y))dt + g(y)dW(t) = f(y)dt + g(y)dW(t), \quad y(0)=y_{0}

  its schema is given by [1]_

  .. math::

      y_{n+1} & =e^{\Delta t A}(y_{n}+ g(y_n)\Delta W_{n})+\varphi(\Delta t A) F(y_{n}) \Delta t \\
       &= y_n + \Delta t \varphi(\Delta t A) f(y) + e^{\Delta t A}g(y_n)\Delta W_{n}

  where :math:`\varphi(z)=\frac{e^{z}-1}{z}`.

  Parameters
  ----------
  diff_eq : DiffEquation
      The differential equation.

  Returns
  -------
  func : callable
      The one-step numerical integrator function.

  References
  ----------
  .. [1] Erdoğan, Utku, and Gabriel J. Lord. "A new class of exponential integrators for stochastic
         differential equations with multiplicative noise." arXiv preprint arXiv:1608.07096 (2016).
  """

  return Wrapper.wrap(Wrapper.exp_euler, f=f, g=g, dt=dt, intg_type=intg_type,
                      var_type=var_type, wiener_type=wiener_type, show_code=show_code)


def milstein(f=None, g=None, dt=None, intg_type=None, var_type=None, wiener_type=None, show_code=None):
  return Wrapper.wrap(Wrapper.milstein, f=f, g=g, dt=dt, intg_type=intg_type,
                      var_type=var_type, wiener_type=wiener_type, show_code=show_code)
