Object.defineProperty(exports, "__esModule", { value: true });
exports.IconList = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconList = React.forwardRef(function IconList(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M15.19,8.75H3.7a.75.75,0,1,1,0-1.5H15.19a.75.75,0,0,1,0,1.5Z"/>
      <circle cx="0.75" cy="8" r="0.75"/>
      <path d="M15.19,15H3.7a.75.75,0,1,1,0-1.5H15.19a.75.75,0,1,1,0,1.5Z"/>
      <circle cx="0.75" cy="14.25" r="0.75"/>
      <path d="M15.19,2.53H3.7A.75.75,0,0,1,3.7,1H15.19a.75.75,0,1,1,0,1.5Z"/>
      <circle cx="0.75" cy="1.75" r="0.75"/>
    </svgIcon_1.default>);
});
exports.IconList = IconList;
IconList.displayName = 'IconList';
//# sourceMappingURL=iconList.jsx.map