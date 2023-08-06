# How does the parser work?

_I recommend you to read [More about FLP Format](flp-format.md) before this._

Since, FLP is an event-based binary format, we need to work with data types of C _(Delphi actually, because FL is written in Delphi, but Delphi's basic data types aren't different from C's data types)_. Python provides a nice way to read these types through the `struct` module. I made my own extension of `io.BytesIO` class named [`BytesIOEx`](https://github.com/demberto/bytesioex) which is inspired by C#'s `BinaryReader` and `BinaryWriter`. The extension `read_*` and `write_*` just convert raw `bytes` objects into a data type.

## `Event`

Then I read all the events into a `list` of `Event` objects which I call the **Event Store**. The parsing logic for this is in [`__build_event_store()`](https://github.com/demberto/PyFLP/blob/master/pyflp/parser.py#L87) method of `Parser`. It is important that every new event has an `index` so it can be sorted later on, while saving. The `Event` class looks like this _minified_:

```Python
class Event:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @property
    def size(self) -> int:
        ...

    def dump(self, new_data: Any):
        """Convert Python data types to binary and set that to self.data"""
        ...

    def to_raw(self) -> bytes:
        """Converts an Event object back to its raw representation (used while saving)"""
        ...
```

Subclasses have additional `to_*` helper methods, which convert basic types to Python types.

## `FLObject`

Once the events are created, the `ProjectParser.parse()` starts building the `Project` object, by examining `Event` IDs. All its fields for e.g. `Channel`, `Insert` etc. inherit from `FLObject`.

FLObject class looks like this _minified_:

```Python
class FLObject:
    def __init__(self):
        self._events: Dict[str, Event] = {}
        ...

    def parse(self):
        """Check implementation for more details"""
        ...

    def save(self) -> Optional[ValuesView[Event]]:
        return self._events.values()
```

When an event from `ChannelEventID` is found that event is sent to a `Channel` object for parsing. This is handled by the `parse()` method. It calls the appropriate `to_*` method of the received `Event` and sets its properties accordingly. It also stores the event in a local dictionary, so whenever property setters are called, the Python data type is dumped back to the event in the local dictionary by calling the `dump()` method of `Event`. When parsing is done, a user can modify the _implemented_ properties very easily and when he is done, `Project.save()` needs to be called to save an FLP back to disk.

`Project.save()` calls `save()` for every `FLObject` and rebuilds the **Event Store**, which is then dumped to a stream along with header data, which can be used directly or saved as well to a files. The chunk length could have been changed, hence it needs to be recalculated which is implemented by `Event.size`.
