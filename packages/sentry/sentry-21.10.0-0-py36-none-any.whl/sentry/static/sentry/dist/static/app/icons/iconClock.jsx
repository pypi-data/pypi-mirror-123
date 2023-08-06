Object.defineProperty(exports, "__esModule", { value: true });
exports.IconClock = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconClock = React.forwardRef(function IconClock(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M8,16a8,8,0,1,1,8-8A8,8,0,0,1,8,16ZM8,1.52A6.48,6.48,0,1,0,14.48,8,6.49,6.49,0,0,0,8,1.52Z"/>
      <path d="M11.62,8.75H8A.76.76,0,0,1,7.25,8V2.88a.75.75,0,1,1,1.5,0V7.25h2.87a.75.75,0,0,1,0,1.5Z"/>
    </svgIcon_1.default>);
});
exports.IconClock = IconClock;
IconClock.displayName = 'IconClock';
//# sourceMappingURL=iconClock.jsx.map