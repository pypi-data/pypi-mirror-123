Object.defineProperty(exports, "__esModule", { value: true });
exports.IconArrow = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const svgIcon_1 = (0, tslib_1.__importDefault)(require("./svgIcon"));
const IconArrow = React.forwardRef(function IconArrow(_a, ref) {
    var { direction = 'up' } = _a, props = (0, tslib_1.__rest)(_a, ["direction"]);
    return (<svgIcon_1.default {...props} ref={ref} css={direction
            ? direction === 'down'
                ? // Down arrows have a zoom issue with Firefox inside of tables due to rotate.
                    // Since arrows are symmetric, scaling to only flip vertically works to fix the issue.
                    (0, react_1.css) `
                transform: scale(1, -1);
              `
                : (0, react_1.css) `
                transform: rotate(${theme_1.default.iconDirections[direction]}deg);
              `
            : undefined}>
      <path d="M13.76,7.32a.74.74,0,0,1-.53-.22L8,1.87,2.77,7.1A.75.75,0,1,1,1.71,6L7.47.28a.74.74,0,0,1,1.06,0L14.29,6a.75.75,0,0,1,0,1.06A.74.74,0,0,1,13.76,7.32Z"/>
      <path d="M8,15.94a.75.75,0,0,1-.75-.75V.81a.75.75,0,0,1,1.5,0V15.19A.75.75,0,0,1,8,15.94Z"/>
    </svgIcon_1.default>);
});
exports.IconArrow = IconArrow;
IconArrow.displayName = 'IconArrow';
//# sourceMappingURL=iconArrow.jsx.map