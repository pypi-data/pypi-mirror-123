Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const badgeDisplayName_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/badgeDisplayName"));
const baseBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/baseBadge"));
const Badge = (_a) => {
    var { hideOverflow = true, team } = _a, props = (0, tslib_1.__rest)(_a, ["hideOverflow", "team"]);
    return (<baseBadge_1.default data-test-id="team-badge" displayName={<badgeDisplayName_1.default hideOverflow={hideOverflow}>{`#${team.slug}`}</badgeDisplayName_1.default>} team={team} {...props}/>);
};
exports.default = Badge;
//# sourceMappingURL=badge.jsx.map