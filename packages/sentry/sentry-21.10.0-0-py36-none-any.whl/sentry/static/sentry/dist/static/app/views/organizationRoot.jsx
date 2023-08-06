Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationRoot = void 0;
const react_1 = require("react");
const react_router_1 = require("react-router");
const navigation_1 = require("app/actionCreators/navigation");
const projects_1 = require("app/actionCreators/projects");
/**
 * This is the parent container for organization-level views such
 * as the Dashboard, Stats, Activity, etc...
 *
 * Currently is just used to unset active project
 */
class OrganizationRoot extends react_1.Component {
    componentDidMount() {
        (0, projects_1.setActiveProject)(null);
    }
    componentWillUnmount() {
        const { location } = this.props;
        const { pathname, search } = location;
        // Save last route so that we can jump back to view from settings
        (0, navigation_1.setLastRoute)(`${pathname}${search || ''}`);
    }
    render() {
        return this.props.children;
    }
}
exports.OrganizationRoot = OrganizationRoot;
exports.default = (0, react_router_1.withRouter)(OrganizationRoot);
//# sourceMappingURL=organizationRoot.jsx.map