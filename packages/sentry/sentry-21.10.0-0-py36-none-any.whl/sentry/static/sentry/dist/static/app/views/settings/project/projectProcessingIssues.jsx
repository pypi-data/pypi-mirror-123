Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectProcessingIssues = exports.projectProcessingIssuesMessages = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const processingIssues_1 = (0, tslib_1.__importDefault)(require("app/data/forms/processingIssues"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
exports.projectProcessingIssuesMessages = {
    native_no_crashed_thread: (0, locale_1.t)('No crashed thread found in crash report'),
    native_internal_failure: (0, locale_1.t)('Internal failure when attempting to symbolicate: {error}'),
    native_bad_dsym: (0, locale_1.t)('The debug information file used was broken.'),
    native_missing_optionally_bundled_dsym: (0, locale_1.t)('An optional debug information file was missing.'),
    native_missing_dsym: (0, locale_1.t)('A required debug information file was missing.'),
    native_missing_system_dsym: (0, locale_1.t)('A system debug information file was missing.'),
    native_missing_symbol: (0, locale_1.t)('Could not resolve one or more frames in debug information file.'),
    native_simulator_frame: (0, locale_1.t)('Encountered an unprocessable simulator frame.'),
    native_unknown_image: (0, locale_1.t)('A binary image is referenced that is unknown.'),
    proguard_missing_mapping: (0, locale_1.t)('A proguard mapping file was missing.'),
    proguard_missing_lineno: (0, locale_1.t)('A proguard mapping file does not contain line info.'),
};
const HELP_LINKS = {
    native_missing_dsym: 'https://docs.sentry.io/platforms/apple/dsym/',
    native_bad_dsym: 'https://docs.sentry.io/platforms/apple/dsym/',
    native_missing_system_dsym: 'https://develop.sentry.dev/self-hosted/',
    native_missing_symbol: 'https://develop.sentry.dev/self-hosted/',
};
class ProjectProcessingIssues extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            formData: {},
            loading: true,
            reprocessing: false,
            expected: 0,
            error: false,
            processingIssues: null,
            pageLinks: null,
        };
        this.fetchData = () => {
            const { orgId, projectId } = this.props.params;
            this.setState({
                expected: this.state.expected + 2,
            });
            this.props.api.request(`/projects/${orgId}/${projectId}/`, {
                success: data => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        loading: expected > 0,
                        formData: data.options,
                    });
                },
                error: () => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
            this.props.api.request(`/projects/${orgId}/${projectId}/processingissues/?detailed=1`, {
                success: (data, _, resp) => {
                    var _a;
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: false,
                        loading: expected > 0,
                        processingIssues: data,
                        pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: () => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        this.sendReprocessing = (e) => {
            e.preventDefault();
            this.setState({
                loading: true,
                reprocessing: true,
            });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Started reprocessing\u2026'));
            const { orgId, projectId } = this.props.params;
            this.props.api.request(`/projects/${orgId}/${projectId}/reprocessing/`, {
                method: 'POST',
                success: () => {
                    this.fetchData();
                    this.setState({
                        reprocessing: false,
                    });
                },
                error: () => {
                    this.setState({
                        reprocessing: false,
                    });
                },
                complete: () => {
                    (0, indicator_1.clearIndicators)();
                },
            });
        };
        this.discardEvents = () => {
            const { orgId, projectId } = this.props.params;
            this.setState({
                expected: this.state.expected + 1,
            });
            this.props.api.request(`/projects/${orgId}/${projectId}/processingissues/discard/`, {
                method: 'DELETE',
                success: () => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: false,
                        loading: expected > 0,
                    });
                    // TODO (billyvg): Need to fix this
                    // we reload to get rid of the badge in the sidebar
                    window.location.reload();
                },
                error: () => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
        this.deleteProcessingIssues = () => {
            const { orgId, projectId } = this.props.params;
            this.setState({
                expected: this.state.expected + 1,
            });
            this.props.api.request(`/projects/${orgId}/${projectId}/processingissues/`, {
                method: 'DELETE',
                success: () => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: false,
                        loading: expected > 0,
                    });
                    // TODO (billyvg): Need to fix this
                    // we reload to get rid of the badge in the sidebar
                    window.location.reload();
                },
                error: () => {
                    const expected = this.state.expected - 1;
                    this.setState({
                        expected,
                        error: true,
                        loading: expected > 0,
                    });
                },
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    renderDebugTable() {
        let body;
        const { loading, error, processingIssues } = this.state;
        if (loading) {
            body = this.renderLoading();
        }
        else if (error) {
            body = <loadingError_1.default onRetry={this.fetchData}/>;
        }
        else if ((processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.hasIssues) ||
            (processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.resolveableIssues) ||
            (processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.issuesProcessing)) {
            body = this.renderResults();
        }
        else {
            body = this.renderEmpty();
        }
        return body;
    }
    renderLoading() {
        return (<panels_1.Panel>
        <loadingIndicator_1.default />
      </panels_1.Panel>);
    }
    renderEmpty() {
        return (<panels_1.Panel>
        <emptyStateWarning_1.default>
          <p>{(0, locale_1.t)('Good news! There are no processing issues.')}</p>
        </emptyStateWarning_1.default>
      </panels_1.Panel>);
    }
    getProblemDescription(item) {
        const msg = exports.projectProcessingIssuesMessages[item.type];
        return msg || (0, locale_1.t)('Unknown Error');
    }
    getImageName(path) {
        const pathSegments = path.split(/^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/');
        return pathSegments[pathSegments.length - 1];
    }
    renderProblem(item) {
        const description = this.getProblemDescription(item);
        const helpLink = HELP_LINKS[item.type];
        return (<div>
        <span>{description}</span>{' '}
        {helpLink && (<externalLink_1.default href={helpLink}>
            <icons_1.IconQuestion size="xs"/>
          </externalLink_1.default>)}
      </div>);
    }
    renderDetails(item) {
        let dsymUUID = null;
        let dsymName = null;
        let dsymArch = null;
        if (item.data._scope === 'native') {
            if (item.data.image_uuid) {
                dsymUUID = <code className="uuid">{item.data.image_uuid}</code>;
            }
            if (item.data.image_path) {
                dsymName = <em>{this.getImageName(item.data.image_path)}</em>;
            }
            if (item.data.image_arch) {
                dsymArch = item.data.image_arch;
            }
        }
        return (<span>
        {dsymUUID && <span> {dsymUUID}</span>}
        {dsymArch && <span> {dsymArch}</span>}
        {dsymName && <span> (for {dsymName})</span>}
      </span>);
    }
    renderResolveButton() {
        const issues = this.state.processingIssues;
        if (issues === null || this.state.reprocessing) {
            return null;
        }
        if (issues.resolveableIssues <= 0) {
            return null;
        }
        const fixButton = (0, locale_1.tn)('Click here to trigger processing for %s pending event', 'Click here to trigger processing for %s pending events', issues.resolveableIssues);
        return (<alertLink_1.default priority="info" onClick={this.sendReprocessing}>
        {(0, locale_1.t)('Pro Tip')}: {fixButton}
      </alertLink_1.default>);
    }
    renderResults() {
        var _a;
        const { processingIssues } = this.state;
        const fixLink = processingIssues ? processingIssues.signedLink : false;
        let fixLinkBlock = null;
        if (fixLink) {
            fixLinkBlock = (<panels_1.Panel>
          <panels_1.PanelHeader>
            {(0, locale_1.t)('Having trouble uploading debug informations? We can help!')}
          </panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <label>
              {(0, locale_1.t)("Paste this command into your shell and we'll attempt to upload the missing symbols from your machine:")}
            </label>
            <AutoSelectTextInput readOnly>
              curl -sL "{fixLink}" | bash
            </AutoSelectTextInput>
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        let processingRow = null;
        if (processingIssues && processingIssues.issuesProcessing > 0) {
            processingRow = (<StyledPanelAlert type="info" icon={<icons_1.IconSettings size="sm"/>}>
          {(0, locale_1.tn)('Reprocessing %s event …', 'Reprocessing %s events …', processingIssues.issuesProcessing)}
        </StyledPanelAlert>);
        }
        return (<React.Fragment>
        {fixLinkBlock}
        <h3>
          {(0, locale_1.t)('Pending Issues')}
          <access_1.default access={['project:write']}>
            {({ hasAccess }) => (<button_1.default size="small" className="pull-right" disabled={!hasAccess} onClick={() => this.discardEvents()}>
                {(0, locale_1.t)('Discard all')}
              </button_1.default>)}
          </access_1.default>
        </h3>
        <panels_1.PanelTable headers={[(0, locale_1.t)('Problem'), (0, locale_1.t)('Details'), (0, locale_1.t)('Events'), (0, locale_1.t)('Last seen')]}>
          {processingRow}
          {(_a = processingIssues === null || processingIssues === void 0 ? void 0 : processingIssues.issues) === null || _a === void 0 ? void 0 : _a.map((item, idx) => (<React.Fragment key={idx}>
              <div>{this.renderProblem(item)}</div>
              <div>{this.renderDetails(item)}</div>
              <div>{item.numEvents + ''}</div>
              <div>
                <timeSince_1.default date={item.lastSeen}/>
              </div>
            </React.Fragment>))}
        </panels_1.PanelTable>
      </React.Fragment>);
    }
    renderReprocessingSettings() {
        const access = new Set(this.props.organization.access);
        if (this.state.loading) {
            return this.renderLoading();
        }
        const { formData } = this.state;
        const { orgId, projectId } = this.props.params;
        return (<form_1.default saveOnBlur onSubmitSuccess={this.deleteProcessingIssues} apiEndpoint={`/projects/${orgId}/${projectId}/`} apiMethod="PUT" initialData={formData}>
        <jsonForm_1.default access={access} forms={processingIssues_1.default} renderHeader={() => (<panels_1.PanelAlert type="warning">
              <textBlock_1.default noMargin>
                {(0, locale_1.t)(`Reprocessing does not apply to Minidumps. Even when enabled,
                    Minidump events with processing issues will show up in the
                    issues stream immediately and cannot be reprocessed.`)}
              </textBlock_1.default>
            </panels_1.PanelAlert>)}/>
      </form_1.default>);
    }
    render() {
        const { projectId } = this.props.params;
        const title = (0, locale_1.t)('Processing Issues');
        return (<div>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectId}/>
        <settingsPageHeader_1.default title={title}/>
        <textBlock_1.default>
          {(0, locale_1.t)(`For some platforms the event processing requires configuration or
          manual action.  If a misconfiguration happens or some necessary
          steps are skipped, issues can occur during processing. (The most common
          reason for this is missing debug symbols.) In these cases you can see
          all the problems here with guides of how to correct them.`)}
        </textBlock_1.default>
        {this.renderDebugTable()}
        {this.renderResolveButton()}
        {this.renderReprocessingSettings()}
      </div>);
    }
}
exports.ProjectProcessingIssues = ProjectProcessingIssues;
const StyledPanelAlert = (0, styled_1.default)(panels_1.PanelAlert) `
  grid-column: 1/5;
`;
const AutoSelectTextInput = (0, styled_1.default)(autoSelectText_1.default) `
  font-family: ${p => p.theme.text.familyMono};
  ${p => (0, input_1.inputStyles)(p)};
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(ProjectProcessingIssues));
//# sourceMappingURL=projectProcessingIssues.jsx.map