Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const addIntegration_1 = (0, tslib_1.__importDefault)(require("./addIntegration"));
class AddIntegrationButton extends React.Component {
    render() {
        const _a = this.props, { provider, buttonText, onAddIntegration, organization, reinstall, analyticsParams, modalParams } = _a, buttonProps = (0, tslib_1.__rest)(_a, ["provider", "buttonText", "onAddIntegration", "organization", "reinstall", "analyticsParams", "modalParams"]);
        const label = buttonText || (0, locale_1.t)(reinstall ? 'Enable' : 'Add %s', provider.metadata.noun);
        return (<tooltip_1.default disabled={provider.canAdd} title={`Integration cannot be added on Sentry. Enable this integration via the ${provider.name} instance.`}>
        <addIntegration_1.default provider={provider} onInstall={onAddIntegration} organization={organization} analyticsParams={analyticsParams} modalParams={modalParams}>
          {onClick => (<button_1.default disabled={!provider.canAdd} {...buttonProps} onClick={() => onClick()}>
              {label}
            </button_1.default>)}
        </addIntegration_1.default>
      </tooltip_1.default>);
    }
}
exports.default = AddIntegrationButton;
//# sourceMappingURL=addIntegrationButton.jsx.map