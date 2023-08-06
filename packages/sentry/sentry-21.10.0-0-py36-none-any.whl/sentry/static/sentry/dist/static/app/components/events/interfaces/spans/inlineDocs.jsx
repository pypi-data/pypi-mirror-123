Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const projects_1 = require("app/actionCreators/projects");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class InlineDocs extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            html: undefined,
            link: undefined,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { platform, api, orgSlug, projectSlug } = this.props;
            if (!platform) {
                return;
            }
            this.setState({ loading: true });
            let tracingPlatform;
            switch (platform) {
                case 'sentry.python': {
                    tracingPlatform = 'python-tracing';
                    break;
                }
                case 'sentry.javascript.node': {
                    tracingPlatform = 'node-tracing';
                    break;
                }
                case 'sentry.javascript.react-native': {
                    tracingPlatform = 'react-native-tracing';
                    break;
                }
                default: {
                    this.setState({ loading: false });
                    return;
                }
            }
            try {
                const { html, link } = yield (0, projects_1.loadDocs)(api, orgSlug, projectSlug, tracingPlatform);
                this.setState({ html, link });
            }
            catch (error) {
                Sentry.captureException(error);
                this.setState({ html: undefined, link: undefined });
            }
            this.setState({ loading: false });
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    render() {
        const { platform } = this.props;
        if (!platform) {
            return null;
        }
        if (this.state.loading) {
            return (<div>
          <loadingIndicator_1.default />
        </div>);
        }
        if (this.state.html) {
            return (<div>
          <h4>{(0, locale_1.t)('Requires Manual Instrumentation')}</h4>
          <DocumentationWrapper dangerouslySetInnerHTML={{ __html: this.state.html }}/>
          <p>
            {(0, locale_1.tct)(`For in-depth instructions on setting up tracing, view [docLink:our documentation].`, {
                    docLink: <a href={this.state.link}/>,
                })}
          </p>
        </div>);
        }
        return (<div>
        <h4>{(0, locale_1.t)('Requires Manual Instrumentation')}</h4>
        <p>
          {(0, locale_1.tct)(`To manually instrument certain regions of your code, view [docLink:our documentation].`, {
                docLink: (<externalLink_1.default href="https://docs.sentry.io/product/performance/getting-started/"/>),
            })}
        </p>
      </div>);
    }
}
const DocumentationWrapper = (0, styled_1.default)('div') `
  p {
    line-height: 1.5;
  }
  pre {
    word-break: break-all;
    white-space: pre-wrap;
  }
`;
exports.default = (0, withApi_1.default)(InlineDocs);
//# sourceMappingURL=inlineDocs.jsx.map