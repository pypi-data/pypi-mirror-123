Object.defineProperty(exports, "__esModule", { value: true });
exports.IconCircle = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconCircle = React.forwardRef(function IconCircle(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M8,16a8,8,0,1,1,8-8A8,8,0,0,1,8,16ZM8,1.53A6.47,6.47,0,1,0,14.47,8,6.47,6.47,0,0,0,8,1.53Z"/>
    </svgIcon_1.default>);
});
exports.IconCircle = IconCircle;
IconCircle.displayName = 'IconCircle';
//# sourceMappingURL=iconCircle.jsx.map