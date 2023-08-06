Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const uniqWith_1 = (0, tslib_1.__importDefault)(require("lodash/uniqWith"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorItem_1 = (0, tslib_1.__importDefault)(require("app/components/events/errorItem"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const eventErrors_1 = require("app/constants/eventErrors");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const styles_1 = require("./styles");
const MAX_ERRORS = 100;
class Errors extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false,
        };
        this.toggle = () => {
            this.setState(state => ({ isOpen: !state.isOpen }));
        };
    }
    componentDidMount() {
        this.checkSourceCodeErrors();
    }
    shouldComponentUpdate(nextProps, nextState) {
        if (this.state.isOpen !== nextState.isOpen) {
            return true;
        }
        return this.props.event.id !== nextProps.event.id;
    }
    componentDidUpdate(prevProps) {
        if (this.props.event.id !== prevProps.event.id) {
            this.checkSourceCodeErrors();
        }
    }
    fetchReleaseArtifacts(query) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgSlug, event, projectSlug } = this.props;
            const { release } = event;
            const releaseVersion = release === null || release === void 0 ? void 0 : release.version;
            if (!releaseVersion || !query) {
                return;
            }
            try {
                const releaseArtifacts = yield api.requestPromise(`/projects/${orgSlug}/${projectSlug}/releases/${encodeURIComponent(releaseVersion)}/files/?query=${query}`, {
                    method: 'GET',
                });
                this.setState({ releaseArtifacts });
            }
            catch (error) {
                Sentry.captureException(error);
                // do nothing, the UI will not display extra error details
            }
        });
    }
    checkSourceCodeErrors() {
        const { event } = this.props;
        const { errors } = event;
        const sourceCodeErrors = (errors !== null && errors !== void 0 ? errors : []).filter(error => error.type === 'js_no_source' && error.data.url);
        if (!sourceCodeErrors.length) {
            return;
        }
        const pathNames = [];
        for (const sourceCodeError of sourceCodeErrors) {
            const url = sourceCodeError.data.url;
            if (url) {
                const pathName = this.getURLPathname(url);
                if (pathName) {
                    pathNames.push(encodeURIComponent(pathName));
                }
            }
        }
        this.fetchReleaseArtifacts(pathNames.join('&query='));
    }
    getURLPathname(url) {
        try {
            return new URL(url).pathname;
        }
        catch (_a) {
            return undefined;
        }
    }
    render() {
        const { event, proGuardErrors } = this.props;
        const { isOpen, releaseArtifacts } = this.state;
        const { dist: eventDistribution, errors: eventErrors = [] } = event;
        // XXX: uniqWith returns unique errors and is not performant with large datasets
        const otherErrors = eventErrors.length > MAX_ERRORS ? eventErrors : (0, uniqWith_1.default)(eventErrors, isEqual_1.default);
        const errors = [...otherErrors, ...proGuardErrors];
        return (<StyledBanner priority="danger">
        <styles_1.BannerSummary>
          <StyledIconWarning />
          <span data-test-id="errors-banner-summary-info">
            {(0, locale_1.tn)('There was %s problem processing this event', 'There were %s problems processing this event', errors.length)}
          </span>
          <StyledButton data-test-id="event-error-toggle" priority="link" onClick={this.toggle}>
            {isOpen ? (0, locale_1.t)('Hide') : (0, locale_1.t)('Show')}
          </StyledButton>
        </styles_1.BannerSummary>
        {isOpen && (<react_1.Fragment>
            <Divider />
            <ErrorList data-test-id="event-error-details" symbol="bullet">
              {errors.map((error, errorIdx) => {
                    var _a, _b;
                    const data = (_a = error.data) !== null && _a !== void 0 ? _a : {};
                    if (error.type === eventErrors_1.JavascriptProcessingErrors.JS_MISSING_SOURCE &&
                        data.url &&
                        !!(releaseArtifacts === null || releaseArtifacts === void 0 ? void 0 : releaseArtifacts.length)) {
                        const releaseArtifact = releaseArtifacts.find(releaseArt => {
                            const pathname = data.url ? this.getURLPathname(data.url) : undefined;
                            if (pathname) {
                                return releaseArt.name.includes(pathname);
                            }
                            return false;
                        });
                        const releaseArtifactDistribution = (_b = releaseArtifact === null || releaseArtifact === void 0 ? void 0 : releaseArtifact.dist) !== null && _b !== void 0 ? _b : null;
                        // Neither event nor file have dist -> matching
                        // Event has dist, file doesn’t -> not matching
                        // File has dist, event doesn’t -> not matching
                        // Both have dist, same value -> matching
                        // Both have dist, different values -> not matching
                        if (releaseArtifactDistribution !== eventDistribution) {
                            error.message = (0, locale_1.t)('Source code was not found because the distribution did not match');
                            data['expected-distribution'] = eventDistribution;
                            data['current-distribution'] = releaseArtifactDistribution;
                        }
                    }
                    return <errorItem_1.default key={errorIdx} error={Object.assign(Object.assign({}, error), { data })}/>;
                })}
            </ErrorList>
          </react_1.Fragment>)}
      </StyledBanner>);
    }
}
const linkStyle = ({ theme }) => (0, react_2.css) `
  font-weight: bold;
  color: ${theme.subText};
  :hover {
    color: ${theme.textColor};
  }
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  ${linkStyle}
`;
const StyledBanner = (0, styled_1.default)(styles_1.BannerContainer) `
  margin-top: -1px;
  a {
    ${linkStyle}
  }
`;
const StyledIconWarning = (0, styled_1.default)(icons_1.IconWarning) `
  color: ${p => p.theme.red300};
`;
// TODO(theme) don't use a custom pink
const customPink = '#e7c0bc';
const Divider = (0, styled_1.default)('div') `
  height: 1px;
  background-color: ${customPink};
`;
const ErrorList = (0, styled_1.default)(list_1.default) `
  margin: 0 ${(0, space_1.default)(4)} 0 40px;
  padding-top: ${(0, space_1.default)(1)};
  padding-bottom: ${(0, space_1.default)(0.5)};
  pre {
    background: #f9eded;
    color: #381618;
    margin: ${(0, space_1.default)(0.5)} 0 0;
  }
`;
exports.default = (0, withApi_1.default)(Errors);
//# sourceMappingURL=errors.jsx.map