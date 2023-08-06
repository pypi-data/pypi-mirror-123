Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BadgeDisplayName = (0, styled_1.default)('span') `
  ${p => p.hideOverflow &&
    `
      ${overflowEllipsis_1.default};
      max-width: ${typeof p.hideOverflow === 'string'
        ? p.hideOverflow
        : p.theme.settings.maxCrumbWidth}
  `};
  padding: ${(0, space_1.default)(0.25)} 0;
`;
exports.default = BadgeDisplayName;
//# sourceMappingURL=badgeDisplayName.jsx.map