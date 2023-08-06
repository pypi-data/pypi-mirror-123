Object.defineProperty(exports, "__esModule", { value: true });
exports.TickAlignment = exports.rawSpanKeys = void 0;
exports.rawSpanKeys = new Set([
    'trace_id',
    'parent_span_id',
    'span_id',
    'start_timestamp',
    'timestamp',
    'same_process_as_parent',
    'op',
    'description',
    'status',
    'data',
    'tags',
]);
var TickAlignment;
(function (TickAlignment) {
    TickAlignment[TickAlignment["Left"] = 0] = "Left";
    TickAlignment[TickAlignment["Right"] = 1] = "Right";
    TickAlignment[TickAlignment["Center"] = 2] = "Center";
})(TickAlignment = exports.TickAlignment || (exports.TickAlignment = {}));
//# sourceMappingURL=types.jsx.map