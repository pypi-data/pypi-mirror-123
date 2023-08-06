Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const members_1 = require("app/actionCreators/members");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const scrollToTop_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/scrollToTop"));
function AlertBuilderProjectProvider(props) {
    const api = (0, useApi_1.default)();
    const { children, params, organization } = props, other = (0, tslib_1.__rest)(props, ["children", "params", "organization"]);
    const { projectId } = params;
    return (<projects_1.default orgId={organization.slug} allProjects>
      {({ projects, initiallyLoaded, isIncomplete }) => {
            if (!initiallyLoaded) {
                return <loadingIndicator_1.default />;
            }
            const project = projects.find(({ slug }) => slug === projectId);
            // if loaded, but project fetching states incomplete or project can't be found, project doesn't exist
            if (isIncomplete || !project) {
                return (<alert_1.default type="warning">
              {(0, locale_1.t)('The project you were looking for was not found.')}
            </alert_1.default>);
            }
            // fetch members list for mail action fields
            (0, members_1.fetchOrgMembers)(api, organization.slug, [project.id]);
            return (<scrollToTop_1.default location={props.location} disable={() => false}>
            {children && React.isValidElement(children)
                    ? React.cloneElement(children, Object.assign(Object.assign(Object.assign({}, other), children.props), { project,
                        organization }))
                    : children}
          </scrollToTop_1.default>);
        }}
    </projects_1.default>);
}
exports.default = AlertBuilderProjectProvider;
//# sourceMappingURL=projectProvider.jsx.map