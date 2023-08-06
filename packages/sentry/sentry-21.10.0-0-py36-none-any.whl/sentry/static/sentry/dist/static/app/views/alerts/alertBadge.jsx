Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("./types");
function AlertBadge({ status, hideText = false, isIssue }) {
    let statusText = (0, locale_1.t)('Resolved');
    let Icon = icons_1.IconCheckmark;
    let color = 'green300';
    if (isIssue) {
        statusText = (0, locale_1.t)('Issue');
        Icon = icons_1.IconIssues;
        color = 'gray300';
    }
    else if (status === types_1.IncidentStatus.CRITICAL) {
        statusText = (0, locale_1.t)('Critical');
        Icon = icons_1.IconFire;
        color = 'red300';
    }
    else if (status === types_1.IncidentStatus.WARNING) {
        statusText = (0, locale_1.t)('Warning');
        Icon = icons_1.IconWarning;
        color = 'yellow300';
    }
    return (<Wrapper displayFlex={!hideText}>
      <AlertIconWrapper color={color} icon={Icon}>
        <Icon color="white"/>
      </AlertIconWrapper>

      {!hideText && <IncidentStatusValue color={color}>{statusText}</IncidentStatusValue>}
    </Wrapper>);
}
exports.default = AlertBadge;
const Wrapper = (0, styled_1.default)('div') `
  display: ${p => (p.displayFlex ? `flex` : `block`)};
  align-items: center;
`;
const AlertIconWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  /* icon warning needs to be treated differently to look visually centered */
  line-height: ${p => (p.icon === icons_1.IconWarning ? undefined : 1)};
  left: 3px;
  min-width: 30px;

  &:before {
    content: '';
    position: absolute;
    width: 22px;
    height: 22px;
    border-radius: ${p => p.theme.borderRadius};
    background-color: ${p => p.theme[p.color]};
    transform: rotate(45deg);
  }

  svg {
    width: ${p => (p.icon === icons_1.IconIssues ? '11px' : '13px')};
    z-index: 1;
  }
`;
const IncidentStatusValue = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
  color: ${p => p.theme[p.color]};
`;
//# sourceMappingURL=alertBadge.jsx.map