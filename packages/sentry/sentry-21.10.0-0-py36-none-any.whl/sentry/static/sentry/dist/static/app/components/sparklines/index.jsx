Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_sparklines_1 = require("react-sparklines");
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
/**
 * This is required because:
 *
 * - React.Suspense only works with default exports
 * - typescript complains that the library's `propTypes` does not
 * have `children defined.
 * - typescript also won't let us access `Sparklines.propTypes`
 */
class SparklinesWithCustomPropTypes extends react_sparklines_1.Sparklines {
}
exports.default = SparklinesWithCustomPropTypes;
SparklinesWithCustomPropTypes.propTypes = {
    children: prop_types_1.default.node,
    data: prop_types_1.default.array,
    limit: prop_types_1.default.number,
    width: prop_types_1.default.number,
    height: prop_types_1.default.number,
    svgWidth: prop_types_1.default.number,
    svgHeight: prop_types_1.default.number,
    preserveAspectRatio: prop_types_1.default.string,
    margin: prop_types_1.default.number,
    style: prop_types_1.default.object,
    min: prop_types_1.default.number,
    max: prop_types_1.default.number,
    onMouseMove: prop_types_1.default.func,
};
//# sourceMappingURL=index.jsx.map