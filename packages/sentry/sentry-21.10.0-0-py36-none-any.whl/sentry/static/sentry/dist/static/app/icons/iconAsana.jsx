Object.defineProperty(exports, "__esModule", { value: true });
exports.IconAsana = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconAsana = React.forwardRef(function IconAsana(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M8,.61A3.48,3.48,0,1,1,4.52,4.09,3.48,3.48,0,0,1,8,.61Z"/>
      <path d="M1,14.38A3.48,3.48,0,1,0,1,9.45,3.49,3.49,0,0,0,1,14.38Z"/>
      <path d="M15,14.38a3.48,3.48,0,1,1,0-4.93A3.49,3.49,0,0,1,15,14.38Z"/>
    </svgIcon_1.default>);
});
exports.IconAsana = IconAsana;
IconAsana.displayName = 'IconAsana';
//# sourceMappingURL=iconAsana.jsx.map