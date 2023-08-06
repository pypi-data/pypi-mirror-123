Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const merge_1 = (0, tslib_1.__importDefault)(require("lodash/merge"));
/**
 * Drawing grid in rectangular coordinates
 *
 * e.g. alignment of your chart?
 */
function Grid(props = {}) {
    return (0, merge_1.default)({
        top: 20,
        bottom: 20,
        // This should allow for sufficient space for Y-axis labels
        left: 4,
        right: '0%',
        containLabel: true,
    }, props);
}
exports.default = Grid;
//# sourceMappingURL=grid.jsx.map