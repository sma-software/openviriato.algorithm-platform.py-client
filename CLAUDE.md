# algorithmplatform.pyclient

Python REST client for the Algorithm Platform (Viriato) API.

## Project layout

```
py_client/
  aidm/                        # Domain model classes (AIDM = Algorithm Interface Data Model)
  algorithm_interface/         # AlgorithmInterface façade + helpers
  communication/               # HTTP layer
  conversion/                  # JSON ↔ AIDM conversion pipeline
  *_test/                      # Unit tests mirroring each package
walkthroughs/                  # Runnable example algorithms
jenkins/                       # Build & release scripts
```

## Running tests

No pytest — use `unittest` directly:

```
"C:/Workspace/PyClient/.venv/Scripts/python.exe" -m unittest <module.path.TestClass> -v
```

Virtual environment: `C:/Workspace/PyClient/.venv` (not `testing_venv`, which does not exist locally).

## Code formatting

Black with line length 160:

```
"C:/Workspace/PyClient/.venv/Scripts/python.exe" -m black --line-length 160 <file(s)>
```

Line length is defined in `jenkins/release_build_classes.py` as `FORMATTING_LINE_LENGTH = 160`.

---

## Routing edge class hierarchy

The routing edge types are split into **Request** types (sent to the API) and **Response** types (received from the API). Both live in `py_client/aidm/aidm_routing_edge_classes.py`.

### Request types (outbound)

Used as method parameters when calling the API (e.g. `get_separation_time_in_station_for_routes`).

```
_RoutingEdgeRequest
├── _IncomingRoutingEdgeRequest
│   ├── IncomingRoutingEdgeRequest          type string: "incoming"
│   └── IncomingNodeTrackRoutingEdgeRequest type string: "incomingNodeTrack"
├── _OutgoingRoutingEdgeRequest
│   ├── OutgoingRoutingEdgeRequest          type string: "outgoing"
│   └── OutgoingNodeTrackRoutingEdgeRequest type string: "outgoingNodeTrack"
└── CrossingRoutingEdgeRequest              type string: "crossing"
```

### Response types (inbound)

Returned by routing edge query methods (`get_incoming_routing_edges`, etc.).

```
_RoutingEdgeResponse
├── IncomingNodeTrackRoutingEdgeResponse    type string: "incomingNodeTrack"
├── OutgoingNodeTrackRoutingEdgeResponse    type string: "outgoingNodeTrack"
└── CrossingRoutingEdgeResponse             type string: "crossing"
```

Note: `IncomingRoutingEdgeResponse` and `OutgoingRoutingEdgeResponse` do **not** exist — the API only returns node-track variants as Response types.

### RoutingEdgeSide enum

```python
class RoutingEdgeSide(Enum):
    A = "a"
    B = "b"
```

Values are the lowercase strings `"a"` / `"b"` (matching the JSON wire format).

---

## JSON ↔ AIDM conversion pipeline

### Inbound (JSON → Python): `py_client/conversion/json_to_aidm_converter.py`

`JsonToAidmConverter` runs a chain of processors in order:
`ListProcessor → SingleAttributeProcessor → OptionalProcessor → DatetimeProcessor → TimedeltaProcessor → EnumProcessor → PolymorphicClassesProcessor → ConflictProcessor → PrimitiveProcessor → GeneralAidmObjectProcessor`

**`PolymorphicClassesProcessor`** handles all polymorphic base types. When extending the routing edge hierarchy, both lists must be kept in sync:

- `types_to_process`: the abstract base(s) that trigger this processor  
  → currently includes `_RoutingEdgeRequest` and `_RoutingEdgeResponse`
- `aidm_types_to_create`: all concrete leaf classes the processor may instantiate  
  → currently includes all 5 Request types + 3 Response types

The type dispatch uses `convert_to_snake_case(ClassName)` substring-matching against the JSON `"type"` field (converted to snake_case). Example: JSON `"incomingNodeTrack"` → snake `"incoming_node_track"` → found in `"incoming_node_track_routing_edge_request"`. Disambiguation between multiple substring matches falls back to constructor argument matching.

**`GeneralAidmObjectProcessor`** handles all other concrete AIDM types via `get_type_hints()` + Python name mangling (`__attr` → strip class prefix). Fields are converted from camelCase JSON to snake_case automatically.

### Outbound (Python → JSON): `py_client/conversion/aidm_to_json_post_processor.py`

`AIDMToJSONPostProcessorChain` adds the `"type"` discriminator field that the serializer omits by default. Two processors cover routing edges:

- `RoutingEdgeRequestPostProcessor` — handles all 5 Request types
- `RoutingEdgeResponseProcessor` — handles all 3 Response types

**When adding a new routing edge subtype, update all four of the above locations.**

---

## Checklist when adding / renaming AIDM types

1. Define the class in `py_client/aidm/aidm_routing_edge_classes.py`
2. Export it from `py_client/aidm/__init__.py` if needed
3. Register it in `PolymorphicClassesProcessor.aidm_types_to_create` (and `types_to_process` for new base types)
4. Add a processor (or extend an existing one) in `aidm_to_json_post_processor.py`
5. Update `algorithm_interface.py` parameter/return type annotations
6. Update `_algorithm_interface_helpers.py` if routing edge query helpers are involved
7. Update the corresponding unit tests in `conversion_test/` and `algorithm_interface_test/`
8. Update py_calls JSON files in the end-to-end test tool (see that project's CLAUDE.md)
9. Run a project-wide grep for the old type name to catch stragglers:
   ```
   grep -r "OldTypeName" py_client/
   ```
