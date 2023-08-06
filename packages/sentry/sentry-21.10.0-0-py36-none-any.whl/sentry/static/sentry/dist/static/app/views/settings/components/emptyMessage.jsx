Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const EmptyMessage = (0, styled_1.default)((_a) => {
    var { title, description, icon, children, action, leftAligned: _leftAligned } = _a, props = (0, tslib_1.__rest)(_a, ["title", "description", "icon", "children", "action", "leftAligned"]);
    return (<div data-test-id="empty-message" {...props}>
      {icon && <IconWrapper>{icon}</IconWrapper>}
      {title && <Title noMargin={!description && !children && !action}>{title}</Title>}
      {description && <Description>{description}</Description>}
      {children && <Description noMargin>{children}</Description>}
      {action && <Action>{action}</Action>}
    </div>);
}) `
  display: flex;
  ${p => p.leftAligned
    ? (0, react_1.css) `
          max-width: 70%;
          align-items: flex-start;
          padding: ${(0, space_1.default)(4)};
        `
    : (0, react_1.css) `
          text-align: center;
          align-items: center;
          padding: ${(0, space_1.default)(4)} 15%;
        `};
  flex-direction: column;
  color: ${p => p.theme.textColor};
  font-size: ${p => p.size && p.size === 'large' ? p.theme.fontSizeExtraLarge : p.theme.fontSizeLarge};
`;
const IconWrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const Title = (0, styled_1.default)('strong') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  ${p => !p.noMargin && `margin-bottom: ${(0, space_1.default)(1)};`}
`;
const Description = (0, styled_1.default)(textBlock_1.default) `
  margin: 0;
`;
const Action = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(2)};
`;
exports.default = EmptyMessage;
//# sourceMappingURL=emptyMessage.jsx.map