Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const detailedError_1 = (0, tslib_1.__importDefault)(require("app/components/errors/detailedError"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const exclamation = ['Raspberries', 'Snap', 'Frig', 'Welp', 'Uhhhh', 'Hmmm'];
function getExclamation() {
    return exclamation[Math.floor(Math.random() * exclamation.length)];
}
class ErrorBoundary extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            error: null,
        };
        this._isMounted = false;
    }
    componentDidMount() {
        this._isMounted = true;
        // Listen for route changes so we can clear error
        this.unlistenBrowserHistory = react_router_1.browserHistory.listen(() => {
            // Prevent race between component unmount and browserHistory change
            // Setting state on a component that is being unmounted throws an error
            if (this._isMounted) {
                this.setState({ error: null });
            }
        });
    }
    componentDidCatch(error, errorInfo) {
        const { errorTag } = this.props;
        this.setState({ error });
        Sentry.withScope(scope => {
            if (errorTag) {
                Object.keys(errorTag).forEach(tag => scope.setTag(tag, errorTag[tag]));
            }
            scope.setExtra('errorInfo', errorInfo);
            Sentry.captureException(error);
        });
    }
    componentWillUnmount() {
        this._isMounted = false;
        if (this.unlistenBrowserHistory) {
            this.unlistenBrowserHistory();
        }
    }
    render() {
        const { error } = this.state;
        if (!error) {
            // when there's not an error, render children untouched
            return this.props.children;
        }
        const { customComponent, mini, message, className } = this.props;
        if (typeof customComponent !== 'undefined') {
            return customComponent;
        }
        if (mini) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>} className={className}>
          {message || (0, locale_1.t)('There was a problem rendering this component')}
        </alert_1.default>);
        }
        return (<Wrapper>
        <detailedError_1.default heading={(0, getDynamicText_1.default)({
                value: getExclamation(),
                fixed: exclamation[0],
            })} message={(0, locale_1.t)(`Something went horribly wrong rendering this page.
We use a decent error reporting service so this will probably be fixed soon. Unless our error reporting service is also broken. That would be awkward.
Anyway, we apologize for the inconvenience.`)}/>
        <StackTrace>{error.toString()}</StackTrace>
      </Wrapper>);
    }
}
ErrorBoundary.defaultProps = {
    mini: false,
};
const Wrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  padding: ${p => p.theme.grid * 3}px;
  max-width: 1000px;
  margin: auto;
`;
const StackTrace = (0, styled_1.default)('pre') `
  white-space: pre-wrap;
  margin: 32px;
  margin-left: 85px;
  margin-right: 18px;
`;
exports.default = ErrorBoundary;
//# sourceMappingURL=errorBoundary.jsx.map