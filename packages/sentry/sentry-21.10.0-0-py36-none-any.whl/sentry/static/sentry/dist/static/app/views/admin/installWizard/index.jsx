Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sentry_pattern_png_1 = (0, tslib_1.__importDefault)(require("sentry-images/pattern/sentry-pattern.png"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const forms_1 = require("app/components/forms");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const options_1 = require("../options");
class InstallWizard extends asyncView_1.default {
    getEndpoints() {
        return [['data', '/internal/options/?query=is:required']];
    }
    renderFormFields() {
        const options = this.state.data;
        let missingOptions = new Set(Object.keys(options).filter(option => !options[option].field.isSet));
        // This is to handle the initial installation case.
        // Even if all options are filled out, we want to prompt to confirm
        // them. This is a bit of a hack because we're assuming that
        // the backend only spit back all filled out options for
        // this case.
        if (missingOptions.size === 0) {
            missingOptions = new Set(Object.keys(options));
        }
        // A mapping of option name to Field object
        const fields = {};
        for (const key of missingOptions) {
            const option = options[key];
            if (option.field.disabled) {
                continue;
            }
            fields[key] = (0, options_1.getOptionField)(key, option.field);
        }
        return (0, options_1.getForm)(fields);
    }
    getInitialData() {
        const options = this.state.data;
        const data = {};
        Object.keys(options).forEach(optionName => {
            const option = options[optionName];
            if (option.field.disabled) {
                return;
            }
            // TODO(dcramer): we need to rethink this logic as doing multiple "is this value actually set"
            // is problematic
            // all values to their server-defaults (as client-side defaults don't really work)
            const displayValue = option.value || (0, options_1.getOptionDefault)(optionName);
            if (
            // XXX(dcramer): we need the user to explicitly choose beacon.anonymous
            // vs using an implied default so effectively this is binding
            optionName !== 'beacon.anonymous' &&
                // XXX(byk): if we don't have a set value but have a default value filled
                // instead, from the client, set it on the data so it is sent to the server
                !option.field.isSet &&
                displayValue !== undefined) {
                data[optionName] = displayValue;
            }
        });
        return data;
    }
    getTitle() {
        return (0, locale_1.t)('Setup Sentry');
    }
    render() {
        const version = configStore_1.default.get('version');
        return (<react_document_title_1.default title={this.getTitle()}>
        <Wrapper>
          <Pattern />
          <SetupWizard>
            <Heading>
              <span>{(0, locale_1.t)('Welcome to Sentry')}</span>
              <Version>{version.current}</Version>
            </Heading>
            {this.state.loading
                ? this.renderLoading()
                : this.state.error
                    ? this.renderError()
                    : this.renderBody()}
          </SetupWizard>
        </Wrapper>
      </react_document_title_1.default>);
    }
    renderError() {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {(0, locale_1.t)('We were unable to load the required configuration from the Sentry server. Please take a look at the service logs.')}
      </alert_1.default>);
    }
    renderBody() {
        return (<forms_1.ApiForm apiMethod="PUT" apiEndpoint={this.getEndpoints()[0][1]} submitLabel={(0, locale_1.t)('Continue')} initialData={this.getInitialData()} onSubmitSuccess={this.props.onConfigured}>
        <p>{(0, locale_1.t)('Complete setup by filling out the required configuration.')}</p>

        {this.renderFormFields()}
      </forms_1.ApiForm>);
    }
}
exports.default = InstallWizard;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
`;
const fixedStyle = (0, react_1.css) `
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
`;
const Pattern = (0, styled_1.default)('div') `
  &::before {
    ${fixedStyle}
    content: '';
    background-image: linear-gradient(
      to right,
      ${p => p.theme.purple200} 0%,
      ${p => p.theme.purple300} 100%
    );
    background-repeat: repeat-y;
  }

  &::after {
    ${fixedStyle}
    content: '';
    background: url(${sentry_pattern_png_1.default});
    background-size: 400px;
    opacity: 0.8;
  }
`;
const Heading = (0, styled_1.default)('h1') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  justify-content: space-between;
  grid-auto-flow: column;
  line-height: 36px;
`;
const Version = (0, styled_1.default)('small') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  line-height: inherit;
`;
const SetupWizard = (0, styled_1.default)('div') `
  background: ${p => p.theme.background};
  border-radius: ${p => p.theme.borderRadius};
  box-shadow: ${p => p.theme.dropShadowHeavy};
  margin-top: 40px;
  padding: 40px 40px 20px;
  width: 600px;
  z-index: ${p => p.theme.zIndex.initial};
`;
//# sourceMappingURL=index.jsx.map