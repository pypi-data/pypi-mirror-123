Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const projectPerformance_1 = (0, tslib_1.__importDefault)(require("./projectPerformance"));
class ProjectPerformanceContainer extends react_1.default.Component {
    render() {
        return (<feature_1.default features={['performance-view']}>
        <projectPerformance_1.default {...this.props}/>
      </feature_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)(ProjectPerformanceContainer);
//# sourceMappingURL=index.jsx.map