Object.defineProperty(exports, "__esModule", { value: true });
exports.DashboardState = exports.DisplayType = exports.MAX_WIDGETS = void 0;
// Max widgets per dashboard we are currently willing
// to allow to limit the load on snuba from the
// parallel requests. Somewhat arbitrary
// limit that can be changed if necessary.
exports.MAX_WIDGETS = 30;
var DisplayType;
(function (DisplayType) {
    DisplayType["AREA"] = "area";
    DisplayType["BAR"] = "bar";
    DisplayType["LINE"] = "line";
    DisplayType["TABLE"] = "table";
    DisplayType["WORLD_MAP"] = "world_map";
    DisplayType["BIG_NUMBER"] = "big_number";
    DisplayType["STACKED_AREA"] = "stacked_area";
    DisplayType["TOP_N"] = "top_n";
})(DisplayType = exports.DisplayType || (exports.DisplayType = {}));
var DashboardState;
(function (DashboardState) {
    DashboardState["VIEW"] = "view";
    DashboardState["EDIT"] = "edit";
    DashboardState["CREATE"] = "create";
    DashboardState["PENDING_DELETE"] = "pending_delete";
})(DashboardState = exports.DashboardState || (exports.DashboardState = {}));
//# sourceMappingURL=types.jsx.map