Object.defineProperty(exports, "__esModule", { value: true });
exports.IconSpan = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconSpan = React.forwardRef(function IconSpan(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M8.28,14.48h6.24V11.16H8.28ZM4.88,9.66h6.24V6.34H4.88Zm7.74,0h2.15A1.25,1.25,0,0,1,16,10.91v3.82A1.25,1.25,0,0,1,14.77,16H8a1.25,1.25,0,0,1-1.25-1.25V11.16H4.63A1.25,1.25,0,0,1,3.38,9.91V6.34H1.23A1.25,1.25,0,0,1,0,5.09V1.27A1.25,1.25,0,0,1,1.23,0H8A1.25,1.25,0,0,1,9.22,1.27V4.84h2.15a1.25,1.25,0,0,1,1.25,1.25ZM1.48,4.84H7.72V1.52H1.48Z"/>
    </svgIcon_1.default>);
});
exports.IconSpan = IconSpan;
IconSpan.displayName = 'IconSpan';
//# sourceMappingURL=iconSpan.jsx.map