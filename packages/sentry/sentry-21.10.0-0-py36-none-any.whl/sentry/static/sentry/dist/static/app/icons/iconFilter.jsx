Object.defineProperty(exports, "__esModule", { value: true });
exports.IconFilter = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconFilter = React.forwardRef(function IconFilter(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M15.19,2.53H.81A.75.75,0,0,1,.81,1H15.19a.75.75,0,1,1,0,1.5Z"/>
      <path d="M11.63,15H4.36a.75.75,0,0,1,0-1.5h7.27a.75.75,0,0,1,0,1.5Z"/>
      <path d="M13.41,8.75H2.58a.75.75,0,0,1,0-1.5H13.41a.75.75,0,0,1,0,1.5Z"/>
    </svgIcon_1.default>);
});
exports.IconFilter = IconFilter;
IconFilter.displayName = 'IconFilter';
//# sourceMappingURL=iconFilter.jsx.map