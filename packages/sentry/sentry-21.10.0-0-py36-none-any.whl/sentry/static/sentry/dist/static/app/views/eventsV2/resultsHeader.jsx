Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const discoverSavedQueries_1 = require("app/actionCreators/discoverSavedQueries");
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("./breadcrumb"));
const eventInputName_1 = (0, tslib_1.__importDefault)(require("./eventInputName"));
const savedQuery_1 = (0, tslib_1.__importDefault)(require("./savedQuery"));
class ResultsHeader extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            savedQuery: undefined,
            loading: true,
        };
    }
    componentDidMount() {
        if (this.props.eventView.id) {
            this.fetchData();
        }
    }
    componentDidUpdate(prevProps) {
        if (prevProps.eventView &&
            this.props.eventView &&
            prevProps.eventView.id !== this.props.eventView.id) {
            this.fetchData();
        }
    }
    fetchData() {
        const { api, eventView, organization } = this.props;
        if (typeof eventView.id === 'string') {
            this.setState({ loading: true });
            (0, discoverSavedQueries_1.fetchSavedQuery)(api, organization.slug, eventView.id).then(savedQuery => {
                this.setState({ savedQuery, loading: false });
            });
        }
    }
    renderAuthor() {
        var _a;
        const { eventView } = this.props;
        const { savedQuery } = this.state;
        // No saved query in use.
        if (!eventView.id) {
            return null;
        }
        let createdBy = ' \u2014 ';
        let lastEdit = ' \u2014 ';
        if (savedQuery !== undefined) {
            createdBy = ((_a = savedQuery.createdBy) === null || _a === void 0 ? void 0 : _a.email) || '\u2014';
            lastEdit = <timeSince_1.default date={savedQuery.dateUpdated}/>;
        }
        return (<Subtitle>
        {(0, locale_1.t)('Created by:')} {createdBy} | {(0, locale_1.t)('Last edited:')} {lastEdit}
      </Subtitle>);
    }
    render() {
        const { organization, location, errorCode, eventView, onIncompatibleAlertQuery, yAxis, } = this.props;
        const { savedQuery, loading } = this.state;
        return (<Layout.Header>
        <StyledHeaderContent>
          <breadcrumb_1.default eventView={eventView} organization={organization} location={location}/>
          <eventInputName_1.default savedQuery={savedQuery} organization={organization} eventView={eventView}/>
          {this.renderAuthor()}
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <savedQuery_1.default location={location} organization={organization} eventView={eventView} savedQuery={savedQuery} savedQueryLoading={loading} disabled={errorCode >= 400 && errorCode < 500} updateCallback={() => this.fetchData()} onIncompatibleAlertQuery={onIncompatibleAlertQuery} yAxis={yAxis}/>
        </Layout.HeaderActions>
      </Layout.Header>);
    }
}
const Subtitle = (0, styled_1.default)('h4') `
  font-size: ${p => p.theme.fontSizeLarge};
  font-weight: normal;
  color: ${p => p.theme.gray300};
  margin: ${(0, space_1.default)(0.5)} 0 0 0;
`;
const StyledHeaderContent = (0, styled_1.default)(Layout.HeaderContent) `
  overflow: unset;
`;
exports.default = (0, withApi_1.default)(ResultsHeader);
//# sourceMappingURL=resultsHeader.jsx.map