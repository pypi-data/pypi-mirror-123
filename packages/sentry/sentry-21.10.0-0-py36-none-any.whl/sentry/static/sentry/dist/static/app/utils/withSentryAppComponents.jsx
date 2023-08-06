Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const sentryAppComponentsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sentryAppComponentsStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
function withSentryAppComponents(WrappedComponent, { componentType } = {}) {
    class WithSentryAppComponents extends React.Component {
        constructor() {
            super(...arguments);
            this.state = { components: sentryAppComponentsStore_1.default.getAll() };
            this.unsubscribe = sentryAppComponentsStore_1.default.listen(() => this.setState({ components: sentryAppComponentsStore_1.default.getAll() }), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            const _a = this.props, { components } = _a, props = (0, tslib_1.__rest)(_a, ["components"]);
            return (<WrappedComponent {...Object.assign({ components: components !== null && components !== void 0 ? components : sentryAppComponentsStore_1.default.getComponentByType(componentType) }, props)}/>);
        }
    }
    WithSentryAppComponents.displayName = `withSentryAppComponents(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithSentryAppComponents;
}
exports.default = withSentryAppComponents;
//# sourceMappingURL=withSentryAppComponents.jsx.map