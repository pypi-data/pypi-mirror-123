Object.defineProperty(exports, "__esModule", { value: true });
exports.IconGraph = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const iconGraphBar_1 = require("./iconGraphBar");
const iconGraphCircle_1 = require("./iconGraphCircle");
const iconGraphLine_1 = require("./iconGraphLine");
const IconGraph = React.forwardRef(function IconGraph(_a, ref) {
    var { type = 'line' } = _a, props = (0, tslib_1.__rest)(_a, ["type"]);
    switch (type) {
        case 'circle':
            return <iconGraphCircle_1.IconGraphCircle {...props} ref={ref}/>;
        case 'bar':
            return <iconGraphBar_1.IconGraphBar {...props} ref={ref}/>;
        default:
            return <iconGraphLine_1.IconGraphLine {...props} ref={ref}/>;
    }
});
exports.IconGraph = IconGraph;
IconGraph.displayName = 'IconGraph';
//# sourceMappingURL=iconGraph.jsx.map