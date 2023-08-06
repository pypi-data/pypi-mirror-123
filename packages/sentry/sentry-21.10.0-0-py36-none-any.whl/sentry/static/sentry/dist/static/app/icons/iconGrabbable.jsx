Object.defineProperty(exports, "__esModule", { value: true });
exports.IconGrabbable = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconGrabbable = React.forwardRef(function IconGrabbable(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <circle cx="4.73" cy="8" r="1.31"/>
      <circle cx="4.73" cy="1.31" r="1.31"/>
      <circle cx="11.27" cy="8" r="1.31"/>
      <circle cx="11.27" cy="1.31" r="1.31"/>
      <circle cx="4.73" cy="14.69" r="1.31"/>
      <circle cx="11.27" cy="14.69" r="1.31"/>
    </svgIcon_1.default>);
});
exports.IconGrabbable = IconGrabbable;
IconGrabbable.displayName = 'IconGrabbable';
//# sourceMappingURL=iconGrabbable.jsx.map