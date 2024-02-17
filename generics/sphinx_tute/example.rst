Title
============

subtitle 
-------------

sub sub Title
^^^^^^^^^^^^^^^^^^

List

- item 1
- item 2

List2

#. item 1
#. item 2

Code block::

    print("Hello World")


sub 2
-----------

sub sub 2
^^^^^^^^^^^^^^^^^^

list of list

#. item 1

    - item 1-1
    - item 1-2

#. item 2


sub 3
-----------

picture

.. figure:: https://www.python.org/static/community_logos/python-logo-master-v3-TM.png
   :alt: python logo
   :width: 200

   python logo

local picture

.. figure:: ../../pic.png
   :alt: alt text
   :width: 200

   pic text

math formula
-----------------------

.. math::

    \int_{-\infty}^\infty g(x) dx

.. math::

    \sum_{i=1}^n a_i=0

X is distributed as a normal with mean \mu and variance \sigma^2:

.. math::

    X \sim \mathcal{N}(\mu,\,\sigma^{2})

normal distribution pdf:

.. math::

    f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}

normal distribution cdf:

.. math::

    F(x) = \frac{1}{2}\left[1+\operatorname{erf}\left(\frac{x-\mu}{\sigma\sqrt{2}}\right)\right]

where erf is the error function, 
and \mu and \sigma are the mean and standard deviation of the distribution.

.. math::

    \operatorname{erf}(x) = \frac{1}{\sqrt\pi}\int_{-x}^x e^{-t^2} dt

Differentiation and integration rules
-------------------------------------

.. math::

    \frac{d}{dx} \left[ u(x) \pm v(x) \right] = \frac{du(x)}{dx} \pm \frac{dv(x)}{dx}

.. math::

    \frac{d}{dx} \left[ c \cdot u(x) \right] = c \cdot \frac{du(x)}{dx}

.. math::

    \frac{d}{dx} \left[ u(x) \cdot v(x) \right] = v(x) \cdot \frac{du(x)}{dx} + u(x) \cdot \frac{dv(x)}{dx}

.. math::

    \frac{d}{dx} \left[ \frac{u(x)}{v(x)} \right] = \frac{v(x) \cdot \frac{du(x)}{dx} - u(x) \cdot \frac{dv(x)}{dx}}{v(x)^2}

.. math::

    \frac{d}{dx} \left[ u(v(x)) \right] = \frac{du(v(x))}{dv(x)} \cdot \frac{dv(x)}{dx}

.. math::

    \int \left[ u(x) \pm v(x) \right] dx = \int u(x) dx \pm \int v(x) dx

.. math::

    \int k \cdot u(x) dx = k \cdot \int u(x) dx

.. math::

    \int x^n dx = \frac{x^{n+1}}{n+1} + c, \text{for } n \neq -1

.. math::

    \int \frac{1}{x} dx = \ln|x| + c

.. math::

    \int e^x dx = e^x + c

.. math::

    \int a^x dx = \frac{a^x}{\ln a} + c

.. math::

    \int \sin x dx = -\cos x + c

.. math::

    \int \cos x dx = \sin x + c

.. math::

    \int \tan x dx = -\ln|\cos x| + c

.. math::

    \int \cot x dx = \ln|\sin x| + c




