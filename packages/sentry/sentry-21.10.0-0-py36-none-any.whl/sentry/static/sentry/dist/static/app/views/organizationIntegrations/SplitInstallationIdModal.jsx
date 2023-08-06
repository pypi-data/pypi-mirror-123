Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
/**
 * This component is a hack for Split.
 * It will display the installation ID after installation so users can copy it and paste it in Split's website.
 * We also have a link for users to click so they can go to Split's website.
 */
class SplitInstallationIdModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.onCopy = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () { 
        // This hack is needed because the normal copying methods with TextCopyInput do not work correctly
        return yield navigator.clipboard.writeText(this.props.installationId); });
        this.handleContinue = () => {
            const delay = 2000;
            this.onCopy();
            (0, indicator_1.addSuccessMessage)('Copied to clipboard');
            setTimeout(() => {
                window.open('https://app.split.io/org/admin/integrations');
            }, delay);
        };
    }
    render() {
        const { installationId, closeModal } = this.props;
        // no need to translate this temporary component
        return (<div>
        <ItemHolder>
          Copy this Installation ID and click to continue. You will use it to finish setup
          on Split.io.
        </ItemHolder>
        <ItemHolder>
          <textCopyInput_1.default onCopy={this.onCopy}>{installationId}</textCopyInput_1.default>
        </ItemHolder>
        <ButtonHolder>
          <button_1.default size="small" onClick={closeModal}>
            Close
          </button_1.default>
          <button_1.default size="small" priority="primary" onClick={this.handleContinue}>
            Copy and Open Link
          </button_1.default>
        </ButtonHolder>
      </div>);
    }
}
exports.default = SplitInstallationIdModal;
const ItemHolder = (0, styled_1.default)('div') `
  margin: 10px;
`;
const ButtonHolder = (0, styled_1.default)(ItemHolder) `
  text-align: right;
  & button {
    margin: 5px;
  }
`;
//# sourceMappingURL=SplitInstallationIdModal.jsx.map