Object.defineProperty(exports, "__esModule", { value: true });
exports.SharedGroupDetails = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const eventEntries_1 = require("app/components/events/eventEntries");
const footer_1 = (0, tslib_1.__importDefault)(require("app/components/footer"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const sharedGroupHeader_1 = (0, tslib_1.__importDefault)(require("./sharedGroupHeader"));
class SharedGroupDetails extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.handleRetry = () => {
            this.setState(this.getInitialState());
            this.fetchData();
        };
    }
    getInitialState() {
        return {
            group: null,
            loading: true,
            error: false,
        };
    }
    getChildContext() {
        return {
            group: this.state.group,
        };
    }
    componentWillMount() {
        document.body.classList.add('shared-group');
    }
    componentDidMount() {
        this.fetchData();
    }
    componentWillUnmount() {
        document.body.classList.remove('shared-group');
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params, api } = this.props;
            const { shareId } = params;
            try {
                const group = yield api.requestPromise(`/shared/issues/${shareId}/`);
                this.setState({ loading: false, group });
            }
            catch (_a) {
                this.setState({ loading: false, error: true });
            }
        });
    }
    getTitle() {
        const { group } = this.state;
        if (group) {
            return group.title;
        }
        return 'Sentry';
    }
    render() {
        const { group, loading, error } = this.state;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!group) {
            return <notFound_1.default />;
        }
        if (error) {
            return <loadingError_1.default onRetry={this.handleRetry}/>;
        }
        const { location, api, route, router } = this.props;
        const { permalink, latestEvent, project } = group;
        const title = this.getTitle();
        return (<react_document_title_1.default title={title}>
        <div className="app">
          <div className="pattern-bg"/>
          <div className="container">
            <div className="box box-modal">
              <div className="box-header">
                <link_1.default className="logo" to="/">
                  <span className="icon-sentry-logo-full"/>
                </link_1.default>
                {permalink && (<link_1.default className="details" to={permalink}>
                    {(0, locale_1.t)('Details')}
                  </link_1.default>)}
              </div>
              <div className="content">
                <sharedGroupHeader_1.default group={group}/>
                <Container className="group-overview event-details-container">
                  <eventEntries_1.BorderlessEventEntries location={location} organization={project.organization} group={group} event={latestEvent} project={project} api={api} route={route} router={router} isBorderless isShare/>
                </Container>
                <footer_1.default />
              </div>
            </div>
          </div>
        </div>
      </react_document_title_1.default>);
    }
}
exports.SharedGroupDetails = SharedGroupDetails;
SharedGroupDetails.childContextTypes = {
    group: sentryTypes_1.default.Group,
};
const Container = (0, styled_1.default)('div') `
  padding: 0 ${(0, space_1.default)(4)};
`;
exports.default = (0, withApi_1.default)(SharedGroupDetails);
//# sourceMappingURL=index.jsx.map