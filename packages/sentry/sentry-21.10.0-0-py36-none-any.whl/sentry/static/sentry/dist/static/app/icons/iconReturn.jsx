Object.defineProperty(exports, "__esModule", { value: true });
exports.IconReturn = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconReturn = React.forwardRef(function IconReturn(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M3.89,15.06a.74.74,0,0,1-.53-.22L.24,11.72a.75.75,0,0,1,0-1.06L3.36,7.55a.74.74,0,0,1,1.06,0,.75.75,0,0,1,0,1.06L1.83,11.19l2.59,2.59a.75.75,0,0,1,0,1.06A.74.74,0,0,1,3.89,15.06Z"/>
      <path d="M15,11.94H.77a.75.75,0,1,1,0-1.5H14.21V2.88H4.49a.75.75,0,0,1,0-1.5H15a.75.75,0,0,1,.75.75v9.06A.74.74,0,0,1,15,11.94Z"/>{' '}
    </svgIcon_1.default>);
});
exports.IconReturn = IconReturn;
IconReturn.displayName = 'IconReturn';
//# sourceMappingURL=iconReturn.jsx.map