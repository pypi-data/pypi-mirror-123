Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const selectText_1 = require("app/utils/selectText");
const installText = (features, featureName) => `# ${(0, locale_1.t)('Enables the %s feature', featureName)}\n${features
    .map(f => `SENTRY_FEATURES['${f}'] = True`)
    .join('\n')}`;
/**
 * DisabledInfo renders a component informing that a feature has been disabled.
 *
 * By default this component will render a help button which toggles more
 * information about why the feature is disabled, showing the missing feature
 * flag and linking to documentation for managing sentry server feature flags.
 */
class FeatureDisabled extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showHelp: false,
        };
        this.toggleHelp = (e) => {
            e.preventDefault();
            this.setState(state => ({ showHelp: !state.showHelp }));
        };
    }
    renderFeatureDisabled() {
        const { showHelp } = this.state;
        const { message, features, featureName, hideHelpToggle } = this.props;
        const showDescription = hideHelpToggle || showHelp;
        return (<React.Fragment>
        <FeatureDisabledMessage>
          {message}
          {!hideHelpToggle && (<HelpButton icon={showHelp ? (<icons_1.IconChevron direction="down" size="xs"/>) : (<icons_1.IconInfo size="xs"/>)} priority="link" size="xsmall" onClick={this.toggleHelp}>
              {(0, locale_1.t)('Help')}
            </HelpButton>)}
        </FeatureDisabledMessage>
        {showDescription && (<HelpDescription onClick={e => {
                    e.stopPropagation();
                    e.preventDefault();
                }}>
            <p>
              {(0, locale_1.tct)(`Enable this feature on your sentry installation by adding the
              following configuration into your [configFile:sentry.conf.py].
              See [configLink:the configuration documentation] for more
              details.`, {
                    configFile: <code />,
                    configLink: <externalLink_1.default href={constants_1.CONFIG_DOCS_URL}/>,
                })}
            </p>
            <clipboard_1.default hideUnsupported value={installText(features, featureName)}>
              <button_1.default borderless size="xsmall" onClick={e => {
                    e.stopPropagation();
                    e.preventDefault();
                }} icon={<icons_1.IconCopy size="xs"/>}>
                {(0, locale_1.t)('Copy to Clipboard')}
              </button_1.default>
            </clipboard_1.default>
            <pre onClick={e => (0, selectText_1.selectText)(e.target)}>
              <code>{installText(features, featureName)}</code>
            </pre>
          </HelpDescription>)}
      </React.Fragment>);
    }
    render() {
        const { alert } = this.props;
        if (!alert) {
            return this.renderFeatureDisabled();
        }
        const AlertComponent = typeof alert === 'boolean' ? alert_1.default : alert;
        return (<AlertComponent type="warning" icon={<icons_1.IconLock size="xs"/>}>
        <AlertWrapper>{this.renderFeatureDisabled()}</AlertWrapper>
      </AlertComponent>);
    }
}
FeatureDisabled.defaultProps = {
    message: (0, locale_1.t)('This feature is not enabled on your Sentry installation.'),
};
const FeatureDisabledMessage = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
const HelpButton = (0, styled_1.default)(button_1.default) `
  font-size: 0.8em;
`;
const HelpDescription = (0, styled_1.default)('div') `
  font-size: 0.9em;
  margin-top: ${(0, space_1.default)(1)};

  p {
    line-height: 1.5em;
  }

  pre,
  code {
    margin-bottom: 0;
    white-space: pre;
  }
`;
const AlertWrapper = (0, styled_1.default)('div') `
  ${HelpButton} {
    color: #6d6319;
    &:hover {
      color: #88750b;
    }
  }

  pre,
  code {
    background: #fbf7e0;
  }
`;
exports.default = FeatureDisabled;
//# sourceMappingURL=featureDisabled.jsx.map