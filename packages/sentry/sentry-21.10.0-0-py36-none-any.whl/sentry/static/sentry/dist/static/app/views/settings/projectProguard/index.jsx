Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const projectProguard_1 = (0, tslib_1.__importDefault)(require("./projectProguard"));
class ProjectProguardContainer extends react_1.Component {
    render() {
        return <projectProguard_1.default {...this.props}/>;
    }
}
exports.default = (0, withOrganization_1.default)(ProjectProguardContainer);
//# sourceMappingURL=index.jsx.map