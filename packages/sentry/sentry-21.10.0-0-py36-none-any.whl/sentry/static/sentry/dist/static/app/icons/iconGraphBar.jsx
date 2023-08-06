Object.defineProperty(exports, "__esModule", { value: true });
exports.IconGraphBar = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconGraphBar = React.forwardRef(function IconGraphBar(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M4.06,16H.74A.75.75,0,0,1,0,15.24v-4a.74.74,0,0,1,.75-.75H4.06a.75.75,0,0,1,.75.75v4A.76.76,0,0,1,4.06,16Zm-2.57-1.5H3.31V12H1.49Z"/>
      <path d="M9.65,16H6.33a.76.76,0,0,1-.75-.75V6.06a.75.75,0,0,1,.75-.75H9.65a.74.74,0,0,1,.75.75v9.18A.75.75,0,0,1,9.65,16Zm-2.57-1.5H8.9V6.81H7.08Z"/>
      <path d="M15.25,16H11.93a.75.75,0,0,1-.75-.75V.76A.75.75,0,0,1,11.93,0h3.32A.76.76,0,0,1,16,.76V15.24A.76.76,0,0,1,15.25,16Zm-2.57-1.5H14.5v-13H12.68Z"/>
    </svgIcon_1.default>);
});
exports.IconGraphBar = IconGraphBar;
IconGraphBar.displayName = 'IconGraphBar';
//# sourceMappingURL=iconGraphBar.jsx.map