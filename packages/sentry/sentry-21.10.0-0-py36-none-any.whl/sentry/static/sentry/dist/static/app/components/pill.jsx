Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Pill = React.memo(({ name, value, children, type, className }) => {
    const getTypeAndValue = () => {
        if (value === undefined) {
            return {};
        }
        switch (value) {
            case 'true':
            case true:
                return {
                    valueType: 'positive',
                    renderValue: 'true',
                };
            case 'false':
            case false:
                return {
                    valueType: 'negative',
                    renderValue: 'false',
                };
            case null:
            case undefined:
                return {
                    valueType: 'error',
                    renderValue: 'n/a',
                };
            default:
                return {
                    valueType: undefined,
                    renderValue: String(value),
                };
        }
    };
    const { valueType, renderValue } = getTypeAndValue();
    return (<StyledPill type={type !== null && type !== void 0 ? type : valueType} className={className}>
      <PillName>{name}</PillName>
      <PillValue>{children !== null && children !== void 0 ? children : renderValue}</PillValue>
    </StyledPill>);
});
const getPillStyle = ({ type, theme }) => {
    switch (type) {
        case 'error':
            return `
        color: ${theme.black};
        background: ${theme.red100};
        background: ${theme.red100};
        border: 1px solid ${theme.red300};
      `;
        default:
            return `
        border: 1px solid ${theme.border};
      `;
    }
};
const getPillValueStyle = ({ type, theme }) => {
    switch (type) {
        case 'positive':
            return `
        color: ${theme.black};
        background: ${theme.green100};
        border: 1px solid ${theme.green300};
        border-left-color: ${theme.green300};
        font-family: ${theme.text.familyMono};
        margin: -1px;
      `;
        case 'error':
            return `
        color: ${theme.black};
        border-left-color: ${theme.red300};
        background: ${theme.red100};
        border: 1px solid ${theme.red300};
        margin: -1px;
      `;
        case 'negative':
            return `
        color: ${theme.black};
        border-left-color: ${theme.red300};
        background: ${theme.red100};
        border: 1px solid ${theme.red300};
        font-family: ${theme.text.familyMono};
        margin: -1px;
      `;
        default:
            return `
        background: ${theme.backgroundSecondary};
        font-family: ${theme.text.familyMono};
      `;
    }
};
const PillName = (0, styled_1.default)('span') `
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
  min-width: 0;
  white-space: nowrap;
  display: flex;
  align-items: center;
`;
const PillValue = (0, styled_1.default)(PillName) `
  border-left: 1px solid ${p => p.theme.border};
  border-radius: ${p => `0 ${p.theme.button.borderRadius} ${p.theme.button.borderRadius} 0`};
  max-width: 100%;
  display: flex;
  align-items: center;

  > a {
    max-width: 100%;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    display: inline-block;
    vertical-align: text-bottom;
  }

  .pill-icon,
  .external-icon {
    display: inline;
    margin: 0 0 0 ${(0, space_1.default)(1)};
    color: ${p => p.theme.gray300};
    &:hover {
      color: ${p => p.theme.textColor};
    }
  }
`;
const StyledPill = (0, styled_1.default)('li') `
  white-space: nowrap;
  margin: 0 ${(0, space_1.default)(1)} ${(0, space_1.default)(1)} 0;
  display: flex;
  border-radius: ${p => p.theme.button.borderRadius};
  box-shadow: ${p => p.theme.dropShadowLightest};
  line-height: 1.2;
  max-width: 100%;
  :last-child {
    margin-right: 0;
  }

  ${getPillStyle};

  ${PillValue} {
    ${getPillValueStyle};
  }
`;
exports.default = Pill;
//# sourceMappingURL=pill.jsx.map