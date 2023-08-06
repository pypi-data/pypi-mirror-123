Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const collapsible_1 = (0, tslib_1.__importDefault)(require("app/components/collapsible"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const styles_2 = require("./styles");
function ProjectTeamAccess({ organization, project }) {
    const hasEditPermissions = organization.access.includes('project:write');
    const settingsLink = `/settings/${organization.slug}/projects/${project === null || project === void 0 ? void 0 : project.slug}/teams/`;
    function renderInnerBody() {
        if (!project) {
            return <placeholder_1.default height="23px"/>;
        }
        if (project.teams.length === 0) {
            return (<button_1.default to={settingsLink} disabled={!hasEditPermissions} title={hasEditPermissions ? undefined : (0, locale_1.t)('You do not have permission to do this')} priority="primary" size="small">
          {(0, locale_1.t)('Assign Team')}
        </button_1.default>);
        }
        return (<collapsible_1.default expandButton={({ onExpand, numberOfHiddenItems }) => (<button_1.default priority="link" onClick={onExpand}>
            {(0, locale_1.tn)('Show %s collapsed team', 'Show %s collapsed teams', numberOfHiddenItems)}
          </button_1.default>)}>
        {project.teams
                .sort((a, b) => a.slug.localeCompare(b.slug))
                .map(team => (<StyledLink to={`/settings/${organization.slug}/teams/${team.slug}/`} key={team.slug}>
              <idBadge_1.default team={team} hideAvatar/>
            </StyledLink>))}
      </collapsible_1.default>);
    }
    return (<StyledSidebarSection>
      <styles_2.SectionHeadingWrapper>
        <styles_1.SectionHeading>{(0, locale_1.t)('Team Access')}</styles_1.SectionHeading>
        <styles_2.SectionHeadingLink to={settingsLink}>
          <icons_1.IconOpen />
        </styles_2.SectionHeadingLink>
      </styles_2.SectionHeadingWrapper>

      <div>{renderInnerBody()}</div>
    </StyledSidebarSection>);
}
const StyledSidebarSection = (0, styled_1.default)(styles_2.SidebarSection) `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  display: block;
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
exports.default = ProjectTeamAccess;
//# sourceMappingURL=projectTeamAccess.jsx.map