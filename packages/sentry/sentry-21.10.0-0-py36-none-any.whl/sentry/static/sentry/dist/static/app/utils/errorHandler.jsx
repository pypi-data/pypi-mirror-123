Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const routeError_1 = (0, tslib_1.__importDefault)(require("app/views/routeError"));
function errorHandler(Component) {
    class ErrorHandler extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                // we are explicit if an error has been thrown since errors thrown are not guaranteed
                // to be truthy (e.g. throw null).
                hasError: false,
                error: undefined,
            };
        }
        static getDerivedStateFromError(error) {
            // Update state so the next render will show the fallback UI.
            return {
                hasError: true,
                error,
            };
        }
        componentDidCatch(_error, info) {
            // eslint-disable-next-line no-console
            console.error('Component stack trace caught in <ErrorHandler />:', info.componentStack);
        }
        render() {
            if (this.state.hasError) {
                return <routeError_1.default error={this.state.error}/>;
            }
            return <Component {...this.props}/>;
        }
    }
    return ErrorHandler;
}
exports.default = errorHandler;
//# sourceMappingURL=errorHandler.jsx.map