hello world
===========

Hello World is the first prototype of the CodeKlavier and it demonstrates the core principes of CodeKlavier. It uses a basic mapping from the piano (midi)keys to characters or predefined strings. These character/string translation is send to SuperCollider to generate sounds. In the original version of Hello World, it instructed a robot toy piano to play notes and motifes. When the piece is performed without the robot toy piano, the piece can also work with recorded samples.

hello_world
-----------
Run an infinite loop (or at least until keyboard intterupt) and run CodeKlavier. This programm set the callback and pass the key presses on towards SuperCollider.

.. NOTE::
    Make sure you have SuperCollider up and running before running the ``hello world`` application. Please reboot SuperCollider Server berfore you astart a live performance.

Video tutorials
...............

A video of the Hello World performance can be found `here <https://www.youtube.com/watch?v=ytpB8FB6VTU>`_. This is an early version; the piece evolved over time. A short video tutorial on the ``~ost`` function can be found `here <https://www.google.nl/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwiKh7LtqojZAhVIY1AKHVulDu4QtwIIMDAB&url=https%3A%2F%2Fvimeo.com%2F239485328&usg=AOvVaw2yWA5KUPWd2iYvincGneZ4>`_ and the ``delay to pitch`` example can be found `here <https://www.google.nl/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&cad=rja&uact=8&ved=0ahUKEwiKh7LtqojZAhVIY1AKHVulDu4QtwIINDAC&url=https%3A%2F%2Fvimeo.com%2F239778747&usg=AOvVaw1IM4ohG61d0Am5ovjOAdnr>`_.

instructions_nkk
----------------
For the *Leiden Nacht van Kunst en Cultuur* a special version is made, so the visitors can also try out the CodeKlavier. To teach them how to get used to the system and how to perform, they can first run through the ``instruction`` for the CodeKlavier.

hello_world_nkk
---------------
This is a special version of the CodeKlaver, made specifically for the *Leiden Nacht van Kunst en Cultuur*. It uses a seperate key-mapping that can be found in ``CodeKlavier.Mapping.Mapping_HelloWorld_NKK``.

Hello World python documentation
--------------------------------

The python scripts in the hello world folder contain documentation.

Hello World
...........

.. automodule:: hello_world.hello_world
    :members:
    :undoc-members:
    :show-inheritance:

Hello World NKK
...............
.. automodule:: hello_world.hello_world_nkk
    :members:
    :undoc-members:
    :show-inheritance:

Instructions
............
.. automodule:: hello_world.instructions_nkk
    :members:
    :undoc-members:
    :show-inheritance:
