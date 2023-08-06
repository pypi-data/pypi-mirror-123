Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const feedbackAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/feedbackAlert"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
const addCodeOwnerModal_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/addCodeOwnerModal"));
const codeowners_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/codeowners"));
const rulesPanel_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/rulesPanel"));
const CodeOwnersHeader = (0, hookOrDefault_1.default)({
    hookName: 'component:codeowners-header',
    defaultComponent: () => <react_1.Fragment />,
});
class ProjectOwnership extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleAddCodeOwner = () => {
            const { codeMappings, integrations } = this.state;
            (0, modal_1.openModal)(modalProps => (<addCodeOwnerModal_1.default {...modalProps} organization={this.props.organization} project={this.props.project} codeMappings={codeMappings} integrations={integrations} onSave={this.handleCodeOwnerAdded}/>));
        };
        this.handleOwnershipSave = (text) => {
            this.setState(prevState => ({
                ownership: Object.assign(Object.assign({}, prevState.ownership), { raw: text }),
            }));
        };
        this.handleCodeOwnerAdded = (data) => {
            const { codeowners } = this.state;
            const newCodeowners = [data, ...(codeowners || [])];
            this.setState({ codeowners: newCodeowners });
        };
        this.handleCodeOwnerDeleted = (data) => {
            const { codeowners } = this.state;
            const newCodeowners = (codeowners || []).filter(codeowner => codeowner.id !== data.id);
            this.setState({ codeowners: newCodeowners });
        };
        this.handleCodeOwnerUpdated = (data) => {
            const codeowners = this.state.codeowners || [];
            const index = codeowners.findIndex(item => item.id === data.id);
            this.setState({
                codeowners: [...codeowners.slice(0, index), data, ...codeowners.slice(index + 1)],
            });
        };
        this.handleAddCodeOwnerRequest = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, project } = this.props;
            try {
                (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Requesting\u2026'));
                yield this.api.requestPromise(`/projects/${organization.slug}/${project.slug}/codeowners-request/`, {
                    method: 'POST',
                    data: {},
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Request Sent'));
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to send request'));
                Sentry.captureException(err);
            }
        });
        this.renderCodeOwnerErrors = () => {
            const { project, organization } = this.props;
            const { codeowners } = this.state;
            const errMessageComponent = (message, values, link, linkValue) => (<react_1.Fragment>
        <ErrorMessageContainer>
          <span>{message}</span>
          <b>{values.join(', ')}</b>
        </ErrorMessageContainer>
        <ErrorCtaContainer>
          <externalLink_1.default href={link}>{linkValue}</externalLink_1.default>
        </ErrorCtaContainer>
      </react_1.Fragment>);
            const errMessageListComponent = (message, values, linkFunction, linkValueFunction) => {
                return (<react_1.Fragment>
          <ErrorMessageContainer>
            <span>{message}</span>
          </ErrorMessageContainer>
          <ErrorMessageListContainer>
            {values.map((value, index) => (<ErrorInlineContainer key={index}>
                <b>{value}</b>
                <ErrorCtaContainer>
                  <externalLink_1.default href={linkFunction(value)} key={index}>
                    {linkValueFunction(value)}
                  </externalLink_1.default>
                </ErrorCtaContainer>
              </ErrorInlineContainer>))}
          </ErrorMessageListContainer>
        </react_1.Fragment>);
            };
            return (codeowners || [])
                .filter(({ errors }) => Object.values(errors).flat().length)
                .map(({ id, codeMapping, errors }) => {
                const errMessage = (type, values) => {
                    var _a, _b;
                    switch (type) {
                        case 'missing_external_teams':
                            return errMessageComponent(`The following teams do not have an association in the organization: ${organization.slug}`, values, `/settings/${organization.slug}/integrations/${(_a = codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.provider) === null || _a === void 0 ? void 0 : _a.slug}/${codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.integrationId}/?tab=teamMappings`, 'Configure Team Mappings');
                        case 'missing_external_users':
                            return errMessageComponent(`The following usernames do not have an association in the organization: ${organization.slug}`, values, `/settings/${organization.slug}/integrations/${(_b = codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.provider) === null || _b === void 0 ? void 0 : _b.slug}/${codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.integrationId}/?tab=userMappings`, 'Configure User Mappings');
                        case 'missing_user_emails':
                            return errMessageComponent(`The following emails do not have an Sentry user in the organization: ${organization.slug}`, values, `/settings/${organization.slug}/members/`, 'Invite Users');
                        case 'teams_without_access':
                            return errMessageListComponent(`The following team do not have access to the project: ${project.slug}`, values, value => `/settings/${organization.slug}/teams/${value.slice(1)}/projects/`, value => `Configure ${value} Permissions`);
                        case 'users_without_access':
                            return errMessageListComponent(`The following users are not on a team that has access to the project: ${project.slug}`, values, email => `/settings/${organization.slug}/members/?query=${email}`, _ => `Configure Member Settings`);
                        default:
                            return null;
                    }
                };
                return (<alert_1.default key={id} type="error" icon={<icons_1.IconWarning size="md"/>} expand={[
                        <AlertContentContainer key="container">
                {Object.entries(errors)
                                .filter(([_, values]) => values.length)
                                .map(([type, values]) => (<ErrorContainer key={`${id}-${type}`}>
                      {errMessage(type, values)}
                    </ErrorContainer>))}
              </AlertContentContainer>,
                    ]}>
            {`There were ${Object.values(errors).flat().length} ownership issues within Sentry on the latest sync with the CODEOWNERS file`}
          </alert_1.default>);
            });
        };
    }
    getTitle() {
        const { project } = this.props;
        return (0, routeTitle_1.default)((0, locale_1.t)('Issue Owners'), project.slug, false);
    }
    getEndpoints() {
        const { organization, project } = this.props;
        const endpoints = [
            ['ownership', `/projects/${organization.slug}/${project.slug}/ownership/`],
            [
                'codeMappings',
                `/organizations/${organization.slug}/code-mappings/`,
                { query: { projectId: project.id } },
            ],
            [
                'integrations',
                `/organizations/${organization.slug}/integrations/`,
                { query: { features: ['codeowners'] } },
            ],
        ];
        if (organization.features.includes('integrations-codeowners')) {
            endpoints.push([
                'codeowners',
                `/projects/${organization.slug}/${project.slug}/codeowners/`,
                { query: { expand: ['codeMapping', 'ownershipSyntax'] } },
            ]);
        }
        return endpoints;
    }
    getPlaceholder() {
        return `#example usage
path:src/example/pipeline/* person@sentry.io #infra
url:http://example.com/settings/* #product
tags.sku_class:enterprise #enterprise`;
    }
    getDetail() {
        return (0, locale_1.tct)(`Automatically assign issues and send alerts to the right people based on issue properties. [link:Learn more].`, {
            link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
        });
    }
    renderBody() {
        const { project, organization } = this.props;
        const { ownership, codeowners } = this.state;
        const disabled = !organization.access.includes('project:write');
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Issue Owners')} action={<react_1.Fragment>
              <button_1.default to={{
                    pathname: `/organizations/${organization.slug}/issues/`,
                    query: { project: project.id },
                }} size="small">
                {(0, locale_1.t)('View Issues')}
              </button_1.default>
              <feature_1.default features={['integrations-codeowners']}>
                <access_1.default access={['org:integrations']}>
                  {({ hasAccess }) => hasAccess ? (<CodeOwnerButton onClick={this.handleAddCodeOwner} size="small" priority="primary" data-test-id="add-codeowner-button">
                        {(0, locale_1.t)('Add CODEOWNERS File')}
                      </CodeOwnerButton>) : (<CodeOwnerButton onClick={this.handleAddCodeOwnerRequest} size="small" priority="primary" data-test-id="add-codeowner-request-button">
                        {(0, locale_1.t)('Request to Add CODEOWNERS File')}
                      </CodeOwnerButton>)}
                </access_1.default>
              </feature_1.default>
            </react_1.Fragment>}/>
        <IssueOwnerDetails>{this.getDetail()}</IssueOwnerDetails>
        <CodeOwnersHeader addCodeOwner={this.handleAddCodeOwner} handleRequest={this.handleAddCodeOwnerRequest}/>

        <permissionAlert_1.default />
        <feedbackAlert_1.default />
        {this.renderCodeOwnerErrors()}
        <rulesPanel_1.default data-test-id="issueowners-panel" type="issueowners" raw={ownership.raw || ''} dateUpdated={ownership.lastUpdated} placeholder={this.getPlaceholder()} controls={[
                <button_1.default key="edit" size="xsmall" onClick={() => (0, modal_1.openEditOwnershipRules)({
                        organization,
                        project,
                        ownership,
                        onSave: this.handleOwnershipSave,
                    })} disabled={disabled}>
              {(0, locale_1.t)('Edit')}
            </button_1.default>,
            ]}/>
        <feature_1.default features={['integrations-codeowners']}>
          <codeowners_1.default codeowners={codeowners || []} onDelete={this.handleCodeOwnerDeleted} onUpdate={this.handleCodeOwnerUpdated} disabled={disabled} {...this.props}/>
        </feature_1.default>
        <form_1.default apiEndpoint={`/projects/${organization.slug}/${project.slug}/ownership/`} apiMethod="PUT" saveOnBlur initialData={{
                fallthrough: ownership.fallthrough,
                autoAssignment: ownership.autoAssignment,
            }} hideFooter>
          <jsonForm_1.default forms={[
                {
                    title: (0, locale_1.t)('Issue Owners'),
                    fields: [
                        {
                            name: 'autoAssignment',
                            type: 'boolean',
                            label: (0, locale_1.t)('Automatically assign issues'),
                            help: (0, locale_1.t)('Assign issues when a new event matches the rules above.'),
                            disabled,
                        },
                        {
                            name: 'fallthrough',
                            type: 'boolean',
                            label: (0, locale_1.t)('Send alert to project members if there’s no assigned owner'),
                            help: (0, locale_1.t)('Alerts will be sent to all users who have access to this project.'),
                            disabled,
                        },
                    ],
                },
            ]}/>
        </form_1.default>
      </react_1.Fragment>);
    }
}
exports.default = ProjectOwnership;
const CodeOwnerButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const AlertContentContainer = (0, styled_1.default)('div') `
  overflow-y: auto;
  max-height: 350px;
`;
const ErrorContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-areas: 'message cta';
  grid-template-columns: 2fr 1fr;
  gap: ${(0, space_1.default)(2)};
  padding: ${(0, space_1.default)(1.5)} 0;
`;
const ErrorInlineContainer = (0, styled_1.default)(ErrorContainer) `
  gap: ${(0, space_1.default)(1.5)};
  grid-template-columns: 1fr 2fr;
  align-items: center;
  padding: 0;
`;
const ErrorMessageContainer = (0, styled_1.default)('div') `
  grid-area: message;
  display: grid;
  gap: ${(0, space_1.default)(1.5)};
`;
const ErrorMessageListContainer = (0, styled_1.default)('div') `
  grid-column: message / cta-end;
  gap: ${(0, space_1.default)(1.5)};
`;
const ErrorCtaContainer = (0, styled_1.default)('div') `
  grid-area: cta;
  justify-self: flex-end;
  text-align: right;
  line-height: 1.5;
`;
const IssueOwnerDetails = (0, styled_1.default)('div') `
  padding-bottom: ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=index.jsx.map