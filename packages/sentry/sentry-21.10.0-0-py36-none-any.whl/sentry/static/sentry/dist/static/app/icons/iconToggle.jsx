Object.defineProperty(exports, "__esModule", { value: true });
exports.IconToggle = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconToggle = React.forwardRef(function IconToggle(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <circle cx="5.36" cy="8" r="3.08"/>
      <path d="M10.68,13.34H5.32a5.34,5.34,0,0,1,0-10.68h5.36a5.34,5.34,0,0,1,0,10.68ZM5.32,4.16a3.84,3.84,0,0,0,0,7.68h5.36a3.84,3.84,0,0,0,0-7.68Z"/>
    </svgIcon_1.default>);
});
exports.IconToggle = IconToggle;
IconToggle.displayName = 'IconToggle';
//# sourceMappingURL=iconToggle.jsx.map