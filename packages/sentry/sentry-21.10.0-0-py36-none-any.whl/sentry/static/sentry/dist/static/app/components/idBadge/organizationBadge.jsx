Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const badgeDisplayName_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/badgeDisplayName"));
const baseBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/baseBadge"));
const OrganizationBadge = (_a) => {
    var { hideOverflow = true, organization } = _a, props = (0, tslib_1.__rest)(_a, ["hideOverflow", "organization"]);
    return (<baseBadge_1.default displayName={<badgeDisplayName_1.default hideOverflow={hideOverflow}>{organization.slug}</badgeDisplayName_1.default>} organization={organization} {...props}/>);
};
exports.default = OrganizationBadge;
//# sourceMappingURL=organizationBadge.jsx.map