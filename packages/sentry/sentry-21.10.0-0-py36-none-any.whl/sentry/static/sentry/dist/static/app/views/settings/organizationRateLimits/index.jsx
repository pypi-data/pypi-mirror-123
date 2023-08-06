Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const organizationRateLimits_1 = (0, tslib_1.__importDefault)(require("./organizationRateLimits"));
const OrganizationRateLimitsContainer = (props) => (!props.organization ? null : <organizationRateLimits_1.default {...props}/>);
exports.default = (0, withOrganization_1.default)(OrganizationRateLimitsContainer);
//# sourceMappingURL=index.jsx.map