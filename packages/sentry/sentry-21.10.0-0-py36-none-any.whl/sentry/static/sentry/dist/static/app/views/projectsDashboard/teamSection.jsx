Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const projectCard_1 = (0, tslib_1.__importDefault)(require("./projectCard"));
const teamMembers_1 = (0, tslib_1.__importDefault)(require("./teamMembers"));
const TeamSection = ({ team, projects, title, showBorder, orgId, access }) => {
    const hasTeamAccess = access.has('team:read');
    const hasProjectAccess = access.has('project:read');
    return (<TeamSectionWrapper data-test-id="team" showBorder={showBorder}>
      <TeamTitleBar>
        <TeamName>{title}</TeamName>
        {hasTeamAccess && team && <teamMembers_1.default teamId={team.slug} orgId={orgId}/>}
      </TeamTitleBar>
      <ProjectCards>
        {projects.map(project => (<projectCard_1.default data-test-id={project.slug} key={project.slug} project={project} hasProjectAccess={hasProjectAccess}/>))}
      </ProjectCards>
    </TeamSectionWrapper>);
};
const ProjectCards = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: minmax(100px, 1fr);
  grid-gap: ${(0, space_1.default)(3)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: repeat(2, minmax(100px, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    grid-template-columns: repeat(3, minmax(100px, 1fr));
  }
`;
const TeamSectionWrapper = (0, styled_1.default)('div') `
  border-bottom: ${p => (p.showBorder ? '1px solid ' + p.theme.border : 0)};
  padding: 0 ${(0, space_1.default)(4)} ${(0, space_1.default)(4)};
`;
const TeamTitleBar = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${(0, space_1.default)(3)} 0 ${(0, space_1.default)(2)};
`;
const TeamName = (0, styled_1.default)(pageHeading_1.default) `
  font-size: 20px;
  line-height: 24px; /* We need this so that header doesn't flicker when lazy loading because avatarList height > this */
`;
exports.default = TeamSection;
//# sourceMappingURL=teamSection.jsx.map