Object.defineProperty(exports, "__esModule", { value: true });
exports.CauseHeader = exports.BannerSummary = exports.BannerContainer = exports.DataSection = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.DataSection = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  padding: ${(0, space_1.default)(2)} 0;
  border-top: 1px solid ${p => p.theme.innerBorder};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)} 0 40px;
  }
`;
function getColors({ priority, theme }) {
    const COLORS = {
        default: {
            background: theme.backgroundSecondary,
            border: theme.border,
        },
        danger: {
            background: theme.alert.error.backgroundLight,
            border: theme.alert.error.border,
        },
        success: {
            background: theme.alert.success.backgroundLight,
            border: theme.alert.success.border,
        },
    };
    return COLORS[priority];
}
exports.BannerContainer = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};

  background: ${p => getColors(p).background};
  border-top: 1px solid ${p => getColors(p).border};
  border-bottom: 1px solid ${p => getColors(p).border};

  /* Muted box & processing errors are in different parts of the DOM */
  &
    + ${ /* sc-selector */exports.DataSection}:first-child,
    &
    + div
    > ${ /* sc-selector */exports.DataSection}:first-child {
    border-top: 0;
  }
`;
exports.BannerSummary = (0, styled_1.default)('p') `
  display: flex;
  align-items: flex-start;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} ${(0, space_1.default)(2)} 40px;
  margin-bottom: 0;

  /* Get icons in top right of content box */
  & > .icon,
  & > svg {
    flex-shrink: 0;
    flex-grow: 0;
    margin-right: ${(0, space_1.default)(1)};
    margin-top: 2px;
  }

  & > span {
    flex-grow: 1;
  }

  & > a {
    align-self: flex-end;
  }
`;
exports.CauseHeader = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(3)};

  & button,
  & h3 {
    color: ${p => p.theme.gray300};
    font-size: 14px;
    font-weight: 600;
    line-height: 1.2;
    text-transform: uppercase;
  }

  & h3 {
    margin-bottom: 0;
  }

  & button {
    background: none;
    border: 0;
    outline: none;
    padding: 0;
  }
`;
//# sourceMappingURL=styles.jsx.map