Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const accountNotificationSettings_1 = require("app/data/forms/accountNotificationSettings");
const locale_1 = require("app/locale");
const withOrganizations_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganizations"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const fields_1 = require("app/views/settings/account/notifications/fields");
const notificationSettingsByType_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/notificationSettingsByType"));
const utils_1 = require("app/views/settings/account/notifications/utils");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const PanelBodyLineItem = (0, styled_1.default)(panels_1.PanelBody) `
  font-size: 1.4rem;
  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const AccountNotificationsByProject = ({ projects, field }) => {
    const projectsByOrg = (0, utils_1.groupByOrganization)(projects);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { title, description } = field, fieldConfig = (0, tslib_1.__rest)(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    const data = Object.values(projectsByOrg).map(org => ({
        name: org.organization.name,
        projects: org.projects.map(project => (Object.assign(Object.assign({}, fieldConfig), { 
            // `name` key refers to field name
            // we use project.id because slugs are not unique across orgs
            name: project.id, label: project.slug }))),
    }));
    return (<react_1.Fragment>
      {data.map(({ name, projects: projectFields }) => (<div key={name}>
          <panels_1.PanelHeader>{name}</panels_1.PanelHeader>
          {projectFields.map(f => (<PanelBodyLineItem key={f.name}>
              <selectField_1.default defaultValue={f.defaultValue} name={f.name} options={f.options} label={f.label}/>
            </PanelBodyLineItem>))}
        </div>))}
    </react_1.Fragment>);
};
const AccountNotificationsByOrganization = ({ organizations, field }) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { title, description } = field, fieldConfig = (0, tslib_1.__rest)(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    const data = organizations.map(org => (Object.assign(Object.assign({}, fieldConfig), { 
        // `name` key refers to field name
        // we use org.id to remain consistent project.id use (which is required because slugs are not unique across orgs)
        name: org.id, label: org.slug })));
    return (<react_1.Fragment>
      {data.map(f => (<PanelBodyLineItem key={f.name}>
          <selectField_1.default defaultValue={f.defaultValue} name={f.name} options={f.options} label={f.label}/>
        </PanelBodyLineItem>))}
    </react_1.Fragment>);
};
const AccountNotificationsByOrganizationContainer = (0, withOrganizations_1.default)(AccountNotificationsByOrganization);
class AccountNotificationFineTuning extends asyncView_1.default {
    getEndpoints() {
        const { fineTuneType } = this.props.params;
        const endpoints = [
            ['notifications', '/users/me/notifications/'],
            ['fineTuneData', `/users/me/notifications/${fineTuneType}/`],
        ];
        if ((0, utils_1.isGroupedByProject)(fineTuneType)) {
            endpoints.push(['projects', '/projects/']);
        }
        endpoints.push(['emails', '/users/me/emails/']);
        if (fineTuneType === 'email') {
            endpoints.push(['emails', '/users/me/emails/']);
        }
        return endpoints;
    }
    // Return a sorted list of user's verified emails
    get emailChoices() {
        var _a, _b, _c;
        return ((_c = (_b = (_a = this.state.emails) === null || _a === void 0 ? void 0 : _a.filter(({ isVerified }) => isVerified)) === null || _b === void 0 ? void 0 : _b.sort((a, b) => {
            // Sort by primary -> email
            if (a.isPrimary) {
                return -1;
            }
            else if (b.isPrimary) {
                return 1;
            }
            return a.email < b.email ? -1 : 1;
        })) !== null && _c !== void 0 ? _c : []);
    }
    renderBody() {
        const { params } = this.props;
        const { fineTuneType } = params;
        if (['alerts', 'deploy', 'workflow'].includes(fineTuneType)) {
            return <notificationSettingsByType_1.default notificationType={fineTuneType}/>;
        }
        const { notifications, projects, fineTuneData, projectsPageLinks } = this.state;
        const isProject = (0, utils_1.isGroupedByProject)(fineTuneType);
        const field = fields_1.ACCOUNT_NOTIFICATION_FIELDS[fineTuneType];
        const { title, description } = field;
        const [stateKey, url] = isProject ? this.getEndpoints()[2] : [];
        const hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length);
        if (fineTuneType === 'email') {
            // Fetch verified email addresses
            field.options = this.emailChoices.map(({ email }) => ({ value: email, label: email }));
        }
        if (!notifications || !fineTuneData) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={title}/>
        {description && <textBlock_1.default>{description}</textBlock_1.default>}

        {field &&
                field.defaultFieldName &&
                // not implemented yet
                field.defaultFieldName !== 'weeklyReports' && (<form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/" initialData={notifications}>
              <jsonForm_1.default title={`Default ${title}`} fields={[accountNotificationSettings_1.fields[field.defaultFieldName]]}/>
            </form_1.default>)}
        <panels_1.Panel>
          <panels_1.PanelBody>
            <panels_1.PanelHeader hasButtons={isProject}>
              <Heading>{isProject ? (0, locale_1.t)('Projects') : (0, locale_1.t)('Organizations')}</Heading>
              <div>
                {isProject &&
                this.renderSearchInput({
                    placeholder: (0, locale_1.t)('Search Projects'),
                    url,
                    stateKey,
                })}
              </div>
            </panels_1.PanelHeader>

            <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint={`/users/me/notifications/${fineTuneType}/`} initialData={fineTuneData}>
              {isProject && hasProjects && (<AccountNotificationsByProject projects={projects} field={field}/>)}

              {isProject && !hasProjects && (<emptyMessage_1.default>{(0, locale_1.t)('No projects found')}</emptyMessage_1.default>)}

              {!isProject && (<AccountNotificationsByOrganizationContainer field={field}/>)}
            </form_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>

        {projects && <pagination_1.default pageLinks={projectsPageLinks} {...this.props}/>}
      </div>);
    }
}
const Heading = (0, styled_1.default)('div') `
  flex: 1;
`;
exports.default = AccountNotificationFineTuning;
//# sourceMappingURL=accountNotificationFineTuning.jsx.map