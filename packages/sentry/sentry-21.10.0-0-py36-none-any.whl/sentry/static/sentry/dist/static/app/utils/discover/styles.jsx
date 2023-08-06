Object.defineProperty(exports, "__esModule", { value: true });
exports.UserIcon = exports.FlexContainer = exports.BarContainer = exports.FieldShortId = exports.OverflowLink = exports.FieldDateTime = exports.NumberContainer = exports.VersionContainer = exports.Container = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const shortId_1 = (0, tslib_1.__importDefault)(require("app/components/shortId"));
const iconUser_1 = require("app/icons/iconUser");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
// Styled components used to render discover result sets.
exports.Container = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
`;
exports.VersionContainer = (0, styled_1.default)('div') `
  display: flex;
`;
exports.NumberContainer = (0, styled_1.default)('div') `
  text-align: right;
  font-variant-numeric: tabular-nums;
  ${overflowEllipsis_1.default};
`;
exports.FieldDateTime = (0, styled_1.default)(dateTime_1.default) `
  color: ${p => p.theme.gray300};
  font-variant-numeric: tabular-nums;
  ${overflowEllipsis_1.default};
`;
exports.OverflowLink = (0, styled_1.default)(link_1.default) `
  ${overflowEllipsis_1.default};
`;
exports.FieldShortId = (0, styled_1.default)(shortId_1.default) `
  justify-content: flex-start;
`;
exports.BarContainer = (0, styled_1.default)('div') `
  max-width: 80px;
  margin-left: auto;
`;
exports.FlexContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
exports.UserIcon = (0, styled_1.default)(iconUser_1.IconUser) `
  margin-left: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray400};
`;
//# sourceMappingURL=styles.jsx.map