Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const feedbackAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/feedbackAlert"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
class StacktraceLinkModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            sourceCodeInput: '',
        };
        this.handleSubmit = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            const { sourceCodeInput } = this.state;
            const { api, closeModal, filename, onSubmit, organization, project } = this.props;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_submit_config', {
                setup_type: 'automatic',
                view: 'stacktrace_issue_details',
                organization,
            });
            const parsingEndpoint = `/projects/${organization.slug}/${project.slug}/repo-path-parsing/`;
            try {
                const configData = yield api.requestPromise(parsingEndpoint, {
                    method: 'POST',
                    data: {
                        sourceUrl: sourceCodeInput,
                        stackPath: filename,
                    },
                });
                const configEndpoint = `/organizations/${organization.slug}/code-mappings/`;
                yield api.requestPromise(configEndpoint, {
                    method: 'POST',
                    data: Object.assign(Object.assign({}, configData), { projectId: project.id, integrationId: configData.integrationId }),
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Stack trace configuration saved.'));
                (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_complete_setup', {
                    setup_type: 'automatic',
                    provider: (_a = configData.config) === null || _a === void 0 ? void 0 : _a.provider.key,
                    view: 'stacktrace_issue_details',
                    organization,
                });
                closeModal();
                onSubmit();
            }
            catch (err) {
                const errors = (err === null || err === void 0 ? void 0 : err.responseJSON)
                    ? Array.isArray(err === null || err === void 0 ? void 0 : err.responseJSON)
                        ? err === null || err === void 0 ? void 0 : err.responseJSON
                        : Object.values(err === null || err === void 0 ? void 0 : err.responseJSON)
                    : [];
                const apiErrors = errors.length > 0 ? `: ${errors.join(', ')}` : '';
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Something went wrong%s', apiErrors));
            }
        });
    }
    onHandleChange(sourceCodeInput) {
        this.setState({
            sourceCodeInput,
        });
    }
    onManualSetup(provider) {
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_manual_option_clicked', {
            view: 'stacktrace_issue_details',
            setup_type: 'manual',
            provider,
            organization: this.props.organization,
        });
    }
    render() {
        const { sourceCodeInput } = this.state;
        const { Header, Body, filename, integrations, organization } = this.props;
        const baseUrl = `/settings/${organization.slug}/integrations`;
        return (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Link Stack Trace To Source Code')}</Header>
        <Body>
          <ModalContainer>
            <div>
              <h6>{(0, locale_1.t)('Automatic Setup')}</h6>
              {(0, locale_1.tct)('Enter the source code URL corresponding to stack trace filename [filename] so we can automatically set up stack trace linking for this project.', {
                filename: <code>{filename}</code>,
            })}
            </div>
            <SourceCodeInput>
              <StyledInputField inline={false} flexibleControlStateSize stacked name="source-code-input" type="text" value={sourceCodeInput} onChange={val => this.onHandleChange(val)} placeholder={(0, locale_1.t)(`https://github.com/helloworld/Hello-World/blob/master/${filename}`)}/>
              <buttonBar_1.default>
                <button_1.default data-test-id="quick-setup-button" type="button" onClick={() => this.handleSubmit()}>
                  {(0, locale_1.t)('Submit')}
                </button_1.default>
              </buttonBar_1.default>
            </SourceCodeInput>
            <div>
              <h6>{(0, locale_1.t)('Manual Setup')}</h6>
              <alert_1.default type="warning">
                {(0, locale_1.t)('We recommend this for more complicated configurations, like projects with multiple repositories.')}
              </alert_1.default>
              {(0, locale_1.t)("To manually configure stack trace linking, select the integration you'd like to use for mapping:")}
            </div>
            <ManualSetup>
              {integrations.map(integration => (<button_1.default key={integration.id} type="button" onClick={() => this.onManualSetup(integration.provider.key)} to={`${baseUrl}/${integration.provider.key}/${integration.id}/?tab=codeMappings&referrer=stacktrace-issue-details`}>
                  {(0, integrationUtil_1.getIntegrationIcon)(integration.provider.key)}
                  <IntegrationName>{integration.name}</IntegrationName>
                </button_1.default>))}
            </ManualSetup>
            <StyledFeedbackAlert />
          </ModalContainer>
        </Body>
      </react_1.Fragment>);
    }
}
const SourceCodeInput = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 5fr 1fr;
  grid-gap: ${(0, space_1.default)(1)};
`;
const ManualSetup = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  justify-items: center;
`;
const ModalContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};

  code {
    word-break: break-word;
  }
`;
const StyledFeedbackAlert = (0, styled_1.default)(feedbackAlert_1.default) `
  margin-bottom: 0;
`;
const StyledInputField = (0, styled_1.default)(inputField_1.default) `
  padding: 0px;
`;
const IntegrationName = (0, styled_1.default)('p') `
  padding-left: 10px;
`;
exports.default = (0, withApi_1.default)(StacktraceLinkModal);
//# sourceMappingURL=stacktraceLinkModal.jsx.map