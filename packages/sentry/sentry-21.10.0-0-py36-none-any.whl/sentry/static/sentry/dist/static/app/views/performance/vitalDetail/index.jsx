Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const tags_1 = require("app/actionCreators/tags");
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const fields_1 = require("app/utils/discover/fields");
const performanceEventViewContext_1 = require("app/utils/performance/contexts/performanceEventViewContext");
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const data_1 = require("../data");
const utils_1 = require("../utils");
const vitalDetailContent_1 = (0, tslib_1.__importDefault)(require("./vitalDetailContent"));
class VitalDetail extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            eventView: (0, data_1.generatePerformanceVitalDetailView)(this.props.organization, this.props.location),
        };
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        return Object.assign(Object.assign({}, prevState), { eventView: (0, data_1.generatePerformanceVitalDetailView)(nextProps.organization, nextProps.location) });
    }
    componentDidMount() {
        const { api, organization, selection } = this.props;
        (0, tags_1.loadOrganizationTags)(api, organization.slug, selection);
        (0, utils_1.addRoutePerformanceContext)(selection);
    }
    componentDidUpdate(prevProps) {
        const { api, organization, selection } = this.props;
        if (!(0, isEqual_1.default)(prevProps.selection.projects, selection.projects) ||
            !(0, isEqual_1.default)(prevProps.selection.datetime, selection.datetime)) {
            (0, tags_1.loadOrganizationTags)(api, organization.slug, selection);
            (0, utils_1.addRoutePerformanceContext)(selection);
        }
    }
    getDocumentTitle() {
        const name = (0, utils_1.getTransactionName)(this.props.location);
        const hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), (0, locale_1.t)('Performance')].join(' - ');
        }
        return [(0, locale_1.t)('Vital Detail'), (0, locale_1.t)('Performance')].join(' - ');
    }
    render() {
        const { organization, location, router } = this.props;
        const { eventView } = this.state;
        if (!eventView) {
            react_router_1.browserHistory.replace({
                pathname: `/organizations/${organization.slug}/performance/`,
                query: Object.assign({}, location.query),
            });
            return null;
        }
        const vitalNameQuery = (0, queryString_1.decodeScalar)(location.query.vitalName);
        const vitalName = Object.values(fields_1.WebVital).indexOf(vitalNameQuery) === -1
            ? undefined
            : vitalNameQuery;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <performanceEventViewContext_1.PerformanceEventViewProvider value={{ eventView: this.state.eventView }}>
          <globalSelectionHeader_1.default>
            <StyledPageContent>
              <noProjectMessage_1.default organization={organization}>
                <vitalDetailContent_1.default location={location} organization={organization} eventView={eventView} router={router} vitalName={vitalName || fields_1.WebVital.LCP}/>
              </noProjectMessage_1.default>
            </StyledPageContent>
          </globalSelectionHeader_1.default>
        </performanceEventViewContext_1.PerformanceEventViewProvider>
      </sentryDocumentTitle_1.default>);
    }
}
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
exports.default = (0, withApi_1.default)((0, withGlobalSelection_1.default)((0, withProjects_1.default)((0, withOrganization_1.default)(VitalDetail))));
//# sourceMappingURL=index.jsx.map