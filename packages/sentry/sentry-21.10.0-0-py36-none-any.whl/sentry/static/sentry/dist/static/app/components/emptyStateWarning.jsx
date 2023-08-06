Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const EmptyStateWarning = ({ small = false, withIcon = true, children, className, }) => small ? (<emptyMessage_1.default className={className}>
      <SmallMessage>
        {withIcon && <StyledIconSearch color="gray300" size="lg"/>}
        {children}
      </SmallMessage>
    </emptyMessage_1.default>) : (<EmptyStreamWrapper data-test-id="empty-state" className={className}>
      {withIcon && <icons_1.IconSearch size="54px"/>}
      {children}
    </EmptyStreamWrapper>);
const EmptyStreamWrapper = (0, styled_1.default)('div') `
  text-align: center;
  font-size: 22px;
  padding: 48px ${(0, space_1.default)(1)};

  p {
    line-height: 1.2;
    margin: 0 auto 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }

  svg {
    fill: ${p => p.theme.gray200};
    margin-bottom: ${(0, space_1.default)(2)};
  }
`;
const SmallMessage = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeExtraLarge};
  line-height: 1em;
`;
const StyledIconSearch = (0, styled_1.default)(icons_1.IconSearch) `
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = EmptyStateWarning;
//# sourceMappingURL=emptyStateWarning.jsx.map