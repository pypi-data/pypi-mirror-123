Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
const finishSetupAlert_1 = (0, tslib_1.__importDefault)(require("./finishSetupAlert"));
class EventDetails extends react_1.Component {
    constructor() {
        super(...arguments);
        this.getEventSlug = () => {
            const { eventSlug } = this.props.params;
            return typeof eventSlug === 'string' ? eventSlug.trim() : '';
        };
    }
    render() {
        const { organization, location, params, router, route } = this.props;
        const documentTitle = (0, locale_1.t)('Performance Details');
        const eventSlug = this.getEventSlug();
        const projectSlug = eventSlug.split(':')[0];
        return (<sentryDocumentTitle_1.default title={documentTitle} orgSlug={organization.slug} projectSlug={projectSlug}>
        <StyledPageContent>
          <noProjectMessage_1.default organization={organization}>
            <projects_1.default orgId={organization.slug} slugs={[projectSlug]}>
              {({ projects }) => {
                if (projects.length === 0) {
                    return null;
                }
                const project = projects.find(p => p.slug === projectSlug);
                // only render setup alert if the project has no real transactions
                if (!project || project.firstTransactionEvent) {
                    return null;
                }
                return <finishSetupAlert_1.default organization={organization} project={project}/>;
            }}
            </projects_1.default>
            <content_1.default organization={organization} location={location} params={params} eventSlug={eventSlug} router={router} route={route}/>
          </noProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)(EventDetails);
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
//# sourceMappingURL=index.jsx.map