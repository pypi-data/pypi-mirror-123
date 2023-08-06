Object.defineProperty(exports, "__esModule", { value: true });
exports.IconCode = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconCode = React.forwardRef(function IconCode(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M3.82 11.8a.79.79 0 0 1-.53-.22l-3-3.05a.74.74 0 0 1 0-1.06l3-3a.75.75 0 0 1 1.06 1.01L1.84 8l2.51 2.52a.75.75 0 0 1-.53 1.28Zm8.36 0a.75.75 0 0 1-.53-1.28L14.16 8l-2.51-2.52a.75.75 0 1 1 1.06-1.06l3 3.05a.743.743 0 0 1 0 1.06l-3 3.05a.79.79 0 0 1-.53.22Zm-6.49 1.95A.75.75 0 0 1 5 12.69l4.62-10a.75.75 0 0 1 1-.36.74.74 0 0 1 .36 1l-4.62 10a.76.76 0 0 1-.67.42Z"/>
    </svgIcon_1.default>);
});
exports.IconCode = IconCode;
IconCode.displayName = 'IconCode';
//# sourceMappingURL=iconCode.jsx.map