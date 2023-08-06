Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const projects_1 = require("app/actionCreators/projects");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const panels_1 = require("app/components/panels");
const projectGeneralSettings_1 = require("app/data/forms/projectGeneralSettings");
const locale_1 = require("app/locale");
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const handleXhrErrorResponse_1 = (0, tslib_1.__importDefault)(require("app/utils/handleXhrErrorResponse"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
class ProjectGeneralSettings extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this._form = {};
        this.handleTransferFieldChange = (id, value) => {
            this._form[id] = value;
        };
        this.handleRemoveProject = () => {
            const { orgId } = this.props.params;
            const project = this.state.data;
            (0, utils_1.removeGlobalSelectionStorage)(orgId);
            if (!project) {
                return;
            }
            (0, projects_1.removeProject)(this.api, orgId, project).then(() => {
                // Need to hard reload because lots of components do not listen to Projects Store
                window.location.assign('/');
            }, (0, handleXhrErrorResponse_1.default)('Unable to remove project'));
        };
        this.handleTransferProject = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgId } = this.props.params;
            const project = this.state.data;
            if (!project) {
                return;
            }
            if (typeof this._form.email !== 'string' || this._form.email.length < 1) {
                return;
            }
            try {
                yield (0, projects_1.transferProject)(this.api, orgId, project, this._form.email);
                // Need to hard reload because lots of components do not listen to Projects Store
                window.location.assign('/');
            }
            catch (err) {
                if (err.status >= 500) {
                    (0, handleXhrErrorResponse_1.default)('Unable to transfer project')(err);
                }
            }
        });
        this.isProjectAdmin = () => new Set(this.props.organization.access).has('project:admin');
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Project Settings'), projectId, false);
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['data', `/projects/${orgId}/${projectId}/`]];
    }
    renderRemoveProject() {
        const project = this.state.data;
        const isProjectAdmin = this.isProjectAdmin();
        const { isInternal } = project;
        return (<field_1.default label={(0, locale_1.t)('Remove Project')} help={(0, locale_1.tct)('Remove the [project] project and all related data. [linebreak] Careful, this action cannot be undone.', {
                project: <strong>{project.slug}</strong>,
                linebreak: <br />,
            })}>
        {!isProjectAdmin &&
                (0, locale_1.t)('You do not have the required permission to remove this project.')}

        {isInternal &&
                (0, locale_1.t)('This project cannot be removed. It is used internally by the Sentry server.')}

        {isProjectAdmin && !isInternal && (<confirm_1.default onConfirm={this.handleRemoveProject} priority="danger" confirmText={(0, locale_1.t)('Remove project')} message={<div>
                <textBlock_1.default>
                  <strong>
                    {(0, locale_1.t)('Removing this project is permanent and cannot be undone!')}
                  </strong>
                </textBlock_1.default>
                <textBlock_1.default>
                  {(0, locale_1.t)('This will also remove all associated event data.')}
                </textBlock_1.default>
              </div>}>
            <div>
              <button_1.default className="ref-remove-project" type="button" priority="danger">
                {(0, locale_1.t)('Remove Project')}
              </button_1.default>
            </div>
          </confirm_1.default>)}
      </field_1.default>);
    }
    renderTransferProject() {
        const project = this.state.data;
        const isProjectAdmin = this.isProjectAdmin();
        const { isInternal } = project;
        return (<field_1.default label={(0, locale_1.t)('Transfer Project')} help={(0, locale_1.tct)('Transfer the [project] project and all related data. [linebreak] Careful, this action cannot be undone.', {
                project: <strong>{project.slug}</strong>,
                linebreak: <br />,
            })}>
        {!isProjectAdmin &&
                (0, locale_1.t)('You do not have the required permission to transfer this project.')}

        {isInternal &&
                (0, locale_1.t)('This project cannot be transferred. It is used internally by the Sentry server.')}

        {isProjectAdmin && !isInternal && (<confirm_1.default onConfirm={this.handleTransferProject} priority="danger" confirmText={(0, locale_1.t)('Transfer project')} renderMessage={({ confirm }) => (<div>
                <textBlock_1.default>
                  <strong>
                    {(0, locale_1.t)('Transferring this project is permanent and cannot be undone!')}
                  </strong>
                </textBlock_1.default>
                <textBlock_1.default>
                  {(0, locale_1.t)('Please enter the email of an organization owner to whom you would like to transfer this project.')}
                </textBlock_1.default>
                <panels_1.Panel>
                  <form_1.default hideFooter onFieldChange={this.handleTransferFieldChange} onSubmit={(_data, _onSuccess, _onError, e) => {
                        e.stopPropagation();
                        confirm();
                    }}>
                    <textField_1.default name="email" label={(0, locale_1.t)('Organization Owner')} placeholder="admin@example.com" required help={(0, locale_1.t)('A request will be emailed to this address, asking the organization owner to accept the project transfer.')}/>
                  </form_1.default>
                </panels_1.Panel>
              </div>)}>
            <div>
              <button_1.default className="ref-transfer-project" type="button" priority="danger">
                {(0, locale_1.t)('Transfer Project')}
              </button_1.default>
            </div>
          </confirm_1.default>)}
      </field_1.default>);
    }
    renderBody() {
        var _a;
        const { organization } = this.props;
        const project = this.state.data;
        const { orgId, projectId } = this.props.params;
        const endpoint = `/projects/${orgId}/${projectId}/`;
        const access = new Set(organization.access);
        const jsonFormProps = {
            additionalFieldProps: {
                organization,
            },
            features: new Set(organization.features),
            access,
            disabled: !access.has('project:write'),
        };
        const team = project.teams.length ? (_a = project.teams) === null || _a === void 0 ? void 0 : _a[0] : undefined;
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Project Settings')}/>
        <permissionAlert_1.default />

        <form_1.default saveOnBlur allowUndo initialData={Object.assign(Object.assign({}, project), { team })} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={resp => {
                this.setState({ data: resp });
                if (projectId !== resp.slug) {
                    (0, projects_1.changeProjectSlug)(projectId, resp.slug);
                    // Container will redirect after stores get updated with new slug
                    this.props.onChangeSlug(resp.slug);
                }
                // This will update our project context
                projectActions_1.default.updateSuccess(resp);
            }}>
          <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Project Details')} fields={[projectGeneralSettings_1.fields.slug, projectGeneralSettings_1.fields.platform]}/>

          <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Email')} fields={[projectGeneralSettings_1.fields.subjectPrefix]}/>

          <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Event Settings')} fields={[projectGeneralSettings_1.fields.resolveAge]}/>

          <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Client Security')} fields={[
                projectGeneralSettings_1.fields.allowedDomains,
                projectGeneralSettings_1.fields.scrapeJavaScript,
                projectGeneralSettings_1.fields.securityToken,
                projectGeneralSettings_1.fields.securityTokenHeader,
                projectGeneralSettings_1.fields.verifySSL,
            ]} renderHeader={() => (<panels_1.PanelAlert type="info">
                <textBlock_1.default noMargin>
                  {(0, locale_1.tct)('Configure origin URLs which Sentry should accept events from. This is used for communication with clients like [link].', {
                    link: (<a href="https://github.com/getsentry/sentry-javascript">
                          sentry-javascript
                        </a>),
                })}{' '}
                  {(0, locale_1.tct)('This will restrict requests based on the [Origin] and [Referer] headers.', {
                    Origin: <code>Origin</code>,
                    Referer: <code>Referer</code>,
                })}
                </textBlock_1.default>
              </panels_1.PanelAlert>)}/>
        </form_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Project Administration')}</panels_1.PanelHeader>
          {this.renderRemoveProject()}
          {this.renderTransferProject()}
        </panels_1.Panel>
      </div>);
    }
}
class ProjectGeneralSettingsContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.changedSlug = undefined;
        this.unsubscribe = projectsStore_1.default.listen(() => this.onProjectsUpdate(), undefined);
    }
    componentWillUnmount() {
        this.unsubscribe();
    }
    onProjectsUpdate() {
        if (!this.changedSlug) {
            return;
        }
        const project = projectsStore_1.default.getBySlug(this.changedSlug);
        if (!project) {
            return;
        }
        react_router_1.browserHistory.replace((0, recreateRoute_1.default)('', Object.assign(Object.assign({}, this.props), { params: Object.assign(Object.assign({}, this.props.params), { projectId: this.changedSlug }) })));
    }
    render() {
        return (<ProjectGeneralSettings onChangeSlug={(newSlug) => (this.changedSlug = newSlug)} {...this.props}/>);
    }
}
exports.default = (0, withOrganization_1.default)(ProjectGeneralSettingsContainer);
//# sourceMappingURL=projectGeneralSettings.jsx.map