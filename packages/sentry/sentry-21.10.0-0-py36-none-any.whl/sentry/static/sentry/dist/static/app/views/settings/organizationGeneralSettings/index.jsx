Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const indicator_1 = require("app/actionCreators/indicator");
const organizations_1 = require("app/actionCreators/organizations");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const panels_1 = require("app/components/panels");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/permissionAlert"));
const organizationSettingsForm_1 = (0, tslib_1.__importDefault)(require("./organizationSettingsForm"));
function OrganizationGeneralSettings(props) {
    const api = (0, useApi_1.default)();
    const { organization, projects, params } = props;
    const { orgId } = params;
    const access = new Set(organization.access);
    const removeConfirmMessage = (<react_1.Fragment>
      <textBlock_1.default>
        {(0, locale_1.tct)('Removing the organization, [name] is permanent and cannot be undone! Are you sure you want to continue?', {
            name: organization && <strong>{organization.name}</strong>,
        })}
      </textBlock_1.default>

      {!!projects.length && (<react_1.Fragment>
          <textBlock_1.default>
            {(0, locale_1.t)('This will also remove the following associated projects:')}
          </textBlock_1.default>
          <list_1.default symbol="bullet" data-test-id="removed-projects-list">
            {projects.map(project => (<listItem_1.default key={project.slug}>{project.slug}</listItem_1.default>))}
          </list_1.default>
        </react_1.Fragment>)}
    </react_1.Fragment>);
    const handleSaveForm = (prevData, data) => {
        if (data.slug && data.slug !== prevData.slug) {
            (0, organizations_1.changeOrganizationSlug)(prevData, data);
            react_router_1.browserHistory.replace(`/settings/${data.slug}/`);
        }
        else {
            // This will update OrganizationStore (as well as OrganizationsStore
            // which is slightly incorrect because it has summaries vs a detailed org)
            (0, organizations_1.updateOrganization)(data);
        }
    };
    const handleConfirmRemoveOrg = () => {
        if (!organization) {
            return;
        }
        (0, indicator_1.addLoadingMessage)();
        (0, organizations_1.removeAndRedirectToRemainingOrganization)(api, {
            orgId: params.orgId,
            successMessage: `${organization.name} is queued for deletion.`,
            errorMessage: `Error removing the ${organization.name} organization`,
        });
    };
    return (<react_1.Fragment>
      <sentryDocumentTitle_1.default title={(0, locale_1.t)('General Settings')} orgSlug={orgId}/>
      <div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Organization Settings')}/>
        <permissionAlert_1.default />

        <organizationSettingsForm_1.default {...props} initialData={organization} access={access} onSave={handleSaveForm}/>

        {access.has('org:admin') && !organization.isDefault && (<panels_1.Panel>
            <panels_1.PanelHeader>{(0, locale_1.t)('Remove Organization')}</panels_1.PanelHeader>
            <field_1.default label={(0, locale_1.t)('Remove Organization')} help={(0, locale_1.t)('Removing this organization will delete all data including projects and their associated events.')}>
              <div>
                <confirm_1.default priority="danger" confirmText={(0, locale_1.t)('Remove Organization')} message={removeConfirmMessage} onConfirm={handleConfirmRemoveOrg}>
                  <button_1.default priority="danger">{(0, locale_1.t)('Remove Organization')}</button_1.default>
                </confirm_1.default>
              </div>
            </field_1.default>
          </panels_1.Panel>)}
      </div>
    </react_1.Fragment>);
}
exports.default = (0, withProjects_1.default)((0, withOrganization_1.default)(OrganizationGeneralSettings));
//# sourceMappingURL=index.jsx.map