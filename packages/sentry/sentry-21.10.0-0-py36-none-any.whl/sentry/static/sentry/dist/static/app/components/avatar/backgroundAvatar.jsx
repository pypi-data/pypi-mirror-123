Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/avatar/styles");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
/**
 * Creates an avatar placeholder that is used when showing multiple
 * suggested assignees
 */
const BackgroundAvatar = (0, styled_1.default)((_a) => {
    var { round: _round, forwardedRef } = _a, props = (0, tslib_1.__rest)(_a, ["round", "forwardedRef"]);
    return (<svg ref={forwardedRef} viewBox="0 0 120 120" {...props}>
      <rect x="0" y="0" width="120" height="120" rx="15" ry="15" fill={theme_1.default.purple100}/>
    </svg>);
}) `
  ${styles_1.imageStyle};
`;
BackgroundAvatar.defaultProps = {
    round: false,
    suggested: true,
};
exports.default = React.forwardRef((props, ref) => (<BackgroundAvatar forwardedRef={ref} {...props}/>));
//# sourceMappingURL=backgroundAvatar.jsx.map