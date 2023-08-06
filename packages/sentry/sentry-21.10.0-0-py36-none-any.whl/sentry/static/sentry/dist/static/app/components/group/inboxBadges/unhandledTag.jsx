Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const UnhandledTag = () => (<tooltip_1.default title={(0, locale_1.t)('An unhandled error was detected in this Issue.')}>
    <UnhandledTagWrapper>
      <StyledIconFire size="xs" color="red300"/>
      {(0, locale_1.t)('Unhandled')}
    </UnhandledTagWrapper>
  </tooltip_1.default>);
exports.default = UnhandledTag;
const UnhandledTagWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  white-space: nowrap;
  color: ${p => p.theme.red300};
`;
const StyledIconFire = (0, styled_1.default)(icons_1.IconFire) `
  margin-right: 3px;
`;
//# sourceMappingURL=unhandledTag.jsx.map