Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const data_1 = require("../data");
const content_1 = (0, tslib_1.__importDefault)(require("./content"));
class TrendsSummary extends react_1.default.Component {
    constructor() {
        super(...arguments);
        this.state = {
            eventView: (0, data_1.generatePerformanceEventView)(this.props.organization, this.props.location, this.props.projects, true),
            error: undefined,
        };
        this.setError = (error) => {
            this.setState({ error });
        };
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        return Object.assign(Object.assign({}, prevState), { eventView: (0, data_1.generatePerformanceEventView)(nextProps.organization, nextProps.location, nextProps.projects, true) });
    }
    getDocumentTitle() {
        return [(0, locale_1.t)('Trends'), (0, locale_1.t)('Performance')].join(' - ');
    }
    renderContent() {
        const { organization, location } = this.props;
        const { eventView } = this.state;
        return (<content_1.default organization={organization} location={location} eventView={eventView}/>);
    }
    render() {
        const { organization } = this.props;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <noProjectMessage_1.default organization={organization}>
            {this.renderContent()}
          </noProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withProjects_1.default)((0, withGlobalSelection_1.default)((0, withApi_1.default)(TrendsSummary))));
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
//# sourceMappingURL=index.jsx.map