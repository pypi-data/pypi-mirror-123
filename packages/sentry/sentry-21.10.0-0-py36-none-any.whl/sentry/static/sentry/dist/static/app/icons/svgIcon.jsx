Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const SvgIcon = React.forwardRef(function SvgIcon(_a, ref) {
    var _b, _c;
    var { color: providedColor = 'currentColor', size: providedSize = 'sm', viewBox = '0 0 16 16' } = _a, props = (0, tslib_1.__rest)(_a, ["color", "size", "viewBox"]);
    const theme = (0, react_1.useTheme)();
    const color = (_b = theme[providedColor]) !== null && _b !== void 0 ? _b : providedColor;
    const size = (_c = theme.iconSizes[providedSize]) !== null && _c !== void 0 ? _c : providedSize;
    return (<svg {...props} viewBox={viewBox} fill={color} height={size} width={size} ref={ref}/>);
});
exports.default = SvgIcon;
//# sourceMappingURL=svgIcon.jsx.map