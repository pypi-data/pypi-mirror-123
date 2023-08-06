Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const retryableImport_1 = (0, tslib_1.__importDefault)(require("app/utils/retryableImport"));
class LazyLoad extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            Component: null,
            error: null,
        };
        this.handleFetchError = (error) => {
            Sentry.withScope(scope => {
                if ((0, utils_1.isWebpackChunkLoadingError)(error)) {
                    scope.setFingerprint(['webpack', 'error loading chunk']);
                }
                Sentry.captureException(error);
            });
            this.handleError(error);
        };
        this.handleError = (error) => {
            // eslint-disable-next-line no-console
            console.error(error);
            this.setState({ error });
        };
        this.fetchComponent = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const getComponent = this.componentGetter;
            if (getComponent === undefined) {
                return;
            }
            try {
                this.setState({ Component: yield (0, retryableImport_1.default)(getComponent) });
            }
            catch (err) {
                this.handleFetchError(err);
            }
        });
        this.fetchRetry = () => {
            this.setState({ error: null }, this.fetchComponent);
        };
    }
    componentDidMount() {
        this.fetchComponent();
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        // No need to refetch when component does not change
        if (nextProps.component && nextProps.component === this.props.component) {
            return;
        }
        // This is to handle the following case:
        // <Route path="a/">
        //   <Route path="b/" component={LazyLoad} componentPromise={...} />
        //   <Route path="c/" component={LazyLoad} componentPromise={...} />
        // </Route>
        //
        // `LazyLoad` will get not fully remount when we switch between `b` and `c`,
        // instead will just re-render.  Refetch if route paths are different
        if (nextProps.route && nextProps.route === this.props.route) {
            return;
        }
        // If `this.fetchComponent` is not in callback,
        // then there's no guarantee that new Component will be rendered
        this.setState({
            Component: null,
        }, this.fetchComponent);
    }
    componentDidCatch(error) {
        Sentry.captureException(error);
        this.handleError(error);
    }
    get componentGetter() {
        var _a, _b;
        return (_a = this.props.component) !== null && _a !== void 0 ? _a : (_b = this.props.route) === null || _b === void 0 ? void 0 : _b.componentPromise;
    }
    render() {
        const { Component, error } = this.state;
        const _a = this.props, { hideBusy, hideError, component: _component } = _a, otherProps = (0, tslib_1.__rest)(_a, ["hideBusy", "hideError", "component"]);
        if (error && !hideError) {
            return (<LoadingErrorContainer>
          <loadingError_1.default onRetry={this.fetchRetry} message={(0, locale_1.t)('There was an error loading a component.')}/>
        </LoadingErrorContainer>);
        }
        if (!Component && !hideBusy) {
            return (<LoadingContainer>
          <loadingIndicator_1.default />
        </LoadingContainer>);
        }
        if (Component === null) {
            return null;
        }
        return <Component {...otherProps}/>;
    }
}
const LoadingContainer = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  align-items: center;
`;
const LoadingErrorContainer = (0, styled_1.default)('div') `
  flex: 1;
`;
exports.default = LazyLoad;
//# sourceMappingURL=lazyLoad.jsx.map