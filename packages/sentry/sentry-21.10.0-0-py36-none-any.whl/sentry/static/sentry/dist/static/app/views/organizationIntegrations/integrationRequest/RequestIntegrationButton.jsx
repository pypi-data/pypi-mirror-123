Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const RequestIntegrationModal_1 = (0, tslib_1.__importDefault)(require("./RequestIntegrationModal"));
class RequestIntegrationButton extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false,
            isSent: false,
        };
    }
    openRequestModal() {
        this.setState({ isOpen: true });
        (0, modal_1.openModal)(renderProps => (<RequestIntegrationModal_1.default {...this.props} {...renderProps} onSuccess={() => this.setState({ isSent: true })}/>), {
            onClose: () => this.setState({ isOpen: false }),
        });
    }
    render() {
        const { isOpen, isSent } = this.state;
        let buttonText;
        if (isOpen) {
            buttonText = (0, locale_1.t)('Requesting Installation');
        }
        else if (isSent) {
            buttonText = (0, locale_1.t)('Installation Requested');
        }
        else {
            buttonText = (0, locale_1.t)('Request Installation');
        }
        return (<StyledRequestIntegrationButton data-test-id="request-integration-button" disabled={isOpen || isSent} onClick={() => this.openRequestModal()} priority="primary" size="small">
        {buttonText}
      </StyledRequestIntegrationButton>);
    }
}
exports.default = RequestIntegrationButton;
const StyledRequestIntegrationButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=RequestIntegrationButton.jsx.map