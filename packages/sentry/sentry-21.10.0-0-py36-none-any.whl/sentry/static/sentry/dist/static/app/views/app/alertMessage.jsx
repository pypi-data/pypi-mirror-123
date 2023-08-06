Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const AlertMessage = ({ alert, system }) => {
    var _a;
    const handleClose = () => alertActions_1.default.closeAlert(alert);
    const { url, message, type } = alert;
    const icon = type === 'success' ? (<icons_1.IconCheckmark size="md" isCircled/>) : (<icons_1.IconWarning size="md"/>);
    return (<StyledAlert type={type} icon={icon} system={system}>
      <StyledMessage>
        {url ? <externalLink_1.default href={url}>{message}</externalLink_1.default> : message}
      </StyledMessage>
      <StyledCloseButton icon={<icons_1.IconClose size="md" isCircled/>} aria-label={(0, locale_1.t)('Close')} onClick={(_a = alert.onClose) !== null && _a !== void 0 ? _a : handleClose} size="zero" borderless/>
    </StyledAlert>);
};
exports.default = AlertMessage;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  margin: 0;
`;
const StyledMessage = (0, styled_1.default)('span') `
  display: block;
  margin: auto ${(0, space_1.default)(4)} auto 0;
`;
const StyledCloseButton = (0, styled_1.default)(button_1.default) `
  background-color: transparent;
  opacity: 0.4;
  transition: opacity 0.1s linear;
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);

  &:hover,
  &:focus {
    background-color: transparent;
    opacity: 1;
  }
`;
//# sourceMappingURL=alertMessage.jsx.map