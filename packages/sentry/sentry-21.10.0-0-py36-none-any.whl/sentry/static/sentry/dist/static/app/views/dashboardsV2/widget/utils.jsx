Object.defineProperty(exports, "__esModule", { value: true });
exports.displayTypes = exports.DataSet = exports.DisplayType = void 0;
const locale_1 = require("app/locale");
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
var DataSet;
(function (DataSet) {
    DataSet["EVENTS"] = "events";
    DataSet["METRICS"] = "metrics";
})(DataSet = exports.DataSet || (exports.DataSet = {}));
exports.displayTypes = {
    [DisplayType.AREA]: (0, locale_1.t)('Area Chart'),
    [DisplayType.BAR]: (0, locale_1.t)('Bar Chart'),
    [DisplayType.LINE]: (0, locale_1.t)('Line Chart'),
    [DisplayType.TABLE]: (0, locale_1.t)('Table'),
    [DisplayType.WORLD_MAP]: (0, locale_1.t)('World Map'),
    [DisplayType.BIG_NUMBER]: (0, locale_1.t)('Big Number'),
    [DisplayType.TOP_N]: (0, locale_1.t)('Top Events'),
};
//# sourceMappingURL=utils.jsx.map