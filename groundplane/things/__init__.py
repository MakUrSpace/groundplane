import groundplane.things.things as things
thing_types = {thing.__name__: thing for thing in things.__dict__.values()
               if type(thing) is type and issubclass(thing, things.thing)}

