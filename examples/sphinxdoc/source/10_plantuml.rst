
PlantUML
========

The docker image contains the sphinxcontrib.plantuml extension for Sphinx which allows
you to embed UML diagrams using PlantUML.

PlantUML_ is a Java component that allows to write UML and some non-UML diagrams:

* `Sequence diagram <http://plantuml.com/sequence-diagram>`_
* `Usecase diagram <http://plantuml.com/use-case-diagram>`_
* `Class diagram <http://plantuml.com/class-diagram>`_
* `Activity diagram <http://plantuml.com/activity-diagram-beta>`_
* `Component diagram <http://plantuml.com/component-diagram>`_
* `State diagram <http://plantuml.com/state-diagram>`_
* `Object diagram <http://plantuml.com/object-diagram>`_
* `Deployment diagram <http://plantuml.com/deployment-diagram>`_
* `Timing diagram <http://plantuml.com/timing-diagram>`_

Diagrams are defined using a simple and intuitive language.
This can be used within many other tools.
Images can be generated in PNG or SVG format.

Examples
--------

In the Sphinx reST documents,
simply begin the PlantUML code with the ``uml`` directive.

.. begin-plantuml-first-example

.. uml:: 
   
   @startuml
   user -> (use PlantUML)

   note left of user
      Hello!   
   end note
   @enduml

.. end-plantuml-first-example

Which generates the following result:

.. uml::

   @startuml
   user -> (use PlantUML)

   note left of user
      Hello!
   end note
   @enduml
