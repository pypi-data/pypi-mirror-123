# -*- coding: utf-8 -*-

import brainpy as bp
import brainpy.math as bm

__all__ = [
  'AMPA',
]


class AMPA(bp.TwoEndConn):
  r"""AMPA conductance-based synapse model.

  **Model Descriptions**

  AMPA receptor is an ionotropic receptor, which is an ion channel.
  When it is bound by neurotransmitters, it will immediately open the
  ion channel, causing the change of membrane potential of postsynaptic neurons.

  A classical model is to use the Markov process to model ion channel switch.
  Here :math:`g` represents the probability of channel opening, :math:`1-g`
  represents the probability of ion channel closing, and :math:`\alpha` and
  :math:`\beta` are the transition probability. Because neurotransmitters can
  open ion channels, the transfer probability from :math:`1-g` to :math:`g`
  is affected by the concentration of neurotransmitters. We denote the concentration
  of neurotransmitters as :math:`[T]` and get the following Markov process.

  .. image:: ../../images/synapse_markov.png
      :align: center

  We obtained the following formula when describing the process by a differential equation.

  .. math::

      \frac{ds}{dt} =\alpha[T](1-g)-\beta g

  where :math:`\alpha [T]` denotes the transition probability from state :math:`(1-g)`
  to state :math:`(g)`; and :math:`\beta` represents the transition probability of
  the other direction. :math:`\alpha` is the binding constant. :math:`\beta` is the
  unbinding constant. :math:`[T]` is the neurotransmitter concentration, and
  has the duration of 0.5 ms.

  Moreover, the post-synaptic current on the post-synaptic neuron is formulated as

  .. math::

      I_{syn} = g_{max} g (V-E)

  where :math:`g_{max}` is the maximum conductance, and `E` is the reverse potential.


  **Model Examples**

  - `Simple illustrated example <../synapses/ampa.ipynb>`_


  **Model Parameters**
  
  ============= ============== ======== ================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- ------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  g_max         .42            µmho(µS) Maximum conductance.
  E             0              mV       The reversal potential for the synaptic current.
  alpha         .98            \        Binding constant.
  beta          .18            \        Unbinding constant.
  T             .5             mM       Neurotransmitter concentration.
  T_duration    .5             ms       Duration of the neurotransmitter concentration.
  ============= ============== ======== ================================================


  **Model Variables**

  ================== ================== ==================================================
  **Member name**    **Initial values** **Explanation**
  ------------------ ------------------ --------------------------------------------------
  g                  0                  Synapse gating variable.
  pre_spike          False              The history of pre-synaptic neuron spikes.
  spike_arrival_time -1e7               The arrival time of the pre-synaptic neuron spike.
  ================== ================== ==================================================

  **References**

  .. [1] Vijayan S, Kopell N J. Thalamic model of awake alpha oscillations
         and implications for stimulus processing[J]. Proceedings of the
         National Academy of Sciences, 2012, 109(45): 18553-18558.
  """

  def __init__(self, pre, post, conn, delay=0., g_max=0.42, E=0., alpha=0.98,
               beta=0.18, T=0.5, T_duration=0.5, update_type='sparse', **kwargs):

    # initialization
    super(AMPA, self).__init__(pre=pre, post=post, conn=conn, **kwargs)

    # checking
    assert hasattr(pre, 't_last_spike'), 'Pre-synaptic group must has "t_last_spike" variable.'
    assert hasattr(post, 'V'), 'Post-synaptic group must has "V" variable.'
    assert hasattr(post, 'input'), 'Post-synaptic group must has "input" variable.'

    # parameters
    self.delay = delay
    self.g_max = g_max
    self.E = E
    self.alpha = alpha
    self.beta = beta
    self.T = T
    self.T_duration = T_duration

    # connections
    if update_type == 'sparse':
      self.pre_ids, self.post_ids = self.conn.requires('pre_ids', 'post_ids')
      self.steps.replace('update', self._sparse_update)
      self.size = len(self.pre_ids)
      self.target_backend = 'numpy'

    elif update_type == 'dense':
      raise NotImplementedError

    else:
      raise bp.errors.UnsupportedError(f'Do not support {update_type} method.')

    # variables
    self.g = bm.Variable(bm.zeros(self.size))
    self.pre_spike = self.register_constant_delay('ps', self.pre.shape, delay)
    self.spike_arrival_time = bm.Variable(bm.ones(self.pre.num) * -1e7)

  @bp.odeint(method='exponential_euler')
  def integral(self, g, t, TT):
    dg = self.alpha * TT * (1 - g) - self.beta * g
    return dg

  def _sparse_update(self, _t, _dt):
    self.pre_spike.push(self.pre.spike)
    delayed_pre_spike = self.pre_spike.pull()
    self.spike_arrival_time[:] = bm.where(delayed_pre_spike, _t, self.spike_arrival_time)
    for i in range(self.size):
      pre_id, post_id = self.pre_ids[i], self.post_ids[i]
      # update
      TT = ((_t - self.spike_arrival_time[pre_id]) < self.T_duration) * self.T
      self.g[i] = self.integral(self.g[i], _t, TT, dt=_dt)
      # output
      self.post.input[post_id] -= self.g_max * self.g[i] * (self.post.V[post_id] - self.E)
