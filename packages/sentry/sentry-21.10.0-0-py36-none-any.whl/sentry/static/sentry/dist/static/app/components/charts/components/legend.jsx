Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("echarts/lib/component/legend");
require("echarts/lib/component/legendScroll");
const merge_1 = (0, tslib_1.__importDefault)(require("lodash/merge"));
const utils_1 = require("../utils");
function Legend(props) {
    const _a = props !== null && props !== void 0 ? props : {}, { truncate, theme } = _a, rest = (0, tslib_1.__rest)(_a, ["truncate", "theme"]);
    const formatter = (value) => (0, utils_1.truncationFormatter)(value, truncate !== null && truncate !== void 0 ? truncate : 0);
    return (0, merge_1.default)({
        show: true,
        type: 'scroll',
        padding: 0,
        formatter,
        icon: 'circle',
        itemHeight: 14,
        itemWidth: 8,
        itemGap: 12,
        align: 'left',
        textStyle: {
            color: theme.textColor,
            verticalAlign: 'top',
            fontSize: 11,
            fontFamily: theme.text.family,
            lineHeight: 14,
        },
        inactiveColor: theme.inactive,
    }, rest);
}
exports.default = Legend;
//# sourceMappingURL=legend.jsx.map