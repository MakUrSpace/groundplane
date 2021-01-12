# GroundPlane

Maker module automation system

##  Things

Things are the primary building block of the automation system. They take a structure like this
```
class dog_thing(thing):
    def required_keys(self):
        return ['fur_color', 'tongue', 'love']

    def lick(self):
        tongue_api('lick', self.tongue)
    ...
```
Things are built with a JSON definition dictionary. The values of this JSON object make up the core of the thing and are added as attributes to its instances.

Thing classes follow these rules:
* Root thing.__init__ must be called in initialization
* {thing_type}.required_keys returns a list of keys that the thing will need

The Thing pattern heavily encourages multiple inheritance. A device/thing is defined as an amalgamation of all its subthings. In this way, subsystems should be easily definable separate from the whole of any system.

During instance initialization, the root thing's __init__ method uses the new thing's class to determine all parent classes. With this list of parent classes, all required keys for the new instance's definition are gathered and compared against the supplied definition.

