Object.defineProperty(exports, "__esModule", { value: true });
exports.IconMenu = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconMenu = React.forwardRef(function IconMenu(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M15.19,2.53H.81A.75.75,0,0,1,.81,1H15.19a.75.75,0,1,1,0,1.5Z"/>
      <path d="M15.19,15H.81a.75.75,0,0,1,0-1.5H15.19a.75.75,0,1,1,0,1.5Z"/>
      <path d="M15.19,8.75H.81a.75.75,0,1,1,0-1.5H15.19a.75.75,0,0,1,0,1.5Z"/>
    </svgIcon_1.default>);
});
exports.IconMenu = IconMenu;
IconMenu.displayName = 'IconMenu';
//# sourceMappingURL=iconMenu.jsx.map