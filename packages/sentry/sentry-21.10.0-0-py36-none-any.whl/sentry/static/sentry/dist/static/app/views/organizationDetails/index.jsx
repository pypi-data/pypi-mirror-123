Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const organizations_1 = require("app/actionCreators/organizations");
const organizationContext_1 = (0, tslib_1.__importDefault)(require("app/views/organizationContext"));
const body_1 = (0, tslib_1.__importDefault)(require("./body"));
function OrganizationDetails(_a) {
    var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
    // Switch organizations when the orgId changes
    (0, react_1.useEffect)(() => void (0, organizations_1.switchOrganization)(), [props.params.orgId]);
    return (<organizationContext_1.default includeSidebar useLastOrganization {...props}>
      <body_1.default>{children}</body_1.default>
    </organizationContext_1.default>);
}
exports.default = OrganizationDetails;
//# sourceMappingURL=index.jsx.map