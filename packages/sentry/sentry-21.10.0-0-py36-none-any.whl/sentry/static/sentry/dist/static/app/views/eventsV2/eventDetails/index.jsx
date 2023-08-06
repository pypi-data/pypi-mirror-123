Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
class EventDetails extends react_1.Component {
    constructor() {
        super(...arguments);
        this.getEventSlug = () => {
            const { eventSlug } = this.props.params;
            if (typeof eventSlug === 'string') {
                return eventSlug.trim();
            }
            return '';
        };
        this.getEventView = () => {
            const { location } = this.props;
            return eventView_1.default.fromLocation(location);
        };
        this.getDocumentTitle = (name) => typeof name === 'string' && String(name).trim().length > 0
            ? [String(name).trim(), (0, locale_1.t)('Discover')]
            : [(0, locale_1.t)('Discover')];
    }
    render() {
        const { organization, location, params, router, route } = this.props;
        const eventView = this.getEventView();
        const eventSlug = this.getEventSlug();
        const documentTitle = this.getDocumentTitle(eventView.name).join(' - ');
        const projectSlug = eventSlug.split(':')[0];
        return (<sentryDocumentTitle_1.default title={documentTitle} orgSlug={organization.slug} projectSlug={projectSlug}>
        <StyledPageContent>
          <noProjectMessage_1.default organization={organization}>
            <content_1.default organization={organization} location={location} params={params} eventView={eventView} eventSlug={eventSlug} router={router} route={route}/>
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