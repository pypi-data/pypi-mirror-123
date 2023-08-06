Object.defineProperty(exports, "__esModule", { value: true });
exports.CodeMappingButtonContainer = exports.StacktraceLink = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const modal_1 = require("app/actionCreators/modal");
const prompts_1 = require("app/actionCreators/prompts");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const hovercard_1 = require("app/components/hovercard");
const icons_1 = require("app/icons");
const iconClose_1 = require("app/icons/iconClose");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const openInContextLine_1 = require("./openInContextLine");
const stacktraceLinkModal_1 = (0, tslib_1.__importDefault)(require("./stacktraceLinkModal"));
class StacktraceLink extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmit = () => {
            this.reloadData();
        };
    }
    get project() {
        // we can't use the withProject HoC on an the issue page
        // so we ge around that by using the withProjects HoC
        // and look up the project from the list
        const { projects, event } = this.props;
        return projects.find(project => project.id === event.projectID);
    }
    get match() {
        return this.state.match;
    }
    get config() {
        return this.match.config;
    }
    get integrations() {
        return this.match.integrations;
    }
    get errorText() {
        const error = this.match.error;
        switch (error) {
            case 'stack_root_mismatch':
                return (0, locale_1.t)('Error matching your configuration.');
            case 'file_not_found':
                return (0, locale_1.t)('Source file not found.');
            default:
                return (0, locale_1.t)('There was an error encountered with the code mapping for this project');
        }
    }
    componentDidMount() {
        this.promptsCheck();
    }
    promptsCheck() {
        var _a;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            const prompt = yield (0, prompts_1.promptsCheck)(this.api, {
                organizationId: organization.id,
                projectId: (_a = this.project) === null || _a === void 0 ? void 0 : _a.id,
                feature: 'stacktrace_link',
            });
            this.setState({
                isDismissed: (0, promptIsDismissed_1.promptIsDismissed)(prompt),
                promptLoaded: true,
            });
        });
    }
    dismissPrompt() {
        var _a;
        const { organization } = this.props;
        (0, prompts_1.promptsUpdate)(this.api, {
            organizationId: organization.id,
            projectId: (_a = this.project) === null || _a === void 0 ? void 0 : _a.id,
            feature: 'stacktrace_link',
            status: 'dismissed',
        });
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_link_cta_dismissed', {
            view: 'stacktrace_issue_details',
            organization,
        });
        this.setState({ isDismissed: true });
    }
    getEndpoints() {
        var _a, _b;
        const { organization, frame, event } = this.props;
        const project = this.project;
        if (!project) {
            throw new Error('Unable to find project');
        }
        const commitId = (_b = (_a = event.release) === null || _a === void 0 ? void 0 : _a.lastCommit) === null || _b === void 0 ? void 0 : _b.id;
        const platform = event.platform;
        return [
            [
                'match',
                `/projects/${organization.slug}/${project.slug}/stacktrace-link/`,
                { query: { file: frame.filename, platform, commitId } },
            ],
        ];
    }
    onRequestError(error, args) {
        Sentry.withScope(scope => {
            scope.setExtra('errorInfo', args);
            Sentry.captureException(new Error(error));
        });
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { showModal: false, sourceCodeInput: '', match: { integrations: [] }, isDismissed: false, promptLoaded: false });
    }
    onOpenLink() {
        var _a;
        const provider = (_a = this.config) === null || _a === void 0 ? void 0 : _a.provider;
        if (provider) {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_link_clicked', {
                view: 'stacktrace_issue_details',
                provider: provider.key,
                organization: this.props.organization,
            }, { startSession: true });
        }
    }
    onReconfigureMapping() {
        var _a;
        const provider = (_a = this.config) === null || _a === void 0 ? void 0 : _a.provider;
        const error = this.match.error;
        if (provider) {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.reconfigure_stacktrace_setup', {
                view: 'stacktrace_issue_details',
                provider: provider.key,
                error_reason: error,
                organization: this.props.organization,
            }, { startSession: true });
        }
    }
    // don't show the error boundary if the component fails.
    // capture the endpoint error on onRequestError
    renderError() {
        return null;
    }
    renderLoading() {
        // TODO: Add loading
        return null;
    }
    renderNoMatch() {
        const { organization } = this.props;
        const filename = this.props.frame.filename;
        const platform = this.props.event.platform;
        if (this.project && this.integrations.length > 0 && filename) {
            return (<access_1.default organization={organization} access={['org:integrations']}>
          {({ hasAccess }) => hasAccess && (<exports.CodeMappingButtonContainer columnQuantity={2}>
                {(0, locale_1.tct)('[link:Link your stack trace to your source code.]', {
                        link: (<a onClick={() => {
                                (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.stacktrace_start_setup', {
                                    view: 'stacktrace_issue_details',
                                    platform,
                                    organization,
                                }, { startSession: true });
                                (0, modal_1.openModal)(deps => this.project && (<stacktraceLinkModal_1.default onSubmit={this.handleSubmit} filename={filename} project={this.project} organization={organization} integrations={this.integrations} {...deps}/>));
                            }}/>),
                    })}
                <StyledIconClose size="xs" onClick={() => this.dismissPrompt()}/>
              </exports.CodeMappingButtonContainer>)}
        </access_1.default>);
        }
        return null;
    }
    renderHovercard() {
        const error = this.match.error;
        const url = this.match.attemptedUrl;
        const { frame } = this.props;
        const { config } = this.match;
        return (<React.Fragment>
        <StyledHovercard header={error === 'stack_root_mismatch' ? (<span>{(0, locale_1.t)('Mismatch between filename and stack root')}</span>) : (<span>{(0, locale_1.t)('Unable to find source code url')}</span>)} body={error === 'stack_root_mismatch' ? (<HeaderContainer>
                <HovercardLine>
                  filename: <code>{`${frame.filename}`}</code>
                </HovercardLine>
                <HovercardLine>
                  stack root: <code>{`${config === null || config === void 0 ? void 0 : config.stackRoot}`}</code>
                </HovercardLine>
              </HeaderContainer>) : (<HeaderContainer>
                <HovercardLine>{url}</HovercardLine>
              </HeaderContainer>)}>
          <StyledIconInfo size="xs"/>
        </StyledHovercard>
      </React.Fragment>);
    }
    renderMatchNoUrl() {
        const { config, error } = this.match;
        const { organization } = this.props;
        const url = `/settings/${organization.slug}/integrations/${config === null || config === void 0 ? void 0 : config.provider.key}/${config === null || config === void 0 ? void 0 : config.integrationId}/?tab=codeMappings`;
        return (<exports.CodeMappingButtonContainer columnQuantity={2}>
        <ErrorInformation>
          {error && this.renderHovercard()}
          <ErrorText>{this.errorText}</ErrorText>
          {(0, locale_1.tct)('[link:Configure Stack Trace Linking] to fix this problem.', {
                link: (<a onClick={() => {
                        this.onReconfigureMapping();
                    }} href={url}/>),
            })}
        </ErrorInformation>
      </exports.CodeMappingButtonContainer>);
    }
    renderMatchWithUrl(config, url) {
        url = `${url}#L${this.props.frame.lineNo}`;
        return (<openInContextLine_1.OpenInContainer columnQuantity={2}>
        <div>{(0, locale_1.t)('Open this line in')}</div>
        <openInContextLine_1.OpenInLink onClick={() => this.onOpenLink()} href={url} openInNewTab>
          {(0, integrationUtil_1.getIntegrationIcon)(config.provider.key)}
          <openInContextLine_1.OpenInName>{config.provider.name}</openInContextLine_1.OpenInName>
        </openInContextLine_1.OpenInLink>
      </openInContextLine_1.OpenInContainer>);
    }
    renderBody() {
        const { config, sourceUrl } = this.match || {};
        const { isDismissed, promptLoaded } = this.state;
        if (config && sourceUrl) {
            return this.renderMatchWithUrl(config, sourceUrl);
        }
        if (config) {
            return this.renderMatchNoUrl();
        }
        if (!promptLoaded || (promptLoaded && isDismissed)) {
            return null;
        }
        return this.renderNoMatch();
    }
}
exports.StacktraceLink = StacktraceLink;
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(StacktraceLink));
exports.CodeMappingButtonContainer = (0, styled_1.default)(openInContextLine_1.OpenInContainer) `
  justify-content: space-between;
`;
const StyledIconClose = (0, styled_1.default)(iconClose_1.IconClose) `
  margin: auto;
  cursor: pointer;
`;
const StyledIconInfo = (0, styled_1.default)(icons_1.IconInfo) `
  margin-right: ${(0, space_1.default)(0.5)};
  margin-bottom: -2px;
  cursor: pointer;
  line-height: 0;
`;
const StyledHovercard = (0, styled_1.default)(hovercard_1.Hovercard) `
  font-weight: normal;
  width: inherit;
  line-height: 0;
  ${hovercard_1.Header} {
    font-weight: strong;
    font-size: ${p => p.theme.fontSizeSmall};
    color: ${p => p.theme.subText};
  }
  ${hovercard_1.Body} {
    font-weight: normal;
    font-size: ${p => p.theme.fontSizeSmall};
  }
`;
const HeaderContainer = (0, styled_1.default)('div') `
  width: 100%;
  display: flex;
  justify-content: space-between;
`;
const HovercardLine = (0, styled_1.default)('div') `
  padding-bottom: 3px;
`;
const ErrorInformation = (0, styled_1.default)('div') `
  padding-right: 5px;
  margin-right: ${(0, space_1.default)(1)};
`;
const ErrorText = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=stacktraceLink.jsx.map