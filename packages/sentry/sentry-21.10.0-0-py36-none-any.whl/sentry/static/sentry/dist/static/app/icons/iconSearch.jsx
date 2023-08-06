Object.defineProperty(exports, "__esModule", { value: true });
exports.IconSearch = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconSearch = React.forwardRef(function IconSearch(props, ref) {
    return (<svgIcon_1.default {...props} ref={ref}>
      <path d="M6,12A6,6,0,1,1,12,6,6,6,0,0,1,6,12ZM6,1.54A4.46,4.46,0,1,0,10.45,6,4.46,4.46,0,0,0,6,1.54Z"/>
      <path d="M15.2,16a.74.74,0,0,1-.53-.22L9.14,10.2A.75.75,0,0,1,10.2,9.14l5.53,5.53a.75.75,0,0,1,0,1.06A.74.74,0,0,1,15.2,16Z"/>
    </svgIcon_1.default>);
});
exports.IconSearch = IconSearch;
IconSearch.displayName = 'IconSearch';
//# sourceMappingURL=iconSearch.jsx.map