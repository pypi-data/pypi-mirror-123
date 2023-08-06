Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const badgeDisplayName_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/badgeDisplayName"));
const baseBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/baseBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const ProjectBadge = (_a) => {
    var { project, organization, to, hideOverflow = true, disableLink = false, className } = _a, props = (0, tslib_1.__rest)(_a, ["project", "organization", "to", "hideOverflow", "disableLink", "className"]);
    const { slug, id } = project;
    const badge = (<baseBadge_1.default displayName={<badgeDisplayName_1.default hideOverflow={hideOverflow}>{slug}</badgeDisplayName_1.default>} project={project} {...props}/>);
    if (!disableLink && (organization === null || organization === void 0 ? void 0 : organization.slug)) {
        const defaultTo = `/organizations/${organization.slug}/projects/${slug}/${id ? `?project=${id}` : ''}`;
        return (<StyledLink to={to !== null && to !== void 0 ? to : defaultTo} className={className}>
        {badge}
      </StyledLink>);
    }
    return React.cloneElement(badge, { className });
};
const StyledLink = (0, styled_1.default)(link_1.default) `
  flex-shrink: 0;

  img:hover {
    cursor: pointer;
  }
`;
exports.default = (0, withOrganization_1.default)(ProjectBadge);
//# sourceMappingURL=projectBadge.jsx.map