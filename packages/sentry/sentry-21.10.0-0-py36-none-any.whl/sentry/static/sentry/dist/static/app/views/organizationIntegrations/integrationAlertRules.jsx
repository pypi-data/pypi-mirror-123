Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const IntegrationAlertRules = ({ projects, organization }) => (<panels_1.Panel>
    <panels_1.PanelHeader>{(0, locale_1.t)('Project Configuration')}</panels_1.PanelHeader>
    <panels_1.PanelBody>
      {projects.length === 0 && (<emptyMessage_1.default size="large">
          {(0, locale_1.t)('You have no projects to add Alert Rules to')}
        </emptyMessage_1.default>)}
      {projects.map(project => (<ProjectItem key={project.slug}>
          <projectBadge_1.default project={project} avatarSize={16}/>
          <button_1.default to={`/organizations/${organization.slug}/alerts/${project.slug}/wizard/`} size="xsmall">
            {(0, locale_1.t)('Add Alert Rule')}
          </button_1.default>
        </ProjectItem>))}
    </panels_1.PanelBody>
  </panels_1.Panel>);
const ProjectItem = (0, styled_1.default)(panels_1.PanelItem) `
  align-items: center;
  justify-content: space-between;
`;
exports.default = (0, withOrganization_1.default)((0, withProjects_1.default)(IntegrationAlertRules));
//# sourceMappingURL=integrationAlertRules.jsx.map