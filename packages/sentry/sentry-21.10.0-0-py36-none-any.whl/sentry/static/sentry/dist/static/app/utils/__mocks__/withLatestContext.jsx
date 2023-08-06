Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const MOCK_ORG = TestStubs.Organization();
const DEFAULTS = {
    organization: MOCK_ORG,
    organizations: [MOCK_ORG],
    project: TestStubs.Project(),
    lastRoute: '',
};
const withLatestContextMock = WrappedComponent => class WithLatestContextMockWrapper extends react_1.Component {
    render() {
        return <WrappedComponent {...DEFAULTS} {...this.props}/>;
    }
};
exports.default = withLatestContextMock;
//# sourceMappingURL=withLatestContext.jsx.map