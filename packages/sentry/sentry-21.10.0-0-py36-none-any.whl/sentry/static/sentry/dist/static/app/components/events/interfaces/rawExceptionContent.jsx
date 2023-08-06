Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const rawStacktraceContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/rawStacktraceContent"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class RawExceptionContent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            error: false,
            crashReport: '',
        };
    }
    componentDidMount() {
        if (this.isNative()) {
            this.fetchAppleCrashReport();
        }
    }
    componentDidUpdate(prevProps) {
        if (this.isNative() && this.props.type !== prevProps.type) {
            this.fetchAppleCrashReport();
        }
    }
    isNative() {
        const { platform } = this.props;
        return platform === 'cocoa' || platform === 'native';
    }
    getAppleCrashReportEndpoint(organization) {
        const { type, projectId, eventId } = this.props;
        const minified = type === 'minified';
        return `/projects/${organization.slug}/${projectId}/events/${eventId}/apple-crash-report?minified=${minified}`;
    }
    getContent(isNative, exc) {
        const { type } = this.props;
        const output = {
            downloadButton: null,
            content: exc.stacktrace
                ? (0, rawStacktraceContent_1.default)(type === 'original' ? exc.stacktrace : exc.rawStacktrace, this.props.platform, exc)
                : null,
        };
        if (!isNative) {
            return output;
        }
        const { loading, error, crashReport } = this.state;
        if (loading) {
            return Object.assign(Object.assign({}, output), { content: <loadingIndicator_1.default /> });
        }
        if (error) {
            return Object.assign(Object.assign({}, output), { content: <loadingError_1.default /> });
        }
        if (!loading && !!crashReport) {
            const { api, organization } = this.props;
            let downloadButton = null;
            if (organization) {
                const appleCrashReportEndpoint = this.getAppleCrashReportEndpoint(organization);
                downloadButton = (<DownloadBtnWrapper>
            <button_1.default size="xsmall" href={`${api.baseUrl}${appleCrashReportEndpoint}&download=1`}>
              {(0, locale_1.t)('Download')}
            </button_1.default>
          </DownloadBtnWrapper>);
            }
            return {
                downloadButton,
                content: <clippedBox_1.default clipHeight={250}>{crashReport}</clippedBox_1.default>,
            };
        }
        return output;
    }
    fetchAppleCrashReport() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization } = this.props;
            // Shared issues do not have access to organization
            if (!organization) {
                return;
            }
            this.setState({
                loading: true,
                error: false,
                crashReport: '',
            });
            try {
                const data = yield api.requestPromise(this.getAppleCrashReportEndpoint(organization));
                this.setState({
                    error: false,
                    loading: false,
                    crashReport: data,
                });
            }
            catch (_a) {
                this.setState({ error: true, loading: false });
            }
        });
    }
    render() {
        const { values } = this.props;
        const isNative = this.isNative();
        if (!values) {
            return null;
        }
        return (<React.Fragment>
        {values.map((exc, excIdx) => {
                const { downloadButton, content } = this.getContent(isNative, exc);
                if (!downloadButton && !content) {
                    return null;
                }
                return (<div key={excIdx}>
              {downloadButton}
              <pre className="traceback plain">{content}</pre>
            </div>);
            })}
      </React.Fragment>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(RawExceptionContent));
const DownloadBtnWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: flex-end;
`;
//# sourceMappingURL=rawExceptionContent.jsx.map