# LandShark

Maker module automation system

##  Controllers

Controllers are the primary building block of the automation system. They take a structure like this
```
class dog_controller(controller):
    def required_keys(self):
        return ['fur_color', 'tongue', 'love']

    def lick(self):
        tongue_api('lick', self.tongue)
    ...
```
Controllers are built with a JSON definition dictionary. The values of this JSON object make up the core of the controller and are added as attributes to its instances.

Controller classes follow these rules:
* Root controller.__init__ must be called in initialization
* {controller_type}.required_keys returns a list of keys that the controller will need

The Controller pattern heavily encourages multiple inheritance. A device/controller is defined as an amalgamation of all its subcontrollers. In this way, subsystems should be easily definable separate from the whole of any system.

During instance initialization, the root controller's __init__ method uses the new controller's class to determine all parent classes. With this list of parent classes, all required keys for the new instance's definition are gathered and compared against the supplied definition.

