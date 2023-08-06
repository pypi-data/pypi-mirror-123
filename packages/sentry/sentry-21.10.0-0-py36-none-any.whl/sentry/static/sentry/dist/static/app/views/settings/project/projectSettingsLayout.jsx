Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const AppStoreConnectContext = (0, tslib_1.__importStar)(require("app/components/projects/appStoreConnectContext"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const projectContext_1 = (0, tslib_1.__importDefault)(require("app/views/projects/projectContext"));
const settingsLayout_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsLayout"));
const projectSettingsNavigation_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectSettingsNavigation"));
function ProjectSettingsLayout(_a) {
    var { params, organization, children, routes } = _a, props = (0, tslib_1.__rest)(_a, ["params", "organization", "children", "routes"]);
    const { orgId, projectId } = params;
    return (<projectContext_1.default orgId={orgId} projectId={projectId}>
      {({ project }) => (<AppStoreConnectContext.Provider project={project} organization={organization}>
          <settingsLayout_1.default params={params} routes={routes} {...props} renderNavigation={() => (<projectSettingsNavigation_1.default organization={organization}/>)}>
            {children && React.isValidElement(children)
                ? React.cloneElement(children, {
                    organization,
                    project,
                })
                : children}
          </settingsLayout_1.default>
        </AppStoreConnectContext.Provider>)}
    </projectContext_1.default>);
}
exports.default = (0, withOrganization_1.default)(ProjectSettingsLayout);
//# sourceMappingURL=projectSettingsLayout.jsx.map